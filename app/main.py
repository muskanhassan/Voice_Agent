from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from app.services.transcript_service import save_transcript
import os

load_dotenv()

app = FastAPI()


# Static files
app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory="app/templates"
)


# Groq Client
client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


# Request Model
class ChatRequest(
    BaseModel
):
    message: str


# Home Page
@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Chat API
@app.post("/chat")
async def chat(
    data: ChatRequest
):

    try:

        response = (
            client.chat
            .completions
            .create(
                model=
                "llama-3.1-8b-instant",

                messages=[
                    {
                        "role":
                        "system",

                        "content":
                        "Reply shortly in English like a helpful AI assistant."
                    },

                    {
                        "role":
                        "user",

                        "content":
                        data.message
                    }
                ]
            )
        )

        reply = (
            response
            .choices[0]
            .message.content
        )

        print(
            "User:",
            data.message
        )

        print(
            "AI:",
            reply
        )

        # SAVE TO MONGODB
        save_transcript(
            user_message=
            data.message,

            agent_reply=
            reply
        )

        print(
            "Saved to MongoDB"
        )

        return {
            "reply":
            reply
        }

    except Exception as e:

        print(
            "Mongo/Groq Error:",
            e
        )

        return {
            "reply":
            "Something went wrong."
        }


#  temporary data 

@app.get("/test")
def test():

    from app.services.transcript_service import save_transcript

    save_transcript(
        "test user",
        "test ai"
    )

    return {
        "message": "saved"
    }        
    