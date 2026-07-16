import asyncio
from agent import identify_plant_species

async def test():
    names = await identify_plant_species("Gray Dragon")
    print("Found names:", names)

if __name__ == "__main__":
    asyncio.run(test())
