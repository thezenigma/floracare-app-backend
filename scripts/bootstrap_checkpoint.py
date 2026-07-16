"""
Rebuilds checkpoint.json by taking the first N plant names directly from ChromaDB
(in the same iteration order as generate_plant_data.py), matching however many
rows are already in the CSV (excluding the header).
This guarantees the name format in the checkpoint matches what the script tracks.
"""
import csv
import json
import os
import chromadb

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "plant_care_data_full.csv")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, "checkpoint.json")

# 1. Count how many data rows are already in the CSV
with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
    rows_done = sum(1 for r in csv.DictReader(f) if r.get("species", "").strip())

print(f"CSV has {rows_done} completed data rows.")

# 2. Pull the plant names from ChromaDB in the same order the script iterates them
db_path = os.path.join(os.path.dirname(SCRIPT_DIR), "chroma_db")
from chromadb.config import Settings
db_client = chromadb.PersistentClient(path=db_path, settings=Settings(anonymized_telemetry=False))
collection = db_client.get_collection("plants")
data = collection.get()

unique_plants_ordered = []
seen = set()
for meta in data["metadatas"]:
    if meta and "name" in meta and meta["name"] not in seen:
        seen.add(meta["name"])
        unique_plants_ordered.append(meta["name"])

print(f"Total unique plants in ChromaDB: {len(unique_plants_ordered)}")

# 3. Mark the first `rows_done` names as completed
done = set(unique_plants_ordered[:rows_done])
print(f"Marking first {rows_done} ChromaDB plants as done: {sorted(list(done))[:5]}... etc.")

with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
    json.dump(list(done), f)

print(f"\nCheckpoint rebuilt with {len(done)} entries.")
print(f"Saved to: {CHECKPOINT_FILE}")
print("Now run generate_plant_data.py — it will skip these and only fetch the remaining plants.")
