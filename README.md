Markdown
# Interactive Arabic Voice Assistant 🎙️🤖

An interactive, real-time voice-to-voice conversational AI system built in Python. The application captures live microphone input, transcribes Arabic speech locally, processes context-aware responses using Cohere's Large Language Model (LLM), and plays back synthesized spoken Arabic answers.

---

## 🌟 Features

* **Offline Speech-to-Text (STT):** Powered by OpenAI's local Whisper (`base` model) to transcribe Arabic audio directly on your CPU without cloud API latency or bandwidth costs.
* **Turn-by-Turn Dialogue:** Retains full conversational context across multi-turn interactions using Cohere's `command-r-08-2024` model.
* **Spoken Audio Output:** Synthesizes Arabic speech using Google Text-to-Speech (`gTTS`) and handles seamless audio playback with `pygame`.
* **Zero OpenAI Credit Dependency:** Built entirely with 100% free local models and free-tier API endpoints.

---

## 🏗️ System Architecture

┌─────────────────┐
│  Microphone     │
└────────┬────────┘
│ (Live Voice)
▼
┌─────────────────┐
│ 1. Local        │ ──► Transcribes Arabic audio locally using CPU
│    Whisper STT  │
└────────┬────────┘
│ (Text Prompt)
▼
┌─────────────────┐
│ 2. Cohere LLM   │ ──► Processes turn context & generates Arabic response
│    Command-R    │
└────────┬────────┘
│ (Response Text)
▼
┌─────────────────┐
│ 3. gTTS +       │ ──► Converts response to MP3 & plays audio out loud
│    Pygame TTS   │
└─────────────────┘


---

## 📦 Required Libraries & Dependencies

| Package | Purpose |
| :--- | :--- |
| `openai-whisper` | Offline Arabic speech recognition on CPU |
| `cohere` | API client for Cohere Large Language Models |
| `gTTS` | Google Text-to-Speech audio synthesis |
| `pygame` | Native MP3 audio loading and playback mixer |
| `SpeechRecognition` | System microphone interface and audio capture |
| `PyAudio` | Low-level system audio stream bindings |

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/majed756/Interactive-Arabic-Voice-Assistant.git](https://github.com/majed756/Interactive-Arabic-Voice-Assistant.git)
   cd Interactive-Arabic-Voice-Assistant
Install all required dependencies:

Bash
python -m pip install openai-whisper cohere gTTS pygame SpeechRecognition PyAudio
Configure API Key:
Get a free Trial Key from Cohere Dashboard and insert it into line 19 of main.py:

Python
COHERE_API_KEY = "YOUR_FREE_COHERE_API_KEY"
🎯 How to Run
Execute the program from your terminal:

Bash
python main.py
