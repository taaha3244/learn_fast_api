from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

from src.db.main import get_session
from src.books.models import Book, BookCreate, BookUpdate

book_router = APIRouter()

# GET endpoint - Retrieve all books
@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    print("Using database for get_all_books")
    result = await session.execute(select(Book))
    books = result.scalars().all()
    return books

# GET endpoint - Retrieve a single book by ID
@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {book_id} not found")
    return book

# POST endpoint - Add a new book
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    db_book = Book.model_validate(book)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

# PUT endpoint - Update a book
@book_router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: UUID, book_update: BookUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {book_id} not found")
    
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

# DELETE endpoint - Delete a book
@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {book_id} not found")
    
    await session.delete(db_book)
    await session.commit()
    return None