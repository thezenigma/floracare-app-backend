import os
import sys
import time
import json
import sqlite3
import asyncio
from collections import deque

# Add the parent directory to sys.path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import process_chat_message

# --- SQLite Memory Setup ---
MEMORY_DB = os.path.join(os.path.dirname(__file__), "test_memory.db")

def init_db():
    conn = sqlite3.connect(MEMORY_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  role TEXT,
                  content TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

def save_memory(conn, role, content):
    c = conn.cursor()
    c.execute("INSERT INTO memory (role, content) VALUES (?, ?)", (role, content))
    conn.commit()

def get_chat_history(conn, limit=5):
    c = conn.cursor()
    c.execute("SELECT role, content FROM memory ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    return list(reversed(rows))

# --- Rate Limiter ---
class RateLimiter:
    def __init__(self, max_requests=40, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def wait_if_needed(self):
        now = time.time()
        # Remove requests outside the time window
        while self.requests and self.requests[0] <= now - self.time_window:
            self.requests.popleft()
            
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                print(f"\n[Rate Limit] 40 RPM reached. Pausing for {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                
        self.requests.append(time.time())

# --- Interactive Tester ---
async def main():
    print("=" * 60)
    print("🌿 FloraCare Interactive RAG Tester (NVIDIA NIM)")
    print("Type '/clear' to wipe memory, '/quit' to exit.")
    print("=" * 60)
    
    conn = init_db()
    rate_limiter = RateLimiter(max_requests=40, time_window=60)
    
    # Pre-defined FM Tests for easy access
    fm_tests = {
        "/fm1": "I bought a ZZ plant and its leaves are turning yellow, but the soil is bone dry. Why?",
        "/fm2": "Compare the watering needs of a ZZ Plant and an Agave.",
        "/fm3": "What is the scientific name for the African Milk Tree and does it need direct sunlight?",
        "/fm4": "Based on my recent journal saying I watered my ZZ plant yesterday, when should I water it next?"
    }

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in ['/quit', '/exit']:
            print("Exiting RAG Tester...")
            break
            
        if user_input.lower() == '/clear':
            c = conn.cursor()
            c.execute("DELETE FROM memory")
            conn.commit()
            print("🧹 Chat memory cleared.")
            continue
            
        if user_input.lower() in fm_tests:
            user_input = fm_tests[user_input.lower()]
            print(f"[Executing {user_input.split()[0]} Test] -> {user_input}")
            
        # 1. Enforce Rate Limits
        rate_limiter.wait_if_needed()
        
        # 2. Append history to query (primitive memory injection for testing)
        history = get_chat_history(conn)
        history_context = "\n".join([f"{r}: {c}" for r, c in history])
        
        # 3. Process via Agent
        print("🤖 FloraCare is thinking (Querying RAG & NVIDIA NIM)...")
        start_time = time.time()
        
        try:
            # We use a dummy UUID for the tester since Supabase requires the uuid type
            response_json = await process_chat_message(
                user_id="00000000-0000-0000-0000-000000000001",
                session_id="00000000-0000-0000-0000-000000000002",
                message=user_input,
                plant_ids=[],
                chat_history=history_context
            )
            
            elapsed = time.time() - start_time
            
            # Format output
            print(f"\n✅ Response received in {elapsed:.2f}s:")
            print("-" * 60)
            print(response_json.get("response", "No response field in JSON."))
            print("-" * 60)
            
            if response_json.get("care_memories_created"):
                print("🧠 Memories Created:")
                for mem in response_json["care_memories_created"]:
                    print(f"  - [{mem.get('memory_type')}] {mem.get('content')}")
            
            # Save to local SQLite memory
            save_memory(conn, "User", user_input)
            save_memory(conn, "FloraCare", response_json.get("response", ""))
            
        except Exception as e:
            print(f"\n❌ Error calling agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())
