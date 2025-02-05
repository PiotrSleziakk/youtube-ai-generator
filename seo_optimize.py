from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_seo_data(topic, script):
    prompt = f"""
    Stwórz chwytliwy tytuł, opis oraz listę hashtagów dla filmu na YouTube o tematyce: {topic}.
    Tytuł powinien zawierać słowa kluczowe i liczby.
    Opis musi mieć 3 zdania, zawierać hashtagi i link do badania.
    Hashtagi powinny być krótkie, zwięzłe i pasujące do tematyki.
    Format odpowiedzi:
    Tytuł: [tu tytuł]
    Opis: [tu opis]
    Hashtagi: [tu hashtagi]
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    title = result.split("Tytuł: ")[1].split("\n")[0]
    description = result.split("Opis: ")[1]
    return title, description