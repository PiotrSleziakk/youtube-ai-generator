"""
fetch_videos.py
---------------
Moduł pobierający klipy wideo z API Pexels na podstawie podanego search_term.
Funkcja download_video pobiera pojedynczy klip, a download_videos – wiele unikalnych klipów.
"""

import requests
import shutil
import os
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound

def download_video(search_term, filename="video.mp4"):
    """
    Pobiera pojedynczy klip wideo na podstawie podanego search_term.
    """
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    url = f"https://api.pexels.com/videos/search?query={search_term} no copyright&per_page=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("videos"):
        video_url = data["videos"][0]["video_files"][0]["link"]
        video_data = requests.get(video_url, stream=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(video_data.raw, f)
        return filename
    else:
        return None

def download_videos(search_term, count, output_dir):
    """
    Pobiera do 'count' unikalnych klipów wideo na podstawie podanego search_term.
    Klipy są zapisywane w folderze output_dir.
    Zwraca listę ścieżek do pobranych klipów – tylko tych, które zostały poprawnie zapisane.
    """
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    url = f"https://api.pexels.com/videos/search?query={search_term} no copyright&per_page={count*2}"
    response = requests.get(url, headers=headers)
    data = response.json()
    video_files = []
    downloaded_ids = set()
    if data.get("videos"):
        for video in data["videos"]:
            video_id = video.get("id")
            if video_id in downloaded_ids:
                continue
            downloaded_ids.add(video_id)
            video_url = video["video_files"][0]["link"]
            filename = os.path.join(output_dir, f"video_{len(video_files)}.mp4")
            video_data = requests.get(video_url, stream=True)
            with open(filename, 'wb') as f:
                shutil.copyfileobj(video_data.raw, f)
            # Sprawdź, czy plik został zapisany i nie jest pusty
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                video_files.append(filename)
            if len(video_files) >= count:
                break
    return video_files

if __name__ == '__main__':
    # Test: pobierz 3 unikalne klipy dla "cat" do bieżącego folderu
    result = download_videos("cat", 3, ".")
    print("Pobrane pliki:", result)
