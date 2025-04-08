import os



class Config:
    # DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_URL = 'postgresql+asyncpg://postgres:password@localhost:5432/dbname'


