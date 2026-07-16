# 🌿 FloraCare Backend

Welcome to the backend architecture for **FloraCare**, an AI-powered digital garden assistant. This backend provides a robust, real-time API for plant identification, conversational care assistance, and deep-dive botanical knowledge retrieval using advanced AI agents and RAG (Retrieval-Augmented Generation) technology.

🔗 **Looking for the Frontend?** 
The user interface is built with React and Vite. You can find the frontend repository here: [FloraCare Frontend Repository](https://github.com/thezenigma/floracare-app)

---

## 🏗️ Architecture Overview

The FloraCare backend is built with **FastAPI** to ensure high-performance, asynchronous request handling. It employs a **Polyrepo** structure, keeping this logic strictly separated from the frontend React application. 

### Core Components
1. **The Brain (Agent & LLM):** Powered by the `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` model, the AI serves as a hyper-intelligent botanical assistant. It handles natural language conversations, diagnosing plant health issues, and perfectly matching user queries against a massive database of 1,232 plant species via context-injected taxonomy.
2. **The RAG Database (ChromaDB):** A local vector database containing highly detailed, deep-dive plant care articles scraped from *The Spruce*. Using `nomic-ai/nomic-embed-text-v1.5` embeddings, this allows the AI to pull hyper-specific, real-world care instructions to answer complex user questions.
3. **The Structured Database (Supabase):** Our primary PostgreSQL database hosted on Supabase. It stores user profiles, their digital garden (saved plants), care journals, and the master reference list of all 1,232 plant species and their exact watering/sunlight requirements.
4. **Real-Time Websockets:** Provides live, instant messaging for the AI chat interface, equipped with keep-alive heartbeat filtering to maintain stable, long-running connections (crucial for tunneling via Ngrok or cloud hosting).

---

## 🚀 Setup & Installation

Follow these steps to deploy the FloraCare backend locally on your machine.

### Prerequisites
- **Python 3.10+** (Tested on Python 3.12)
- A **Supabase** account and project
- An **NVIDIA API Key** (for accessing the Nemotron LLM)
- **Ngrok** (For tunneling localhost to the web)

### 1. Clone the Repository
```bash
git clone https://github.com/thezenigma/floracare-app-backend.git
cd floracare-app-backend
```

### 2. Create a Virtual Environment
It is highly recommended to isolate your dependencies using a virtual environment.
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root of the project:
```bash
touch .env
```
Add your sensitive credentials to the `.env` file:
```ini
SUPABASE_URL="your-supabase-project-url"
SUPABASE_KEY="your-supabase-service-role-key"
NVIDIA_API_KEY="your-nvidia-api-key"
```

### 5. Initialize the Databases
Before running the server, you need to populate both of your databases.

**A. Supabase (The Master List):**
Run the upload script to populate your Supabase `plant_care_reference` table with the 1,232 plant species.
```bash
python scripts/upload_to_supabase.py
```

**B. ChromaDB (The RAG Deep-Dive):**
Run the ingestion script to scrape and embed the deep-dive botanical articles into your local vector database. Note: A Chromium browser will visibly open to bypass bot protections.
```bash
python scripts/chroma_ingest.py
```

### 6. Start the Server
Run the FastAPI application using Uvicorn.
```bash
python -m uvicorn main:web_app --reload
```
The server will now be live at `http://localhost:8000`. 

### 7. Tunneling with Ngrok (Connecting the Frontend)
If you are deploying the React frontend on a platform like Vercel (which enforces HTTPS), the frontend cannot talk directly to your `localhost:8000`. You must create a secure tunnel.

If you don't have Ngrok installed, [download it here](https://ngrok.com/download).

In a **new terminal window**, run:
```bash
ngrok http 8000
```
Ngrok will give you an HTTPS forwarding URL (e.g., `https://abc-123.ngrok-free.app`). 
Copy this URL and paste it into your **Frontend** environment variables as the `VITE_API_URL` so that the cloud-hosted React app knows how to reach your local backend!

---

## 🔐 Security & Best Practices
- **Service Keys:** This backend uses the Supabase Service Role Key to bypass RLS (Row Level Security) safely on the server side. Never expose your `.env` file or commit it to version control.
- **WebSocket Stability:** Idle WebSockets are prone to dropping on cloud deployments or Ngrok tunnels. We have implemented a rigid keep-alive heartbeat system (`ping`/`pong`) that maintains the connection indefinitely without disrupting the chat UI.
