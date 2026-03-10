from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.homework_system

# Collections
semesters_col = db.semesters
courses_col   = db.courses
homeworks_col = db.homeworks
exams_col     = db.exams
images_col    = db.images
