from TTS.api import TTS
import torch

def main():
    try:
        # Verifica se a GPU está disponível
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Usando dispositivo: {device}")
        
        # Tenta carregar o modelo VITS em português
        model_name = "tts_models/pt/cv/vits"
        print(f"Tentando carregar modelo: {model_name}")
        
        tts = TTS(model_name=model_name)
        print("Modelo carregado com sucesso!")
        
        # Tenta sintetizar um texto
        text = "Olá, este é um teste de síntese de voz."
        print(f"Sintetizando texto: {text}")
        
        tts.tts_to_file(text=text, file_path="test_output.wav")
        print("Áudio gerado com sucesso!")
        
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main() 