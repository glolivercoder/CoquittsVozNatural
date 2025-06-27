from TTS.api import TTS
import torch
import os

def download_models():
    """
    Baixa os modelos necessários para síntese de voz em português
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")
    
    # Lista todos os modelos disponíveis
    print("\nModelos disponíveis:")
    tts = TTS()
    models = tts.list_models()
    print(models)
    
    # Baixa o modelo XTTS v2
    print("\nBaixando XTTS v2...")
    try:
        os.environ["COQUI_TOS_AGREED"] = "1"  # Aceita os termos de serviço
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("XTTS v2 baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar XTTS v2: {str(e)}")
    
    # Baixa o modelo YourTTS
    print("\nBaixando YourTTS...")
    try:
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts").to(device)
        print("YourTTS baixado com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar YourTTS: {str(e)}")

if __name__ == "__main__":
    download_models() 