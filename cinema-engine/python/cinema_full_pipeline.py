"""
CINEMA PIPELINE v3 — RealVisXL V5.0 → 5 keyframes → FFmpeg
Uses the working float32 + cpu_offload config from v3_realvisxl.py
Compressed prompts (77-token safe) with shot-specific variations
"""

import torch, numpy as np, gc
from pathlib import Path
from diffusers import AutoPipelineForText2Image

OUT = Path.home() / "Desktop" / "cinema_output" / "pipeline"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 512, 896

print("=" * 60)
print("RealVisXL V5.0 → 5 keyframes (15 steps, 77-token safe)")
print("=" * 60)

pipe = AutoPipelineForText2Image.from_pretrained(
    "SG161222/RealVisXL_V5.0",
    torch_dtype=torch.float32,
    use_safetensors=True,
    variant="fp16",
)
try:
    pipe.enable_model_cpu_offload(device="mps")
except TypeError:
    pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
print("Pipeline ready.\n")

# Character core (fits in ~50 tokens, leaving ~25 for shot-specific)
CORE = (
    "Stylized 3D animated, Puss in Boots Last Wish style. "
    "Tiny terrier hunched into C-shape comma silhouette. "
    "Graphic dark eye bags, oversized red scarf trailing, "
    "sandy fur, cream belly, one white paw, buck tooth, "
    "torn black vest under scarf, floppy drooping ears. "
    "Tired melancholic half-closed eyes. "
)

NEG = (
    "2D flat animation, cel shading, ink outlines, thick lines, "
    "photorealistic live-action, uncanny valley, 2D rig, low polygon, "
    "bad textures, anime, manga, watercolor, hand-drawn, sketch, "
    "realistic fur, hyper-realistic, naturalistic, dull colors, "
    "desaturated, multiple characters, bright cheerful, daytime"
)

keyframes = [
    {
        "name": "kf1_corner",
        "prompt": CORE + "Curled in corner where step meets wall. Scarf pooled around him. Indian chai stall blue shutter. Golden hour fading dusk warm light long shadows. Lonely melancholic.",
        "seed": 42,
    },
    {
        "name": "kf2_moving",
        "prompt": CORE + "Uncurling standing wobbly using wall. Red scarf sliding revealing torn vest. Shuffling toward step. Indian chai stall. Golden dusk warm light. Dignified exhausted.",
        "seed": 142,
    },
    {
        "name": "kf3_on_step",
        "prompt": CORE + "Sitting alone on elevated concrete step center. Small alone. Torn vest visible. Looking at empty pavement. Chai stall blue shutter. Golden dusk warm step glow. Quiet grief.",
        "seed": 242,
    },
    {
        "name": "kf4_closeup",
        "prompt": CORE + "Close-up 85mm face fills frame. Enormous eye bags prominent. Golden light fading cool blue. Looking into middle distance. Blurred chai stall background. Quiet acceptance.",
        "seed": 342,
    },
    {
        "name": "kf5_flicker",
        "prompt": CORE + "Close-up 85mm deep sigh body deflates. Ears droop further. Streetlamp flickers background. Golden light gone cool blue dusk. Torn vest red scarf. Beautiful sadness acceptance.",
        "seed": 442,
    },
]

results = []
for i, kf in enumerate(keyframes):
    print(f"[{i+1}/5] {kf['name']} (seed={kf['seed']})")
    gen = torch.Generator(device="cpu").manual_seed(kf["seed"])
    img = pipe(
        prompt=kf["prompt"],
        negative_prompt=NEG,
        num_inference_steps=15,
        guidance_scale=7.0,
        generator=gen,
        height=H, width=W,
    ).images[0]

    path = OUT / f"{kf['name']}.png"
    img.save(path)
    arr = np.array(img).astype(np.float32)
    mean, warm = arr.mean(), arr[:,:,0].mean() - arr[:,:,2].mean()
    ok = "OK" if not (np.isnan(arr).any() or mean < 1) else "FAIL"
    print(f"  {ok}: mean={mean:.1f} warm={warm:.1f} -> {path.name}")
    results.append({"name": kf["name"], "warm": warm, "ok": ok, "path": str(path)})
    gc.collect()

print("\n" + "=" * 60)
print("KEYFRAMES DONE")
for r in results:
    print(f"  {r['ok']} {r['name']}: warm={r['warm']:.1f}")
print(f"\nNow run: bash ~/cinema_assemble.sh")
