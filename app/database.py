from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User

client = AsyncIOMotorClient(settings.mongodb_url)
database = client[settings.mongodb_db]


async def init_db():
    await init_beanie(
        database=database,
        document_models=[User],
    )