from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voices
import torch
import torchaudio
import os
from datetime import datetime
import re

# Skapa output-mapp om den inte finns
output_dir = "generated_audio"
os.makedirs(output_dir, exist_ok=True)

# Optimera för RTX 4090
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Initiera TTS med GPU-stöd och optimeringar
tts = TextToSpeech(
    device='cuda',
    half=True,  # Använd FP16 för snabbare beräkning
    kv_cache=True  # Aktivera kv_cache för snabbare generering
)

# Lista med meningar att generera
sentences = [
    "Together, we will make Bastjanster strong again.",
    "We will make Bastjanster wealthy again.",
    "We will make Bastjanster proud again.",
    "God bless Bastjanster."
]

voice_name = "trump"
# Ladda rösten
voice_samples, conditioning_latents = load_voices([voice_name])

# Lista för att lagra filnamn
wav_files = []

# Generera tal för varje mening
for i, text in enumerate(sentences):
    print(f"\nGenererar tal för mening {i+1}...")
    wav = tts.tts_with_preset(
        text,
        voice_samples=voice_samples,
        conditioning_latents=conditioning_latents,
        preset='ultra_fast',
        num_autoregressive_samples=16,
        diffusion_iterations=40,  # Öka för bättre kvalitet
        temperature=0.7,  # Sänk för mer konsekvent uttal
        length_penalty=1.0,
        repetition_penalty=2.0,
        top_p=0.8,
        max_mel_tokens=100,
        cond_free=True,
        cond_free_k=2.0,
        diffusion_temperature=0.8,  # Sänk för mindre brus
        cvvp_amount=0.0,
        k=1
    )

    # Skapa filnamn med datum, text och röst
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Ta bort ogiltiga tecken från texten för filnamnet
    safe_text = re.sub(r'[<>:"/\\|?*]', '', text)[:50]  # Begränsa längden och ta bort ogiltiga tecken
    filename = f"{timestamp}_{voice_name}_{i+1}_{safe_text}.wav"
    output_path = os.path.join(output_dir, filename)

    # Spara resultatet
    print(f"\nSparar ljudfil som: {filename}")
    torchaudio.save(output_path, wav.squeeze(0).cpu(), 24000)
    wav_files.append(output_path)

# Kombinera alla ljudfiler
print("\nKombinerar alla ljudfiler...")
combined_wav = None
sample_rate = None

for wav_file in wav_files:
    wav, sr = torchaudio.load(wav_file)
    if combined_wav is None:
        combined_wav = wav
        sample_rate = sr
    else:
        # Lägg till en kort paus mellan meningarna (0.05 sekunder)
        silence = torch.zeros((1, int(sr * 0.05)))  # 0.05 sekunder av tystnad
        combined_wav = torch.cat([combined_wav, silence, wav], dim=1)
    # Ta bort delfilen direkt efter att den har kombinerats
    os.remove(wav_file)
    print(f"Raderade: {os.path.basename(wav_file)}")

# Spara den kombinerade ljudfilen
combined_filename = f"{timestamp}_{voice_name}_combined_full_speech.wav"
combined_output_path = os.path.join(output_dir, combined_filename)
torchaudio.save(combined_output_path, combined_wav, sample_rate)
print(f"\nSparar kombinerad ljudfil som: {combined_filename}")

print("\nMax längd per fil är 30 sekunder (600 mel tokens)")
print("Totalt antal tecken per fil bör inte överstiga cirka 100-150 tecken för bästa resultat") 