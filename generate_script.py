from openai import OpenAI
import os
from dotenv import load_dotenv
from fetch_news import get_latest_news
import re

""" 
Moduł generujący ciekawostkę naukową na podstawie tematu i dodatkowych wskazówek.
Zwraca ciekawostkę, główne słowo kluczowe, źródło, tagi oraz tytuł.

"""

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fact_and_keywords(topic, custom_hint=""):
    # Pobierz najnowsze informacje dotyczące tematu
    news_list = get_latest_news(topic, max_results=3)
    if news_list:
        news_context = "\n".join(news_list)
        # Próba wyekstrahowania źródła z pierwszego artykułu
        match = re.search(r'\((https?://[^)]+)\)', news_list[0])
        if match:
            source = match.group(1)
        else:
            source = f"https://news.google.com/search?q={topic}"
    else:
        news_context = "Brak najnowszych informacji. Dla najnowszych wiadomości sprawdź:"
        source = f"https://news.google.com/search?q={topic}"

    # Jeśli użytkownik podał dodatkowe wskazówki, wstawiamy je do promptu
    extra = f"\nDodatkowe wskazówki: {custom_hint}" if custom_hint.strip() else ""

    prompt = f"""
Stwórz ciekawostkę naukową na temat: {topic}.
Uwzględnij poniższe najnowsze informacje:
{news_context}
{extra}
Ciekawostka musi być napisana w sposób przystępny dla zwykłego człowieka, nie budzić kontrowersji i zachęcać do oglądania kolejnych ciekawostek.
Podaj konkretne liczby oraz nazwę badania, ale **nie podawaj dokładnych dat ani lat** – użyj przybliżonych przedziałów lub opisu, który nie wymaga dokładnych dat.
Zakończ ciekawostkę pytaniem do widza.

Następnie, wypunktuj jedną kluczową frazę wizualną, która najlepiej oddaje główne elementy tej ciekawostki, przydatną do wyszukiwania klipów wideo.

Wygeneruj do tej ciekawostki tagi, które zostaną dołączone pod filmikiem.

Wygeneruj także 3 chwytliwe tytuły, które przyciągną uwagę widza.
Na końcu, wypisz źródło informacji w formacie:
Źródło:
[URL]

Użyj następującego formatu:

Ciekawostka:
[Twoja ciekawostka tutaj]

Klucz:
[fraza]

Tagi:
[#tag1 #tag2 #tag3]

Tytuł:
[Twój tytuł tutaj]

Źródło:
[{source}]
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    try:
        fact = content.split("Ciekawostka:")[1].split("Klucz:")[0].strip()
        keyword_raw = content.split("Klucz:")[1].split("Tagi:")[0].strip()
        # Wybieramy pierwsze słowo jako główny wyraz kluczowy
        keyword = keyword_raw.split(",")[0].strip()
        if " " in keyword:
            keyword = keyword.split()[0].strip()
        tags_line = content.split("Tagi:")[1].split("Tytuł:")[0].strip()
        tags = tags_line
        title_line = content.split("Tytuł:")[1].split("Źródło:")[0].strip()
        title = title_line
        source_extracted = content.split("Źródło:")[1].strip()
        if not source_extracted:
            source_extracted = source
        return fact, keyword, source_extracted, tags, title
    except Exception as e:
        print("Błąd przy parsowaniu odpowiedzi:", e)
        return content, "", source, "", ""

if __name__ == '__main__':
    fact, keyword, source, tags, title = generate_fact_and_keywords("koty", custom_hint="Uwzględnij ich różnorodność.")
    print("Ciekawostka:", fact)
    print("Klucz:", keyword)
    print("Źródło:", source)
    print("Tagi:", tags)
    print("Tytuł:", title)
