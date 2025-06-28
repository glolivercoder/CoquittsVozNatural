from TTS.api import TTS
import torch
import os
import threading
from typing import Optional, Dict, List
import logging
import sys
from pathlib import Path

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
                "languages": ["pt-br"]
            }
        }
        
        self._setup_environment()
    
    def _setup_environment(self):
        """Configura o ambiente necessário para o TTS"""
        try:
            # Configura o PyTorch
            torch.set_grad_enabled(False)  # Desativa gradientes para inferência
            if self.device == "cuda":
                torch.cuda.empty_cache()
            
            # Configura os diretórios de cache
            cache_dir = Path.home() / ".cache" / "tts"
            cache_dir.mkdir(parents=True, exist_ok=True)
            os.environ["TTS_HOME"] = str(cache_dir)
            
            # Adiciona classes seguras para carregamento
            # Nota: Removido temporariamente devido a problemas de tipagem
            # Será tratado em uma atualização futura
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar ambiente: {e}", exc_info=True)
    
    def load_model(self, model_path: str) -> bool:
        """
        Carrega um modelo TTS específico
        
        Args:
            model_path: Caminho do modelo (ex: tts_models/pt/cv/vits)
            
        Returns:
            bool: True se o modelo foi carregado com sucesso
        """
        try:
            self.logger.info(f"Tentando carregar modelo: {model_path}")
            
            # Limpa o modelo atual e a memória CUDA
            if self.current_model:
                del self.current_model
                if self.device == "cuda":
                    torch.cuda.empty_cache()
            
            # Garante que o nome do modelo está no formato correto
            if not model_path.startswith("tts_models/"):
                # Converte o formato antigo para o novo
                parts = model_path.split(" ")
                model_type = parts[0].lower()  # ex: VITS -> vits
                lang = "pt"  # default para português
                dataset = "cv"  # Common Voice como dataset padrão
                model_path = f"tts_models/{lang}/{dataset}/{model_type}"
            
            self.logger.info(f"Usando caminho de modelo formatado: {model_path}")
            
            # Tenta carregar o modelo
            try:
                self.current_model = TTS(model_name=model_path)
                if self.device == "cuda":
                    self.current_model.to(self.device)
                self.logger.info(f"Modelo {model_path} carregado com sucesso")
                return True
                
            except RuntimeError as e:
                error_msg = str(e).lower()
                
                if "espeak" in error_msg:
                    self.logger.warning("Espeak não encontrado, tentando sem fonemas")
                    self.current_model = TTS(model_name=model_path, use_phonemes=False)
                    if self.device == "cuda":
                        self.current_model.to(self.device)
                    return True
                    
                elif "cuda out of memory" in error_msg:
                    self.logger.warning("Memória CUDA insuficiente, usando CPU")
                    self.device = "cpu"
                    self.current_model = TTS(model_name=model_path)
                    return True
                    
                else:
                    raise
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar modelo {model_path}: {str(e)}", exc_info=True)
            self.current_model = None
            if self.device == "cuda":
                torch.cuda.empty_cache()
            return False
    
    def generate_speech(self, 
                       text: str, 
                       output_path: str = "output.wav",
                       speaker_wav: Optional[str] = None,
                       language: Optional[str] = None) -> str:
        """Gera fala a partir do texto"""
        if not self.current_model:
            raise Exception("Nenhum modelo carregado")
        
        try:
            # Configura os parâmetros para síntese
            kwargs = {
                "text": text,
                "file_path": output_path,
                "split_sentences": True
            }
            
            # Adiciona parâmetros específicos se necessário
            if speaker_wav and hasattr(self.current_model, "speakers"):
                kwargs["speaker_wav"] = speaker_wav
            
            if language and "multilingual" in str(self.current_model.model_name):
                kwargs["language"] = language
            
            # Gera o áudio
            self.logger.info(f"Gerando áudio com modelo: {self.current_model.model_name}")
            self.current_model.tts_to_file(**kwargs)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar fala: {e}", exc_info=True)
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
        if not self.current_model:
            return []
        if hasattr(self.current_model, "speakers"):
            return [str(s) for s in self.current_model.speakers]  # Garante que são strings
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