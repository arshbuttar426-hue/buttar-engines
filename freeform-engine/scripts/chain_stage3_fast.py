#!/usr/bin/env python3
"""Stage 3: SD 1.5 img2img fp32 — fast refinement on ControlNet output."""

import torch, numpy as np
from pathlib import Path
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

SRC = Path("/tmp/chain_stage2.png")
OUT = Path("/tmp/chain_stage3.png")
W, H = 512, 896

init_img = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32,
    use_safetensors=True,
    safety_checker=None,
).to("mps")
pipe.enable_attention_slicing()

prompt = (
    "cinematic cityscape at twilight, photorealistic, "
    "tall skyscrapers with lit windows, moon, "
    "river reflection, bridge, warm amber and deep blue, "
    "professional photography, sharp focus, volumetric lighting, "
    "highly detailed, atmospheric, 8K"
)
neg = "cartoon, illustration, drawing, low quality, blurry, deformed"

result = pipe(
    prompt=prompt, negative_prompt=neg, image=init_img,
    strength=0.35,
    num_inference_steps=20, guidance_scale=7.0,
    generator=torch.Generator(device="cpu").manual_seed(137),
    height=H, width=W,
).images[0]

result.save(OUT)

arr = np.array(result).astype(np.float32)
mean = arr.mean()
r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
print(f"Stage 3 PASS: mean={mean:.1f} RGB=({r:.0f},{g:.0f},{b:.0f}) -> {OUT}")
