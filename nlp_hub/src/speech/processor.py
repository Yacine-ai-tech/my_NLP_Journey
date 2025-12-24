"""Speech processing module for STT and TTS."""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass
from pathlib import Path
from ..utils.logger import get_logger
from ..utils.exceptions import SpeechError, ModelNotFoundError
from ..config.settings import settings


logger = get_logger(__name__, level=settings.log_level)


@dataclass
class SpeechRecognitionResult:
    """Speech recognition result."""
    text: str
    confidence: float
    language: str
    duration: float
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TextToSpeechResult:
    """Text-to-speech synthesis result."""
    audio_path: Path
    duration: float
    sample_rate: int
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SpeechProcessor(ABC):
    """Base class for speech processing."""
    
    def __init__(self, language: str = None):
        """
        Initialize speech processor.
        
        Args:
            language: Language code
        """
        self.language = language or settings.speech.language
        self._load_model()
    
    @abstractmethod
    def _load_model(self):
        """Load speech models."""
        pass
    
    @abstractmethod
    def transcribe(self, audio_path: Path) -> SpeechRecognitionResult:
        """Convert speech to text."""
        pass
    
    @abstractmethod
    def synthesize(self, text: str, output_path: Path) -> TextToSpeechResult:
        """Convert text to speech."""
        pass


class GoogleSpeechProcessor(SpeechProcessor):
    """Speech processing using Google Cloud Speech API."""
    
    def _load_model(self):
        """Initialize Google Speech API client."""
        try:
            from google.cloud import speech_v1, texttospeech_v1
            
            logger.info("Initializing Google Speech API")
            self.speech_client = speech_v1.SpeechClient()
            self.tts_client = texttospeech_v1.TextToSpeechClient()
        except ImportError:
            raise ModelNotFoundError(
                "Google Cloud libraries not installed. Install with: "
                "pip install google-cloud-speech google-cloud-texttospeech"
            )
        except Exception as e:
            raise ModelNotFoundError(f"Failed to initialize Google Speech API: {str(e)}")
    
    def transcribe(self, audio_path: Path) -> SpeechRecognitionResult:
        """Transcribe audio using Google Speech-to-Text."""
        try:
            from google.cloud.speech_v1 import RecognitionConfig
            
            audio_path = Path(audio_path)
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            with open(audio_path, "rb") as audio_file:
                content = audio_file.read()
            
            audio = {"content": content}
            config = RecognitionConfig(
                encoding=RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=settings.speech.sample_rate,
                language_code=self.language,
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                
                return SpeechRecognitionResult(
                    text=transcript,
                    confidence=confidence,
                    language=self.language,
                    duration=0.0,  # Would need to calculate from audio
                )
            
            return SpeechRecognitionResult(
                text="",
                confidence=0.0,
                language=self.language,
                duration=0.0,
            )
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise SpeechError(f"Transcription failed: {str(e)}")
    
    def synthesize(self, text: str, output_path: Path) -> TextToSpeechResult:
        """Synthesize speech using Google Text-to-Speech."""
        try:
            from google.cloud import texttospeech_v1
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            input_text = texttospeech_v1.SynthesisInput(text=text)
            
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code=self.language,
                ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL,
            )
            
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
            )
            
            response = self.tts_client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config,
            )
            
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            return TextToSpeechResult(
                audio_path=output_path,
                duration=0.0,
                sample_rate=settings.speech.sample_rate,
            )
        except Exception as e:
            logger.error(f"Synthesis failed: {str(e)}")
            raise SpeechError(f"Synthesis failed: {str(e)}")


class DummySpeechProcessor(SpeechProcessor):
    """Dummy speech processor for testing."""
    
    def _load_model(self):
        """Initialize dummy processor."""
        logger.info("Using dummy speech processor")
    
    def transcribe(self, audio_path: Path) -> SpeechRecognitionResult:
        """Return dummy transcription."""
        return SpeechRecognitionResult(
            text="This is a dummy transcription",
            confidence=0.95,
            language=self.language,
            duration=5.0,
        )
    
    def synthesize(self, text: str, output_path: Path) -> TextToSpeechResult:
        """Create dummy audio file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.touch()
        
        return TextToSpeechResult(
            audio_path=output_path,
            duration=len(text) * 0.1,
            sample_rate=settings.speech.sample_rate,
        )


def get_speech_processor(processor_type: str = "google") -> SpeechProcessor:
    """
    Factory function to get speech processor.
    
    Args:
        processor_type: Type of processor ('google' or 'dummy')
    
    Returns:
        SpeechProcessor instance
    """
    if processor_type == "google":
        return GoogleSpeechProcessor()
    elif processor_type == "dummy":
        return DummySpeechProcessor()
    else:
        raise ValueError(f"Unknown processor type: {processor_type}")
