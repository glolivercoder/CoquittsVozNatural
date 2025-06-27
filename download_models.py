from TTS.api import TTS
import os

def download_models():
    # Diretório para salvar os modelos
    models_dir = "models/pt_BR"
    os.makedirs(models_dir, exist_ok=True)

    # 1. XTTS v2 - Melhor modelo multilíngue atual
    print("Baixando XTTS v2...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    tts.tts_to_file(
        text="Olá, isso é um teste de voz em português brasileiro.",
        file_path="samples/teste_xtts_v2.wav",
        language="pt",
        speaker_wav="samples/reference_voice.wav"
    )

    # 2. YourTTS - Outro excelente modelo multilíngue
    print("Baixando YourTTS...")
    tts = TTS("tts_models/multilingual/multi-dataset/your_tts")
    tts.tts_to_file(
        text="Este é um teste do modelo YourTTS em português.",
        file_path="samples/teste_your_tts.wav",
        language="pt-br",
        speaker_wav="samples/reference_voice.wav"
    )

    print("Download concluído! Os modelos foram salvos em:", models_dir)
    print("Arquivos de teste foram gerados em: samples/")

if __name__ == "__main__":
    download_models() 