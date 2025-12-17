# 🎙️ WhisperTranslator

Sistema automatizado de tradução de áudio que converte vídeos MP4 em português para áudio MP3 em inglês, preservando a voz original através de clonagem de voz.

## 📋 Descrição

O WhisperTranslator utiliza inteligência artificial para:
1. **Extrair áudio** de arquivos MP4
2. **Transcrever e traduzir** o áudio de português para inglês usando Whisper
3. **Gerar áudio em inglês** com voz clonada usando Coqui TTS (XTTS v2)

O resultado é um arquivo MP3 em inglês que mantém as características da voz original.

## ✨ Funcionalidades

- 🎬 Extração automática de áudio de arquivos MP4
- 🌐 Tradução automática de português para inglês
- 🗣️ Clonagem de voz usando XTTS v2
- 🎵 Conversão para formato MP3
- 🚀 Suporte para GPU (CUDA) e CPU
- 🐳 Execução via Docker ou ambiente local

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **faster-whisper** - Modelo Whisper otimizado para transcrição e tradução
- **Coqui TTS** - Sistema de síntese de voz com clonagem (XTTS v2)
- **PyTorch** - Framework de deep learning
- **FFmpeg** - Processamento de áudio/vídeo

## 📦 Requisitos

### Para execução local (Windows):

- Python 3.10 ou superior
- FFmpeg instalado e no PATH do sistema
- 5-10 GB de espaço em disco (para modelos)
- (Opcional) NVIDIA GPU com CUDA para aceleração

### Para execução com Docker:

- Docker Desktop instalado
- Docker Compose instalado
- (Opcional) NVIDIA Docker Toolkit para suporte a GPU

## 🚀 Instalação

### Opção 1: Execução Local (Windows)

#### 1. Instalar Python
Baixe e instale Python 3.10+ de [python.org](https://www.python.org/downloads/)
- ⚠️ **Importante**: Marque a opção "Add Python to PATH" durante a instalação

#### 2. Instalar FFmpeg

**Via Chocolatey (recomendado):**
```powershell
choco install ffmpeg
```

**Ou manualmente:**
- Baixe de [ffmpeg.org](https://ffmpeg.org/download.html)
- Extraia e adicione ao PATH do sistema
- Verifique: `ffmpeg -version`

#### 3. Criar ambiente virtual
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se aparecer erro de política de execução:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Instalar dependências
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Configurar variável de ambiente
```powershell
$env:COQUI_TOS_AGREED=1
```

Ou configure permanentemente:
- Painel de Controle → Sistema → Variáveis de Ambiente
- Adicione `COQUI_TOS_AGREED` = `1`

### Opção 2: Execução com Docker

#### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd WhisperTranslator
```

#### 2. Construir e executar com Docker Compose
```bash
docker-compose build
docker-compose up
```

#### 3. (Opcional) Habilitar suporte a GPU
Descomente as linhas 19-24 no arquivo `docker-compose.yml` se tiver NVIDIA GPU.

## 📖 Como Usar

### Execução Local

1. Coloque um arquivo `input.mp4` na pasta do projeto
2. Execute o script:
   ```powershell
   python app.py
   ```
3. Aguarde o processamento (pode levar alguns minutos na primeira execução)
4. O arquivo `audio_english.mp3` será gerado na pasta do projeto

### Execução com Docker

1. Coloque um arquivo `input.mp4` na pasta do projeto
2. Execute:
   ```bash
   docker-compose up
   ```
3. O arquivo `audio_english.mp3` será gerado na pasta do projeto

## 📁 Estrutura do Projeto

```
WhisperTranslator/
│
├── app.py                 # Script principal
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── docker-compose.yml    # Orquestração Docker
├── Readme.md             # Este arquivo
│
├── input.mp4             # Arquivo de entrada (você precisa fornecer)
├── audio_english.mp3     # Arquivo de saída (gerado)
│
└── cache_*/              # Cache de modelos (criado automaticamente)
    ├── cache_huggingface/
    └── cache_tts/
```

## ⚙️ Configurações

Você pode ajustar as configurações no arquivo `app.py`:

```python
INPUT_FILE = "input.mp4"           # Nome do arquivo de entrada
OUTPUT_FILE = "audio_english.mp3"  # Nome do arquivo de saída
MODEL_SIZE = "medium"              # Tamanho do modelo Whisper
                                   # Opções: tiny, base, small, medium, large-v3
```

**Modelos Whisper disponíveis:**
- `tiny` - Mais rápido, menor qualidade
- `base` - Equilíbrio básico
- `small` - Boa qualidade
- `medium` - Alta qualidade (padrão)
- `large-v3` - Melhor qualidade (mais pesado e lento)

## 🔍 Processo de Processamento

O pipeline executa 3 etapas principais:

1. **🎬 Extração de Áudio** - Extrai áudio do MP4 usando FFmpeg
2. **🎧 Transcrição e Tradução** - Whisper transcreve e traduz para inglês
3. **🗣️ Síntese de Voz** - Coqui TTS gera áudio em inglês clonando a voz original
4. **🔄 Conversão** - Converte o resultado final para MP3

## ⚠️ Observações Importantes

- **Primeira execução**: Os modelos serão baixados automaticamente (pode levar vários minutos e ocupar ~5-10 GB)
- **Tempo de processamento**: Depende do tamanho do arquivo e do hardware (GPU é muito mais rápido)
- **Espaço em disco**: Reserve pelo menos 10 GB para modelos e cache
- **Qualidade**: Modelos maiores (`large-v3`) oferecem melhor qualidade mas são mais lentos

## 🐛 Troubleshooting

### Erro: "ffmpeg não encontrado"
- Certifique-se de que o FFmpeg está instalado e no PATH
- Verifique com: `ffmpeg -version`

### Erro: "COQUI_TOS_AGREED não definido"
- Configure a variável de ambiente: `$env:COQUI_TOS_AGREED=1`

### Erro ao baixar modelos
- Verifique sua conexão com a internet
- Os modelos são baixados do Hugging Face na primeira execução

### Processamento muito lento
- Considere usar GPU (CUDA) para acelerar
- Use modelos menores (`tiny`, `base`, `small`) para processamento mais rápido

### Erro de memória
- Use modelos menores (`tiny`, `base`, `small`)
- Feche outros aplicativos que consomem muita RAM

## 📝 Licença

Este projeto está disponível para uso pessoal e educacional.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Whisper e Coqui TTS**

