import os

from dotenv import load_dotenv

load_dotenv()

PG_DSN = os.getenv("DATABASE_URL")
BASE_URL = "https://swapi.dev/api/people/"
CHUNK_SIZE = 10
PEOPLE_COUNT = 80
