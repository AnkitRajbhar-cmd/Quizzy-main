from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client.get_database()

# Collections
users_collection = db.users
quizzes_collection = db.quizzes
scores_collection = db.quiz_scores
