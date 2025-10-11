import os
import sys
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import time
import json
import sounddevice as sd
import soundfile as sf
from flask import Flask, jsonify, send_file, Response
import threading

print("Starting Urdu-Arabic Language Bridge...", file=sys.stderr)

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env", file=sys.stderr)
    sys.exit(1)

# Configure Google Generative AI
genai.configure(api_key=api_key)
try:
    model = genai.GenerativeModel("gemini-pro")  # Permanent stable model (no 404)
    print("Gemini model loaded successfully", file=sys.stderr)
except Exception as e:
    print(f"Gemini error: {e}", file=sys.stderr)
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
print("Flask app initialized", file=sys.stderr)

class LanguageBridge:
    def __init__(self):
        self.recording = False
        self.audio_path = "recording.wav"
        self.logs_dir = "analysis_logs"
        self.summary_path = "learning_summary.txt"
        self.status = "Idle"
        self.progress = 0
        self.previous_context = ""
        self.frames = []

    def start_recording(self):
        self.status = "Recording"
        self.progress = 0
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
        
        samplerate = 44100
        duration = 10  # Initial duration; extend if needed
        try:
            print("Recording started... Speak in Urdu for 10s", file=sys.stderr)
            self.frames = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
            sd.wait()  # Wait for recording to finish
            sf.write(self.audio_path, self.frames, samplerate)
            print("Recording stopped.", file=sys.stderr)
            self.recording = False
            self.status = "Processing"
            self.process_audio()
        except Exception as e:
            print(f"Recording error: {e} (check microphone)", file=sys.stderr)
            self.status = "Error: Microphone issue (run as admin)"

    def process_audio(self):
        if not os.path.exists(self.audio_path):
            self.status = "Error: No audio to process"
            print(self.status, file=sys.stderr)
            return
        
        os.makedirs(self.logs_dir, exist_ok=True)
        
        try:
            # Load audio
            audio_data, samplerate = sf.read(self.audio_path)
            
            # Chunk into 2s segments
            interval = 2
            chunk_size = int(interval * samplerate)
            analyses = []
            
            for t in range(0, len(audio_data), chunk_size):
                chunk = audio_data[t:t+chunk_size]
                if len(chunk) < samplerate:  # Skip short chunks
                    continue
                chunk_path = os.path.join(self.logs_dir, f"chunk_{t//chunk_size}.wav")
                sf.write(chunk_path, chunk, samplerate)
                
                with open(chunk_path, "rb") as audio_file:
                    try:
                        audio = genai.upload_file(audio_file, mime_type='audio/wav', display_name="Urdu Audio Chunk")  # Added display_name
                        prompt = f"""
                        Transcribe this Urdu audio, then translate to Arabic (Gulf dialect for Saudi Arabia). Provide:
                        - Urdu text
                        - Arabic translation
                        - Pronunciation tips (e.g., 'Roll R for ر')
                        - Context from previous: {self.previous_context[:200]}... (avoid repeats)

                        Time: {t/samplerate:.1f}s to {(t+chunk_size)/samplerate:.1f}s
                        """
                        response = model.generate_content([prompt, audio])
                        analyses.append(response.text)
                        self.previous_context = response.text
                        print(f"Analyzed chunk: {response.text[:100]}...", file=sys.stderr)
                    except Exception as upload_e:
                        print(f"Upload error for {chunk_path}: {upload_e}", file=sys.stderr)
                        analyses.append(f"Error transcribing chunk at {t/samplerate:.1f}s: {upload_e}")
            
            self.generate_summary(analyses)
        except Exception as e:
            print(f"Error processing audio: {e}", file=sys.stderr)
            self.status = f"Error: {e}"

    def generate_summary(self, analyses):
        try:
            with open(self.summary_path, 'w', encoding='utf-8') as f:
                f.write(f"Urdu-Arabic Learning Summary\nDate: {time.strftime('%B %d, %Y %H:%M:%S PKT')}\n\n")
                for i, analysis in enumerate(analyses, 1):
                    f.write(f"Section {i}.0 - Time {i*2-2:.1f}s to {i*2:.1f}s\n")
                    f.write(analysis + "\n\n")
                f.write("Quiz: Translate these to Arabic:\n- Peace\n- Thank you\n- How are you?\n")
            self.status = "Summary Generated"
            self.progress = 100
            print(f"Summary generated: {self.summary_path}", file=sys.stderr)
        except Exception as e:
            self.status = f"Error generating summary: {e}"
            print(self.status, file=sys.stderr)

    def get_summary_preview(self):
        if not os.path.exists(self.summary_path):
            return "Summary not found."
        try:
            with open(self.summary_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Preview error: {e}"

bridge = LanguageBridge()

@app.route('/')
def serve_index():
    if not os.path.exists('index.html'):
        print("Error: index.html not found", file=sys.stderr)
        return "Error: UI file missing", 500
    return send_file('index.html')

@app.route('/start', methods=['POST'])
def start_recording():
    if not bridge.recording:
        threading.Thread(target=bridge.start_recording).start()
        return jsonify({"status": bridge.status})
    return jsonify({"status": "Already recording"})

@app.route('/stop', methods=['POST'])
def stop_recording():
    if bridge.recording:
        bridge.recording = False
        return jsonify({"status": bridge.status})
    return jsonify({"status": "Not recording"})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": bridge.status, "progress": bridge.progress})

@app.route('/preview', methods=['GET'])
def get_summary_preview():
    preview = bridge.get_summary_preview()
    return Response(preview, mimetype='text/plain')

if __name__ == "__main__":
    print("Starting Flask server...", file=sys.stderr)
    app.run(debug=True, host="0.0.0.0", port=5000)