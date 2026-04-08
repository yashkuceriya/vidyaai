import tempfile
import os
import base64
import whisper
import edge_tts
import asyncio

# Lazy-load whisper model
_whisper_model = None

LANGUAGE_MAP = {
    "hindi": "hi",
    "english": "en",
    "marathi": "mr",
    "tamil": "ta",
}

TTS_VOICE_MAP = {
    "hindi": "hi-IN-SwaraNeural",
    "english": "en-IN-NeerjaNeural",
    "marathi": "mr-IN-AarohiNeural",
    "tamil": "ta-IN-PallaviNeural",
}


def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("small")
    return _whisper_model


def transcribe_audio(audio_bytes: bytes, language: str = "hindi") -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name

    try:
        model = _get_whisper_model()
        lang_code = LANGUAGE_MAP.get(language, "hi")
        result = model.transcribe(tmp_path, language=lang_code)
        return result.get("text", "").strip()
    finally:
        os.unlink(tmp_path)


async def synthesize_speech(text: str, language: str = "hindi") -> str:
    voice = TTS_VOICE_MAP.get(language, TTS_VOICE_MAP["hindi"])

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp_path = f.name

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)

        with open(tmp_path, "rb") as f:
            audio_data = f.read()

        audio_b64 = base64.b64encode(audio_data).decode("utf-8")
        return f"data:audio/mp3;base64,{audio_b64}"
    finally:
        os.unlink(tmp_path)
