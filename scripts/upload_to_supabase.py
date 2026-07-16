import os
import csv
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
if not key:
    key = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

records = []
with open("plant_care_data_full.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean up data
        try:
            water = int(float(row.get('watering_frequency_days') or -1))
        except ValueError:
            water = -1
            
        try:
            fert = int(float(row.get('fertilizing_frequency_days') or -1))
        except ValueError:
            fert = -1
            
        records.append({
            "species": row.get('species', '').strip(),
            "watering_frequency_days": water,
            "fertilizing_frequency_days": fert,
            "sunlight_needs": row.get('sunlight_needs', '').strip()
        })

# Deduplicate by species
unique_records = {}
for r in records:
    if r['species']:
        unique_records[r['species']] = r
records = list(unique_records.values())

# Upsert in batches of 100
BATCH_SIZE = 100
for i in range(0, len(records), BATCH_SIZE):
    batch = records[i:i + BATCH_SIZE]
    try:
        data, count = supabase.table('plant_care_reference').upsert(batch).execute()
        print(f"Uploaded batch {i//BATCH_SIZE + 1}/{(len(records) + BATCH_SIZE - 1)//BATCH_SIZE}")
    except Exception as e:
        print(f"Error on batch {i//BATCH_SIZE + 1}: {e}")

print("Upload complete.")
