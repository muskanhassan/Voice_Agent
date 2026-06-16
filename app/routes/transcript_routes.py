from fastapi import APIRouter
from app.database import transcripts_collection

router = APIRouter()


@router.get("/transcripts")
def get_transcripts():

    transcripts = list(
        transcripts_collection.find()
    )

    # Convert ObjectId to string
    for t in transcripts:
        t["_id"] = str(t["_id"])

    return transcripts