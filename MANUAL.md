# Manual do Coqui TTS - Treinamento e Uso

## Índice
1. [Treinamento de Voz Personalizada](#treinamento-de-voz-personalizada)
2. [Usando o TTS no WhatsApp com IA](#usando-o-tts-no-whatsapp-com-ia)

## Treinamento de Voz Personalizada

### Preparação do Ambiente
1. Abra a interface do Coqui TTS
2. Navegue até a aba "Treinamento"

### Preparando seu Dataset
1. **Gravação de Áudio**
   - Grave entre 30 minutos a 1 hora de áudio da voz desejada
   - Use um microfone de boa qualidade
   - Grave em ambiente silencioso
   - Mantenha uma distância consistente do microfone
   - Fale de forma clara e natural

2. **Requisitos dos Arquivos**
   - Formato: WAV
   - Sample Rate: 22050 Hz
   - Bits por amostra: 16-bit
   - Canal: Mono

### Processo de Treinamento
1. **Configuração Inicial**
   - Selecione "Novo Treinamento" na aba Treinamento
   - Escolha o modelo base (recomendado: XTTS v2 para melhor qualidade)
   - Defina um nome para seu modelo

2. **Carregamento do Dataset**
   - Clique em "Carregar Dataset"
   - Selecione a pasta com seus arquivos de áudio
   - Aguarde o processamento inicial

3. **Parâmetros de Treinamento**
   - Epochs: 1000 (recomendado)
   - Batch Size: 32
   - Learning Rate: 0.0001
   - Validação: a cada 1000 steps

4. **Iniciando o Treinamento**
   - Clique em "Iniciar Treinamento"
   - Monitore o progresso na aba de logs
   - O treinamento pode levar várias horas dependendo do seu hardware

### Dicas Importantes
- Use GPU para treinamento mais rápido
- Mantenha o computador conectado à energia
- Faça backups regulares do modelo
- Teste o modelo periodicamente durante o treinamento

## Usando o TTS no WhatsApp com IA

### Configuração no Sistema WhatsApp
1. **Localização do Modelo**
   - Copie seu modelo treinado para a pasta `G:/Projetos2025BKP/WhatsappAirflow/modulo-audio-weaviate-new/models`

2. **Configuração do TTS**
   ```python
   from TTS.api import TTS
   
   tts = TTS(model_path="./models/seu_modelo.pth",
             config_path="./models/config.json",
             use_cuda=True)
   ```

3. **Integração com Agentes IA**
   - O sistema já possui integração com agentes IA
   - O TTS será chamado automaticamente após a resposta do agente
   - Os áudios serão gerados em tempo real

### Uso Prático
1. **Geração de Áudio**
   - As respostas dos agentes são convertidas automaticamente
   - O áudio é enviado diretamente no WhatsApp
   - Tempo médio de geração: 2-3 segundos por mensagem

2. **Ajustes de Voz**
   - Velocidade de fala ajustável
   - Entonação natural preservada
   - Suporte a múltiplos idiomas

### Recomendações
- Mantenha o modelo atualizado
- Monitore o uso de recursos do sistema
- Faça testes periódicos de qualidade
- Mantenha backups dos modelos treinados

### Solução de Problemas
1. **Áudio não gerado:**
   - Verifique se o modelo está no caminho correto
   - Confirme se há espaço em disco suficiente
   - Verifique logs de erro

2. **Qualidade baixa:**
   - Ajuste os parâmetros de geração
   - Verifique se está usando GPU
   - Considere retreinar o modelo

3. **Lentidão:**
   - Otimize o cache do sistema
   - Use GPU quando possível
   - Ajuste o tamanho do batch

## Suporte
Para problemas ou dúvidas adicionais, consulte:
- Documentação oficial do Coqui TTS
- Fórum da comunidade
- Issues no GitHub do projeto 