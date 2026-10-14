from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import Author
from app.schemas import AuthorIn, AuthorOut

router = APIRouter(tags=["Авторы"])


@router.get("/authors", response_model=list[AuthorOut])
def get_authors(db=Depends(get_db)):
    return db.query(Author).all()


@router.get("/authors/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db=Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return author


@router.post("/authors", response_model=AuthorOut, status_code=201)
def create_author(data: AuthorIn, db=Depends(get_db)):
    author = Author(name=data.name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@router.put("/authors/{author_id}", response_model=AuthorOut)
def update_author(author_id: int, data: AuthorIn, db=Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    author.name = data.name
    db.commit()
    db.refresh(author)
    return author


@router.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: int, db=Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    if author.books:
        raise HTTPException(status_code=400, detail="Нельзя удалить автора, у которого есть книги")
    db.delete(author)
    db.commit()
