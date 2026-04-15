import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import multiprocessing
import pyttsx3

API_URL = "http://127.0.0.1:8000/ask"

# ---- STT ----
model = whisper.load_model("base")


def record_audio(filename="input.wav", duration=3, fs=16000):
    print("🎤 Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    print("✅ Recording complete")


def transcribe_audio(filename="input.wav"):
    result = model.transcribe(filename)
    return result["text"]


# ---- TTS (multiprocessing fix) ----
def speak_worker(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def speak(text):
    p = multiprocessing.Process(target=speak_worker, args=(text,))
    p.start()
    p.join()


# ---- MAIN LOOP ----
def main():
    while True:
        input("\nPress ENTER to speak...")

        record_audio()
        query = transcribe_audio()

        print(f"\n🧑 You: {query}")

        # ---- CALL API ----
        response = requests.post(
            API_URL,
            json={"query": query}
        )

        data = response.json()
        answer = data["response"]

        print(f"\n🤖 Agent: {answer}")

        speak(answer)


if __name__ == "__main__":
    main()