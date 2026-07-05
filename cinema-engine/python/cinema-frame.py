"""
Cinema → Controlled Frames → Video
Diffusers + MPS (Apple Silicon) + ControlNet + GLIGEN
"""

import json, os, subprocess, torch, numpy as np
from pathlib import Path
from diffusers import (
    StableDiffusionXLControlNetPipeline,
    StableDiffusionXLGLIGENPipeline,
    ControlNetModel,
    GLIGENScheduledSampling,
    DDIMScheduler
)
from diffusers.utils import load_image
from PIL import Image, ImageDraw
from transformers import CLIPTextModel, CLIPTokenizer

# --- CONFIG ---
OUTPUT_DIR = Path.home() / "Desktop" / "cinema_output"
OUTPUT_DIR.mkdir(exist_ok=True)

device = "mps"  # Apple Silicon Metal
dtype = torch.float16


def check_setup():
    """Verify MPS is available and install torch if needed."""
    if not torch.backends.mps.is_available():
        print("MPS not available. Ensure you're on Apple Silicon.")
        return False
    print(f"MPS available. PyTorch {torch.__version__}")
    return True


def load_models():
    """Load ControlNet + GLIGEN models."""
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_openpose",
        torch_dtype=dtype
    ).to(device)

    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        controlnet=controlnet,
        torch_dtype=dtype,
        use_safetensors=True
    ).to(device)
    
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe.enable_model_cpu_offload()
    
    return pipe


def build_pose_map(spec):
    """Convert Cinema character spec to a pose skeleton image.
    Returns: PIL Image (512x512), white background with skeleton lines.
    """
    img = Image.new("RGB", (512, 512), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Parse character positions from spec
    chars = spec.get("characters", spec.get("subjects", []))
    for char in chars:
        pos = char.get("position", {})
        x = pos.get("x", 256)
        y = pos.get("y", 256)
        # Head
        draw.ellipse([x-15, y-40, x+15, y-10], outline=(0,0,0), width=3)
        # Body
        draw.line([x, y-10, x, y+40], fill=(0,0,0), width=3)
        # Arms
        draw.line([x-30, y, x+30, y], fill=(0,0,0), width=3)
        # Legs
        draw.line([x, y+40, x-20, y+70], fill=(0,0,0), width=3)
        draw.line([x, y+40, x+20, y+70], fill=(0,0,0), width=3)
    
    return img


def build_layout_map(spec):
    """Convert Cinema spatial spec to segmentation map for ControlNet."""
    img = Image.new("RGB", (512, 512), (200, 200, 200))
    draw = ImageDraw.Draw(img)
    
    objects = spec.get("objects", spec.get("props", []))
    for obj in objects:
        box = obj.get("bounding_box", {})
        x1 = box.get("x1", 0)
        y1 = box.get("y1", 0)
        x2 = box.get("x2", 512)
        y2 = box.get("y2", 512)
        color = tuple(np.random.randint(0, 255, 3).tolist())
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
    
    return img


def build_gligen_boxes(spec):
    """Convert spec to GLIGEN bounding boxes + phrases."""
    boxes = []
    phrases = []
    
    characters = spec.get("characters", [])
    for c in characters:
        box = c.get("bounding_box", [0, 0, 1, 1])
        boxes.append(box)
        phrases.append(c.get("description", "a person"))
    
    objects = spec.get("objects", [])
    for o in objects:
        box = o.get("bounding_box", [0, 0, 1, 1])
        boxes.append(box)
        phrases.append(o.get("description", "an object"))
    
    return torch.tensor([boxes]), phrases


def generate_frame(pipe, spec, prompt, seed=42, is_first=False):
    """Generate one frame with full control pipeline."""
    generator = torch.Generator(device="cpu").manual_seed(seed)
    
    # Build control inputs from spec
    pose_image = build_pose_map(spec)
    layout_image = build_layout_map(spec)
    
    # Generate
    image = pipe(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted",
        num_inference_steps=25,
        generator=generator,
        image=[pose_image, layout_image],
        controlnet_conditioning_scale=[0.7, 0.5],
        guidance_scale=7.5,
        height=512,
        width=512,
    ).images[0]
    
    return image


def cinema_spec_to_frames(spec_path, frame_count=24):
    """Process a Cinema spec into controlled frames."""
    with open(spec_path) as f:
        spec = json.load(f)
    
    pipe = load_models()
    prompt = spec.get("prompt", spec.get("description", "a scene"))
    
    frames = []
    for i in range(frame_count):
        print(f"  Frame {i+1}/{frame_count} (seed={42+i})")
        frame = generate_frame(pipe, spec, prompt, seed=42+i, is_first=(i==0))
        path = OUTPUT_DIR / f"frame_{i:04d}.png"
        frame.save(path)
        frames.append(path)
    
    return frames


def frames_to_video(frame_paths, output="short.mp4", fps=12):
    """Stitch to video with ffmpeg."""
    r = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)
    if r.returncode != 0:
        subprocess.run(["brew", "install", "ffmpeg"], capture_output=True)
    
    list_file = OUTPUT_DIR / "frames.txt"
    with open(list_file, "w") as f:
        for p in frame_paths:
            f.write(f"file '{p}'\nduration 1/{fps}\n")
    
    out = OUTPUT_DIR / output
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-vsync", "vfr", "-pix_fmt", "yuv420p",
        str(out)
    ], capture_output=True)
    
    list_file.unlink()
    return str(out)


if __name__ == "__main__":
    if not check_setup():
        exit(1)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="Cinema spec JSON")
    parser.add_argument("--frames", type=int, default=24)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--output", default="short.mp4")
    args = parser.parse_args()
    
    print(f"Loading models...")
    frames = cinema_spec_to_frames(args.spec, args.frames)
    
    print(f"Rendering video...")
    video = frames_to_video(frames, args.output, args.fps)
    
    print(f"Done: {video}")
