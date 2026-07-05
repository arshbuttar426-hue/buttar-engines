"""
Cinema Diffusion v2 — Using ACTUAL character designs from YAML specs
- Reads chiku.yaml, _style.yaml for exact character details
- Uses the actual render prompt structure from S02_render.yaml
- Experimental: sweeps guidance_scale, steps, seeds, prompt variants
- SD-Turbo float32 (known working MPS config)
"""

import torch, numpy as np, itertools
from pathlib import Path
from diffusers import AutoPipelineForText2Image, EulerDiscreteScheduler

OUT = Path.home() / "Desktop" / "cinema_output" / "v2_experiment"
OUT.mkdir(parents=True, exist_ok=True)

print("Loading SD-Turbo (float32, MPS)...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float32,
    use_safetensors=True,
    safety_checker=None,
).to("mps")
pipe.enable_attention_slicing()

# ---- PROMPTS (from actual chiku.yaml + _style.yaml) ----
# Priority: STYLE > CHARACTER SILHOUETTE > CHARACTER DETAILS > EXPRESSION > ENVIRONMENT > LIGHTING > MOOD
# Must fit 77 CLIP tokens

prompt_a = (
    "Stylized 3D animated, Puss in Boots Last Wish style. "
    "Tiny terrier curled into C-shape, hunched comma silhouette. "
    "Graphic dark half-circle eye bags, oversized trailing red scarf, "
    "sandy fur, cream belly, one white paw, buck tooth, "
    "torn black vest under scarf, floppy drooping ears. "
    "Tired melancholic half-closed eyes. "
    "Concrete step, Indian chai stall, blue shutter, empty pavement. "
    "Golden hour fading dusk, warm light, long shadows, cool sky. "
    "Lonely wistful."
)

prompt_b = (
    "Stylized 3D animated character, Mitchells vs Machines quality. "
    "A tiny tired terrier dog hunched into a comma C-shape with legs. "
    "Enormous graphic dark eye bags under half-closed weary eyes. "
    "Oversized bright red scarf trailing behind. Sandy brown fur, "
    "cream belly, one white front paw, single buck tooth. "
    "Torn black vest visible under scarf. "
    "Sitting alone on concrete step by Indian chai stall blue shutter. "
    "Golden hour fading to dusk, warm light right, long shadows. "
    "Melancholic lonely cinematic."
)

prompt_c = (
    "3D stylized cartoon, Pixar quality. Small C-shaped hunched dog, "
    "comma silhouette, massive red scarf trailing, graphic eye bags, "
    "sandy fur, cream belly, white paw, buck tooth, torn black suit, "
    "drooping ears, tired eyes. Step, chai stall, empty pavement, "
    "golden dusk, warm light, long shadows. Lonely, melancholic."
)

# Negative prompt from _style.yaml (precise — excludes 2D flat, not all cartoon)
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

prompts = {"A_keyword": prompt_a, "B_descriptive": prompt_b, "C_compressed": prompt_c}

# ---- EXPERIMENTAL PARAMETER SWEEP ----
# SD-Turbo is distilled — guidance=0.0 is default, but we experiment
guidance_scales = [0.0, 1.5, 3.0, 7.5]
steps_options = [4, 8]
seeds = [42, 100]

W, H = 544, 960  # 9:16, divisible by 8

total = len(prompts) * len(guidance_scales) * len(steps_options) * len(seeds)
print(f"\nExperimental sweep: {total} images")
print(f"  Prompts: {list(prompts.keys())}")
print(f"  Guidance: {guidance_scales}")
print(f"  Steps: {steps_options}")
print(f"  Seeds: {seeds}")
print(f"  Resolution: {W}x{H}\n")

idx = 0
results = []

for pname, prompt in prompts.items():
    for gs in guidance_scales:
        for steps in steps_options:
            for seed in seeds:
                idx += 1
                gen = torch.Generator(device="cpu").manual_seed(seed)
                
                img = pipe(
                    prompt=prompt,
                    negative_prompt=neg,
                    num_inference_steps=steps,
                    guidance_scale=gs,
                    generator=gen,
                    height=H,
                    width=W,
                ).images[0]
                
                fname = f"v2_{pname}_gs{gs}_s{steps}_seed{seed}.png"
                path = OUT / fname
                img.save(path)
                
                arr = np.array(img).astype(np.float32)
                mean = arr.mean()
                warm = arr[:,:,0].mean() - arr[:,:,2].mean()
                
                nan_flag = "NaN" if (np.isnan(arr).any() or mean < 1.0) else "OK"
                
                print(f"  [{idx:02d}/{total}] {pname} gs={gs} steps={steps} seed={seed} "
                      f"| mean={mean:.0f} warm={warm:.1f} {nan_flag} -> {fname}")
                
                results.append({
                    "prompt": pname, "gs": gs, "steps": steps, "seed": seed,
                    "mean": mean, "warm": warm, "file": fname, "nan": nan_flag
                })

# Summary
print("\n" + "=" * 70)
print("SUMMARY — Top 5 by warmth (golden hour match)")
print("=" * 70)
valid = [r for r in results if r["nan"] == "OK"]
for r in sorted(valid, key=lambda x: x["warm"], reverse=True)[:5]:
    print(f"  {r['file']}: warm={r['warm']:.1f} mean={r['mean']:.0f} "
          f"(gs={r['gs']} steps={r['steps']} seed={r['seed']} prompt={r['prompt']})")

print(f"\nAll {total} images saved to: {OUT}")
