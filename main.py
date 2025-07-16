import asyncio
from tooling.models.model import Model

model = Model("gpt-4o-mini")

async def test():
    response = await model.generate("pick a random number between 1 and 100")
    print(response)

if __name__ == "__main__":
    asyncio.run(test()) 