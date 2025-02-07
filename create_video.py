from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx.crop import crop


def ensure_even_dimensions(clip):
    w, h = clip.size
    even_w = w if w % 2 == 0 else w + 1
    even_h = h if h % 2 == 0 else h + 1
    if (even_w, even_h) != (w, h):
        clip = clip.resize((even_w, even_h))
    return clip


def resize_to_vertical(clip, target_width=720, target_height=1280):
    """
    Przeskaluj klip tak, aby pasował do pionowego formatu.
    Najpierw zmieniamy szerokość do target_width, a następnie, jeśli wysokość jest za mała, zmieniamy skalę.
    Na końcu przycinamy środek klipu do docelowej rozdzielczości.
    """
    clip_resized = clip.resize(width=target_width)
    w, h = clip_resized.size
    if h < target_height:
        clip_resized = clip.resize(height=target_height)
        w, h = clip_resized.size
    x_center = w / 2
    y_center = h / 2
    clip_cropped = crop(clip_resized, width=target_width, height=target_height, x_center=x_center, y_center=y_center)
    return clip_cropped


def create_montage(video_paths, audio_path, output="output.mp4", max_duration=60):
    audio = AudioFileClip(audio_path)
    num_clips = len(video_paths)
    # Oblicz czas trwania jednego klipu, aby całość nie przekroczyła max_duration
    clip_duration = min(max_duration / num_clips, audio.duration / num_clips)

    clips = []
    for video_file in video_paths:
        clip = VideoFileClip(video_file).subclip(0, clip_duration)
        clip = resize_to_vertical(clip, target_width=720, target_height=1280)
        clip = ensure_even_dimensions(clip)
        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    final_video.write_videofile(
        output,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )
    return output


# Przykładowe użycie (testowe)
if __name__ == '__main__':
    create_montage(["video.mp4"], "voiceover.mp3", "final_video.mp4")
