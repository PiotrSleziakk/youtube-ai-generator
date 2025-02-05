from elevenlabs.client import ElevenLabs
import os

def generate_audio(text, filename="audio.mp3"):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio_stream = client.generate(
        text=text,
        voice="uqraVs4sETJ6tk5pn0js",
        model="eleven_multilingual_v2"
    )
    with open(filename, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    return filename
