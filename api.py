from google import genai
from dotenv import load_dotenv
import os,io
from gtts import gTTS

#loading env file
load_dotenv()


#gemini api key
gemini_api_key = os.getenv("GEMINI_KEY")

#initialize client
client = genai.Client(api_key = gemini_api_key)


note_promt = """Summarize the uploaded pictures in one paragraph with important quotes, dates and other events at max 150 words. Also add necessary markdowns
"""

def note_generator(note_images,language):
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = [note_images, note_promt+f"Generate the content in {language}"]
    )

    return response.text


def audio_generator(note_summary,language):
    lang = {"English":"en", "Bangla":"bn"}
    tts = gTTS(note_summary, lang = lang[language], slow = False)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)

    return audio_buffer


def quiz_generator(note_images, difficulty,language):
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = [note_images, f"""Generate 5 quiz questions based on the uploaded notes with difficulty level {difficulty}. Show the answer for all the questions at the end and with short explanations. Also use proper markdown where necessary"""+f"Generate the content in {language}"]
    )

    return response.text