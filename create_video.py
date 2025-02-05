from moviepy.editor import ImageClip, AudioFileClip


def create_video(image_path, audio_path, output="output.mp4"):
    audio = AudioFileClip(audio_path)
    clip = ImageClip(image_path).set_duration(audio.duration)
    clip = clip.set_audio(audio)

    # Upewnij się, że szerokość klipu jest podzielna przez 2
    w, h = clip.size
    if w % 2 != 0:
        w += 1
        clip = clip.resize((w, h))

    clip.write_videofile(
        output,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )
    return output


if __name__ == '__main__':
    # Przykładowe wywołanie
    create_video("background.jpg", "voiceover.mp3", "final_video.mp4")
