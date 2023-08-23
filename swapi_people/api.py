import asyncio
from http import HTTPStatus

from aiohttp import ClientSession
from more_itertools import chunked

from common import BASE_URL, CHUNK_SIZE, PEOPLE_COUNT

from .database import Session
from .models import PersonModel


async def extract_name_from_url(url, session):
    async with session.get(url) as response:
        data = await response.json()
        return data.get("name")


async def extract_names_from_urls(urls, session):
    names = []
    for url in urls:
        name = await extract_name_from_url(url, session)
        if name:
            names.append(name)
    return ", ".join(names)


async def chunked_async(async_iter, size):
    buffer = []
    while True:
        try:
            item = await async_iter.__anext__()
        except StopAsyncIteration:
            break
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []


async def insert_people(people_chunk):
    async with Session() as session:
        async with ClientSession() as session_deep:
            for people_json in people_chunk:
                if people_json.get("status") == HTTPStatus.NOT_FOUND:
                    break
                homeworld_name = await extract_name_from_url(
                    people_json["homeworld"], session_deep
                )
                films_names = await extract_names_from_urls(
                    people_json["films"], session_deep
                )
                species_names = await extract_names_from_urls(
                    people_json["species"], session_deep
                )
                starships_names = await extract_names_from_urls(
                    people_json["starships"], session_deep
                )
                vehicles_names = await extract_names_from_urls(
                    people_json["vehicles"], session_deep
                )
                new_people = PersonModel(
                    birth_year=people_json["birth_year"],
                    eye_color=people_json["eye_color"],
                    gender=people_json["gender"],
                    hair_color=people_json["hair_color"],
                    height=people_json["height"],
                    mass=people_json["mass"],
                    name=people_json["name"],
                    skin_color=people_json["skin_color"],
                    homeworld=homeworld_name,
                    films=films_names,
                    species=species_names,
                    starships=starships_names,
                    vehicles=vehicles_names,
                )
                session.add(new_people)
                await session.commit()


async def get_person(people_id: int, session: ClientSession):
    print(f"begin {people_id}")
    async with session.get(f"{BASE_URL}{people_id}") as response:
        if response.status == HTTPStatus.NOT_FOUND:
            return {"status": HTTPStatus.NOT_FOUND}
        json_data = await response.json()
        print(f"end {people_id}")
        return json_data


async def get_people():
    async with ClientSession() as session:
        for chunk in chunked(range(1, PEOPLE_COUNT), CHUNK_SIZE):
            coroutines = [get_person(people_id=i, session=session) for i in chunk]
            results = await asyncio.gather(*coroutines)
            for result in results:
                yield result
