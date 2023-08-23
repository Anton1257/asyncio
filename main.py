import asyncio
from datetime import datetime

from common import CHUNK_SIZE
from swapi_people.api import chunked_async, get_people, insert_people
from swapi_people.database import Base, engine


async def main():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    async for chunk in chunked_async(get_people(), CHUNK_SIZE):
        asyncio.create_task(insert_people(chunk))
    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start)
