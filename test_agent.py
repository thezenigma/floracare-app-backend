import asyncio
import os
import sys

# Add current dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import process_chat_message

async def main():
    print("Testing agent...")
    res = await process_chat_message("test_user", "test_session", "Hello!")
    print("Result:")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
