from pymongo import (
    MongoClient
)

try:

    client = MongoClient(
        "mongodb://localhost:27017/"
    )

    db = client[
        "voice_agent_db"
    ]

    transcripts_collection = (
        db["transcripts"]
    )

    print(
        "✅ MongoDB Connected"
    )

except Exception as e:

    print(
        "❌ MongoDB Connection Error:",
        e
    )