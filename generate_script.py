from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fact(topic):
    prompt = f"""
    Stwórz ciekawostkę naukową na temat: {topic}. 
    Podaj konkretne liczby, nazwę badania i rok. 
    Zakończ pytaniem do widza.
    Przykład: "Badanie z 2023 (Nature) wykazało, że... Co o tym sądzisz?"
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content