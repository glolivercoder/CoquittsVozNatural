# Guia de Treinamento de Áudio para Coqui TTS

## Modelos Pré-treinados em Português
Existe um modelo pré-treinado em português brasileiro desenvolvido por Edresson Casanova, disponível no [TTS-Portuguese-Corpus](https://github.com/Edresson/TTS-Portuguese-Corpus). Este modelo pode ser usado como base para transfer learning, o que pode melhorar significativamente os resultados e reduzir o tempo de treinamento.

## Estrutura do Dataset
Você pode usar **vários arquivos de áudio separados** que somem 1 hora no total. Não é necessário que seja um áudio contínuo, desde que cada arquivo individual:
- Tenha boa qualidade de gravação
- Contenha fala clara e consistente
- Esteja devidamente transcrito

## Textos para Gravação
Abaixo estão textos estruturados para criar seu dataset de treinamento. Grave cada seção separadamente:

### 1. Frases Cotidianas (15 minutos)
```
Bom dia! Como você está hoje?
Preciso marcar uma reunião para amanhã.
Que horas são? Já está ficando tarde.
O tempo está muito agradável hoje.
Vou ao mercado fazer algumas compras.
Você poderia me ajudar com isso?
Preciso terminar este relatório até amanhã.
Vamos almoçar juntos hoje?
O trânsito está muito intenso nesta manhã.
Por favor, você pode repetir o que disse?
```

### 2. Textos Informativos (15 minutos)
```
O Brasil é o maior país da América do Sul.
A Amazônia é considerada o pulmão do mundo.
São Paulo é a maior cidade do hemisfério sul.
O Rio de Janeiro é famoso por suas praias e montanhas.
A capital do Brasil é Brasília, inaugurada em 1960.
O Pantanal é a maior planície alagada do mundo.
O café é um dos principais produtos de exportação brasileiros.
A língua portuguesa é falada por mais de 250 milhões de pessoas.
O carnaval brasileiro é a maior festa popular do planeta.
O Sistema Único de Saúde atende toda a população brasileira.
```

### 3. Expressões Emocionais (10 minutos)
```
Que alegria ver você aqui!
Sinto muito pelo que aconteceu.
Isso é realmente incrível!
Não acredito que conseguimos!
Que tristeza essa notícia.
Estou muito orgulhoso de você!
Que surpresa maravilhosa!
Isso me deixou muito preocupado.
Que emoção poder estar aqui!
Estou ansioso para o nosso encontro!
```

### 4. Números e Datas (10 minutos)
```
Hoje é dia vinte e três de março de dois mil e vinte e cinco.
O número de telefone é nove oito sete seis cinco quatro três dois.
São exatamente três horas e quarenta e cinco minutos.
O valor total é mil trezentos e vinte e cinco reais.
A temperatura está em vinte e dois graus celsius.
O CEP é zero cinco quatro três dois um zero zero.
O aniversário é no dia quinze de agosto.
São duas mil e quinhentas unidades.
O documento tem cinquenta e três páginas.
O prazo termina em trinta dias.
```

### 5. Perguntas e Respostas (10 minutos)
```
Qual é o seu nome?
Onde você mora?
Como posso ajudar você?
Quando é o seu aniversário?
Por que você escolheu esta profissão?
Quanto tempo falta para o término?
Como foi seu dia hoje?
Qual é sua cor favorita?
O que você gosta de fazer nas horas livres?
Onde você pretende passar as férias?
```

## Requisitos Técnicos para Gravação

### Configuração de Áudio
- Formato: WAV
- Sample Rate: 22050 Hz
- Bits por amostra: 16-bit
- Canal: Mono
- Qualidade: Sem ruídos de fundo

### Ambiente de Gravação
1. **Local**:
   - Sala silenciosa
   - Sem eco
   - Sem ruídos externos
   - Temperatura controlada (evitar ventilador/ar condicionado)

2. **Equipamento**:
   - Microfone de qualidade (USB ou XLR)
   - Pop filter
   - Suporte para microfone
   - Fones de ouvido para monitoramento

### Dicas para Gravação
1. **Posicionamento**:
   - Mantenha distância constante do microfone (20-30cm)
   - Use pop filter para evitar plosivas
   - Mantenha postura consistente

2. **Voz**:
   - Fale em tom natural
   - Mantenha ritmo constante
   - Faça pausas adequadas
   - Articule bem as palavras
   - Mantenha volume consistente

3. **Processo**:
   - Grave cada seção separadamente
   - Faça pequenas pausas entre frases
   - Revise cada gravação
   - Regravar se necessário
   - Salvar cada arquivo separadamente

## Organização dos Arquivos
```
dataset/
  ├── cotidiano/
  │   ├── frase_001.wav
  │   ├── frase_002.wav
  │   └── ...
  ├── informativos/
  │   ├── info_001.wav
  │   ├── info_002.wav
  │   └── ...
  ├── emocoes/
  │   ├── emocao_001.wav
  │   ├── emocao_002.wav
  │   └── ...
  ├── numeros/
  │   ├── num_001.wav
  │   ├── num_002.wav
  │   └── ...
  └── perguntas/
      ├── perg_001.wav
      ├── perg_002.wav
      └── ...
```

## Validação do Dataset
1. Verifique cada arquivo de áudio:
   - Qualidade do som
   - Ausência de ruídos
   - Correta correspondência com o texto
   - Formato adequado

2. Prepare o arquivo de metadados:
   ```
   wavs/cotidiano/frase_001.wav|Bom dia! Como você está hoje?
   wavs/cotidiano/frase_002.wav|Preciso marcar uma reunião para amanhã.
   ...
   ```

3. Teste uma pequena amostra antes do treinamento completo 