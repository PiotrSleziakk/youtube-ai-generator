import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import threading
import os
import math
import queue
from main import run_generation
from create_video import create_montage
from moviepy.editor import AudioFileClip
from deep_translator import GoogleTranslator
import math
import queue

# Globalna zmienna na ścieżkę tła muzycznego
bg_music_path = None

def select_bg_music():
    global bg_music_path
    filetypes = [("Pliki audio", "*.mp3 *.wav")]
    bg_music_path = filedialog.askopenfilename(title="Wybierz plik muzyczny", filetypes=filetypes)
    if bg_music_path:
        messagebox.showinfo("Muzyka", f"Wybrano: {bg_music_path}")
    else:
        bg_music_path = None

def get_custom_input(title, prompt):
    q = queue.Queue()
    def ask():
        result = simpledialog.askstring(title, prompt)
        q.put(result)
    root.after(0, ask)
    return q.get()

def get_edited_text(text):
    q = queue.Queue()
    def ask():
        result = simpledialog.askstring("Edytuj tekst", "Edytuj tekst:", initialvalue=text)
        q.put(result)
    root.after(0, ask)
    return q.get()

def update_status(message):
    status_var.set(message)
    root.update_idletasks()

def disable_generate_button():
    generate_btn.config(state="disabled")

def enable_generate_button():
    root.after(0, lambda: generate_btn.config(state="normal"))

def select_auto_videos(video_list):
    sel_win = tk.Toplevel(root)
    sel_win.title("Wybierz klipy")
    label = tk.Label(sel_win, text="Zaznacz klipy, które chcesz użyć:")
    label.pack(pady=5)
    listbox = tk.Listbox(sel_win, selectmode=tk.MULTIPLE, width=50)
    for idx, video in enumerate(video_list):
        listbox.insert(tk.END, f"{idx + 1}: {os.path.basename(video)}")
    listbox.pack(padx=10, pady=10)
    result_queue = queue.Queue()
    def on_select():
        selections = listbox.curselection()
        selected = [video_list[i] for i in selections]
        result_queue.put(selected)
        sel_win.destroy()
    select_btn = tk.Button(sel_win, text="Zatwierdź wybór", command=on_select)
    select_btn.pack(pady=5)
    sel_win.wait_window()
    return result_queue.get()

def auto_video_selection_auto(output_dir, english_theme, topic, audio_path, btn_auto, btn_manual):
    btn_auto.config(state="disabled")
    btn_manual.config(state="disabled")
    try:
        from fetch_videos import download_videos
        voiceover = AudioFileClip(audio_path)
        duration = voiceover.duration
        num_clips = max(2, int(math.ceil(duration / 10)))
        video_list = download_videos(english_theme, num_clips * 2, output_dir)
        if not video_list:
            messagebox.showerror("Błąd", "Nie udało się pobrać klipów wideo na temat.")
            return
        selected_videos = select_auto_videos(video_list)
        if not selected_videos:
            messagebox.showwarning("Uwaga", "Nie wybrano klipów. Użyjemy automatycznie pobranych klipów.")
            selected_videos = video_list[:num_clips]
        final_video_path = create_montage(selected_videos, audio_path, os.path.join(output_dir, "final_video.mp4"), bg_music_path=bg_music_path)
        messagebox.showinfo("Sukces", "Finalny filmik został zapisany:\n" + os.path.abspath(final_video_path))
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas montażu:\n{e}")
    finally:
        btn_auto.config(state="normal")
        btn_manual.config(state="normal")
        update_status("Gotowy.")

def manual_video_selection(output_dir, audio_path, btn_auto, btn_manual):
    btn_auto.config(state="disabled")
    btn_manual.config(state="disabled")
    messagebox.showinfo("Wybór klipów", "Wybierz pliki wideo do montażu.")
    filetypes = [("Pliki wideo", "*.mp4 *.mov *.avi *.mkv")]
    filenames = filedialog.askopenfilenames(title="Wybierz klipy wideo", filetypes=filetypes)
    if not filenames:
        messagebox.showerror("Błąd", "Nie wybrano żadnych plików.")
        btn_auto.config(state="normal")
        btn_manual.config(state="normal")
        return
    output_path = os.path.join(output_dir, "final_video_manual.mp4")
    try:
        create_montage(list(filenames), audio_path, output=output_path, bg_music_path=bg_music_path)
        messagebox.showinfo("Sukces", "Finalny filmik został zapisany:\n" + os.path.abspath(output_path))
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas montażu:\n{e}")
    finally:
        btn_auto.config(state="normal")
        btn_manual.config(state="normal")

def auto_video_selection_english(output_dir, english_theme, polish_fact_text, btn_eng):
    btn_eng.config(state="disabled")
    try:
        english_fact = GoogleTranslator(source='pl', target='en').translate(polish_fact_text)
    except Exception as e:
        english_fact = polish_fact_text
    from text_to_speech import generate_audio as elevenlabs_generate_audio
    english_audio_path = os.path.join(output_dir, "voiceover_en.wav")
    elevenlabs_generate_audio(english_fact, english_audio_path, use_ssml=True)
    from fetch_videos import download_videos
    voiceover_en = AudioFileClip(english_audio_path)
    duration = voiceover_en.duration
    num_clips = max(2, int(math.ceil(duration / 10)))
    video_list = download_videos(english_theme, num_clips * 2, output_dir)
    if not video_list:
        messagebox.showerror("Błąd", "Nie udało się pobrać klipów wideo na temat (wersja angielska).")
        btn_eng.config(state="normal")
        return
    selected_videos = select_auto_videos(video_list)
    if not selected_videos:
        messagebox.showwarning("Uwaga", "Nie wybrano klipów. Użyjemy automatycznie pobranych.")
        selected_videos = video_list[:num_clips]
    try:
        final_video_path = create_montage(selected_videos, english_audio_path,
                                          os.path.join(output_dir, "final_video_en.mp4"), bg_music_path=bg_music_path)
        messagebox.showinfo("Sukces",
                            "Angielska wersja filmiku została zapisana:\n" + os.path.abspath(final_video_path))
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas tworzenia angielskiej wersji montażu:\n{e}")
    finally:
        btn_eng.config(state="normal")

def montaz_existing_audio():
    update_status("Wybierz istniejący plik audio TTS:")
    filetypes = [("Pliki audio", "*.wav *.mp3")]
    existing_audio = filedialog.askopenfilename(title="Wybierz plik audio TTS", filetypes=filetypes)
    if not existing_audio:
        messagebox.showwarning("Błąd", "Nie wybrano pliku audio.")
        return
    topic_for_montaz = get_custom_input("Temat", "Podaj temat (dla klipów):")
    if not topic_for_montaz:
        messagebox.showwarning("Błąd", "Nie podano tematu.")
        return
    english_theme = topic_for_montaz
    output_dir = filedialog.askdirectory(title="Wybierz folder zapisu montażu")
    if not output_dir:
        messagebox.showwarning("Błąd", "Nie wybrano folderu.")
        return
    update_status("Tworzenie montażu...")
    from fetch_videos import download_videos
    voiceover = AudioFileClip(existing_audio)
    duration = voiceover.duration
    num_clips = max(2, int(math.ceil(duration / 10)))
    video_list = download_videos(english_theme, num_clips * 2, output_dir)
    if not video_list:
        messagebox.showerror("Błąd", "Nie udało się pobrać klipów.")
        return
    selected_videos = select_auto_videos(video_list)
    if not selected_videos:
        messagebox.showwarning("Uwaga", "Nie wybrano klipów, użyjemy automatycznie pobranych.")
        selected_videos = video_list[:num_clips]
    try:
        final_video_path = create_montage(selected_videos, existing_audio,
                                          os.path.join(output_dir, "final_video_existing.mp4"),
                                          bg_music_path=bg_music_path)
        messagebox.showinfo("Sukces",
                            "Montaż z istniejącego audio został zapisany:\n" + os.path.abspath(final_video_path))
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas montażu:\n{e}")
    update_status("Gotowy.")

def generate_and_show():
    global topic, use_trends, mode, output_dir, english_theme, audio_path, source_text, fact_text, keyword_pl, title_text
    update_status("Generowanie treści...")
    custom_hint = hint_entry.get().strip() if hint_entry.get().strip() else ""
    if mode_var.get() == "custom_fact":
        custom_fact = get_custom_input("Własna ciekawostka", "Podaj własną ciekawostkę:")
        if not custom_fact:
            messagebox.showwarning("Błąd", "Nie podano ciekawostki!")
            enable_generate_button()
            update_status("Gotowy.")
            return
        output_dir, fact_text, keyword_pl, english_theme, audio_path, source_text, title_text = run_generation(topic, use_trends, custom_fact=custom_fact, tts_engine=tts_var.get())
    else:
        try:
            output_dir, fact_text, keyword_pl, english_theme, audio_path, source_text, title_text = run_generation(topic, use_trends, custom_hint=hint_entry.get().strip(), tts_engine=tts_var.get())
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd generowania:\n{e}")
            enable_generate_button()
            update_status("Gotowy.")
            return

    if messagebox.askyesno("Edycja", "Czy chcesz edytować wygenerowaną ciekawostkę?"):
        edited_text = get_edited_text(fact_text)
        if edited_text is not None:
            fact_text = edited_text
            with open(os.path.join(output_dir, "fact.txt"), "w", encoding="utf-8") as f:
                f.write(fact_text)
    # Używamy wybranego silnika TTS, aby wygenerować audio tylko raz, po ewentualnej edycji
    if tts_var.get() == "gTTS":
        from text_to_speech_gtts import generate_audio as tts_generate_audio
        audio_path = tts_generate_audio(fact_text, os.path.join(output_dir, "voiceover.wav"))
    else:
        from text_to_speech import generate_audio as tts_generate_audio
        audio_path = tts_generate_audio(fact_text, os.path.join(output_dir, "voiceover.wav"), use_ssml=True)

    try:
        with open(os.path.join(output_dir, "fact.txt"), "r", encoding="utf-8") as f:
            fact_text = f.read()
    except Exception:
        fact_text = "Brak ciekawostki."
    try:
        with open(os.path.join(output_dir, "keywords_pl.txt"), "r", encoding="utf-8") as f:
            keywords_text = f.read()
    except Exception:
        keywords_text = "Brak słów kluczowych."
    try:
        with open(os.path.join(output_dir, "source.txt"), "r", encoding="utf-8") as f:
            source_text = f.read()
    except Exception:
        source_text = "Brak źródła."
    try:
        with open(os.path.join(output_dir, "title.txt"), "r", encoding="utf-8") as f:
            title_text = f.read()
    except Exception:
        title_text = "Brak tytułu."

    update_status("Wyświetlanie wygenerowanej treści...")
    info_win = tk.Toplevel(root)
    info_win.title("Wygenerowana ciekawostka")
    text_box = tk.Text(info_win, wrap=tk.WORD, width=60, height=22)
    text_box.insert(tk.END,
                    f"Tytuł:\n{title_text}\n\nCiekawostka (PL):\n{fact_text}\n\nŹródło:\n{source_text}\n\nSłowo klucz (PL):\n{keyword_pl}")
    text_box.config(state="disabled")
    text_box.pack(padx=10, pady=10)

    btn_select_music = tk.Button(info_win, text="Dodaj tło muzyczne", font=("Helvetica", 12), command=select_bg_music)
    btn_select_music.pack(pady=5)

    btn_auto = tk.Button(info_win, text="Użyj automatycznych klipów (PL)", font=("Helvetica", 12),
                         command=lambda: threading.Thread(target=auto_video_selection_auto, args=(output_dir, english_theme, topic, audio_path, btn_auto, btn_manual), daemon=True).start())
    btn_auto.pack(pady=5)
    btn_manual = tk.Button(info_win, text="Wybierz ręcznie klipy wideo (PL)", font=("Helvetica", 12),
                           command=lambda: threading.Thread(target=manual_video_selection, args=(output_dir, audio_path, btn_auto, btn_manual), daemon=True).start())
    btn_manual.pack(pady=5)

    btn_eng = tk.Button(info_win, text="Generuj wersję angielską", font=("Helvetica", 12),
                        command=lambda: threading.Thread(target=auto_video_selection_english, args=(output_dir, english_theme, fact_text, btn_eng), daemon=True).start())
    btn_eng.pack(pady=5)

    tk.Button(info_win, text="Zamknij", font=("Helvetica", 12), command=info_win.destroy).pack(pady=5)

    messagebox.showinfo("Gotowe", "Proces generacji zakończony.\nSprawdź folder:\n" + os.path.abspath(output_dir))
    update_status("Gotowy.")
    enable_generate_button()


def on_generate_click():
    global topic, use_trends, mode
    disable_generate_button()
    update_status("Uruchamianie generacji...")
    mode = mode_var.get()
    if mode == "custom_topic":
        topic = topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Błąd", "Proszę wpisać temat!")
            enable_generate_button()
            update_status("Gotowy.")
            return
        use_trends = False
    elif mode == "custom_fact":
        topic = topic_entry.get().strip()  # temat dla kontekstu
        if not topic:
            messagebox.showwarning("Błąd", "Proszę wpisać temat (dla kontekstu)!")
            enable_generate_button()
            update_status("Gotowy.")
            return
        use_trends = False
    elif mode == "montaz":
        threading.Thread(target=montaz_existing_audio, daemon=True).start()
        enable_generate_button()
        update_status("Gotowy.")
        return
    else:  # trends
        use_trends = True
        topic = None
    threading.Thread(target=generate_and_show, daemon=True).start()

root = tk.Tk()
root.title("Generator ciekawostek wideo")

# Wybór silnika TTS
tts_var = tk.StringVar(root)
tts_var.set("elevenlabs")
tts_frame = tk.Frame(root, padx=20, pady=5)
tts_frame.pack()
tts_label = tk.Label(tts_frame, text="Wybierz silnik TTS:", font=("Helvetica", 12))
tts_label.pack(side=tk.LEFT)
rb_tts1 = tk.Radiobutton(tts_frame, text="ElevenLabs", variable=tts_var, value="elevenlabs", font=("Helvetica", 12))
rb_tts1.pack(side=tk.LEFT, padx=5)
rb_tts2 = tk.Radiobutton(tts_frame, text="gTTS", variable=tts_var, value="gTTS", font=("Helvetica", 12))
rb_tts2.pack(side=tk.LEFT, padx=5)

mode_var = tk.StringVar(root)
# Opcje: "custom_topic" – wpisz temat i generuj ciekawostkę,
# "custom_fact" – podaj własną ciekawostkę,
# "trends" – generuj na podstawie trendów,
# "montaz" – utwórz montaż z istniejącego audio.
mode_var.set("custom_topic")

status_var = tk.StringVar(root)
status_var.set("Gotowy.")

status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 10), fg="blue")
status_label.pack(pady=5)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

title_label = tk.Label(frame, text="Generator ciekawostek wideo", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

rb_custom_topic = tk.Radiobutton(frame, text="Wpisz temat i generuj ciekawostkę", variable=mode_var,
                                 value="custom_topic", font=("Helvetica", 12))
rb_custom_topic.grid(row=1, column=0, sticky="w", pady=5)
rb_custom_fact = tk.Radiobutton(frame, text="Podaj własną ciekawostkę", variable=mode_var,
                                value="custom_fact", font=("Helvetica", 12))
rb_custom_fact.grid(row=1, column=1, sticky="w", pady=5)
rb_trends = tk.Radiobutton(frame, text="Generuj na podstawie trendów", variable=mode_var,
                           value="trends", font=("Helvetica", 12))
rb_trends.grid(row=2, column=0, sticky="w", pady=5, columnspan=2)
rb_montaz = tk.Radiobutton(frame, text="Utwórz montaż z istniejącego audio", variable=mode_var,
                           value="montaz", font=("Helvetica", 12))
rb_montaz.grid(row=3, column=0, sticky="w", pady=5, columnspan=2)

topic_label = tk.Label(frame, text="Podaj temat (dla kontekstu):", font=("Helvetica", 12))
topic_label.grid(row=4, column=0, sticky="w", pady=(10, 0))
topic_entry = tk.Entry(frame, width=30, font=("Helvetica", 12))
topic_entry.grid(row=4, column=1, pady=(10, 0))

hint_label = tk.Label(frame, text="Dodatkowe wskazówki (opcjonalnie):", font=("Helvetica", 12))
hint_label.grid(row=5, column=0, sticky="w", pady=(10, 0))
hint_entry = tk.Entry(frame, width=30, font=("Helvetica", 12))
hint_entry.grid(row=5, column=1, pady=(10, 0))

generate_btn = tk.Button(frame, text="Generuj", font=("Helvetica", 12), command=on_generate_click)
generate_btn.grid(row=6, column=0, columnspan=2, pady=20)

root.mainloop()
