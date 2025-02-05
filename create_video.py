from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


def ensure_even_dimensions(clip):
    w, h = clip.size
    # Jeśli szerokość lub wysokość są nieparzyste, powiększ je o 1
    even_w = w if w % 2 == 0 else w + 1
    even_h = h if h % 2 == 0 else h + 1
    if (even_w, even_h) != (w, h):
        clip = clip.resize((even_w, even_h))
    return clip


def create_slideshow(image_paths, audio_path, output="output.mp4", max_duration=60):
    audio = AudioFileClip(audio_path)
    num_slides = len(image_paths)
    # Oblicz czas wyświetlania jednego slajdu
    slide_duration = min(max_duration / num_slides, audio.duration / num_slides)

    clips = []
    for img_path in image_paths:
        clip = ImageClip(img_path).set_duration(slide_duration)
        clip = ensure_even_dimensions(clip)  # Upewnij się, że wymiary są parzyste
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    video.write_videofile(
        output,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )
    return output


# Przykładowe użycie funkcji (możesz testować oddzielnie)
if __name__ == '__main__':
    create_slideshow(["background.jpg"], "voiceover.mp3", "final_video.mp4")
