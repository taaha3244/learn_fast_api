from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlmodel import SQLModel
from src.config import Config

# Parse the URL without query parameters to handle SSL separately
base_url = Config.DATABASE_URL.split("?")[0]

# Create an async engine directly with connection pooling settings
engine = create_async_engine(
    base_url,
    connect_args={"ssl": True},
    pool_pre_ping=True,  # Check connection before using it
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=True
)

# Create an async session factory
async_session_maker = async_sessionmaker(
    engine, 
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_db():
    # Import models here to ensure they're registered with SQLModel
    from src.books.models import Book
    
    async with engine.begin() as conn:
        # Create tables based on SQLModel classes
        await conn.run_sync(SQLModel.metadata.create_all)
        
        # Test query
        statement = text("SELECT 'hello';")
        result = await conn.execute(statement)
        print(result.all())

# Dependency for route handlers
async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()