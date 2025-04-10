# Tortoise-TTS

A customized version of Tortoise-TTS for text-to-speech conversion with support for various voices, optimized for RTX 4090 GPU.

## 🚀 Features

- Support for multiple voices (e.g., Trump, Freeman, William, etc.)
- Automatic detection of available voices
- GPU optimization
- Short, natural pauses between sentences (0.1 seconds)
- High audio quality with customized parameters
- Automatic combination of sentences into a single audio file

## 📋 Installation

1. Clone the repo:
```bash
git clone https://github.com/jonashagstrom79/Tortoise-TTS.git
cd Tortoise-TTS
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Run the script:
```bash
python do_tts.py
```

2. Select a voice from the list
3. Enter the text you want to convert to speech

Generated audio files are saved in the `generated_audio/` directory.

## ⚙️ Configuration

The script is optimized for:
- RTX 4090 GPU
- Short pauses between sentences (0.1 seconds)
- High audio quality with customized parameters:
  - Diffusion iterations: 40
  - Temperature: 0.7
  - Diffusion temperature: 0.8

## 📁 Project Structure

```
Tortoise-TTS/
├── do_tts.py           # Main script for text-to-speech conversion
├── requirements.txt    # Dependencies
├── .gitignore         # Ignored files
├── tortoise/          # Tortoise-TTS library
├── voices/            # Voice files
└── generated_audio/   # Generated audio files (ignored by git)
```

## 📝 Tips

- Maximum length per file is 30 seconds (600 mel tokens)
- Recommended character count per file is 100-150 characters
- Longer texts are automatically split into sentences

## 📄 License

This project is based on Tortoise-TTS and follows its license terms.
# Tortoise-tts
