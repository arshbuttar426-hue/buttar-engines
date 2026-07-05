"""
Cinema → Diffusion: S02 frame optimized for CLIP's 77-token limit
All department specs (camera, lighting, spatial, character, environment)
must fit within 77 tokens. Priorities: character > lighting > spatial > camera.
"""

import subprocess, torch, numpy as np, json
from pathlib import Path
from diffusers import AutoPipelineForText2Image

OUT = Path.home() / "Desktop" / "cinema_output"
OUT.mkdir(exist_ok=True)

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float32, use_safetensors=True, safety_checker=None
).to("mps")
pipe.enable_attention_slicing()

# After lighting and environment testing, use the best one as base
# Current best: seed 301 (warmest shift, highest constrast)
# We try seeds around it with the optimized prompt

# The CLIP limit is 77 tokens. Each ~6 words = 1 token for CLIP.
# We've compressed to ~135-145 chars max for the prompt.
prompts = [
    # Seed 301 extension: nearby seeds for coverage
    # frame 0: Chiku curled in corner (initial position)
    "3D animated cartoon style chihuahua dog curled in corner blue shutter wall wearing red scarf torn black suit tired melancholic "
    "warm golden sunset light from right long shadows cool blue sky dusk moody lonely empty pavement streetlamp flickering",
    
    # frame 1: Chiku sitting on step (final position) - slightly different framing
    "3D animated cartoon style chihuahua small dog sitting on concrete step wearing red scarf torn black suit tired wistful "
    "golden hour light fading warm orange step glow cool blue sky dusk contrast melancholic quiet empty pavement",
    
    # frame 2: Close focus on Chiku, more emotional
    "3D animated cartoon style chihuahua dog tired melancholic large eye bags drooping ears red scarf torn suit visible "
    "warm golden key light low right cool blue fill above step glowing orange long shadows melancholy quiet evening",
    
    # frame 3: Medium shot, environmental emphasis
    "3D animated cartoon style small dog alone on empty pavement concrete step indian chai stall blue shutter streetlamp "
    "golden sunset warm light fading cool dusk arriving long shadows warm-cool contrast loneliness nostalgia quiet",
    
    # frame 4: Same composition as seed 301 but more lighting emphasis
    "3D animated cartoon style chihuahua dog sitting step red scarf torn black suit melancholic expression tired eyes "
    "dusk scene warm golden light low right cool ambient blue sky step residual heat orange glow contrast",
]

neg = (
    "2D animation, flat colors, ink outlines, cel shading, thick lines, "
    "vector art, Flash, watercolor, sketch, hand-drawn, realistic fur, "
    "multiple dogs, bright colors, happy, daytime, noon, harsh light"
)

print("Generating S02 frames with CLIP-optimized prompts...\n")

for i, seed in enumerate([301, 305, 310, 311, 312]):
    gen = torch.Generator(device="cpu").manual_seed(seed)
    img = pipe(
        prompt=prompts[i],
        negative_prompt=neg,
        num_inference_steps=4,
        guidance_scale=0.0,
        generator=gen,
        height=960,
        width=544,
    ).images[0]
    
    path = OUT / f"s02_frame_{i}_seed{seed}.png"
    img.save(path)
    arr = np.array(img)
    mean = arr.mean()
    warm = arr[:,:,0].mean() - arr[:,:,2].mean()
    r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
    
    print(f"  [{i}] seed={seed}: mean={mean:.1f} warmth={warm:.1f} R={r:.0f} G={g:.0f} B={b:.0f}")
    print(f"       prompt: {prompts[i][:80]}...")

print("\nDone. Files on Desktop/cinema_output/")
