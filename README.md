# CoquittsVozNatural Models

Repositório de modelos e configurações para Coqui TTS em Português Brasileiro.

## Sobre
Este repositório contém modelos de voz treinados para síntese de fala em português brasileiro usando Coqui TTS. O objetivo é fornecer modelos pré-treinados de alta qualidade para uso em aplicações de texto para fala.

## Estrutura
```
CoquittsVozNatural/
├── models/         # Modelos treinados e pré-treinados
├── configs/        # Arquivos de configuração
├── samples/        # Amostras de áudio
└── docs/          # Documentação
```

## Modelos Disponíveis
- XTTS v2 (Português)
  - Suporte nativo ao português brasileiro
  - Alta qualidade de síntese
  - Clonagem de voz com apenas 6 segundos de áudio

## Como Usar
1. Clone o repositório
```bash
git clone https://github.com/glolivercoder/CoquittsVozNatural.git
cd CoquittsVozNatural
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Baixe os modelos
Os modelos serão disponibilizados na pasta `models/` após o treinamento.

## Requisitos do Sistema
- Python 3.8+
- CUDA (opcional, mas recomendado para treinamento)
- 8GB RAM (mínimo)
- CPU multi-core (recomendado)

## Licença
MIT
