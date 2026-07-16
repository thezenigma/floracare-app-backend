import json
from openai import AsyncOpenAI
from config import NVIDIA_API_KEY, NVIDIA_BASE_URL, MODEL_NAME
from db_client import get_user_plants, get_recent_journals
from rag_client import get_relevant_context

client = AsyncOpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)

SYSTEM_PROMPT = """You are FloraCare AI, a professional botanist and friendly garden companion.
You should behave like a normal human in conversation. If the user is just saying hello, asking how you are, or making casual conversation, respond naturally and casually. **ABSOLUTE RULE:** Do NOT mention the user's plants, do not give "quick tips", and do not abruptly force the topic of plants unless the user explicitly asks about their plants or asks for advice. Treat the provided [User Plants] context as background knowledge to be kept secret until needed.

When the user DOES ask about a plant or gardening, analyze their inquiry based on the [Botanical Knowledge Base] for factual plant care, and [User Plants] / [Recent Journals] for their personal history. 
ALWAYS check the Botanical Knowledge Base first when a plant is mentioned. Do not claim you don't know if the information is provided in the context.

When providing plant advice, your response MUST be thorough, detailed, and highly actionable. Break down your reasoning so the user understands WHY a plant is reacting a certain way, and give step-by-step recovery or care instructions.
At the end of your plant advice, include one light, constructive follow-up question to keep the conversation engaging.

You must respond strictly in JSON format conforming to the exact output schema requested."""


async def expand_query(message: str) -> str:
    prompt = """You are a botanical taxonomy assistant. 
Extract the plant name from the user's message.
If the plant name is a colloquial or common name (e.g., 'gray dragon', 'swiss cheese plant'), 
convert it to its most standard botanical/scientific name (e.g., 'Alocasia Maharani', 'Monstera Deliciosa').
Output ONLY the scientific or standard common name. Do not output anything else.
If no plant is mentioned, just output 'none'."""

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.1,
        )
        extracted = response.choices[0].message.content.strip()
        if extracted.lower() == 'none' or not extracted:
            return None
        # Combine the expanded botanical name with the original query for maximum embedding match
        return f"{extracted} {message}"
    except Exception as e:
        print(f"[DEBUG] Query expansion failed: {e}")
        return None

async def process_chat_message(user_id: str, session_id: str, message: str, plant_ids: list = None, chat_history: str = ""):
    print("[STEP 4] Gathering local context (User Plants & Recent Journals)...")
    # 1. Gather Context
    plants = get_user_plants(user_id, plant_ids)
    journals = get_recent_journals(user_id, plant_ids)
    
    print("[STEP 5] Expanding query to optimize RAG search (using Fast Model)...")
    # Expand query for better RAG matching
    expanded_message = await expand_query(message)
    print(f"         > Expanded Query: {expanded_message}")
    
    rag_context = ""
    if expanded_message:
        print("[STEP 6] Executing RAG search in ChromaDB...")
        rag_context = get_relevant_context(expanded_message)
        print(f"         > Retrieved {len(rag_context)} characters of context from Knowledge Base.")
    else:
        print("[STEP 6] RAG skipped (no plant terms detected in user query).")

    context_block = f"""
    [User Plants]: {json.dumps(plants)}
    [Recent Journals]: {json.dumps(journals)}
    [Botanical Knowledge Base]: {rag_context}
    [Previous Chat History]: {chat_history}
    """

    # 2. Extract image URL if present
    import re
    image_url = None
    clean_message = message
    
    img_match = re.search(r'(https?://[^\s]+supabase\.co/storage[^\s\]]+)', message, re.IGNORECASE)
    if img_match:
        image_url = img_match.group(1).strip()
        # Clean the text using aggressive regex replacements
        clean_message = re.sub(r'\[IMAGE:.*?\]', '', message, flags=re.IGNORECASE | re.DOTALL)
        clean_message = clean_message.replace(image_url, '').replace('[IMAGE:', '').replace(']', '').strip()

    print(f"[STEP 7] Sending prompt and compiled context to AI Endpoint ({MODEL_NAME})...")
    
    # Construct Multimodal Content Payload
    text_prompt = f"Context:\n{context_block}\n\nUser Message: {clean_message}\n\nRespond with JSON matching: {{\"response\": \"string\", \"care_memories_created\": [{{\"memory_type\": \"diagnosis|schedule|general\", \"content\": \"string\", \"plant_id\": \"uuid\"}}], \"status\": \"success\"}}\n\nCRITICAL: The 'response' string MUST be highly structured using Markdown (e.g., use **bolding**, bullets, and insert proper ESCAPED newlines like \\\\n\\\\n between paragraphs and steps for vertical readability). Do NOT output a single block of text."
    
    if image_url:
        print(f"         > Attached image to prompt: {image_url}")
        content_payload = [
            {"type": "text", "text": text_prompt},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    else:
        content_payload = text_prompt

    # 3. Call LLM demanding JSON output
    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content_payload}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    print("[STEP 8] Received JSON response from AI endpoint.")
    
    raw_response = response.choices[0].message.content.strip()
    
    # Strip markdown JSON wrappers if the LLM hallucinated them
    if raw_response.startswith('```json'):
        raw_response = raw_response[7:]
    if raw_response.startswith('```'):
        raw_response = raw_response[3:]
    if raw_response.endswith('```'):
        raw_response = raw_response[:-3]
    
    raw_response = raw_response.strip()
    
    try:
        return json.loads(raw_response, strict=False)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        # Fallback to graceful degradation if JSON is completely mangled
        return {
            "response": raw_response,
            "care_memories_created": [],
            "status": "error"
        }

import os
import csv

KNOWN_SPECIES = []

def get_known_species():
    global KNOWN_SPECIES
    if not KNOWN_SPECIES:
        csv_path = os.path.join(os.path.dirname(__file__), 'scripts', 'plant_care_data_full.csv')
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                KNOWN_SPECIES = [row['species'].strip() for row in reader if row.get('species')]
        except Exception as e:
            print(f"Failed to load CSV: {e}")
            KNOWN_SPECIES = []
    return KNOWN_SPECIES

async def identify_plant_species(query: str):
    print(f"\n[DEBUG] Identifying species for: {query}")
    
    known = get_known_species()
    # It's okay to send 1200 names, it's just a few kb. The Nemotron model has 32k context limit.
    known_str = ", ".join(known)
    
    prompt = f"""You are a botanical taxonomy assistant.
The user provides a common name, scientific name, or description of a plant (User Query).
You have a specific database of known plant species.
KNOWN DATABASE SPECIES:
[{known_str}]

Your task:
1. Identify the plant the user is referring to.
2. Find the EXACT MATCHING string from the KNOWN DATABASE SPECIES list.
3. You must respond strictly in JSON format with a single key 'names' containing a LIST of strings.
4. If you find a perfect or near-perfect match in the database, put it first in the list EXACTLY as it appears in the database.
5. You can also include other synonyms as backup.
Example: {{"names": ["Exact Database Name", "Another Synonym"]}}"""
    
    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"User Query: {query}\n\nRespond with JSON matching: {{\"names\": [\"Name 1\", \"Name 2\"]}}"}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content).get("names", [])

