import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://scoreboard:scoreboard@localhost:5432/scoreboard"
)
