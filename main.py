import io
import os
import sys
import time
import cohere
from gtts import gTTS
import pygame
import speech_recognition as sr
import whisper

# Force Windows terminal encoding to display Arabic characters cleanly
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Initialize Pygame Mixer for MP3 voice playback
pygame.mixer.init()

# 🔑 YOUR COHERE TRIAL KEY
COHERE_API_KEY = ""

print("⏳ Loading local Whisper AI model... (This runs offline on your PC)")
# 'base' model provides much higher accuracy for Arabic than 'tiny'
whisper_model = whisper.load_model("base")
print("✅ Whisper model loaded successfully!\n")

co = cohere.ClientV2(api_key=COHERE_API_KEY)
recognizer = sr.Recognizer()


def record_and_transcribe_local():
    """Step 1: Record mic audio and transcribe locally using Whisper AI"""
    with sr.Microphone() as source:
        print("\n🎙️ Listening... Speak in Arabic now!")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        print("   ✅ Processing voice locally with Whisper...")

        temp_wav = "temp_input.wav"
        with open(temp_wav, "wb") as f:
            f.write(audio.get_wav_data())

        try:
            result = whisper_model.transcribe(temp_wav, language="ar")
            text = result["text"].strip()
            print(f"👤 You: {text}")
            return text
        except Exception as e:
            print(f"❌ Whisper error: {e}")
            return ""


def generate_cohere_response(user_text, history):
    """Step 2: Generate response using active Cohere model"""
    print("🧠 Cohere AI thinking...")

    messages = [
        {
            "role": "system",
            "content": "أنت مساعد صوتی ذکی. أجب دائمًا باللغة العربية بأسلوب قصير، مباشر ومناسب للمحادثات الصوتية.",
        }
    ] + history
    messages.append({"role": "user", "content": user_text})

    # Updated to an active model version
    response = co.chat(model="command-r-08-2024", messages=messages)

    ai_text = response.message.content[0].text
    print(f"🤖 Cohere AI: {ai_text}")
    return ai_text


def speak_text_gtts(text, output_file="response.mp3"):
    """Step 3: Convert Arabic response text to speech and play via Pygame"""
    print("🔊 Playing voice response...")
    tts = gTTS(text=text, lang="ar")
    tts.save(output_file)

    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()


def start_conversation():
    print("==================================================")
    print("🤖 Interactive Arabic Voice Assistant")
    print("Local Whisper (STT) -> Cohere (LLM) -> gTTS (TTS)")
    print("==================================================")

    history = []

    while True:
        try:
            input("\n👉 Press ENTER when you are ready to speak...")

            # 1. Local Speech-to-Text
            user_text = record_and_transcribe_local()
            if not user_text:
                print("⚠️ No speech detected. Try speaking again!")
                continue

            if user_text in ["خروج", "إغلاق", "مع السلامة"]:
                print("👋 Goodbye!")
                break

            # 2. LLM Response
            ai_response = generate_cohere_response(user_text, history)

            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": ai_response})

            # 3. Audio Playback
            speak_text_gtts(ai_response)

        except KeyboardInterrupt:
            print("\n👋 Conversation stopped.")
            break
        except Exception as e:
            print(f"\n❌ Error during turn: {e}")


if __name__ == "__main__":
    start_conversation()