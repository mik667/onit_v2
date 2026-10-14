from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import Reader
from app.schemas import ReaderIn, ReaderOut

router = APIRouter(tags=["Читатели"])


@router.get("/readers", response_model=list[ReaderOut])
def get_readers(db=Depends(get_db)):
    return db.query(Reader).all()


@router.get("/readers/{reader_id}", response_model=ReaderOut)
def get_reader(reader_id: int, db=Depends(get_db)):
    reader = db.get(Reader, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader


@router.post("/readers", response_model=ReaderOut, status_code=201)
def create_reader(data: ReaderIn, db=Depends(get_db)):
    reader = Reader(name=data.name, email=data.email)
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


@router.put("/readers/{reader_id}", response_model=ReaderOut)
def update_reader(reader_id: int, data: ReaderIn, db=Depends(get_db)):
    reader = db.get(Reader, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    reader.name = data.name
    reader.email = data.email
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/readers/{reader_id}", status_code=204)
def delete_reader(reader_id: int, db=Depends(get_db)):
    reader = db.get(Reader, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    if reader.books:
        raise HTTPException(status_code=400, detail="Нельзя удалить читателя, у которого есть книги")
    db.delete(reader)
    db.commit()
