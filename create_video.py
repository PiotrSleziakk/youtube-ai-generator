from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from moviepy.video.fx.crop import crop

"""
Moduł odpowiedzialny za tworzenie montażu wideo.
Funkcja create_montage łączy klipy wideo, synchronizuje je z plikiem audio (voiceover)
i ewentualnie miksuje tło muzyczne.
"""

def ensure_even_dimensions(clip):

    """Upewnia się, że szerokość i wysokość klipu są parzyste, co jest wymagane przez niektóre kodeki."""

    w, h = clip.size
    even_w = w if w % 2 == 0 else w + 1
    even_h = h if h % 2 == 0 else h + 1
    if (even_w, even_h) != (w, h):
        clip = clip.resize((even_w, even_h))
    return clip


def resize_to_vertical(clip, target_width=720, target_height=1280):

    """Przeskalowuje i przycina klip, aby pasował do formatu pionowego."""

    clip_resized = clip.resize(width=target_width)
    w, h = clip_resized.size
    if h < target_height:
        clip_resized = clip.resize(height=target_height)
        w, h = clip_resized.size
    x_center = w / 2
    y_center = h / 2
    clip_cropped = crop(clip_resized, width=target_width, height=target_height, x_center=x_center, y_center=y_center)
    return clip_cropped


def create_montage(video_paths, voiceover_path, output="output.mp4", bg_music_path=None, transition_duration=1):
    """
    Tworzy montaż wideo:
      - Klipy są przycinane do równego czasu trwania (całkowity czas voiceover / liczba klipów).
      - Dodawane są przejścia crossfade między klipami.
      - Jeśli podane, miksowane jest tło muzyczne z głównym audio.
    """

    voiceover = AudioFileClip(voiceover_path)
    total_duration = voiceover.duration
    num_clips = len(video_paths)
    if num_clips == 0:
        raise Exception("Brak klipów wideo do montażu.")
    # Oblicz czas trwania jednego klipu (bez uwzględnienia przejść)
    clip_duration = total_duration / num_clips

    clips = []
    for idx, video_file in enumerate(video_paths):
        clip = VideoFileClip(video_file).subclip(0, clip_duration)
        clip = resize_to_vertical(clip, target_width=720, target_height=1280)
        clip = ensure_even_dimensions(clip)
        # Dodaj crossfadein i /out dla wszystkich klipów poza pierwszym
        if idx != 0:
            clip = clip.crossfadein(transition_duration)
            clip = clip.crossfadeout(transition_duration)
        clips.append(clip)

    # Łączymy klipy – metoda "compose" zachowa przejścia
    final_video = concatenate_videoclips(clips, method="compose")

    # Ustaw główne audio (voiceover)
    final_audio = voiceover

    # Jeśli podano background music, miksujemy ją z voiceoverem
    if bg_music_path is not None:
        bg_music = AudioFileClip(bg_music_path).volumex(0.05)  # obniżona głośność
        bg_music = bg_music.set_duration(total_duration)
        final_audio = CompositeAudioClip([voiceover, bg_music])

    final_video = final_video.set_audio(final_audio)
    final_video.write_videofile(
        output,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-preset", "ultrafast", "-pix_fmt", "yuv420p"]
    )
    return output


if __name__ == '__main__':
    # Testowy przykład: upewnij się, że posiadasz odpowiednie pliki audio i wideo.
    test_video = create_montage(["video.mp4", "video2.mp4"], "voiceover.mp3", "final_video.mp4",
                                bg_music_path="bg_music.mp3")
    print("Final video saved as:", test_video)
