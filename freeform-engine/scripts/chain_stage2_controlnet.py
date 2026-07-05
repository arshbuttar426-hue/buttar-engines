#!/usr/bin/env python3
"""Stage 2: Canny edges → ControlNet SD 1.5 fp32 → enhanced cityscape."""

import torch, numpy as np
from pathlib import Path
from PIL import Image, ImageFilter
from scipy.ndimage import sobel
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

SRC = Path("/tmp/chain_input.png")
OUT = Path("/tmp/chain_stage2.png")

W, H = 512, 896

# ─── Canny edges ───
img = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)
gray = np.array(img.convert("L"), dtype=np.uint8)
edges = np.hypot(sobel(gray.astype(float), axis=1), sobel(gray.astype(float), axis=0))
edges = (edges / edges.max() * 255).astype(np.uint8)
edges = np.where(edges > 60, 255, 0).astype(np.uint8)
canny = Image.fromarray(edges).filter(ImageFilter.GaussianBlur(radius=0.5))

# ─── Load ControlNet ───
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny", torch_dtype=torch.float32)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet,
    torch_dtype=torch.float32, use_safetensors=True, safety_checker=None
).to("mps")
pipe.enable_attention_slicing()

prompt = (
    "cinematic cityscape at twilight, photorealistic, "
    "tall skyscrapers with lit windows, moon in sky, "
    "reflection on river water, bridge with lights, "
    "warm orange glow on horizon, deep blue night sky, "
    "highly detailed, professional photography, atmospheric, "
    "sharp focus, volumetric lighting, 8K"
)
neg = "cartoon, illustration, drawing, sketch, line art, low quality, blurry, deformed"

result = pipe(
    prompt=prompt, negative_prompt=neg, image=canny,
    num_inference_steps=20, guidance_scale=7.0,
    controlnet_conditioning_scale=0.85,
    generator=torch.Generator(device="cpu").manual_seed(137),
    height=H, width=W,
).images[0]

result.save(OUT)

arr = np.array(result).astype(np.float32)
mean = arr.mean()
r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
print(f"Stage 2 PASS: mean={mean:.1f} RGB=({r:.0f},{g:.0f},{b:.0f}) -> {OUT}")

del pipe, controlnet
import gc; gc.collect()
import torch; torch.mps.empty_cache()
