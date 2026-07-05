"""
Cinema Diffusion v3 — RealVisXL V5.0
The actual model the user was happy with. Fine-tuned SDXL for quality.
Uses float32 + model_cpu_offload (proven working config on 16GB M5).
"""

import torch, numpy as np
from pathlib import Path
from diffusers import AutoPipelineForText2Image

OUT = Path.home() / "Desktop" / "cinema_output" / "v3_realvisxl"
OUT.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("RealVisXL V5.0 — float32 + cpu_offload")
print("=" * 60)

pipe = AutoPipelineForText2Image.from_pretrained(
    "SG161222/RealVisXL_V5.0",
    torch_dtype=torch.float32,
    use_safetensors=True,
    variant="fp16",
)

try:
    pipe.enable_model_cpu_offload(device="mps")
    print("Using model_cpu_offload(device='mps')")
except TypeError:
    pipe.enable_model_cpu_offload()
except Exception as e:
    print(f"cpu_offload failed: {e}, falling back to .to('mps')")
    pipe = pipe.to("mps")

pipe.enable_attention_slicing()

# Actual Chiku character design from chiku.yaml + _style.yaml
prompt = (
    "Stylized 3D animated character, Puss in Boots Last Wish style. "
    "A tiny tired terrier dog hunched into a comma C-shape with legs. "
    "Enormous graphic dark eye bags under half-closed weary eyes. "
    "Oversized bright red scarf trailing behind. Sandy brown fur, "
    "cream belly, one white front paw, single buck tooth. "
    "Torn black vest visible under scarf. "
    "Sitting alone on concrete step by Indian chai stall blue shutter. "
    "Golden hour fading to dusk, warm light right, long shadows. "
    "Melancholic lonely cinematic."
)

neg = (
    "2D flat animation, cel shading, ink outlines, thick lines, "
    "limited animation, motion graphics, vector art, Flash, "
    "photorealistic live-action, uncanny valley, human skin, "
    "realistic human proportions, 2D rig, low polygon, "
    "bad textures, anime, manga, watercolor, painted background, "
    "paper texture, hand-drawn, sketch, realistic fur, "
    "strand-level detail, hyper-realistic, naturalistic, "
    "dull colors, desaturated"
)

W, H = 512, 896

print(f"\nModel: RealVisXL V5.0")
print(f"Resolution: {W}x{H} (9:16)")
print(f"Steps: 25, guidance: 7.5\n")

for seed in [42, 100, 200]:
    print(f"[RealVisXL V5] seed={seed} generating...")
    gen = torch.Generator(device="cpu").manual_seed(seed)

    img = pipe(
        prompt=prompt,
        negative_prompt=neg,
        num_inference_steps=25,
        guidance_scale=7.5,
        generator=gen,
        height=H,
        width=W,
    ).images[0]

    path = OUT / f"v3_realvisxl_v5_s02_chiku_seed{seed}.png"
    img.save(path)

    arr = np.array(img).astype(np.float32)
    mean = arr.mean()
    warm = arr[:,:,0].mean() - arr[:,:,2].mean()
    r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()

    if np.isnan(arr).any() or mean < 1.0:
        print(f"  FAIL: NaN/black (mean={mean:.1f})")
    else:
        print(f"  PASS: mean={mean:.1f} warm={warm:.1f} RGB=({r:.0f},{g:.0f},{b:.0f}) -> {path.name}")

print(f"\nDone. Check {OUT}")
