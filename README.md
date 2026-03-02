# 🎙️ Jarvis Voice Assistant

Jarvis is a powerful, web-based AI voice assistant designed to simplify your digital life. Built with **Flask** and powered by **OpenAI's GPT-3.5**, Jarvis can handle conversations, open websites, manage your contacts, and even control your Android device via ADB for calling and messaging.

---

## 🚀 Features

### 🤖 Smart Conversations
- **AI-Powered Chat:** Natural language conversations using OpenAI GPT-3.5.
- **Voice Interaction:** Supports full voice input (Speech Recognition) and output (Text-to-Speech).
- **History Tracking:** Automatically stores and displays your interaction history in a local database.

### 🌐 Smart Browsing & Utilities
- **Quick-Open Apps:** Open popular platforms instantly (YouTube, Spotify, Netflix, WhatsApp, GMail, etc.).
- **Time & Date:** Get real-time updates for your current location.
- **Microphone Control:** Toggle voice listening mode through a dedicated UI.

### 👤 User & Contact Management
- **Secure Login:** Full authentication system (Sign-up, Log-in, Log-out).
- **Contact Database:** Store names and phone numbers in a secure SQLite database.

### 📱 Android Device Integration
- **Make Calls:** Trigger phone calls on your connected Android device.
- **Send Messages:** Compose and send SMS messages using ADB commands.
- **Remote Control:** Seamless mobile-desktop integration using ADB Shell.

---

## 🛠️ Tech Stack

- **Backend:** [Python](https://pypi.org/project/Flask/) (Flask)
- **Database:** [SQLite3](https://www.sqlite.org/index.html)
- **AI/ML:** [OpenAI API](https://platform.openai.com/docs/api-reference) (GPT-3.5)
- **Speech Services:**
  - Speech-To-Text: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
  - Text-To-Speech: [pyttsx3](https://pypi.org/project/pyttsx3/)
- **Frontend:** HTML5, CSS3 (Parallax Effects), JavaScript (AJAX, DOM Manipulation)
- **Mobile Connectivity:** [ADB (Android Debug Bridge)](https://developer.android.com/tools/adb)

---

## ⚙️ Installation

### 1. Prerequisites
- **Python 3.8+** installed.
- **ADB Tools** installed and added to PATH (for mobile features).
- **Microphone** and **Speakers** for voice interaction.
- **OpenAI API Key** ([Get it here](https://platform.openai.com/)).

### 2. Clone the Repository
```bash
git clone https://github.com/VigneshKode/Jarvis-Voice-Assistant.git
cd Jarvis-Voice-Assistant
```

### 3. Setup Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install flask openai pyttsx3 SpeechRecognition PyAudio
```

### 5. Configure API Key
Open `app.py` and replace the placeholder API key with your own:
```python
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"
```

---

## 🏃 Usage

1. **Connect your Android Device** via USB (Enable USB Debugging).
2. **Launch the application:**
   ```bash
   python app.py
   ```
3. **Access the web interface:**
   Go to `http://127.0.0.1:5000` in your browser.
4. **Interact:**
   - Type your question in the input field.
   - Or click the **Microphone Icon** (or type "voice") to start voice mode.
   - Try commands like *"Open Youtube"* or *"Add contact John Doe, 1234567890"*.

---

## 📂 Project Structure

```text
Jarvis-Voice-Assistant/
├── static/               # CSS, JS, and UI Images (Hills, Plants, Leaves)
├── templates/            # HTML templates (Home, Login, Registration)
├── app.py                # Main Flask application & AI logic
├── users.db              # SQLite Database (Auto-generated)
└── README.md             # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the AI prompts, UI design, or add new device control commands, please feel free to fork the repo and create a pull request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ by [Vignesh Kode](https://github.com/VigneshKode)**
