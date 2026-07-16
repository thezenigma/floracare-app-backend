import os
import sys
import asyncio
import csv
import json
import time
import chromadb

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import NVIDIA_API_KEY, NVIDIA_BASE_URL, MODEL_NAME
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "plant_care_data_full.csv")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, "checkpoint.json")
FIELDNAMES = ["species", "watering_frequency_days", "fertilizing_frequency_days", "sunlight_needs"]

# --- Retry config ---
MAX_RETRIES = 8
BASE_DELAY_SECONDS = 3.0   # seconds between each request (safe under 40 RPM)
RETRY_BASE = 5             # base seconds for exponential backoff on 429


async def query_plant_info(species: str, context: str) -> dict | None:
    system_prompt = (
        "You are a botanical data extraction assistant. "
        "Extract the care requirements for the specified plant based ONLY on the provided context. "
        "Output ONLY raw JSON with no markdown or backticks. "
        'Schema: {"species": "string", "watering_frequency_days": int, '
        '"fertilizing_frequency_days": int, "sunlight_needs": "string"}'
        "If context lacks exact days, make a logical botanical estimate."
    )
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Plant Species: {species}\n\nContext:\n{context[:4000]}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            err = str(e)
            if "429" in err:
                wait = RETRY_BASE * (2 ** (attempt - 1))
                print(f"  [429] Rate limited. Waiting {wait}s before retry {attempt}/{MAX_RETRIES}...")
                await asyncio.sleep(wait)
            else:
                print(f"  [ERROR] Unrecoverable error for '{species}': {e}")
                return None
    print(f"  [FAILED] Gave up on '{species}' after {MAX_RETRIES} retries.")
    return None


def load_checkpoint() -> set:
    """Returns a set of plant names that have already been processed."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_checkpoint(done: set):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(done), f)


def append_row(row: dict):
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)


async def main():
    print("Connecting to ChromaDB...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
    from chromadb.config import Settings
    db_client = chromadb.PersistentClient(path=db_path, settings=Settings(anonymized_telemetry=False))
    collection = db_client.get_collection("plants")
    data = collection.get()

    # Build unique plant map {name -> document}
    unique_plants = {}
    for meta, doc in zip(data["metadatas"], data["documents"]):
        if meta and "name" in meta and meta["name"] not in unique_plants:
            unique_plants[meta["name"]] = doc

    total = len(unique_plants)
    print(f"Found {total} unique plants in the RAG database.")

    # Resume support: load already-done set
    done = load_checkpoint()
    remaining = [(n, d) for n, d in unique_plants.items() if n not in done]
    print(f"Already processed: {len(done)}. Remaining: {len(remaining)}.")

    # Ensure CSV exists with header if starting fresh
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

    count = len(done)
    for name, doc in remaining:
        count += 1
        print(f"[{count}/{total}] Processing: {name}...")

        result = await query_plant_info(name, doc)

        if result:
            append_row(result)
        else:
            # On permanent failure, write a placeholder row so nothing is skipped
            append_row({
                "species": name,
                "watering_frequency_days": -1,
                "fertilizing_frequency_days": -1,
                "sunlight_needs": "UNKNOWN - REVIEW MANUALLY"
            })
        # Always checkpoint using the ChromaDB name (not LLM output) for consistent resume
        done.add(name)
        save_checkpoint(done)

        # Respectful delay between requests
        await asyncio.sleep(BASE_DELAY_SECONDS)

    print(f"\nAll {total} plants processed! CSV: {OUTPUT_CSV}")
    # Clean up checkpoint on success
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
    print("Checkpoint file removed. Run complete.")


if __name__ == "__main__":
    asyncio.run(main())
