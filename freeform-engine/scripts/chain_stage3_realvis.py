#!/usr/bin/env python3
"""RealVisXL img2img — quality bump on stage 2 output."""

import torch, numpy as np, time
from pathlib import Path
from PIL import Image
from diffusers import AutoPipelineForImage2Image

t0 = time.time()
SRC = Path("/tmp/chain_stage2.png")
OUT = Path("/tmp/chain_final.png")
W, H = 512, 896

init_img = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)

print("Loading RealVisXL (fp32, cpu_offload)...")
pipe = AutoPipelineForImage2Image.from_pretrained(
    "SG161222/RealVisXL_V5.0",
    torch_dtype=torch.float32,
    use_safetensors=True,
)
try:
    pipe.enable_model_cpu_offload(device="mps")
except Exception:
    pipe = pipe.to("mps")
pipe.enable_attention_slicing()
print(f"Loaded in {time.time()-t0:.0f}s")

prompt = "cinematic cityscape twilight, photorealistic, skyscrapers lit windows, river reflection, bridge, warm amber deep blue, sharp focus, volumetric lighting, highly detailed"
neg = "cartoon, illustration, drawing, low quality, blurry, deformed"

t1 = time.time()
result = pipe(
    prompt=prompt, negative_prompt=neg, image=init_img,
    strength=0.35, num_inference_steps=15, guidance_scale=6.0,
    generator=torch.Generator(device="cpu").manual_seed(137),
    height=H, width=W,
).images[0]
gen_time = time.time() - t1
print(f"Generated in {gen_time:.0f}s")

result.save(OUT)
arr = np.array(result).astype(np.float32)
mean = arr.mean()
r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
print(f"Final: mean={mean:.1f} RGB=({r:.0f},{g:.0f},{b:.0f}) -> {OUT}")
print(f"Total: {time.time()-t0:.0f}s")
