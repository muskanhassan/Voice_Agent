from app.database import (
    transcripts_collection
)


def save_transcript(
    user_message,
    agent_reply
):

    try:

        data = {

            "user_message":
            user_message,

            "agent_reply":
            agent_reply
        }

        result = (
            transcripts_collection
            .insert_one(data)
        )

        print(
            "✅ Mongo Saved:",
            result.inserted_id
        )

    except Exception as e:

        print(
            "❌ MongoDB Error:",
            e
        )