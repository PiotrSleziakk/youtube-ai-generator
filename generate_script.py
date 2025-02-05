from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fact(topic):
    prompt = f"""
    Stwórz ciekawostkę naukową na temat: {topic}. 
    Ciekawostka musi być napisana w sposób przystępny dla zwykłego człowieka, nie budzić kontrowersji i zachęcać do oglądania kolejnych ciekawostek.
    Podaj konkretne liczby, nazwę badania i rok. 
    Zakończ ciekawostkę pytaniem do widza.
    Przykład: "Badanie z 2023 (Nature) wykazało, że... Co o tym sądzisz/Daj znać co o tym myślisz w komentarzu?"
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def adapt_fact_text(text):
    """
    Dostosuj ciekawostkę, aby była bardziej przystępna, niebudząca kontrowersji
    i zachęcająca do oglądania kolejnych ciekawostek.
    """
    prompt = f"""
    Dostosuj poniższą ciekawostkę, aby była prosta, przystępna dla zwykłego człowieka, 
    nie budziła kontrowersji i zachęcała do obejrzenia kolejnych ciekawostek:

    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def extract_keywords(text):
    prompt = f"""
    Podziel poniższy tekst na listę kluczowych fraz, które oddają główne elementy opisywanej ciekawostki:

    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    keywords_raw = response.choices[0].message.content
    # Zakładamy, że frazy są oddzielone przecinkami
    keywords = [kw.strip() for kw in keywords_raw.split(',')]
    return keywords