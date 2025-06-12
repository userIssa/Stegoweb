# 🕵️ Steganography Toolkit (Web + CLI)

A simple but powerful steganography tool for hiding and extracting information in images and audio files.  
Includes both a **terminal-based interface** and a **Flask-powered web interface** with file previews and dark mode.

---

## 🌐 Web Interface Features

- 🔐 Embed and extract hidden data (text or files)
- 🖼️ Supports images (JPG, PNG) and audio (MP3, WAV)
- 🎧 Built-in previews for uploaded cover/stego files
- 🌙 Dark mode interface with responsive design
- 🧪 Built on Python, Flask, and open-source stego tools

---

## 💻 Terminal Usage (Kali Linux)

This tool uses `steghide` and `steghide`-compatible workflows in the terminal.

### 🔧 Installation Requirements

```bash
sudo apt update
sudo apt install steghide sox python3 python3-pip
pip install flask
```

---

## ▶️ Running the Web Server

### 📂 1. Clone the Repository

```bash
git clone https://github.com/your-username/stego-toolkit.git
cd stego-toolkit
```
### 🚀 2. Start the Flask Server

```bash
python3 app.py
```
Then visit:
```bash
http://localhost:5000
```

---

## 🧪 Example Workflow
### ✅ Embedding
Choose a cover file (image or audio)

Upload the secret file (e.g. secret.txt)

Enter a password and click Embed

Download the resulting stego file

### 🔓 Extracting
Upload the stego file

Enter the password used during embedding

Download the extracted hidden data

---


## ⚠️ Notes
Use common formats: .jpg, .png, .mp3, .wav, .txt

For audio steganography, .wav files are most reliable

Uses steghide (lossless formats are preferred)

---


## 📁 Folder Structure
```bash
stego-toolkit/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── (optional: download folder, logs, stylesheets)
└── README.md
```

---

## 📜 License
MIT License © 2025 Issa Oderinde

---

## 🤝 Contributions
Pull requests and suggestions are welcome.
Let’s build better tools for ethical cybersecurity and forensics!
