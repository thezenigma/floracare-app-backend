import httpx
import asyncio

async def main():
    print("starting request...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get('https://integrate.api.nvidia.com/v1/models')
            print(r.status_code)
    except Exception as e:
        print("Error:", e)

asyncio.run(main())
