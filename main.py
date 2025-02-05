from trends import get_google_trends
from generate_script import generate_fact
from text_to_speech import generate_audio
from fetch_images import download_image
from create_video import create_video
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

load_dotenv()  # Wczytaj .env

# Utwórz unikalny folder wyjściowy na podstawie daty i godziny
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
output_dir = os.path.join("output", timestamp)
os.makedirs(output_dir, exist_ok=True)


# 1. Znajdź trendy
topics = get_google_trends()
topic = topics[0]  # Wybierz pierwszy trend

# 2. Wygeneruj ciekawostkę
fact = generate_fact(topic)

# 3. Stwórz audio i wideo – pamiętaj o poprawnych ścieżkach
audio_path = generate_audio(fact, os.path.join(output_dir, "voiceover.mp3"))
image_path = download_image(topic, os.path.join(output_dir, "background.jpg"))
video_path = create_video(image_path, audio_path, os.path.join(output_dir, "final_video.mp4"))

# 4. SEO i miniaturka
title, description = generate_seo_data(topic, fact)
thumbnail_path = create_thumbnail(title, image_path, os.path.join(output_dir, "thumbnail.jpg"))

# 5. Zapisz metadane
save_metadata(title, description, os.path.join(output_dir, "metadata.txt"))

print(f"Gotowe! Sprawdź folder {output_dir} i wrzuć film ręcznie na YouTube.")
