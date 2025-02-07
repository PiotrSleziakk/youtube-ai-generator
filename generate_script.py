from openai import OpenAI
import os
from dotenv import load_dotenv
from fetch_news import get_latest_news
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_fact_and_keywords(topic):
    # Pobierz najnowsze informacje dotyczące tematu
    news_list = get_latest_news(topic, max_results=3)
    news_context = "\n".join(news_list) if news_list else "Brak najnowszych informacji."

    # Wyodrębnij źródło – pobieramy URL z pierwszego artykułu, jeśli dostępny
    source = ""
    if news_list:
        match = re.search(r'\((https?://[^)]+)\)', news_list[0])
        if match:
            source = match.group(1)

    prompt = f"""
Stwórz ciekawostkę naukową na temat: {topic}.
Uwzględnij poniższe najnowsze informacje:
{news_context}
Ciekawostka musi być napisana w sposób przystępny dla zwykłego człowieka, nie budzić kontrowersji i zachęcać do oglądania kolejnych ciekawostek.
Podaj konkretne liczby oraz nazwę badania, ale **nie podawaj dokładnych dat ani lat** – użyj przybliżonych przedziałów lub opisu, który nie wymaga dokładnych dat.
Zakończ ciekawostkę pytaniem do widza.

Następnie, wypunktuj jedną kluczową frazę wizualną, która najlepiej oddaje główne elementy tej ciekawostki, przydatną do wyszukiwania klipów wideo.
Użyj następującego formatu:

Ciekawostka:
[Twoja ciekawostka tutaj]

Klucz:
[fraza]
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content

    try:
        fact = content.split("Ciekawostka:")[1].split("Klucz:")[0].strip()
        keyword_raw = content.split("Klucz:")[1].strip()
        # Jeśli jest lista, bierzemy pierwszą; dodatkowo wybieramy pierwsze słowo, aby uzyskać pojedynczy główny wyraz.
        keyword = keyword_raw.split(",")[0].strip()
        if " " in keyword:
            keyword = keyword.split()[0].strip()
        return fact, keyword, source
    except Exception as e:
        print("Błąd przy parsowaniu odpowiedzi:", e)
        return content, "", source


# Przykładowe użycie:
if __name__ == '__main__':
    fact, keyword, source = generate_fact_and_keywords("koty")
    print("Ciekawostka:", fact)
    print("Klucz:", keyword)
    print("Źródło:", source)
