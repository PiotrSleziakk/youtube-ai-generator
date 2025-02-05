import requests
import shutil
import os


def download_image(query, filename="image.jpg"):
    # Dodajemy dodatkowy kontekst do zapytania, aby uzyskać ilustrację na temat
    search_query = f"{query} ilustracja"
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=1"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("photos"):
        image_url = data["photos"][0]["src"]["large"]
        image_data = requests.get(image_url, stream=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(image_data.raw, f)
        return filename
    else:
        # Fallback: pobierz obraz z Openverse
        url = f"https://api.openverse.engineering/v1/images/?q={query}&license_type=commercial,modification"
        response = requests.get(url)
        image_url = response.json()["results"][0]["url"]
        image_data = requests.get(image_url, stream=True)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(image_data.raw, f)
        return filename