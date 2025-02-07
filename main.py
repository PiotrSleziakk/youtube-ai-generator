from trends import get_google_trends
from generate_script import generate_fact_and_keywords
from text_to_speech_gtts import generate_audio  # Aktualnie używamy gTTS
from fetch_videos import download_video
from create_video import create_montage, ensure_even_dimensions
from seo_optimize import generate_seo_data
from create_thumbnail import create_thumbnail
from save_metadata import save_metadata
from translate_keywords import translate_keywords
from dotenv import load_dotenv
import os
from datetime import datetime
from PIL import Image

try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    pass

load_dotenv()  # Wczytaj zmienne środowiskowe z pliku .env

def run_generation(topic=None, use_trends=False):
    """
    Generuje ciekawostkę, słowo kluczowe oraz plik audio.
    Zwraca: (output_dir, fact, keyword_pl, english_keyword, audio_path, source)
    """
    if use_trends:
        from trends import get_google_trends
        topics = get_google_trends()
        topic = topics[0]
    if not topic:
        raise Exception("Nie podano tematu ani nie wybrano trendów.")

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    output_dir = os.path.join("output", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    fact, keyword_pl, source = generate_fact_and_keywords(topic)
    with open(os.path.join(output_dir, "fact.txt"), "w", encoding="utf-8") as f:
        f.write(fact)
    with open(os.path.join(output_dir, "keywords_pl.txt"), "w", encoding="utf-8") as f:
        f.write(keyword_pl)
    with open(os.path.join(output_dir, "source.txt"), "w", encoding="utf-8") as f:
        f.write(source)

    english_keyword = translate_keywords([keyword_pl], src='pl', dest='en')[0]
    with open(os.path.join(output_dir, "keywords_en.txt"), "w", encoding="utf-8") as f:
        f.write(english_keyword)

    audio_path = generate_audio(fact, os.path.join(output_dir, "voiceover.wav"))

    return output_dir, fact, keyword_pl, english_keyword, audio_path, source

if __name__ == '__main__':
    # Dla testów – stały temat
    output_folder = run_generation(topic="koty", use_trends=False)
    print(f"Gotowe! Sprawdź folder {output_folder} i wrzuć film ręcznie na YouTube.")
