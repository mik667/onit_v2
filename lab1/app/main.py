from fastapi import FastAPI

from app.routers import authors, books, readers

app = FastAPI(title="Библиотека")

app.include_router(authors.router)
app.include_router(books.router)
app.include_router(readers.router)
