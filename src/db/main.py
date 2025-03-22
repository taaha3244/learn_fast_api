from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from src.config import Config

# Parse the URL without query parameters to handle SSL separately
base_url = Config.DATABASE_URL.split("?")[0]

# Create an async engine directly
engine = create_async_engine(
    base_url,
    connect_args={"ssl": True},
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello';")
        result = await conn.execute(statement)
        print(result.all())