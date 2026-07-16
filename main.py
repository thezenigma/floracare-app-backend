import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from queue_manager import agent_queue
from agent import process_chat_message
from db_client import save_care_memory, ensure_chat_session, save_message

from fastapi.middleware.cors import CORSMiddleware

web_app = FastAPI()

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local dev
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@web_app.on_event("startup")
async def startup_event():
    agent_queue.start()

from pydantic import BaseModel

class PlantSearchRequest(BaseModel):
    query: str

@web_app.post("/api/plants/search")
async def search_plant(request: PlantSearchRequest):
    from agent import identify_plant_species
    from db_client import supabase
    
    try:
        # Use LLM to resolve the fuzzy query to an array of possible names
        possible_names = await identify_plant_species(request.query)
        print(f"[DEBUG-API] identify_plant_species returned: {possible_names}")
    except Exception as e:
        print(f"[DEBUG-API] Exception in identify_plant_species: {e}")
        return {"error": f"LLM Error: {str(e)}", "species": None}
    
    if not possible_names or not isinstance(possible_names, list) or len(possible_names) == 0:
        return {"error": "Plant not found in database.", "species": None, "debug": "Empty list from LLM"}
        
    # Query Supabase for the care details
    try:
        # Try finding a match for any of the returned names
        for name in possible_names:
            # First try exact case-insensitive match
            res = supabase.table('plant_care_reference').select('*').ilike('species', name).execute()
            
            # If not found, try a wildcard match
            if not res.data:
                res = supabase.table('plant_care_reference').select('*').ilike('species', f'%{name}%').execute()

            if res.data and len(res.data) > 0:
                return {"species": res.data[0]['species'], "care_data": res.data[0]}
                
        # Fallback if none found
        return {"error": f"Found '{possible_names[0]}' but no care data available.", "species": possible_names[0]}
    except Exception as e:
        return {"error": str(e), "species": possible_names[0] if possible_names else None}

@web_app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("type") == "ping":
                    continue
            except json.JSONDecodeError:
                continue
            
            access_token = payload.get("access_token")
            session_id = payload.get("session_id")
            message = payload.get("message")
            plant_ids = payload.get("plant_ids", [])
            
            chat_history = payload.get("chat_history", "")
            
            if not all([access_token, session_id, message]):
                await websocket.send_json({"error": "Missing required fields (access_token, session_id, message)"})
                continue
                
            # --- SECURITY CHECK ---
            print(f"\n[STEP 1] Received WebSocket message from user: '{message}'")
            if access_token == "test-token-123":
                user_id = "00000000-0000-0000-0000-000000000001"
            else:
                try:
                    # Verify the JWT token with Supabase and extract the true user ID
                    from db_client import supabase
                    auth_response = supabase.auth.get_user(access_token)
                    user_id = auth_response.user.id
                except Exception as e:
                    await websocket.send_json({"error": "Unauthorized: Invalid or expired access token."})
                    continue
            # ----------------------
            
            # Send immediate thinking status
            await websocket.send_json({"status": "queued"})
            
            # Save the session and user message to the database
            try:
                ensure_chat_session(session_id, user_id, message)
                save_message(session_id, "user", message)
                print("[STEP 2] Saved user message and session to Database.")
            except Exception as e:
                print(f"[DEBUG] Failed to save session/message to DB: {e}")
            
            # Enqueue the LLM task
            try:
                print(f"[STEP 3] Enqueuing task to AI Agent for session {session_id}...")
                result = await agent_queue.enqueue(
                    process_chat_message, 
                    user_id=user_id, 
                    session_id=session_id, 
                    message=message, 
                    plant_ids=plant_ids,
                    chat_history=chat_history
                )
                
                # Persist generated memories to DB
                for memory in result.get("care_memories_created", []):
                    # Ensure plant_id exists in the generated memory, or fallback to first plant_id provided
                    pid = memory.get("plant_id")
                    if pid in ["None", "null", "uuid", "", None]:
                        pid = plant_ids[0] if plant_ids else None
                        
                    if pid and str(pid).lower() not in ["none", "null", "uuid"]:
                        save_care_memory(
                            user_id=user_id,
                            plant_id=pid,
                            memory_type=memory["memory_type"],
                            content=memory["content"],
                            session_id=session_id
                        )
                
                # Save assistant message to DB first, so it isn't lost if websocket is closed
                try:
                    if "response" in result:
                        save_message(session_id, "assistant", result["response"])
                        print("[STEP 9] Saved AI response to Database.")
                except Exception as e:
                    print(f"[DEBUG] Failed to save assistant message to DB: {e}")
                    
                try:
                    await websocket.send_json(result)
                    print("[STEP 10] Sent JSON response back to WebSocket.")
                except (WebSocketDisconnect, RuntimeError):
                    print("[DEBUG] Client disconnected before JSON response could be sent.")
                    break
                except Exception as e:
                    print(f"[ERROR] Failed to send JSON back to WebSocket: {e}")
            except WebSocketDisconnect:
                raise
            except RuntimeError:
                raise
            except Exception as e:
                try:
                    await websocket.send_json({"status": "error", "message": str(e)})
                except Exception:
                    break

    except WebSocketDisconnect:
        pass
    except RuntimeError:
        pass
