def save_metadata(title, description, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Tytuł: {title}\n\nOpis:\n{description}")
