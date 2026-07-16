import asyncio
import os
import sys

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import NVIDIA_API_KEY, NVIDIA_BASE_URL, MODEL_NAME
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)

async def test_llm():
    print("Testing LLM endpoint...")
    SYSTEM_PROMPT = """You are FloraCare AI, a professional botanist and friendly garden companion.
You must respond strictly in JSON format conforming to the exact output schema requested."""

    content_payload = "Recommend organic pest control for roses"
    
    text_prompt = f"Context:\n[]\n\nUser Message: {content_payload}\n\nRespond with JSON matching: {{\"response\": \"string\", \"care_memories_created\": [{{\"memory_type\": \"diagnosis|schedule|general\", \"content\": \"string\", \"plant_id\": \"uuid\"}}], \"status\": \"success\"}}\n\nCRITICAL: The 'response' string MUST be highly structured using Markdown (e.g., use **bolding**, bullets, and insert proper ESCAPED newlines like \\n\\n between paragraphs and steps for vertical readability). Do NOT output a single block of text."

    print(f"Sending request to {MODEL_NAME}...")
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        print("Response object:")
        print(response)
        
        content = response.choices[0].message.content
        print(f"Raw Content length: {len(content) if content else 'None'}")
        print(f"Raw Content: {content}")
        
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm())
