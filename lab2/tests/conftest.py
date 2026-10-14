import os

os.environ["POSTGRES_DB"] = "library_test"

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import engine
from app.main import app


@pytest.fixture
def client():
    command.upgrade(Config("alembic.ini"), "head")
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE books, authors, readers RESTART IDENTITY"))
    return TestClient(app)
