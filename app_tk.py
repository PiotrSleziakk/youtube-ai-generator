import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
from main import run_generation, create_montage  # run_generation zwraca (output_dir, fact, keyword_pl, english_keyword, audio_path, source)
import time

def auto_video_selection_auto(output_dir, english_keyword, topic, audio_path, btn_auto, btn_manual):
    btn_auto.config(state="disabled")
    btn_manual.config(state="disabled")
    try:
        from fetch_videos import download_video
        video_paths = []
        vp = download_video(english_keyword, topic, os.path.join(output_dir, f"video_0.mp4"))
        if vp:
            video_paths.append(vp)
        if len(video_paths) < 1:
            additional_query = f"{topic} variety no copyright"
            vp = download_video(additional_query, topic, os.path.join(output_dir, "video_additional.mp4"))
            if vp:
                video_paths.append(vp)
        if not video_paths:
            messagebox.showerror("Błąd", "Nie udało się pobrać żadnych filmików na temat.")
            return
        try:
            final_video_path = create_montage(video_paths, audio_path, os.path.join(output_dir, "final_video.mp4"), max_duration=60)
            messagebox.showinfo("Sukces", "Finalny filmik został zapisany:\n" + os.path.abspath(final_video_path))
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas tworzenia automatycznego montażu:\n{e}")
    finally:
        update_status("Gotowy.")
        btn_auto.config(state="normal")
        btn_manual.config(state="normal")

def manual_video_selection(output_dir, audio_path, btn_auto, btn_manual):
    btn_auto.config(state="disabled")
    btn_manual.config(state="disabled")
    messagebox.showinfo("Wybór klipów", "Wybierz pliki wideo, które mają zostać użyte do montażu.")
    filetypes = [("Pliki wideo", "*.mp4 *.mov *.avi *.mkv")]
    filenames = filedialog.askopenfilenames(title="Wybierz klipy wideo", filetypes=filetypes)
    if not filenames:
        messagebox.showerror("Błąd", "Nie wybrano żadnych plików. Finalny filmik pozostanie automatycznie wygenerowany.")
        btn_auto.config(state="normal")
        btn_manual.config(state="normal")
        return
    output_path_manual = os.path.join(output_dir, "final_video_manual.mp4")
    try:
        create_montage(list(filenames), audio_path, output=output_path_manual, max_duration=60)
        messagebox.showinfo("Sukces", "Finalny filmik został zapisany:\n" + os.path.abspath(output_path_manual))
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas tworzenia montażu z ręcznie wybranych klipów:\n{e}")
    finally:
        btn_auto.config(state="normal")
        btn_manual.config(state="normal")

def update_status(message):
    status_var.set(message)
    root.update_idletasks()

def disable_generate_button():
    generate_btn.config(state="disabled")

def enable_generate_button():
    root.after(0, lambda: generate_btn.config(state="normal"))

def generate_and_show():
    global topic, use_trends, option, output_dir, english_keyword, audio_path, source_text
    update_status("Generowanie treści...")
    try:
        output_dir, fact_text, keyword_pl, english_keyword, audio_path, source_text = run_generation(topic, use_trends)
    except Exception as e:
        messagebox.showerror("Błąd", f"Błąd podczas generowania treści:\n{e}")
        enable_generate_button()
        update_status("Gotowy.")
        return

    try:
        with open(os.path.join(output_dir, "fact.txt"), "r", encoding="utf-8") as f:
            fact_text = f.read()
    except Exception:
        fact_text = "Nie udało się odczytać treści ciekawostki."
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

    update_status("Wyświetlanie wygenerowanej treści...")
    info_win = tk.Toplevel(root)
    info_win.title("Wygenerowana ciekawostka")
    text_box = tk.Text(info_win, wrap=tk.WORD, width=60, height=20)
    text_box.insert(tk.END, f"Ciekawostka:\n{fact_text}\n\nŹródło:\n{source_text}\n\nSłowa kluczowe (PL):\n{keywords_text}")
    text_box.config(state="disabled")
    text_box.pack(padx=10, pady=10)

    btn_auto = tk.Button(info_win, text="Użyj automatycznych klipów", font=("Helvetica", 12),
                         command=lambda: threading.Thread(target=auto_video_selection_auto, args=(output_dir, english_keyword, topic, audio_path, btn_auto, btn_manual), daemon=True).start())
    btn_auto.pack(pady=5)
    btn_manual = tk.Button(info_win, text="Wybierz ręcznie klipy wideo", font=("Helvetica", 12),
                           command=lambda: threading.Thread(target=manual_video_selection, args=(output_dir, audio_path, btn_auto, btn_manual), daemon=True).start())
    btn_manual.pack(pady=5)
    tk.Button(info_win, text="Zamknij", font=("Helvetica", 12), command=info_win.destroy).pack(pady=5)

    messagebox.showinfo("Gotowe", "Proces generacji zakończony.\nSprawdź folder:\n" + os.path.abspath(output_dir))
    update_status("Gotowy.")
    enable_generate_button()

def on_generate_click():
    global topic, use_trends, option
    disable_generate_button()
    update_status("Uruchamianie generacji...")
    if custom_var.get():
        option = "custom"
        topic = topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Błąd", "Proszę wpisać temat!")
            enable_generate_button()
            update_status("Gotowy.")
            return
        use_trends = False
    else:
        option = "trends"
        use_trends = True
        topic = None
    threading.Thread(target=generate_and_show, daemon=True).start()

root = tk.Tk()
root.title("Generator ciekawostek wideo")

status_var = tk.StringVar(root)
status_var.set("Gotowy.")

status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 10), fg="blue")
status_label.pack(pady=5)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

title_label = tk.Label(frame, text="Generator ciekawostek wideo", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

custom_var = tk.BooleanVar(value=True)
rb_custom = tk.Radiobutton(frame, text="Wpisz własny temat", variable=custom_var, value=True, font=("Helvetica", 12))
rb_custom.grid(row=1, column=0, sticky="w", pady=5)
rb_trends = tk.Radiobutton(frame, text="Generuj na podstawie trendów", variable=custom_var, value=False, font=("Helvetica", 12))
rb_trends.grid(row=1, column=1, sticky="w", pady=5)

topic_label = tk.Label(frame, text="Podaj temat:", font=("Helvetica", 12))
topic_label.grid(row=2, column=0, sticky="w", pady=(10, 0))
topic_entry = tk.Entry(frame, width=30, font=("Helvetica", 12))
topic_entry.grid(row=2, column=1, pady=(10, 0))

generate_btn = tk.Button(frame, text="Generuj", font=("Helvetica", 12), command=on_generate_click)
generate_btn.grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()
