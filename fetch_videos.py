import requests
import shutil
import os
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound


def download_video(query, topic, filename="video.mp4"):
    # Upewnij się, że topic nie jest None
    if topic is None:
        topic = ""
    try:
        english_topic = GoogleTranslator(source='pl', target='en').translate(topic)
    except TranslationNotFound:
        english_topic = ""
    except Exception as e:
        english_topic = ""

    # Jeśli tłumaczenie się nie udało lub zwróciło pusty ciąg, użyj oryginalnego tematu
    if not english_topic:
        english_topic = topic
    # Upewnij się, że english_topic jest typu string
    english_topic = str(english_topic)

    # Upewnij się, że query nie jest None i jest ciągiem znaków
    if query is None:
        query = ""
    query = str(query)

    # Łączymy temat z zapytaniem, jeśli english_topic nie występuje już w query
    if english_topic.lower() not in query.lower():
        search_query = f"{english_topic} {query} no copyright"
    else:
        search_query = f"{query} no copyright"

    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    url = f"https://api.pexels.com/videos/search?query={search_query}&per_page=1"
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


# Przykładowe użycie (testowe)
if __name__ == '__main__':
    # Przykład: pobierz video dla słowa kluczowego "cat" z tematem "koty"
    result = download_video("cat", "koty", "test_video.mp4")
    print("Pobrany plik:", result)
