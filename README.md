<h1 align="center">🎬 SubtitleTranslator</h1>

<p align="center">
  <b>Translate your .SRT subtitle files into Persian automatically — powered by Python & Google Translate</b><br>
  <sub>Developed with 💙 by <a href="https://github.com/dishonored103">Dishonored</a></sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Translator-Google%20Translate-orange?logo=googletranslate" />
  <img src="https://img.shields.io/github/last-commit/dishonored103/SubtitleTranslator?color=brightgreen" />
</p>

---

## 🚀 About the Project
**SubtitleTranslator** is a lightweight Python tool that translates `.srt` subtitle files into **Persian (Farsi)** —  
keeping their original timing and structure intact.

It uses the [`deep-translator`](https://pypi.org/project/deep-translator/) package to access **Google Translate**,  
so you don’t need any API key or paid services.

---

## ✨ Features

✅ Batch translation (20 blocks per batch)  
✅ Multi-file support — translate multiple subtitles in one run  
✅ Keeps all timestamps and numbering intact  
✅ Works on Windows, macOS, and Linux  
✅ No API key required — 100% free  
✅ Clean and readable code  

---

## 🧰 Installation

> Make sure you have Python 3.10 or newer installed.  
> If not, download it from [python.org](https://www.python.org/downloads/).

Then install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

You can translate one or many `.srt` files at once:

### 🔹 Example 1 – Single file
```bash
python subtitle_translator.py "example.srt"
```

### 🔹 Example 2 – All subtitles in a folder
```bash
python subtitle_translator.py *.srt
```

### 🔹 Example 3 – Whole directory
```bash
python subtitle_translator.py "C:\MySubtitles"
```

After running, each translated subtitle will appear with `_fa` at the end, like:
```
example_fa.srt
```

---

## 🧠 How It Works

1. Reads each `.srt` file and splits it into blocks (by empty lines).  
2. Sends each batch of 20 text blocks to Google Translate via `deep-translator`.  
3. Rebuilds the `.srt` with the original numbering and timing preserved.  
4. Saves the translated version beside the original file.

---

## 📸 Demo Screenshot

<p align="center">
  <img src="https://github.com/dishonored103/SubtitleTranslator/assets/demo_screenshot.png" width="80%" alt="Subtitle Translator running in Windows Command Prompt" />
</p>

> *(You can replace this with your own screenshot later — e.g. from your CMD window while translation is running.)*

---

## 🧾 Requirements
- Python ≥ 3.10  
- [deep-translator](https://pypi.org/project/deep-translator/)  
- [tqdm](https://pypi.org/project/tqdm/)

Install all via:
```bash
pip install deep-translator tqdm
```

---

## 🛠️ Project Structure

```
SubtitleTranslator/
│
├── subtitle_translator.py      # Main translator script
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
├── LICENSE                      # MIT License
└── .gitignore                   # Ignore cache files
```

---

## ❤️ Author
**Dishonored**  
📍 IT Infrastructure & Virtualization Engineer  
🔗 [GitHub Profile](https://github.com/dishonored103)

---

## 🪪 License
This project is licensed under the **MIT License** — you are free to use, modify, and distribute it.

---

<p align="center">⭐ If you find this project useful, don’t forget to star the repo!</p>
