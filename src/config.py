from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# Debugging
print(f"Current directory: {os.getcwd()}")
print(f"Env file exists: {os.path.exists('.env')}")

Config = Settings()

# Debugging
print(f"DATABASE_URL: {Config.DATABASE_URL}")