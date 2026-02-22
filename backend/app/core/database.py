# app/core/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None
database = None


async def connect_to_mongo():
    global client, database
    client = AsyncIOMotorClient(settings.MONGO_URL)
    database = client[settings.DATABASE_NAME]
    print("✅ MongoDB Connected")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ MongoDB Disconnected")


def get_database():
    if database is None:
        raise RuntimeError("Database not initialized")
    return database