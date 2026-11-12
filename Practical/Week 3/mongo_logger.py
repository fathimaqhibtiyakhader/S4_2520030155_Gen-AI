
from pymongo import MongoClient
from datetime import datetime, timezone
import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

DATABASE_NAME = "llm_monitoring"
COLLECTION_NAME = "call_logs"


def get_collection():
    """Connect to MongoDB and return the call_logs collection."""

    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    # Verify that MongoDB is reachable.
    client.admin.command("ping")

    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    return client, collection


def log_call(call_data):
    """Save an LLM API call and its details in MongoDB."""

    client = None

    try:
        client, collection = get_collection()

        log_entry = {
            "provider": call_data.get("provider"),
            "model": call_data.get("model"),
            "prompt": call_data.get("prompt"),
            "response": call_data.get("response"),
            "input_tokens": call_data.get("input_tokens", 0),
            "output_tokens": call_data.get("output_tokens", 0),
            "response_time": call_data.get("response_time", 0),
            "cost": call_data.get("cost", 0),
            "timestamp": datetime.now(timezone.utc)
        }

        result = collection.insert_one(log_entry)

        print("Call successfully logged!")
        print("MongoDB Document ID:", result.inserted_id)

        return result.inserted_id

    except Exception as error:
        print("MongoDB logging failed:", error)
        return None

    finally:
        if client:
            client.close()


if __name__ == "__main__":
    sample_data = {
        "provider": "test",
        "model": "test-model",
        "prompt": "Hello MongoDB!",
        "response": "MongoDB connection successful!",
        "input_tokens": 10,
        "output_tokens": 15,
        "response_time": 0.5,
        "cost": 0.001
    }

    log_call(sample_data)
