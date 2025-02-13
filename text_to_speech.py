from elevenlabs.client import ElevenLabs
from num2words import num2words
import os
import re


"""Moduł odpowiedzialny za generowanie pliku audio przy użyciu ElevenLabs."""


def convert_numbers_to_words(text):
    """
    Znajduje wszystkie liczby w tekście i zamienia je na ich odpowiedniki słowne w języku polskim.
    """
    def replace_number(match):
        number = match.group(0)
        try:
            return num2words(int(number), lang='pl')
        except Exception:
            return number  # w razie problemów zwróć oryginalną liczbę
    return re.sub(r'\b\d+\b', replace_number, text)

def generate_audio(text, filename="audio.mp3", use_ssml=False):
    # Przed wysłaniem tekstu do syntezatora, konwertujemy liczby na słowa
    text = convert_numbers_to_words(text)
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    if use_ssml:
        # Opakowanie tekstu w znaczniki SSML dla lepszej intonacji
        text = f"<speak>{text}</speak>"
    audio_stream = client.generate(
        text=text,
        voice="D3ApGBEdEn4RYrbx4tvx",
        model="eleven_multilingual_v2"
    )
    with open(filename, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    return filename

if __name__ == '__main__':
    sample_text = "Badanie z 2023 roku wykazało, że 123 osób wzięło udział w badaniu. Co o tym sądzisz?"
    output = generate_audio(sample_text, "sample_audio.mp3")
    print(f"Plik audio został zapisany jako: {output}")
