import uuid
import sys
from db_client import get_user_plants, get_recent_journals

def test_supabase_connection():
    try:
        # Generate a dummy UUID
        dummy_user_id = str(uuid.uuid4())
        
        print("Testing get_user_plants...")
        plants = get_user_plants(dummy_user_id)
        print(f"Result: {plants}")
        
        print("\nTesting get_recent_journals...")
        journals = get_recent_journals(dummy_user_id)
        print(f"Result: {journals}")
        
        print("\n✅ Database connection and read operations succeeded! Tables are verified.")
    except Exception as e:
        print(f"\n❌ Error during database test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_supabase_connection()
