import os
import json
import requests
from typing import Dict, List

class ModelManager:
    def __init__(self, models_dir="./models"):
        self.models_dir = models_dir
        self.ensure_models_dir()
        self.predefined_models = {
            "Português BR": {
                "VITS": "tts_models/pt/cv/vits",
                "XTTS": "tts_models/multilingual/multi-dataset/xtts_v2"
            },
            "Inglês": {
                "Tacotron2": "tts_models/en/ljspeech/tacotron2-DDC",
                "VITS": "tts_models/en/ljspeech/vits",
                "Neural HMM": "tts_models/en/ljspeech/neural_hmm"
            },
            "Espanhol": {
                "Tacotron2": "tts_models/es/mai/tacotron2-DDC",
                "VITS": "tts_models/es/css10/vits"
            }
        }
    
    def ensure_models_dir(self):
        """Garante que o diretório de modelos existe"""
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
    
    def get_installed_models(self) -> List[str]:
        """Retorna lista de modelos instalados"""
        installed = []
        for root, dirs, files in os.walk(self.models_dir):
            for file in files:
                if file.endswith('.pth') or file.endswith('.pt'):
                    installed.append(os.path.relpath(os.path.join(root, file), self.models_dir))
        return installed
    
    def get_predefined_models(self) -> Dict:
        """Retorna modelos pré-definidos"""
        return self.predefined_models
    
    def download_model(self, model_name: str, progress_callback=None):
        """Baixa um modelo"""
        try:
            # Aqui você implementaria a lógica real de download do modelo
            # Usando a API do Coqui TTS ou outro método apropriado
            pass
        except Exception as e:
            raise Exception(f"Erro ao baixar modelo: {e}")
    
    def remove_model(self, model_path: str):
        """Remove um modelo"""
        full_path = os.path.join(self.models_dir, model_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    
    def validate_model(self, model_path: str) -> bool:
        """Valida se um modelo é válido"""
        full_path = os.path.join(self.models_dir, model_path)
        return os.path.exists(full_path) and os.path.getsize(full_path) > 0 