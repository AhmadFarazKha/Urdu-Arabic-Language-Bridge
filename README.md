# Urdu-Arabic-Language-Bridge

Real-time Urdu-to-Arabic translation and learning companion using AI, computer vision, and Google APIs. Designed for WhatsApp calls and Gulf conversations (e.g., Saudi Arabia). Built with Python, Gemini, and OpenCV.


# Urdu-Arabic Language Bridge 🌍

A real-time speech translation application that converts Urdu audio to Arabic with sentiment analysis, pronunciation guidance, and dialect selection. Built with Python Flask backend and interactive web frontend.

## Features

✨ **Real-time Urdu to Arabic Translation**

* Instant speech-to-text transcription in Urdu
* Multi-dialect Arabic support (Gulf, Levantine, Egyptian, Moroccan, Standard)
* Powered by Google Gemini 2.0 Flash for fast processing

📊 **Advanced Analysis**

* Sentiment analysis with emotional scoring (1-10)
* Pronunciation tips for accurate Arabic speaking
* Complete conversation history tracking

🎤 **User-Friendly Interface**

* Simple one-click recording
* Clear separation of input and output
* Color-coded sections for easy understanding
* Responsive design for all devices

🔄 **Multi-Language Support**

* Primary: Urdu
* Secondary support: Punjabi, Hindi (extensible)

## Technical Stack

* **Backend** : Python Flask
* **AI/ML** : Google Gemini 2.0 Flash API
* **Frontend** : HTML5, CSS3, JavaScript (Web Audio API)
* **Audio Processing** : MediaRecorder API
* **Deployment** : Local Flask server

## Prerequisites

* Python 3.8+
* Google Generative AI API Key
* Modern web browser with microphone access
* Internet connection

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/urdu-arabic-bridge.git
cd urdu-arabic-bridge
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install flask google-generativeai python-dotenv
```

4. **Set up API Key**
   Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

## Usage

1. **Start the Flask server**

```bash
python main.py
```

2. **Open browser**
   Navigate to: `http://127.0.0.1:5000`
3. **Record and Translate**

* Select Arabic dialect
* Click "Start Recording"
* Speak in Urdu (clear, audible speech)
* Click "Stop Recording"
* View results in color-coded boxes:
  * **Blue** : Your Urdu text
  * **Purple** : Arabic translation
  * **Orange** : Sentiment analysis
  * **Green** : Pronunciation tips

## Project Structure

```
urdu-arabic-bridge/
├── main.py              # Flask backend + API endpoints
├── index.html           # Frontend UI
├── .env                 # API configuration (create this)
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## How It Works

1. **Audio Recording** : Browser captures Urdu speech via Web Audio API
2. **Base64 Encoding** : Audio converted to base64 format
3. **Server Processing** :

* Receives encoded audio
* Sends to Google Gemini 2.0 Flash API
* Extracts transcription, translation, sentiment

1. **Display Results** : Frontend parses and displays in separate sections

## API Endpoints

### POST `/process`

Process Urdu audio and get Arabic translation

**Request:**

```json
{
  "audio": "base64_encoded_audio",
  "dialect": "gulf"
}
```

**Response:**

```json
{
  "status": "success",
  "result": "===== URDU =====\n[text]\n===== ARABIC =====\n[text]\n..."
}
```

### POST `/clear`

Clear conversation history

### GET `/`

Serve the HTML interface

## Configuration

Edit `main.py` to change:

* **Model** : Currently using `gemini-2.0-flash-exp` (fastest)
* **Dialects** : Supported Arabic dialects in dropdown
* **Port** : Default 5000 (modify in `if __name__` section)
* **Max Tokens** : Currently 500 (line ~35 in backend)

## Supported Arabic Dialects

* **Gulf Arabic** - Saudi Arabia, UAE, Kuwait
* **Levantine Arabic** - Syria, Lebanon, Palestine
* **Egyptian Arabic** - Egypt, popular across region
* **Moroccan Arabic** - Morocco, Algeria
* **Standard Arabic** - Formal, all regions

## Performance

* **Processing Time** : 5-15 seconds (depends on audio length)
* **Accuracy** : Depends on Gemini model performance
* **Limitation** : Requires internet for API calls

## Troubleshooting

### "No audio data"

* Check microphone permissions
* Ensure browser allows microphone access

### "Translation failed"

* Verify GOOGLE_API_KEY in .env
* Check internet connection
* Ensure API key has Generative AI access

### Slow processing

* Use shorter audio clips (5-10 seconds)
* Speak clearly
* Check internet speed

### Results not displaying

* Open browser console (F12) for errors
* Check Flask terminal for backend errors
* Ensure server is running on correct port

## Future Enhancements

* [ ] Real-time streaming transcription
* [ ] Batch processing for multiple files
* [ ] Export translations to PDF/CSV
* [ ] Custom dialect training
* [ ] Offline mode with local models
* [ ] Multi-language support expansion
* [ ] Audio playback of Arabic translations
* [ ] Vocabulary learning module

## Limitations

* Requires active internet connection
* API rate limiting based on Google's policy
* Audio quality affects transcription accuracy
* Processing time varies with server load
* Browser-based, not mobile app

## Privacy & Security

* Audio data sent only to Google servers
* No local storage of conversations (unless cleared manually)
* API key should never be committed to version control
* Use HTTPS in production

## API Costs

Uses Google Generative AI API:

* Free tier: 60 requests/minute (Gemini 2.0 Flash)
* Paid tier: Higher limits available
* Check: https://ai.google.dev/pricing

## Contributing

Contributions welcome! Areas for improvement:

* Frontend UI/UX
* Additional language pairs
* Performance optimization
* Mobile app version

## License

MIT License - Feel free to use for personal/commercial projects

## Author

Developed as an AI/ML project for Urdu-Arabic language learning and translation.

## Support & Contact

For issues, questions, or suggestions:

* Create GitHub issue
* Email: [your.email@example.com]
* LinkedIn: [Your LinkedIn Profile]

## Acknowledgments

* Google Gemini API for core translation
* Web Audio API for browser recording
* Flask framework for backend
* Contributors and testers

---

 **Last Updated** : 2025
 **Version** : 1.3
 **Status** : Active Development ✅
