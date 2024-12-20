import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()

async def start_livekit(ctx: JobContext):
    # Initialize the chat context with a system prompt for the assistant
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should understand user intents like password resets and respond with concise, user-friendly messages."
        ),
    )

    # Connect to the LiveKit room with audio-only subscription
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    print("Connected to LiveKit room.")

    # Initialize function context
    fnc_ctx = AssistantFnc()

    # Create the VoiceAssistant instance
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),  # Voice Activity Detection
        stt=openai.STT(),  # Speech-to-Text
        llm=openai.LLM(),  # Language Model
        tts=openai.TTS(),  # Text-to-Speech
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )

    # Start the assistant in the LiveKit room
    assistant.start(ctx.room)
    print("Voice assistant started.")

    # Greet the user
    await assistant.say("Hello! How can I assist you today?", allow_interruptions=False)

    # Define a callback for processing user speech
    @assistant.on_user_speech
    async def handle_user_input(transcribed_text: str):
        try:
            if transcribed_text.strip():
                print(f"User said: {transcribed_text}")  # Log user input

                # Generate a response from the assistant
                response = await assistant.chat(transcribed_text)
                print(f"Assistant response: {response}")  # Log assistant's response

                # Speak the response back to the user
                await assistant.say(response, allow_interruptions=False)
        except Exception as e:
            print(f"Error while processing user input: {e}")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cli.run_app(WorkerOptions(entrypoint_fnc=start_livekit)))

if __name__ == "__main__":
    main()
