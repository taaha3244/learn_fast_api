from fastapi import FastAPI,status
from typing_extensions import Dict, List
from pydantic import BaseModel
from fastapi.exceptions import HTTPException



books = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "published_year": 1960,
        "genre": "Fiction",
        "pages": 281
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "published_year": 1949,
        "genre": "Dystopian Fiction",
        "pages": 328
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "published_year": 1813,
        "genre": "Romance",
        "pages": 432
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "published_year": 1925,
        "genre": "Classic Fiction",
        "pages": 180
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "published_year": 1937,
        "genre": "Fantasy",
        "pages": 310
    },
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "published_year": 1997,
        "genre": "Fantasy",
        "pages": 223
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "published_year": 1951,
        "genre": "Coming-of-age Fiction",
        "pages": 234
    },
    {
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "published_year": 1954,
        "genre": "Fantasy",
        "pages": 1178
    },
    {
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "published_year": 1866,
        "genre": "Psychological Fiction",
        "pages": 671
    },
    {
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel García Márquez",
        "published_year": 1967,
        "genre": "Magical Realism",
        "pages": 417
    }
]




app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str
    pages: int


@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


@app.post("/books",status_code=status.HTTP_201_CREATED)
async def create_new_book(book_data: Book) :
    new_book= book_data.model_dump()
    books.append(new_book)
    return books


@app.get("/book/{title}")
async def  get_book_by_title(title:str):
        
        for book in books:
            if book['title'].lower().strip()==title.lower().strip():
                return book
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")



class Update_Books(BaseModel):
     Author : str

@app.patch("/book/{title}")
async def  update_book_by_title(title:str , update_data:Update_Books):
        
        for book in books:
            if book['title'].lower().strip()==title.lower().strip():
                book['author'] = update_data.Author
                return book
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")


@app.delete("/delete_book/{title}")

async def delete_book(title:str):
     for book in books:
          if book['title'].lower().strip()==title.lower().strip():
            books.remove(book)
            return f"The book {title} has been removed"
          
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
