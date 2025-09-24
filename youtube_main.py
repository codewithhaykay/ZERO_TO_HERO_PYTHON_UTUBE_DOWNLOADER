import tkinter as tk
from tkinter import ttk, messagebox
import threading
from queue import Queue, Empty
from yt_dlp import YoutubeDL
from pathlib import Path
from PIL import ImageTk

# --- minimal UI ---
my_gui = tk.Tk()
my_gui.eval("tk::PlaceWindow . center")
my_gui.configure(bg="lightblue")
my_gui.title("YouTube Downloader")
my_gui.resizable(False, False)
from PIL import Image, ImageTk
from pathlib import Path

# Use the script's directory to build the image path
script_dir = Path(__file__).parent              #Relative - zero_to_hero_assignment2\100Days_Challenge\youtube_main.py
image_path = script_dir / "YOUTUBELOGO.png"     #Absolute D:\Users\easyt\DocumentsIN_D\ZERO_TO_HERO\zero_to_hero_assignment2\...
logo_imag = ImageTk.PhotoImage(Image.open(image_path))
    # Resize the image to fit nicely in the UI
resized_img = Image.open(image_path).resize((390, 50))
logo_imag = ImageTk.PhotoImage(resized_img)
logo_widget = tk.Label(my_gui, image=logo_imag)
logo_widget.image = logo_imag
logo_widget.pack(pady=(10, 0))

yt_frame =tk.Frame(my_gui, bg="yellow")
yt_frame.rowconfigure(0, weight=1, minsize=50)
yt_frame.columnconfigure([0,1], weight=1, minsize=50)
yt_frame.pack(pady=10)
yt_url_label = tk.Label(yt_frame, text="YouTube URL:", bg="yellow")
yt_url_label.grid(row=0, column=0, sticky=tk.W)
url_variable = tk.StringVar()
yt_entry = tk.Entry(yt_frame, textvariable=url_variable, width=52)
yt_entry.grid(row=0, column=1, sticky=tk.E)

choice_of_conv = tk.StringVar(value="video")
frm = ttk.Frame(my_gui)
frm.rowconfigure(0, weight=1, minsize=23)
frm.columnconfigure([0,1], weight=1, minsize=23)
frm.pack()
vid_radio = ttk.Radiobutton(frm, text="Video (MP4 Format)", variable=choice_of_conv, value="video", width=29)
vid_radio.grid(row=0, column=0, sticky=tk.W)
aud_radio = ttk.Radiobutton(frm, text="MP3 (audio only)", variable=choice_of_conv, value="mp3", width=29)
aud_radio.grid(row=0, column=1, sticky=tk.E)
progress = ttk.Progressbar(my_gui, length=400, mode="determinate", maximum=100)
progress.pack(padx=10, pady=(10, 2))
status_bar = tk.StringVar(value="Download_Status")
ttk.Label(my_gui, textvariable=status_bar).pack(padx=10, pady=(0, 8))

btn_download = ttk.Button(my_gui, text="Download")
btn_download.pack(padx=10, pady=(0, 12))

# tiny, safe comms between thread and UI
wtq = Queue()

def progress_hook(dico):
    # Called from worker thread by yt-dlp
    if dico.get('status') == 'downloading':
        total = dico.get('total_bytes') or dico.get('total_bytes_estimate') or 0
        done = dico.get('downloaded_bytes') or 0
        if total:
            wtq.put(('progress', int(done * 100 / total)))
        else:
            wtq.put(('note', 'Downloading...'))
    elif dico.get('status') == 'finished':
        wtq.put(('progress', 100))
        wtq.put(('note', 'Processing...'))

def do_download(url: str, kind: str):
    try:
        outdir = Path("downloads")
        outdir.mkdir(exist_ok=True)
        if kind == "video":
            ydl_opts = {
                "outtmpl": str(outdir / "%(title)s.%(ext)s"),
                # Prefer mp4 if available; otherwise best
                "format": "bv*+ba/best[ext=mp4]/best",
                "noprogress": True,
                "progress_hooks": [progress_hook],
                "merge_output_format": "mp4",
            }
        else:  # mp3
            ydl_opts = {
                "outtmpl": str(outdir / "%(title)s.%(ext)s"),
                "format": "bestaudio/best",
                "noprogress": True,
                "progress_hooks": [progress_hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        wtq.put(('done', f"Saved to: {outdir.resolve()}"))
    except Exception as e:
        wtq.put(('error', str(e)))

def start():
    url = url_variable.get().strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        messagebox.showerror("Invalid URL", "Please paste a valid YouTube link.")
        return
    btn_download.config(state="disabled")
    progress["value"] = 0
    status_bar.set("Starting...")
    threading.Thread(target=do_download, args=(url, choice_of_conv.get()), daemon=True).start()

def poll():
    try:
        while True:
            kind, payload = wtq.get_nowait()
            if kind == 'progress':
                progress["value"] = payload
                status_bar.set(f"Downloading... {payload}%")
            elif kind == 'note':
                status_bar.set(payload)
            elif kind == 'done':
                status_bar.set("Done.")
                messagebox.showinfo("Completed", payload)
                btn_download.config(state="normal")
            elif kind == 'error':
                status_bar.set("Failed.")
                messagebox.showerror("Error", payload)
                btn_download.config(state="normal")
    except Empty:
        pass
    my_gui.after(100, poll)

btn_download.config(command=start)
poll()
my_gui.mainloop()
