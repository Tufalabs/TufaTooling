import asyncio
from tooling.models.model import Model

from tooling.utils.extractor.xml_tags import xml_tag_extractor

model = Model("gpt-4o-mini")

async def test():
    response = await model.generate("pick a random number between 1 and 100, output in <answer> tags")
    extracted = xml_tag_extractor(response, "answer")

    
    print(extracted)

if __name__ == "__main__":
    asyncio.run(test()) 