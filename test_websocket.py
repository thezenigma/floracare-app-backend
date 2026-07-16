import asyncio
import websockets
import json
import os
import sys
from dotenv import load_dotenv

# Load keys
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

async def test_chat_server():
    print("🔑 Bypassing Supabase auth for local testing using test token...")
    token = "test-token-123"
    
    print(f"✅ Token acquired! Connecting to WebSocket...")

    # 2. Connect to the local FastAPI server
    uri = "ws://localhost:8000/ws/chat"
    try:
        async with websockets.connect(uri) as websocket:
            
            # 3. Send the payload
            payload = {
                "access_token": token,
                "session_id": "test-session-123",
                "message": "The tips of my aloe vera are turning brown and crispy. What should I do?",
                "plant_ids": []
            }
            
            print(f"📤 Sending Message: {payload['message']}")
            await websocket.send(json.dumps(payload))
            
            # 4. Listen for the responses
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                
                if data.get("status") == "queued":
                    print("⏳ Server acknowledged: Message Queued!")
                elif data.get("status") == "error":
                    print(f"❌ Error from server: {data.get('response')}")
                    break
                else:
                    print("\n🤖 AI Agent Response:")
                    print(json.dumps(data, indent=2))
                    break
                    
    except Exception as e:
        print(f"❌ WebSocket connection failed (is the server running?): {e}")

if __name__ == "__main__":
    asyncio.run(test_chat_server())
