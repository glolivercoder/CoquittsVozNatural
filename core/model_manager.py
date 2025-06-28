import os
import json
import requests
import shutil
import torch
from typing import Dict, List, Optional
from TTS.api import TTS
from .logger import app_logger

class ModelManager:
    def __init__(self, models_dir="./models"):
        self.models_dir = models_dir
        self.ensure_models_dir()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        app_logger.info(f"ModelManager iniciado com diretório: {models_dir} e device: {self.device}")
        
        # Configuração dos modelos predefinidos
        self.predefined_models = {
            "pt": {
                "vits": "tts_models/pt/cv/vits",
                "xtts": "tts_models/multilingual/multi-dataset/xtts_v2",
                "tacotron2": "tts_models/pt/cv/tacotron2"
            },
            "en": {
                "vits": "tts_models/en/ljspeech/vits",
                "xtts": "tts_models/multilingual/multi-dataset/xtts_v2",
                "tacotron2": "tts_models/en/ljspeech/tacotron2"
            },
            "es": {
                "vits": "tts_models/es/css10/vits",
                "xtts": "tts_models/multilingual/multi-dataset/xtts_v2",
                "tacotron2": "tts_models/es/css10/tacotron2"
            }
        }
        app_logger.debug(f"Modelos predefinidos carregados: {len(self.predefined_models)} idiomas")
    
    def ensure_models_dir(self):
        """Garante que o diretório de modelos existe"""
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
            app_logger.info(f"Diretório de modelos criado: {self.models_dir}")
    
    def get_installed_models(self) -> List[Dict]:
        """Retorna lista de modelos instalados com metadados"""
        installed = []
        for language in self.predefined_models:
            for model_name, model_path in self.predefined_models[language].items():
                model_info = {
                    "name": model_name,
                    "language": language,
                    "path": model_path,
                    "installed": self.is_model_installed(model_path)
                }
                installed.append(model_info)
        return installed
    
    def load_model(self, model_name: str) -> Optional[TTS]:
        """Carrega um modelo TTS"""
        try:
            app_logger.info(f"Tentando carregar modelo: {model_name}")
            
            # Configurações específicas para cada tipo de modelo
            if "xtts" in model_name.lower():
                model = TTS(model_name=model_name, progress_bar=True, gpu=torch.cuda.is_available())
            else:
                model = TTS(model_name=model_name)
            
            app_logger.info(f"Modelo {model_name} carregado com sucesso")
            return model
            
        except Exception as e:
            app_logger.error(f"Erro ao carregar modelo {model_name}: {str(e)}")
            return None
    
    def get_available_models(self) -> List[str]:
        """Retorna lista de modelos disponíveis"""
        try:
            app_logger.debug("Obtendo lista de modelos disponíveis")
            available_models = []
            
            # Mapeia sufixos de idioma
            language_suffixes = {
                "pt": " (Português BR)",
                "en": " (Inglês)",
                "es": " (Espanhol)"
            }
            
            # Lista modelos por idioma
            for language, models in self.predefined_models.items():
                suffix = language_suffixes.get(language, "")
                for model_type in models:
                    model_path = self.get_model_path(model_type, language)
                    if self.is_model_installed(model_path):
                        model_name = f"{model_type.upper()}{suffix}"
                        available_models.append(model_name)
                        app_logger.debug(f"Modelo encontrado: {model_name}")
            
            if not available_models:
                app_logger.warning("Nenhum modelo encontrado")
                return ["Nenhum modelo encontrado"]
                
            return sorted(available_models)
            
        except Exception as e:
            app_logger.error(f"Erro ao listar modelos: {e}", exc_info=True)
            return ["Erro ao carregar modelos"]
    
    def is_model_installed(self, model_name: str) -> bool:
        """Verifica se um modelo está instalado"""
        try:
            # Tenta carregar o modelo apenas para verificar se está instalado
            TTS(model_name=model_name)
            return True
        except Exception as e:
            app_logger.debug(f"Modelo {model_name} não está instalado: {str(e)}")
            return False
    
    def download_model(self, model_name: str) -> bool:
        """Baixa um modelo TTS"""
        try:
            app_logger.info(f"Iniciando download do modelo: {model_name}")
            TTS(model_name=model_name, progress_bar=True)
            app_logger.info(f"Modelo {model_name} baixado com sucesso")
            return True
        except Exception as e:
            app_logger.error(f"Erro ao baixar modelo {model_name}: {str(e)}")
            return False
    
    def remove_model(self, model_path: str) -> bool:
        """Remove um modelo específico"""
        try:
            app_logger.info(f"Removendo modelo: {model_path}")
            
            # Para modelos do Coqui TTS, eles são armazenados no cache local
            # Vamos tentar encontrar e remover o diretório do modelo
            import platform
            import shutil
            
            if platform.system() == "Windows":
                cache_dir = os.path.expanduser("~\\AppData\\Local\\tts")
            else:
                cache_dir = os.path.expanduser("~/.local/share/tts")
            
            # Converte o nome do modelo para o formato de diretório
            model_dir_name = model_path.replace("/", "--")
            model_dir = os.path.join(cache_dir, model_dir_name)
            
            app_logger.debug(f"Procurando modelo em: {model_dir}")
            
            if os.path.exists(model_dir):
                shutil.rmtree(model_dir)
                app_logger.info(f"Modelo {model_path} removido do diretório: {model_dir}")
                return True
            else:
                app_logger.warning(f"Diretório do modelo não encontrado: {model_dir}")
                return False
                
        except Exception as e:
            app_logger.error(f"Erro ao remover modelo {model_path}: {str(e)}", exc_info=True)
            return False
    
    def get_model_info(self, model_path: str) -> Optional[Dict]:
        """
        Obtém informações detalhadas sobre um modelo
        
        Args:
            model_path: Caminho do modelo
            
        Returns:
            Dict com informações do modelo ou None se não encontrado
        """
        try:
            tts = TTS(model_name=model_path)
            info = {
                "path": model_path,
                "languages": tts.languages,
                "speakers": tts.speakers if hasattr(tts, "speakers") else None,
                "is_multi_speaker": hasattr(tts, "speakers"),
                "is_multi_lingual": len(tts.languages) > 1 if hasattr(tts, "languages") else False
            }
            return info
        except:
            return None
    
    def get_predefined_models(self) -> Dict:
        """Retorna modelos pré-definidos"""
        return self.predefined_models
    
    def validate_model(self, model_path: str) -> bool:
        """Valida se um modelo é válido"""
        full_path = os.path.join(self.models_dir, model_path)
        return os.path.exists(full_path) and os.path.getsize(full_path) > 0

    def list_models(self) -> List[Dict]:
        """
        Lista todos os modelos disponíveis com seu status de instalação.
        
        Returns:
            List[Dict]: Lista de dicionários com informações dos modelos
        """
        app_logger.debug("Iniciando listagem de modelos")
        models = []
        
        try:
            for language, language_models in self.predefined_models.items():
                for name, model_path in language_models.items():
                    try:
                        is_installed = self.is_model_installed(model_path)
                        model_info = {
                            "name": name,
                            "path": model_path,
                            "language": language,
                            "installed": is_installed
                        }
                        models.append(model_info)
                        app_logger.debug(f"Modelo {name} ({language}): {'instalado' if is_installed else 'não instalado'}")
                    except Exception as e:
                        app_logger.error(f"Erro ao verificar modelo {name}: {str(e)}", exc_info=True)
        except Exception as e:
            app_logger.error("Erro ao listar modelos", exc_info=True)
            return []
            
        app_logger.info(f"Total de modelos listados: {len(models)}")
        return models 

    def get_model_path(self, model_name: str, language: str = "pt") -> str:
        """
        Obtém o caminho completo do modelo
        
        Args:
            model_name: Nome do modelo (ex: 'vits', 'xtts')
            language: Código do idioma (ex: 'pt', 'en', 'es')
            
        Returns:
            str: Caminho completo do modelo
        """
        try:
            # Se já é um caminho completo, retorna como está
            if "/" in model_name:
                return model_name
            
            # Remove sufixos de idioma se presentes
            model_base = model_name.lower()
            for suffix in [" (português br)", " (inglês)", " (espanhol)"]:
                model_base = model_base.replace(suffix.lower(), "")
            
            # Obtém o caminho do modelo predefinido
            if language in self.predefined_models and model_base in self.predefined_models[language]:
                return self.predefined_models[language][model_base]
            
            # Se não encontrou, tenta criar um caminho padrão
            dataset = "cv" if language == "pt" else "ljspeech" if language == "en" else "css10"
            return f"tts_models/{language}/{dataset}/{model_base}"
        
        except Exception as e:
            app_logger.error(f"Erro ao obter caminho do modelo: {e}", exc_info=True)
            return model_name  # Retorna o nome original em caso de erro 