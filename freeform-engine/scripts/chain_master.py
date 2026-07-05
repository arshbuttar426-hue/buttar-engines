#!/usr/bin/env python3
"""Chain master: Stage 1 (draw) → Stage 2 (ControlNet) → Stage 3 (SDXL) → Freeform."""

import subprocess, time, sys

scripts = [
    ("Stage 1: Quartz draw",     "chain_stage1_draw.py"),
    ("Stage 2: Canny ControlNet","chain_stage2_controlnet.py"),
    ("Stage 3: SD 1.5 img2img",  "chain_stage3_fast.py"),
]

base = "/Users/arshbuttar/.opencode_knowledge/scripts"

for label, script in scripts:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, f"{base}/{script}"],
        capture_output=True, text=True, timeout=600
    )
    print(result.stdout)
    if result.stderr:
        for line in result.stderr.splitlines():
            if "error" in line.lower() or "fail" in line.lower() or "traceback" in line.lower():
                print(f"STDERR: {line}")
    if result.returncode != 0:
        print(f"FAILED at {label} (exit code {result.returncode})")
        sys.exit(1)

# ─── Paste final result into Freeform ───
final = "/tmp/chain_stage3.png"
print(f"\nPasting final result into Freeform: {final}")

import AppKit
ns_img = AppKit.NSImage.alloc().initWithContentsOfFile_(final)
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

print("\nDone — full chain complete. Final result in Freeform.")
