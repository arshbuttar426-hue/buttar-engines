"""
APPROACH 3: SD 1.5 + ControlNet depth (float32)
- Spatial/camera spec encoded as hand-crafted depth map
- Text prompt freed to focus on style, character, lighting
- SD 1.5 float32 (~4GB) + ControlNet float32 (~1.5GB) = 5.5GB, fits in 16GB
- Tests: can ControlNet inject spatial staging deterministically?
"""

import torch, numpy as np
from pathlib import Path
from PIL import Image, ImageFilter
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

OUT = Path.home() / "Desktop" / "cinema_output" / "controlnet"
OUT.mkdir(parents=True, exist_ok=True)

# ---- 1. Build depth map from S02 spatial staging spec ----
# Convention: white = close to camera, black = far
# Spec: wall left (close), step left-center (close, elevated),
#        pavement center-right (receding), streetlamp far right (tall),
#        sky top (far), blue shutter left (recessed)

W, H = 512, 896
depth = np.zeros((H, W), dtype=np.uint8)

# Sky: top 35% — dark (far)
depth[:int(H*0.35), :] = 25
for y in range(int(H*0.35), int(H*0.40)):
    t = (y - int(H*0.35)) / max(int(H*0.40) - int(H*0.35), 1)
    depth[y, :] = int(25 + t * 30)

# Buildings: 40-55% — medium-dark
depth[int(H*0.40):int(H*0.55), :] = 55

# Pavement: 55-100% — receding (brighter near bottom = closer)
for y in range(int(H*0.55), H):
    t = (y - int(H*0.55)) / max(H - int(H*0.55), 1)
    depth[y, :] = int(55 + t * 70)

# Wall on left edge (close): brighten
depth[:, :int(W*0.15)] = np.clip(depth[:, :int(W*0.15)].astype(int) + 80, 0, 255).astype(np.uint8)

# Blue shutter (recessed into wall)
depth[int(H*0.42):int(H*0.75), int(W*0.02):int(W*0.12)] = 120

# Concrete step (elevated, close): bright block
depth[int(H*0.58):int(H*0.72), int(W*0.10):int(W*0.45)] = 220

# Chiku on step: brightest spot
depth[int(H*0.50):int(H*0.60), int(W*0.20):int(W*0.32)] = 250

# Streetlamp (far right, tall): bright vertical
lamp_x = int(W * 0.88)
depth[int(H*0.20):int(H*0.85), lamp_x:lamp_x+8] = 180
depth[int(H*0.18):int(H*0.24), lamp_x-5:lamp_x+13] = 210

depth_img = Image.fromarray(depth).filter(ImageFilter.GaussianBlur(radius=3))
depth_path = OUT / "s02_depth_map.png"
depth_img.save(depth_path)
print(f"Depth map saved: {depth_path}")

# ---- 2. Load ControlNet + SD 1.5 (float32, MPS-safe) ----
print("\nLoading ControlNet depth (float32)...")
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-depth",
    torch_dtype=torch.float32,
)

print("Loading SD 1.5 + ControlNet pipeline (float32)...")
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float32,
    use_safetensors=True,
    safety_checker=None,
).to("mps")
pipe.enable_attention_slicing()

# ---- 3. Prompt — spatial info via depth map, text for style/character/lighting ----
prompt = (
    "3D animated cartoon style, Pixar DreamWorks quality, stylized. "
    "Small tired chihuahua dog, sandy brown fur, cream belly, drooping ears, "
    "red scarf around neck, torn black suit visible, large dark eye bags, "
    "melancholic expression. "
    "Golden hour fading to dusk. Warm orange key light from right, "
    "cool blue-grey sky, long shadows, warm step glow. "
    "Indian chai stall, concrete step, flickering streetlamp. "
    "Lonely, wistful, cinematic lighting, highly detailed."
)

neg = (
    "2D animation, flat colors, ink outlines, cel shading, thick lines, "
    "vector art, watercolor, sketch, realistic fur, photorealistic, "
    "multiple characters, group, bright cheerful, daytime, harsh light, "
    "low quality, blurry, deformed, extra limbs"
)

print(f"\nResolution: {W}x{H} (9:16)")
print(f"Steps: 25, guidance: 7.5, controlnet_scale: 0.8\n")

seeds = [42, 100, 200]
for seed in seeds:
    print(f"[ControlNet] seed={seed} generating...")
    gen = torch.Generator(device="cpu").manual_seed(seed)

    img = pipe(
        prompt=prompt,
        negative_prompt=neg,
        image=depth_img,
        num_inference_steps=25,
        guidance_scale=7.5,
        controlnet_conditioning_scale=0.8,
        generator=gen,
        height=H,
        width=W,
    ).images[0]

    path = OUT / f"controlnet_s02_chiku_seed{seed}.png"
    img.save(path)

    arr = np.array(img).astype(np.float32)
    mean = arr.mean()
    warm = arr[:,:,0].mean() - arr[:,:,2].mean()
    r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()

    if np.isnan(arr).any() or mean < 1.0:
        print(f"  FAIL: NaN/black output (mean={mean:.1f})")
    else:
        print(f"  PASS: mean={mean:.1f} warmth={warm:.1f} RGB=({r:.0f},{g:.0f},{b:.0f}) -> {path.name}")

print("\nControlNet done.")
