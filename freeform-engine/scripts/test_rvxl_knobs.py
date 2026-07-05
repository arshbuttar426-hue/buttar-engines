#!/usr/bin/env python3
"""Test different RealVisXL knobs: schedulers × CFG, all fp32 cpu_offload."""

import torch, numpy as np, time, gc
from pathlib import Path
from PIL import Image
from diffusers import AutoPipelineForImage2Image, DDIMScheduler, EulerAncestralDiscreteScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler

SRC = Path("/tmp/chain_stage2.png")
OUT_DIR = Path("/tmp/rvxl_tests")
OUT_DIR.mkdir(exist_ok=True)
W, H = 512, 896

init_img = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)

prompt = "cinematic cityscape twilight, photorealistic, skyscrapers lit windows, river reflection, bridge, warm amber deep blue, sharp focus, volumetric lighting, highly detailed"
neg = "cartoon, illustration, drawing, low quality, blurry, deformed"

# ─── Tests: (name, scheduler_class, cfg, steps, extra_kwargs) ───
tests = [
    ("cfg4_dpmpp",    DPMSolverMultistepScheduler,         4.0, 15, {}),
    ("cfg7_dpmpp",    DPMSolverMultistepScheduler,         7.0, 15, {}),  # baseline
    ("cfg11_dpmpp",   DPMSolverMultistepScheduler,        11.0, 15, {}),
    ("cfg7_eulera",   EulerAncestralDiscreteScheduler,     7.0, 15, {}),
    ("cfg7_euler",    EulerDiscreteScheduler,              7.0, 15, {}),
    ("cfg7_ddim",     DDIMScheduler,                       7.0, 25, {}),
]

print("Loading RealVisXL fp32 + cpu_offload...")
t0 = time.time()
pipe = AutoPipelineForImage2Image.from_pretrained(
    "SG161222/RealVisXL_V5.0",
    torch_dtype=torch.float32, use_safetensors=True,
)
try:
    pipe.enable_model_cpu_offload(device="mps")
except Exception:
    pipe = pipe.to("mps")
pipe.enable_attention_slicing()
print(f"Loaded in {time.time()-t0:.0f}s\n")

results = []
for name, sched_cls, cfg, steps, extra in tests:
    t1 = time.time()
    pipe.scheduler = sched_cls.from_config(pipe.scheduler.config, **extra)
    seed = 137
    gen = torch.Generator(device="cpu").manual_seed(seed)

    result = pipe(
        prompt=prompt, negative_prompt=neg, image=init_img,
        strength=0.35, num_inference_steps=steps,
        guidance_scale=cfg, generator=gen,
        height=H, width=W,
    ).images[0]

    path = OUT_DIR / f"{name}.png"
    result.save(path)
    dt = time.time() - t1

    arr = np.array(result).astype(np.float32)
    r, g, b = arr[:,:,0].mean(), arr[:,:,1].mean(), arr[:,:,2].mean()
    unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))

    results.append((name, dt, r, g, b, unique_colors, cfg, steps, sched_cls.__name__))
    print(f"{name:20s}  {dt:4.0f}s  RGB=({r:3.0f},{g:3.0f},{b:3.0f})  unique={unique_colors}  cfg={cfg}  sched={sched_cls.__name__}")

    gc.collect()
    torch.mps.empty_cache()

print("\n─── Summary ───")
print(f"{'Name':20s}  {'Time':6s}  {'RGB':20s}  {'Unique':8s}  {'CFG':5s}  {'Scheduler':20s}")
print("-" * 80)
for name, dt, r, g, b, uc, cfg, steps, sched_name in results:
    print(f"{name:20s}  {dt:4.0f}s   ({r:3.0f},{g:3.0f},{b:3.0f})  {uc:6d}    {cfg:4.1f}  {sched_name:20s}")
