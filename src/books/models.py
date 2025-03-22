from typing import Optional
from sqlmodel import Field, SQLModel 
from datetime import datetime, timezone
import uuid
from uuid import UUID

# Define SQLModel models
class BookBase(SQLModel):
    title: str
    author: str
    year_published: int
    genre: str
    pages: int
    isbn: str
    price: float
    in_stock: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Book(BookBase, table=True):
    id: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )

class BookCreate(SQLModel):
    title: str
    author: str
    year_published: int
    genre: str
    pages: int
    isbn: str
    price: float
    in_stock: bool

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year_published: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    isbn: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))