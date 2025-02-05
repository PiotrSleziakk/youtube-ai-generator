# Dodaj obsługę czcionki dla różnych systemów
from PIL import Image, ImageDraw, ImageFont
import os


def create_thumbnail(text, background_path, output="thumbnail.jpg"):
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    img = Image.open(background_path)
    draw = ImageDraw.Draw(img)
    draw.text((50, 50), text, fill="white", font=font)
    img.save(output)
    return output