import csv
import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
csv_path = r'f:\Floracare\backend\scripts\plant_care_data_full.csv'

async def update_db():
    print("Reading CSV and updating Supabase DB...")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        updates = []
        for row in reader:
            updates.append({
                "species": row["species"],
                "common_name": row["common_name"]
            })
    
    print(f"Total rows to update: {len(updates)}")
    # Supabase bulk upsert
    batch_size = 100
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i+batch_size]
        # Use species to update the common_name
        for item in batch:
            try:
                supabase.table('plant_care_reference').update({'common_name': item['common_name']}).eq('species', item['species']).execute()
            except Exception as e:
                pass
        print(f"Processed {i + len(batch)} rows...")
        
    print("Database updated!")

if __name__ == "__main__":
    asyncio.run(update_db())
