from TTS.api import TTS
import torch
import os

def test_xtts():
    """
    Testa o modelo XTTS v2 com uma frase em português
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")
    
    try:
        # Inicializa o modelo XTTS v2 localmente
        model_path = os.path.join("xtts_v2", "model.pth")
        config_path = os.path.join("xtts_v2", "config.json")
        
        tts = TTS(model_path=model_path, config_path=config_path, progress_bar=True)
        
        # Gera um áudio de teste
        text = "Olá, este é um teste do modelo XTTS v2 em português."
        output_path = "test_output.wav"
        
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            language="pt",
            speaker_wav=None  # Por enquanto sem clonagem de voz
        )
        
        print(f"Áudio gerado com sucesso em: {output_path}")
        
    except Exception as e:
        print(f"Erro ao testar XTTS v2: {str(e)}")

if __name__ == "__main__":
    test_xtts() 