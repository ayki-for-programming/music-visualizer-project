from audiocraft.models import MusicGen
import torchaudio
import os

# Load model ONCE (important for performance)
model = MusicGen.get_pretrained("small")


def generate_music(prompt):

    print(f"Generating music for: {prompt}")

    # control duration (8–12 sec keeps it fast)
    model.set_generation_params(duration=8)

    # AI generate audio
    wav = model.generate([prompt])[0].cpu()

    filename = "generated_music.wav"

    # save audio
    torchaudio.save(filename, wav, 32000)

    return filename