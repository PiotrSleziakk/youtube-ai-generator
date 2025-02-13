from trends import get_google_trends
from generate_script import generate_fact_and_keywords
from seo_optimize import generate_seo_data
from create_thumbnail import create_thumbnail
from save_metadata import save_metadata
from translate_keywords import translate_keywords
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
from tkinter import simpledialog
import tkinter as tk
import queue
import os
os.environ["FFMPEG_BINARY"] = r"D:\ffmpeg\ffmpeg-7.1-full_build\bin\ffmpeg.exe"

try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    pass

load_dotenv()  # Wczytaj zmienne środowiskowe


def get_custom_input(title, prompt):
    q = queue.Queue()

    def ask():
        result = simpledialog.askstring(title, prompt)
        q.put(result)

    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()
    root.after(0, ask)
    return q.get()


def run_generation(topic=None, use_trends=False, custom_fact=None, custom_hint="", tts_engine="elevenlabs"):
    """
    Generuje ciekawostkę, słowo kluczowe (PL), tytuł oraz inne dane tekstowe.
    Jeśli custom_fact jest podany, używamy go zamiast generowania ciekawostki.
    Zapisuje wyniki (ciekawostkę, słowo kluczowe, źródło, tagi, tytuł) do folderu.
    Dodatkowo tłumaczy temat (pierwsze dwa wyrazy) na angielski.

    Zwraca: (output_dir, fact, keyword_pl, english_theme, audio_path, source, title)
    """
    if use_trends:
        topics = get_google_trends()
        topic = topics[0]
    if not topic:
        raise Exception("Nie podano tematu ani nie wybrano trendów.")

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    output_dir = os.path.join("output", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    if custom_fact:
        fact = custom_fact
        keyword_pl = get_custom_input("Słowo kluczowe", "Podaj słowo kluczowe (PL) dla ciekawostki:")
        if not keyword_pl:
            keyword_pl = ""
        source = get_custom_input("Źródło", "Podaj źródło informacji:")
        if not source:
            source = "Źródło: Wprowadzone przez użytkownika"
        tags = ""
        title = get_custom_input("Tytuł", "Podaj chwytliwy tytuł dla ciekawostki:")
        if not title:
            title = ""
    else:
        fact, keyword_pl, source, tags, title = generate_fact_and_keywords(topic, custom_hint=custom_hint)

    with open(os.path.join(output_dir, "fact.txt"), "w", encoding="utf-8") as f:
        f.write(fact)
    with open(os.path.join(output_dir, "keywords_pl.txt"), "w", encoding="utf-8") as f:
        f.write(keyword_pl)
    with open(os.path.join(output_dir, "source.txt"), "w", encoding="utf-8") as f:
        f.write(source)
    with open(os.path.join(output_dir, "tags.txt"), "w", encoding="utf-8") as f:
        f.write(tags)
    with open(os.path.join(output_dir, "title.txt"), "w", encoding="utf-8") as f:
        f.write(title)

    # Tłumaczenie tematu: używamy pierwszych dwóch słów
    words = topic.split()
    main_words = " ".join(words[:2]) if len(words) >= 2 else words[0]
    english_theme = translate_keywords([main_words], src='pl', dest='en')[0]
    with open(os.path.join(output_dir, "theme_en.txt"), "w", encoding="utf-8") as f:
        f.write(english_theme)

    # Nie generujemy audio tutaj – audio zostanie wygenerowane później po edycji
    audio_path = ""  # Pusty, do wygenerowania później
    return output_dir, fact, keyword_pl, english_theme, audio_path, source, title


if __name__ == '__main__':
    # Test – stały temat
    output_folder = run_generation(topic="koty", use_trends=False)
    print(f"Gotowe! Sprawdź folder {output_folder} i wrzuć film ręcznie na YouTube.")
