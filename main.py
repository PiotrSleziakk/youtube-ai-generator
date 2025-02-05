from trends import get_google_trends
from generate_script import generate_fact, extract_keywords
from text_to_speech import generate_audio
from fetch_images import download_image
from create_video import create_slideshow  # Używamy zmodyfikowanej funkcji
from seo_optimize import generate_seo_data
from create_thumbnail import create_thumbnail
from save_metadata import save_metadata
from dotenv import load_dotenv
import os
from datetime import datetime
from PIL import Image

try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    pass

load_dotenv()  # Wczytaj zmienne środowiskowe z .env

# Utwórz unikalny folder wyjściowy oparty na dacie i godzinie
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
output_dir = os.path.join("output", timestamp)
os.makedirs(output_dir, exist_ok=True)

# # 1. Pobierz trendy z Google
# topics = get_google_trends()
# topic = topics[0]  # Wybieramy pierwszy trend
# 1. Ustaw stały temat
topic = "koty"

# 2. Wygeneruj ciekawostkę na dany temat (już dostosowana)
fact = generate_fact(topic)

# 3. Wyodrębnij kluczowe frazy z ciekawostki
keywords = extract_keywords(fact)

# 4. Wygeneruj audio z wykorzystaniem SSML (dla lepszej wymowy)
audio_path = generate_audio(fact, os.path.join(output_dir, "voiceover.mp3"), use_ssml=True)

# 5. Pobierz obrazy dla każdej kluczowej frazy
image_paths = []
for i, kw in enumerate(keywords):
    img_path = download_image(kw, os.path.join(output_dir, f"background_{i}.jpg"))
    image_paths.append(img_path)

# 6. Stwórz filmik w formie sekwencji slajdów, gdzie łączny czas nie przekracza 60 sekund
video_path = create_slideshow(image_paths, audio_path, os.path.join(output_dir, "final_video.mp4"), max_duration=60)

# 7. Wygeneruj SEO: tytuł, opis oraz tagi
title, description, hashtags = generate_seo_data(topic, fact)
thumbnail_path = create_thumbnail(title, image_paths[0], os.path.join(output_dir, "thumbnail.jpg"))

# 8. Zapisz metadane do pliku tekstowego
save_metadata(title, f"{description}\nHashtagi: {hashtags}", os.path.join(output_dir, "metadata.txt"))

print(f"Gotowe! Sprawdź folder {output_dir} i wrzuć film ręcznie na YouTube.")
