from fastapi import  APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from src.books.books_data import books

book_router=APIRouter()

# Pydantic model for Book
class Book(BaseModel):
    id: int
    title: str
    author: str
    year_published: int
    genre: str
    pages: int
    isbn: str
    price: float
    in_stock: bool

# Pydantic model for creating a new book (id will be assigned automatically)
class BookCreate(BaseModel):
    title: str
    author: str
    year_published: int
    genre: str
    pages: int
    isbn: str
    price: float
    in_stock: bool

# Pydantic model for updating a book (all fields optional except id)
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year_published: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    isbn: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None



# Helper function to find a book by ID
def find_book_by_id(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            return (index, book)
    return (None, None)


# GET endpoint - Retrieve all books
@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    return books


# GET endpoint - Retrieve a single book by ID
@book_router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int):
    index, book = find_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {book_id} not found")
    return book


# POST endpoint - Add a new book
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    # Generate a new ID (max ID + 1)
    new_id = max([b["id"] for b in books]) + 1 if books else 1
    
    # Create new book with the generated ID
    new_book = book.model_dump()
    new_book["id"] = new_id
    
    # Add the book to our collection
    books.append(new_book)
    return new_book


# PUT endpoint - Update a book
@book_router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update: BookUpdate):
    index, book = find_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {book_id} not found")
    
    # Update only the fields that are provided
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:  # Skip None values
            books[index][key] = value
            
    return books[index]


# DELETE endpoint - Delete a book
@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    index, book = find_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {book_id} not found")
    
    # Remove the book from our collection
    books.pop(index)
    return None


