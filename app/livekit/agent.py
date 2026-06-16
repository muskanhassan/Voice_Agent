from app.services.transcript_service import save_transcript
from dotenv import load_dotenv
import asyncio

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)

from livekit.plugins import (
    groq,
    deepgram,
    cartesia
)

load_dotenv()


# Voices
VOICES = {
    "female":
    "79a125e8-cd45-4c13-8a67-188112f4dd22",

    "male":
    "a0e99841-438c-4a64-b679-ae501e7d6091"
}


class Assistant(Agent):

    def __init__(self):

        super().__init__(
            instructions="""
            You are a helpful AI assistant.

            Keep answers short.

            Speak naturally.

            If user speaks Hindi,
            reply in Roman Hindi
            (English letters only).

            Example:
            Namaste, aap kaise ho?

            Never use Hindi script.
            """
        )


async def entrypoint(
    ctx: JobContext
):

    print("Connecting...")

    await ctx.connect()

    print("Connected!")

    current_voice = "female"
    current_language = "hindi"

    session = AgentSession(

        stt=deepgram.STT(
            model="nova-2"
        ),
llm=groq.LLM(
    model="llama-3.1-8b-instant"
),

        tts=cartesia.TTS(
            voice=VOICES[
                current_voice
            ]
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant()
    )

    print("Session Started")

    greeting = (
        "Namaste! Main aapka AI assistant hoon."
    )

    await session.say(
        greeting
    )

    save_transcript(
        user_message="system greeting",
        agent_reply=greeting
    )

    print("Agent Ready...")

    async def handle_user_input(
        message
    ):

        nonlocal current_voice
        nonlocal current_language

        if not message.is_final:
            return

        user_text = (
            message.transcript
            .strip()
            .lower()
        )

        print(
            "User:",
            user_text
        )

        # ----------------
        # LANGUAGE SWITCH
        # ----------------

        if (
            "english language"
            in user_text
        ):

            current_language = (
                "english"
            )

            await session.say(
                "Okay, I will speak English now."
            )

            return

        elif (
            "hindi language"
            in user_text
        ):

            current_language = (
                "hindi"
            )

            await session.say(
                "Theek hai, ab main Hindi mein baat karunga."
            )

            return

        # ----------------
        # VOICE SWITCH
        # ----------------

        elif (
            "male voice"
            in user_text
        ):

            current_voice = (
                "male"
            )

            session.tts = (
                cartesia.TTS(
                    voice=VOICES[
                        "male"
                    ]
                )
            )

            await session.say(
                "Male voice activated."
            )

            return

        elif (
            "female voice"
            in user_text
        ):

            current_voice = (
                "female"
            )

            session.tts = (
                cartesia.TTS(
                    voice=VOICES[
                        "female"
                    ]
                )
            )

            await session.say(
                "Female voice activated."
            )

            return

        # ----------------
        # NORMAL CHAT
        # ----------------

        try:

            if (
                current_language
                == "english"
            ):

                prompt = f"""
                Reply only in English.

                Keep answer short.

                Speak naturally.

                User:
                {user_text}
                """

            else:

                prompt = f"""
                You are an Indian assistant.

                Reply ONLY in Roman Hindi.

                Use English letters only.

                Never use Hindi script.

                Speak like a real Indian person.

                Example:
                Main theek hoon.
                Aap kaise ho?

                Keep answer short.

                User:
                {user_text}
                """

            response = await session.generate_reply(
                user_input=user_text,
                instructions=prompt
            )

            ai_reply = str(response)

            print(
                "AI:",
                ai_reply
            )

            await session.say(
                ai_reply
            )

            save_transcript(
                user_message=user_text,
                agent_reply=ai_reply
            )

            print(
                "Transcript saved!"
            )

        except Exception as e:

            print(
                "Error:",
                e
            )

    @session.on(
        "user_input_transcribed"
    )
    def on_user_input(
        message
    ):

        asyncio.create_task(
            handle_user_input(
                message
            )
        )


if __name__ == "__main__":

    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="voice-agent"
        )
    )