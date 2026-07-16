import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, NVIDIA_API_KEY]):
    raise ValueError("Missing critical environment variables (SUPABASE_URL, SUPABASE_KEY, NVIDIA_API_KEY).")

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning" # User requested model
