#!/usr/bin/env python3
"""ControlNet enhancement of cityscape — Canny edges → SD 1.5 fp32 → Freeform."""

import torch, numpy as np, time, subprocess
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image

OUT = Path("/tmp")
SRC = OUT / "cityscape.png"

# ─── 1. Load cityscape and extract Canny edges ───
print("Loading cityscape and extracting edges...")
img = Image.open(SRC).convert("RGB")
ow, oh = img.size  # 660×700

# Resize to 512×896 (portrait, good for cityscape)
W, H = 512, 896
img_resized = img.resize((W, H), Image.LANCZOS)

# Convert to grayscale and run Canny
gray = img_resized.convert("L")
gray_np = np.array(gray, dtype=np.uint8)

# Simple Sobel-based edge detection (no opencv dependency)
from scipy.ndimage import sobel
edges_x = sobel(gray_np.astype(float), axis=1)
edges_y = sobel(gray_np.astype(float), axis=0)
edges = np.hypot(edges_x, edges_y)
edges = (edges / edges.max() * 255).astype(np.uint8)
# Threshold to binary
edges = np.where(edges > 60, 255, 0).astype(np.uint8)

canny_img = Image.fromarray(edges).filter(ImageFilter.GaussianBlur(radius=0.5))
canny_path = OUT / "cityscape_canny.png"
canny_img.save(canny_path)
print(f"Canny edges saved: {canny_path}")

# ─── 2. Load ControlNet Canny + SD 1.5 (fp32, MPS-safe) ───
print("\nLoading ControlNet Canny (float32)...")
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float32,
)

print("Loading SD 1.5 pipeline (float32)...")
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float32,
    use_safetensors=True,
    safety_checker=None,
).to("mps")
pipe.enable_attention_slicing()

# ─── 3. Prompt — cityscape from the Canny edges ───
prompt = (
    "cinematic cityscape at twilight, photorealistic, "
    "tall skyscrapers with lit windows, moon in sky, "
    "reflection on river water, bridge with lights, "
    "warm orange glow on horizon, deep blue night sky, "
    "highly detailed, professional photography, atmospheric, "
    "sharp focus, volumetric lighting, 8K"
)

neg = (
    "cartoon, illustration, drawing, sketch, line art, 2D, "
    "low quality, blurry, distorted, deformed, ugly, oversaturated, "
    "grainy, noisy, extra buildings, duplicated, text, watermark"
)

print(f"\nResolution: {W}x{H}")
print(f"Steps: 20, guidance: 7.0, controlnet_scale: 0.85\n")

seeds = [137, 42]
for seed in seeds:
    print(f"[ControlNet] seed={seed} generating...")
    gen = torch.Generator(device="cpu").manual_seed(seed)

    result = pipe(
        prompt=prompt,
        negative_prompt=neg,
        image=canny_img,
        num_inference_steps=20,
        guidance_scale=7.0,
        controlnet_conditioning_scale=0.85,
        generator=gen,
        height=H,
        width=W,
    ).images[0]

    path = OUT / f"cityscape_controlnet_seed{seed}.png"
    result.save(path)

    arr = np.array(result).astype(np.float32)
    mean = arr.mean()
    valid = arr.shape[0] * arr.shape[1]

    if np.isnan(arr).any() or mean < 1.0:
        print(f"  FAIL: NaN/black output (mean={mean:.1f})")
    else:
        r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
        print(f"  PASS: mean={mean:.1f} RGB=({r:.0f},{g:.0f},{b:.0f}) -> {path.name}")

# ─── 4. Paste best result into Freeform ───
best_path = OUT / "cityscape_controlnet_seed137.png"
print(f"\nPasting into Freeform: {best_path}")

import AppKit
ns_img = AppKit.NSImage.alloc().initWithContentsOfFile_(str(best_path))
AppKit.NSPasteboard.generalPasteboard().clearContents()
AppKit.NSPasteboard.generalPasteboard().writeObjects_([ns_img])
time.sleep(0.2)

subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True)
time.sleep(0.5)
subprocess.run(['osascript', '-e', '''
    tell app "System Events"
        tell process "Freeform"
            click menu item "New Board" of menu "File" of menu bar 1
        end tell
    end tell
'''], capture_output=True)
time.sleep(1.5)
subprocess.run(['osascript', '-e', '''
    tell app "System Events"
        tell process "Freeform"
            keystroke "v" using command down
        end tell
    end tell
'''], capture_output=True)
time.sleep(1)

print("Done — ControlNet cityscape pasted to Freeform.")
