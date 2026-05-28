# AIDA

AIDA significa **Artificial Intelligence for Dialogue and Affection**. O projeto é uma API em Python criada para conversar de forma mais natural, guardar memórias importantes, manter continuidade entre mensagens e gerar áudio opcional com voz em português brasileiro.

## Objetivo do projeto

AIDA foi criada como uma assistente conversacional simples, mas evolutiva. A ideia principal é sair de respostas mecânicas e criar uma base com:

- respostas variadas por intenção;
- detecção emocional simples;
- memória seletiva por usuário;
- histórico recente de conversa;
- personalidade própria configurada;
- geração opcional de voz em MP3;
- API HTTP para integração com outras interfaces.

## Tecnologias utilizadas

O projeto utiliza as seguintes tecnologias e bibliotecas:

- **Python**: linguagem principal do projeto.
- **FastAPI**: framework usado para criar a API.
- **Uvicorn**: servidor ASGI usado para rodar a aplicação FastAPI.
- **Pydantic**: validação dos dados recebidos no corpo das requisições.
- **edge-tts**: geração de áudio com voz natural em português brasileiro.
- **JSON**: armazenamento simples de memória e histórico de conversas.

Também são utilizados módulos nativos do Python:

- `json`: leitura e gravação dos arquivos de dados.
- `pathlib`: manipulação de caminhos e pastas.
- `datetime`: registro do horário das mensagens.
- `uuid`: criação de nomes únicos para arquivos de áudio.
- `random.choice`: escolha aleatória de respostas variadas.
- `unicodedata`: normalização de texto para detectar intenções com ou sem acento.

## Estrutura do projeto

```text
AIDA/
├── main.py
├── requirements.txt
├── README.md
├── core/
│   ├── aida.py
│   ├── memory.py
│   ├── personality.py
│   ├── utils.py
│   └── voice.py
└── data/
    ├── conversations.json
    └── memory.json
```

## Função de cada arquivo

### `main.py`

Arquivo principal da API. Ele cria a aplicação FastAPI, registra as rotas e conecta as mensagens recebidas ao motor da AIDA.

Rotas principais:

- `GET /`: mostra uma apresentação básica da AIDA.
- `GET /health`: retorna o status e as capacidades atuais do projeto.
- `POST /chat`: recebe uma mensagem, gera uma resposta e opcionalmente cria áudio.
- `GET /audio/{filename}`: entrega arquivos MP3 gerados pela AIDA.

### `core/aida.py`

Contém o motor principal da assistente. É onde ficam:

- banco de respostas variadas;
- detecção de emoção;
- detecção de intenções;
- respostas opinativas;
- uso de memória e histórico;
- montagem da resposta final da AIDA.

Esse arquivo é o coração do comportamento conversacional.

### `core/memory.py`

Gerencia memória e histórico de conversa. Ele salva:

- fatos importantes do usuário;
- último assunto relevante;
- histórico recente das mensagens;
- mensagens da AIDA e do usuário.

A memória é seletiva: AIDA não guarda tudo, apenas mensagens que parecem úteis para conversas futuras.

### `core/personality.py`

Define a personalidade da AIDA, incluindo:

- nome;
- nome completo;
- estilo de conversa;
- missão;
- regras de comportamento;
- mensagem inicial.

Esse arquivo ajuda a manter o tom da assistente consistente.

### `core/utils.py`

Contém funções auxiliares para carregar e salvar arquivos JSON. Também garante que os arquivos e pastas necessários sejam criados quando ainda não existem.

### `core/voice.py`

Responsável por gerar áudio em MP3 usando `edge-tts`. A voz padrão configurada é:

```text
pt-BR-FranciscaNeural
```

Os arquivos de áudio são salvos na pasta:

```text
data/audio/
```

### `data/memory.json`

Arquivo onde ficam as memórias importantes salvas por usuário.

### `data/conversations.json`

Arquivo onde fica o histórico recente das conversas.

### `requirements.txt`

Lista as dependências necessárias para instalar e rodar o projeto:

```text
fastapi
uvicorn
pydantic
edge-tts
```

## Como rodar o projeto

Instale as dependências:

```bash
pip install -r requirements.txt
```

Rode a API com Uvicorn:

```bash
uvicorn main:app --reload
```

Depois acesse:

```text
http://127.0.0.1:8000
```

## Exemplo de uso do chat

Requisição para `POST /chat`:

```json
{
    "user_id": "default_user",
    "message": "quero deixar aida com mais opções de resposta",
    "voice_enabled": false
}
```

Resposta esperada:

```json
{
    "assistant": "AIDA",
    "user_id": "default_user",
    "response": "Boa. Para deixar a AIDA com mais opções de resposta, o caminho é criar intenções diferentes e várias frases por intenção, em vez de uma resposta fixa para tudo.",
    "message": "Boa. Para deixar a AIDA com mais opções de resposta, o caminho é criar intenções diferentes e várias frases por intenção, em vez de uma resposta fixa para tudo.",
    "emotion_detected": "neutro",
    "context_used": true
}
```

## Recursos atuais

- API com FastAPI.
- Conversa via endpoint `/chat`.
- Respostas variadas por tipo de intenção.
- Detecção simples de emoções.
- Memória seletiva salva em JSON.
- Histórico recente de conversa.
- Personalidade configurável.
- Geração opcional de voz.
- Arquivos comentados para facilitar estudo e manutenção.

## Possíveis melhorias futuras

- Integrar um modelo de IA externo, como OpenAI, Ollama ou Gemini.
- Criar uma interface web para conversar com a AIDA.
- Melhorar a extração automática de memórias.
- Adicionar autenticação por usuário.
- Criar testes automatizados.
- Separar configurações em variáveis de ambiente.
- Permitir escolha de voz pelo usuário.

