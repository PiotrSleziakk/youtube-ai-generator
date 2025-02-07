import requests

def get_latest_news(topic, max_results=3):
    """
    Pobiera najnowsze artykuły dotyczące danego tematu z GDELT API.
    Zwraca listę tekstów zawierających tytuł oraz URL artykułu.
    """
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": topic,
        "mode": "ArtList",
        "format": "JSON",
        "maxrecords": max_results
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            news_list = []
            for article in articles:
                title = article.get("title", "").strip()
                url = article.get("url", "").strip()
                if title and url:
                    news_list.append(f"{title} ({url})")
            return news_list
        else:
            return []
    except Exception:
        return []
