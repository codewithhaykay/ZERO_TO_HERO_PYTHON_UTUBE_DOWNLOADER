# YouTube Downloader (Tkinter + yt-dlp)

A simple graphical YouTube downloader built with Python, Tkinter, and yt-dlp.  
It allows you to download YouTube videos or extract audio as MP3, while showing a live progress bar.

---

## Features

- **Graphical User Interface** built with Tkinter  
- **Video download** (MP4 preferred)  
- **Audio download** (MP3 extraction via FFmpeg)  
- **Progress bar** with real-time updates  
- **Threaded downloading** so the GUI does not freeze  

---

## Screenshots

<img width="293" height="200" alt="Project_Screenshot" src="https://github.com/user-attachments/assets/dac6dcc7-4956-4565-b380-9e03c16227d0" />
<img width="292" height="202" alt="Project_Screenshot2" src="https://github.com/user-attachments/assets/4907c702-7c17-4d08-8a06-52e1c928b76b" />

<img width="295" height="197" alt="Project_Screenshot3" src="https://github.com/user-attachments/assets/7c0c54e0-c05f-4229-ab8c-a3caee71bcfb" />

---

## Installation

1. **Clone this repository**


git clone https://github.com/codewithhaykay/zero_to_hero_python_utube_downloader.git
cd zero_to_hero_python_utube_downloader

2. **Create a virtual environment**
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. ** Install Dependencies**
   pip install -r requirements.txt

4. Install FFmpeg
You need FFmpeg installed and on your system PATH for MP3 conversion to work.
[Download from](https://ffmpeg.org/download.html)

## Usage
* Paste a YouTube link in the entry field.
* Choose Video (MP4) or MP3 (audio only).
* Click Download.
* Files will be saved in the downloads folder automatically.

## How It Works
* The Tkinter GUI runs in the main thread.
* The actual download runs in a background thread using threading.Thread.
* Progress updates are sent via a queue.Queue to the main thread.
* The main thread polls the queue every 100ms using root.after().
* This prevents the GUI from freezing during downloads.

## Contributing
Pull requests are welcome. 
If you find a bug or want to add a feature, feel free to open an issue first.
