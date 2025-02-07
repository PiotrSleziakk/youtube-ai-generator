from deep_translator import GoogleTranslator

def translate_keywords(keywords, src='pl', dest='en'):
    translator = GoogleTranslator(source=src, target=dest)
    results = []
    for kw in keywords:
        try:
            translation = translator.translate(kw)
            results.append(translation)
        except Exception as e:
            # Jeśli tłumaczenie się nie powiedzie, zwracamy oryginalny tekst
            results.append(kw)
    return results
