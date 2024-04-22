import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
#integrado es nombre para la base de datos
database = client.integrado

def collection(data):
    #student_collection = database.get_collection("students_collection")
    student_collection = database.get_collection(data)
    return student_collection

