import os
import subprocess
import torch

# Fix para problema de compatibilidade do BeamSearchScorer com transformers
# Aplica o patch ANTES de importar qualquer módulo do TTS
import sys
import importlib

def patch_transformers():
    """Aplica patch para BeamSearchScorer antes do TTS ser importado"""
    import transformers
    
    # Tenta diferentes locais onde BeamSearchScorer pode estar
    if not hasattr(transformers, 'BeamSearchScorer'):
        try:
            from transformers.generation import BeamSearchScorer
            transformers.BeamSearchScorer = BeamSearchScorer
            setattr(transformers, 'BeamSearchScorer', BeamSearchScorer)
        except ImportError:
            try:
                from transformers.generation.beam_search import BeamSearchScorer
                transformers.BeamSearchScorer = BeamSearchScorer
                setattr(transformers, 'BeamSearchScorer', BeamSearchScorer)
            except ImportError:
                # Cria stub se necessário (XTTS pode não usar diretamente)
                class BeamSearchScorer:
                    def __init__(self, *args, **kwargs):
                        pass
                transformers.BeamSearchScorer = BeamSearchScorer
                setattr(transformers, 'BeamSearchScorer', BeamSearchScorer)
    
    # Também adiciona ao __all__ se existir
    if hasattr(transformers, '__all__'):
        if 'BeamSearchScorer' not in transformers.__all__:
            transformers.__all__.append('BeamSearchScorer')

# Aplica o patch imediatamente
patch_transformers()

from faster_whisper import WhisperModel
from TTS.api import TTS

# Configurações
INPUT_FILE = "input.mp4"
OUTPUT_FILE = "audio_english.mp3"
TEMP_AUDIO_FILE = "temp_audio.wav"
MODEL_SIZE = "medium" # Use 'large-v3' para melhor qualidade (mais pesado)

# Verifica dispositivo (GPU vs CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

print(f"🚀 Iniciando processamento usando: {device.upper()}")

def extract_audio_from_mp4(input_mp4, output_wav):
    """Extrai áudio de um arquivo MP4 usando ffmpeg"""
    print(f"\n🎬 [0/3] Extraindo áudio do arquivo MP4...")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_mp4,
                "-vn",  # Remove vídeo
                "-acodec", "pcm_s16le",  # Codec PCM 16-bit
                "-ar", "22050",  # Sample rate
                "-ac", "1",  # Mono
                "-y",  # Sobrescrever arquivo se existir
                output_wav
            ],
            check=True,
            capture_output=True
        )
        print(f"✅ Áudio extraído: {output_wav}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao extrair áudio: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("❌ Erro: ffmpeg não encontrado. Instale o ffmpeg e adicione ao PATH.")
        return False

def convert_wav_to_mp3(input_wav, output_mp3):
    """Converte arquivo WAV para MP3 usando ffmpeg"""
    print(f"\n🔄 [3/3] Convertendo áudio para MP3...")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_wav,
                "-codec:a", "libmp3lame",
                "-qscale:a", "2",  # Qualidade alta (0-9, menor é melhor)
                "-y",
                output_mp3
            ],
            check=True,
            capture_output=True
        )
        print(f"✅ Conversão para MP3 concluída: {output_mp3}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao converter para MP3: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("❌ Erro: ffmpeg não encontrado. Instale o ffmpeg e adicione ao PATH.")
        return False

def pipeline():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erro: Arquivo '{INPUT_FILE}' não encontrado. Coloque um arquivo MP4 na pasta.")
        return

    # --- PASSO 0: Extrair áudio do MP4 ---
    if not extract_audio_from_mp4(INPUT_FILE, TEMP_AUDIO_FILE):
        return

    # --- PASSO 1: Whisper (Audio PT -> Texto EN) ---
    print("\n🎧 [1/3] Ouvindo e Traduzindo com Whisper...")
    
    # Carrega o modelo
    model = WhisperModel(MODEL_SIZE, device=device, compute_type=compute_type)
    
    # Task="translate" força a saída em Inglês
    segments, info = model.transcribe(TEMP_AUDIO_FILE, task="translate")
    
    translated_text = ""
    for segment in segments:
        translated_text += segment.text + " "
        print(f"   -> Segmento: {segment.text}")
    
    print(f"\n📝 Texto Traduzido: {translated_text}")

    # --- PASSO 2: TTS (Texto EN -> Audio EN com Clone) ---
    print("\n🗣️ [2/3] Gerando Áudio em Inglês (Clonando voz)...")
    
    # Arquivo temporário para o TTS (WAV)
    temp_output_wav = "temp_output.wav"
    
    # Inicializa Coqui TTS com modelo XTTS v2 (Melhor qualidade atual)
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    tts.tts_to_file(
        text=translated_text,
        file_path=temp_output_wav,
        speaker_wav=TEMP_AUDIO_FILE,  # Usa o áudio extraído para clonar o timbre
        language="en"
    )
    
    # --- PASSO 3: Converter WAV para MP3 ---
    if not convert_wav_to_mp3(temp_output_wav, OUTPUT_FILE):
        return
    
    # Limpar arquivos temporários
    try:
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)
        if os.path.exists(temp_output_wav):
            os.remove(temp_output_wav)
        print("\n🧹 Arquivos temporários removidos.")
    except Exception as e:
        print(f"\n⚠️ Aviso: Não foi possível remover arquivos temporários: {e}")
    
    print(f"\n✅ Concluído! Arquivo salvo como: {OUTPUT_FILE}")

if __name__ == "__main__":
    pipeline()