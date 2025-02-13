def save_metadata(title, description, source, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Tytuł: {title}\n\nOpis:\n{description}\n\nŹródło:\n{source}")
