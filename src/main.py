from fastapi import FastAPI
from src.books.router import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting")
    await init_db()
    yield
    print(f"Server stop")



app = FastAPI(
    title="Books Backend",
    description="A REST API for Books",
    lifespan=life_span
)

app.include_router(book_router, prefix="/books/v1", tags=['books'])