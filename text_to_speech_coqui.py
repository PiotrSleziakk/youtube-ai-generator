from TTS.api import TTS
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
            return number  # w razie problemów zwróć oryginalną liczbę

    return re.sub(r'\b\d+\b', replace_number, text)


def generate_audio(text, filename="audio_coqui.wav", lang="pl"):
    """
    Generuje plik audio przy użyciu Coqui TTS z pretrenowanym modelem dla języka polskiego.
    Przed generacją zamienia liczby na słowa.

    Parametry:
      text (str): Tekst do konwersji.
      filename (str): Ścieżka do zapisu pliku audio.
      lang (str): Kod języka, domyślnie "pl".

    Zwraca:
      str: Ścieżkę do wygenerowanego pliku audio.
    """
    text = convert_numbers_to_words(text)
    # Wybieramy pretrenowany model dla języka polskiego.
    # Przykładowy model: "tts_models/pl/mai/tacotron2-DDC" (dostępny w repozytorium Coqui TTS)
    model_name = "tts_models/pl/mai/tacotron2-DDC"
    tts = TTS(model_name)
    tts.tts_to_file(text=text, file_path=filename)
    return filename


if __name__ == '__main__':
    sample_text = "Badanie z 2023 roku wykazało, że 123 osób wzięło udział. Co o tym sądzisz?"
    output = generate_audio(sample_text, "sample_coqui.wav")
    print(f"Plik audio został zapisany jako: {output}")
