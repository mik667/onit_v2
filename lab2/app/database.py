import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
