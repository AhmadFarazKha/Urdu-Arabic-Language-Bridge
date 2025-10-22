import os
import sys
import base64
import tempfile
import time
from flask import Flask, jsonify, send_file, request
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not in .env", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

class Bridge:
    def __init__(self):
        self.history = []
        self.dialect = "gulf"
        
    def process(self, base64_audio, dialect="gulf"):
        """Main processing function"""
        self.dialect = dialect
        
        try:
            # Decode audio
            print("Decoding audio...", file=sys.stderr)
            audio_bytes = base64.b64decode(base64_audio)
            print(f"Audio size: {len(audio_bytes)} bytes", file=sys.stderr)
            
            if len(audio_bytes) < 1000:
                return {"error": "Audio too short", "status": "fail"}
            
            # Create prompt
            prompt = f"""Transcribe this Urdu audio and provide:
1. Urdu text
2. Sentiment score (1-10)
3. Arabic translation ({self.dialect})
4. Tips

Format:
---
URDU: [text]
SENTIMENT: [number]
ARABIC: [translation]
TIPS: [tips]
---"""
            
            # Send directly with base64
            print("Sending to Gemini...", file=sys.stderr)
            
            content = [
                prompt,
                {
                    "mime_type": "audio/webm",
                    "data": base64_audio,
                }
            ]
            
            result_response = model.generate_content(content)
            result_text = result_response.text
            
            print("✓ Translation complete", file=sys.stderr)
            self.history.append(result_text)
            
            return {"result": result_text, "status": "success"}
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ ERROR: {error_msg}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return {"error": error_msg, "status": "fail"}

bridge = Bridge()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        audio = data.get('audio')
        dialect = data.get('dialect', 'gulf')
        
        if not audio:
            return jsonify({"error": "No audio data", "status": "fail"}), 400
        
        result = bridge.process(audio, dialect)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "status": "fail"}), 500

@app.route('/clear', methods=['POST'])
def clear():
    bridge.history = []
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("\n✓ Server running at http://127.0.0.1:5000\n", file=sys.stderr)
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)