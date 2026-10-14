import pytest
from pydantic import ValidationError

from app.schemas import AuthorIn, BookIn, ReaderIn


def test_author_valid():
    author = AuthorIn(name="Лев Толстой")
    assert author.name == "Лев Толстой"


def test_author_name_too_short():
    with pytest.raises(ValidationError):
        AuthorIn(name="Л")


def test_book_year_too_big():
    with pytest.raises(ValidationError):
        BookIn(title="Война и мир", year=3000, author_id=1)


def test_book_without_author():
    with pytest.raises(ValidationError):
        BookIn(title="Война и мир", year=1869)


def test_reader_wrong_email():
    with pytest.raises(ValidationError):
        ReaderIn(name="Иван Петров", email="not-an-email")
