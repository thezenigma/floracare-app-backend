import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import NVIDIA_API_KEY, NVIDIA_BASE_URL
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)

async def test_vision():
    # Use a public image of a cat
    test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
    
    import httpx
    import base64
    
    print("Fetching image and converting to base64...")
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get(test_image_url)
        b64 = base64.b64encode(resp.content).decode('utf-8')
        img_data = f"data:image/jpeg;base64,{b64}"
        
    print("Sending vision request with URL...")
    try:
        response = await client.chat.completions.create(
            model="meta/llama-3.2-11b-vision-instruct",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {"type": "image_url", "image_url": {"url": img_data}}
                ]}
            ],
            temperature=0.1,
            max_tokens=300
        )
        print("Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_vision())
