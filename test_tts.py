from TTS.api import TTS
import torch
import os
import argparse

def initialize_tts(model_name="tts_models/multilingual/multi-dataset/your_tts"):
    """
    Inicializa o modelo TTS e retorna a instância
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")
    return TTS(model_name=model_name).to(device)

def list_capabilities(tts):
    """
    Lista as capacidades do modelo (speakers e idiomas disponíveis)
    """
    print("\nSpeakers disponíveis:")
    print(tts.speakers)
    
    print("\nIdiomas disponíveis:")
    print(tts.languages)

def generate_speech(tts, text, output_path, language="pt-br", speaker_wav=None, speed=1.0):
    """
    Gera áudio a partir do texto usando o modelo TTS
    
    Args:
        tts: Instância do modelo TTS
        text: Texto para converter em fala
        output_path: Caminho para salvar o arquivo de áudio
        language: Código do idioma (default: pt-br)
        speaker_wav: Caminho para o arquivo de voz de referência
        speed: Velocidade da fala (default: 1.0)
    """
    try:
        # Cria o diretório de saída se não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Configura os parâmetros para a geração do áudio
        kwargs = {
            "text": text,
            "file_path": output_path,
            "language": language,
            "speed": speed
        }
        
        # Adiciona speaker_wav se fornecido
        if speaker_wav:
            kwargs["speaker_wav"] = speaker_wav
            
        # Gera o áudio
        tts.tts_to_file(**kwargs)
        print(f"Áudio gerado com sucesso em: {output_path}")
        
    except Exception as e:
        print(f"Erro ao gerar áudio: {str(e)}")
        raise

def process_batch(tts, texts, output_dir, language="pt-br", speaker_wav=None, speed=1.0):
    """
    Processa múltiplos textos em batch
    """
    for i, text in enumerate(texts):
        output_path = os.path.join(output_dir, f"output_{i+1}.wav")
        generate_speech(tts, text, output_path, language, speaker_wav, speed)

def main():
    parser = argparse.ArgumentParser(description="Gerador de voz usando YourTTS")
    parser.add_argument("--text", type=str, help="Texto para converter em fala")
    parser.add_argument("--output", type=str, default="outputs/output.wav", help="Caminho do arquivo de saída")
    parser.add_argument("--language", type=str, default="pt-br", help="Código do idioma")
    parser.add_argument("--speaker_wav", type=str, default="xtts_v2/samples/pt_sample.wav", help="Arquivo de voz de referência")
    parser.add_argument("--speed", type=float, default=1.0, help="Velocidade da fala")
    parser.add_argument("--batch_file", type=str, help="Arquivo com múltiplos textos (um por linha)")
    
    args = parser.parse_args()
    
    try:
        # Inicializa o modelo
        tts = initialize_tts()
        list_capabilities(tts)
        
        if args.batch_file:
            # Processa múltiplos textos de um arquivo
            with open(args.batch_file, 'r', encoding='utf-8') as f:
                texts = f.read().splitlines()
            output_dir = os.path.dirname(args.output)
            process_batch(tts, texts, output_dir, args.language, args.speaker_wav, args.speed)
        else:
            # Processa um único texto
            if not args.text:
                args.text = "Olá, este é um teste do modelo YourTTS em português."
            generate_speech(tts, args.text, args.output, args.language, args.speaker_wav, args.speed)
            
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    main() 