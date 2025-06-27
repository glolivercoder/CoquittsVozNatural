from TTS.api import TTS
import torch
import os
import threading
from typing import Optional, Dict, List
import logging

class TTSEngine:
    def __init__(self):
        self.current_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger = logging.getLogger(__name__)
        
        # Modelos pré-definidos por idioma
        self.available_models = {
            "pt-br": {
                "VITS": "tts_models/pt/cv/vits",
                "XTTS v2": "tts_models/multilingual/multi-dataset/xtts_v2",
            },
            "en": {
                "Tacotron2": "tts_models/en/ljspeech/tacotron2-DDC",
                "VITS": "tts_models/en/ljspeech/vits",
                "Neural HMM": "tts_models/en/ljspeech/neural_hmm"
            },
            "es": {
                "Tacotron2": "tts_models/es/mai/tacotron2-DDC",
                "VITS": "tts_models/es/css10/vits"
            },
            "multilingual": {
                "XTTS v2": "tts_models/multilingual/multi-dataset/xtts_v2"
            }
        }
        
        # Configurações específicas por modelo
        self.model_configs = {
            "XTTS v2": {
                "support_voice_cloning": True,
                "requires_speaker_wav": True,
                "languages": ["pt-br", "en", "es"]
            },
            "VITS": {
                "support_voice_cloning": False,
                "requires_speaker_wav": False,
                "languages": ["pt-br", "en", "es"]
            },
            "Tacotron2": {
                "support_voice_cloning": False,
                "requires_speaker_wav": False,
                "languages": ["en", "es"]
            },
            "Neural HMM": {
                "support_voice_cloning": False,
                "requires_speaker_wav": False,
                "languages": ["en"]
            }
        }
    
    def load_model(self, model_name: str, language: str = "pt-br") -> bool:
        """Carrega um modelo TTS específico"""
        try:
            if language in self.available_models:
                model_path = self.available_models[language].get(model_name)
                if model_path:
                    self.logger.info(f"Carregando modelo {model_name} para {language}")
                    self.current_model = TTS(model_path).to(self.device)
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelo: {e}")
            return False
    
    def generate_speech(self, 
                       text: str, 
                       output_path: str = "output.wav",
                       speaker_wav: Optional[str] = None,
                       language: Optional[str] = None) -> str:
        """
        Gera fala a partir do texto
        
        Args:
            text: Texto para sintetizar
            output_path: Caminho para salvar o áudio
            speaker_wav: Arquivo de áudio do speaker para clonagem de voz (opcional)
            language: Código do idioma (opcional)
        
        Returns:
            Caminho do arquivo de áudio gerado
        """
        if not self.current_model:
            raise Exception("Nenhum modelo carregado")
        
        try:
            kwargs = {"text": text, "file_path": output_path}
            
            # Adiciona parâmetros específicos se necessário
            if speaker_wav and hasattr(self.current_model, "speakers"):
                kwargs["speaker_wav"] = speaker_wav
            
            if language and "multilingual" in self.current_model.model_name:
                kwargs["language"] = language
            
            self.current_model.tts_to_file(**kwargs)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar fala: {e}")
            raise
    
    def get_model_info(self, model_name: str) -> Dict:
        """Retorna informações sobre um modelo específico"""
        return self.model_configs.get(model_name, {})
    
    def list_available_models(self, language: Optional[str] = None) -> Dict:
        """Lista modelos disponíveis para um idioma específico ou todos"""
        if language:
            return self.available_models.get(language, {})
        return self.available_models
    
    def list_speakers(self) -> List[str]:
        """Lista speakers disponíveis no modelo atual"""
        if self.current_model and hasattr(self.current_model, "speakers"):
            return self.current_model.speakers
        return []
    
    def supports_voice_cloning(self) -> bool:
        """Verifica se o modelo atual suporta clonagem de voz"""
        if not self.current_model:
            return False
        return "xtts" in self.current_model.model_name.lower()
    
    def get_model_languages(self) -> List[str]:
        """Retorna os idiomas suportados pelo modelo atual"""
        if not self.current_model:
            return []
        if "multilingual" in self.current_model.model_name:
            return ["pt-br", "en", "es"]  # XTTS v2 suporta múltiplos idiomas
        return [self.current_model.language] if hasattr(self.current_model, "language") else [] 