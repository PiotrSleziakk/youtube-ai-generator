from gtts import gTTS
import os
import re
from num2words import num2words


def convert_numbers_to_words(text):
    """
    Znajduje wszystkie liczby w tekście i zamienia je na ich odpowiedniki słowne w języku polskim.
    """

    def replace_number(match):
        number = match.group(0)
        try:
            return num2words(int(number), lang='pl')
        except Exception:
            return number  # W razie problemów zwróć oryginalną liczbę

    return re.sub(r'\b\d+\b', replace_number, text)


def generate_audio(text, filename="audio_gtts.mp3", lang="pl"):
    """
    Generuje plik audio przy użyciu gTTS.
    Używa przekształcenia liczb na słowa przed generacją.

    Parametry:
      text (str): Tekst do konwersji.
      filename (str): Ścieżka do zapisu pliku audio.
      lang (str): Kod języka (domyślnie "pl" dla języka polskiego).

    Zwraca:
      str: Ścieżkę do wygenerowanego pliku audio.
    """
    # Konwersja liczb na słowa
    text = convert_numbers_to_words(text)
    tts = gTTS(text, lang=lang)
    tts.save(filename)
    return filename


if __name__ == '__main__':
    sample_text = "Badanie z 2023 roku wykazało, że 123 osób wzięło udział w badaniu. Co o tym sądzisz?"
    output = generate_audio(sample_text, "sample_gtts.mp3")
    print(f"Plik audio został zapisany jako: {output}")
