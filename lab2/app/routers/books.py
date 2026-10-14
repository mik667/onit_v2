from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import Author, Book, Reader
from app.schemas import BookIn, BookOut

router = APIRouter(tags=["Книги"])

MAX_BOOKS_PER_READER = 3


@router.get("/books", response_model=list[BookOut])
def get_books(db=Depends(get_db)):
    return db.query(Book).all()


@router.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db=Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@router.post("/books", response_model=BookOut, status_code=201)
def create_book(data: BookIn, db=Depends(get_db)):
    if db.get(Author, data.author_id) is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    book = Book(title=data.title, year=data.year, author_id=data.author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookIn, db=Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    if db.get(Author, data.author_id) is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    book.title = data.title
    book.year = data.year
    book.author_id = data.author_id
    db.commit()
    db.refresh(book)
    return book


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db=Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    db.delete(book)
    db.commit()


@router.post("/books/{book_id}/issue/{reader_id}", response_model=BookOut)
def issue_book(book_id: int, reader_id: int, db=Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    reader = db.get(Reader, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    if book.reader_id is not None:
        raise HTTPException(status_code=400, detail="Книга уже выдана")
    if len(reader.books) >= MAX_BOOKS_PER_READER:
        raise HTTPException(status_code=400, detail="У читателя уже 3 книги")
    book.reader_id = reader.id
    db.commit()
    db.refresh(book)
    return book


@router.post("/books/{book_id}/return", response_model=BookOut)
def return_book(book_id: int, db=Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    book.reader_id = None
    db.commit()
    db.refresh(book)
    return book
