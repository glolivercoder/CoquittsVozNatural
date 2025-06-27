import os
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import torch
from TTS.config import load_config
from TTS.trainer import Trainer, TrainingArgs
from TTS.utils.audio import AudioProcessor

@dataclass
class TrainingConfig:
    model_name: str
    dataset_path: str
    output_path: str
    epochs: int
    batch_size: int
    learning_rate: float
    language: str = "pt-br"
    use_cuda: bool = True

class TrainingManager:
    def __init__(self, base_path: str = "./"):
        self.logger = logging.getLogger(__name__)
        self.base_path = base_path
        self.models_dir = os.path.join(base_path, "models")
        self.datasets_dir = os.path.join(base_path, "datasets")
        self.output_dir = os.path.join(base_path, "outputs")
        
        # Configurações padrão por modelo
        self.model_configs = {
            "VITS": {
                "config_path": "config/vits_config.json",
                "requires_phonemes": True,
                "supports_multi_speaker": True
            },
            "Tacotron2": {
                "config_path": "config/tacotron2_config.json",
                "requires_phonemes": True,
                "supports_multi_speaker": False
            },
            "FastSpeech2": {
                "config_path": "config/fastspeech2_config.json",
                "requires_phonemes": True,
                "supports_multi_speaker": True
            },
            "XTTS": {
                "config_path": "config/xtts_config.json",
                "requires_phonemes": True,
                "supports_multi_speaker": True
            }
        }
        
        self.ensure_directories()
    
    def ensure_directories(self):
        """Garante que os diretórios necessários existam"""
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.datasets_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def validate_dataset(self, dataset_path: str) -> Dict:
        """
        Valida um dataset para treinamento
        
        Args:
            dataset_path: Caminho para o dataset
            
        Returns:
            Dict com informações sobre o dataset
        """
        try:
            # Verificar estrutura do dataset
            if not os.path.exists(dataset_path):
                raise ValueError(f"Dataset não encontrado: {dataset_path}")
            
            metadata_path = os.path.join(dataset_path, "metadata.csv")
            if not os.path.exists(metadata_path):
                raise ValueError(f"Arquivo metadata.csv não encontrado em: {dataset_path}")
            
            wavs_dir = os.path.join(dataset_path, "wavs")
            if not os.path.exists(wavs_dir):
                raise ValueError(f"Diretório 'wavs' não encontrado em: {dataset_path}")
            
            # Analisar metadata
            import pandas as pd
            metadata = pd.read_csv(metadata_path, sep="|")
            
            # Verificar colunas necessárias
            required_columns = ["file_name", "text"]
            missing_columns = [col for col in required_columns if col not in metadata.columns]
            if missing_columns:
                raise ValueError(f"Colunas obrigatórias ausentes no metadata: {missing_columns}")
            
            # Verificar arquivos de áudio
            audio_files = metadata["file_name"].tolist()
            missing_files = []
            for audio_file in audio_files:
                if not os.path.exists(os.path.join(wavs_dir, audio_file)):
                    missing_files.append(audio_file)
            
            if missing_files:
                raise ValueError(f"Arquivos de áudio ausentes: {missing_files[:5]}...")
            
            # Analisar duração total e estatísticas
            total_files = len(audio_files)
            
            return {
                "status": "success",
                "total_files": total_files,
                "total_duration": "N/A",  # TODO: Implementar cálculo de duração
                "sample_rate": "N/A",  # TODO: Implementar detecção de sample rate
                "has_phonemes": "phonemes" in metadata.columns,
                "has_speaker_info": "speaker_name" in metadata.columns
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao validar dataset: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def prepare_training(self, config: TrainingConfig) -> bool:
        """
        Prepara ambiente para treinamento
        
        Args:
            config: Configurações de treinamento
            
        Returns:
            True se preparação foi bem sucedida
        """
        try:
            # Validar dataset
            dataset_info = self.validate_dataset(config.dataset_path)
            if dataset_info["status"] == "error":
                raise ValueError(f"Dataset inválido: {dataset_info['error']}")
            
            # Carregar configuração do modelo
            model_config = self.model_configs.get(config.model_name)
            if not model_config:
                raise ValueError(f"Modelo não suportado: {config.model_name}")
            
            # Verificar requisitos específicos do modelo
            if model_config["requires_phonemes"] and not dataset_info["has_phonemes"]:
                self.logger.warning("Dataset não possui informações de fonemas. Será feita conversão automática.")
            
            if model_config["supports_multi_speaker"] and not dataset_info["has_speaker_info"]:
                self.logger.warning("Dataset não possui informações de speaker. Treinamento será single-speaker.")
            
            # Verificar GPU
            if config.use_cuda and not torch.cuda.is_available():
                self.logger.warning("GPU não disponível. Usando CPU para treinamento.")
                config.use_cuda = False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao preparar treinamento: {e}")
            return False
    
    def start_training(self, config: TrainingConfig, progress_callback=None):
        """
        Inicia o treinamento de um modelo
        
        Args:
            config: Configurações de treinamento
            progress_callback: Função para reportar progresso
        """
        try:
            # Preparar treinamento
            if not self.prepare_training(config):
                raise ValueError("Falha ao preparar treinamento")
            
            # Carregar configuração do modelo
            model_config = load_config(self.model_configs[config.model_name]["config_path"])
            
            # Configurar argumentos de treinamento
            training_args = TrainingArgs(
                epochs=config.epochs,
                batch_size=config.batch_size,
                learning_rate=config.learning_rate,
                output_path=config.output_path,
                use_cuda=config.use_cuda
            )
            
            # Inicializar trainer
            trainer = Trainer(
                training_args,
                config=model_config,
                output_path=config.output_path,
                progress_bar=True
            )
            
            # Iniciar treinamento
            trainer.fit()
            
        except Exception as e:
            self.logger.error(f"Erro durante treinamento: {e}")
            raise
    
    def stop_training(self):
        """Para o treinamento atual"""
        # TODO: Implementar parada de treinamento
        pass
    
    def get_training_progress(self) -> Dict:
        """Retorna progresso do treinamento atual"""
        # TODO: Implementar monitoramento de progresso
        return {
            "epoch": 0,
            "loss": 0.0,
            "step": 0,
            "time_elapsed": 0
        }
    
    def export_model(self, output_path: str, format: str = "tflite"):
        """
        Exporta modelo treinado para formato específico
        
        Args:
            output_path: Caminho para salvar modelo
            format: Formato de exportação (tflite, onnx, etc)
        """
        # TODO: Implementar exportação de modelo
        pass 