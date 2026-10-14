from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AuthorIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class AuthorOut(AuthorIn):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ReaderIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class ReaderOut(ReaderIn):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    author_id: int


class BookOut(BookIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reader_id: int | None
