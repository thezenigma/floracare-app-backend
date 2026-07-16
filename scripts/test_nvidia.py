import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

async def test():
    client = AsyncOpenAI(api_key=os.getenv('NVIDIA_API_KEY'), base_url='https://integrate.api.nvidia.com/v1')
    try:
        r = await client.chat.completions.create(
            model='meta/llama-3.1-8b-instruct',
            messages=[{'role': 'user', 'content': 'hello'}],
            temperature=0.3
        )
        print("Success:", r.choices[0].message.content)
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
