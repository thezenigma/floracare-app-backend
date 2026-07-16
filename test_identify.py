import asyncio
from agent import identify_plant_species

async def test():
    print("Identifying...")
    res = await identify_plant_species("Swiss Cheese Plant")
    print(f"Result: {res}")

if __name__ == "__main__":
    asyncio.run(test())
