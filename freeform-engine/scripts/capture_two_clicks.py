import time, os, subprocess
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *
from Quartz import *

clicks = []

def cb(proxy, event_type, event, refcon):
    if event_type == kCGEventLeftMouseDown:
        loc = CGEventGetLocation(event)
        clicks.append((loc.x, loc.y))
        print(f"  Click at ({loc.x:.0f}, {loc.y:.0f})")
    return event

mask = (1 << kCGEventLeftMouseDown)
tap = CGEventTapCreate(kCGSessionEventTap, kCGHeadInsertEventTap,
                       kCGEventTapOptionDefault, mask, cb, None)
src = CFMachPortCreateRunLoopSource(None, tap, 0)
CFRunLoopAddSource(CFRunLoopGetCurrent(), src, kCFRunLoopDefaultMode)
CGEventTapEnable(tap, True)

subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True)
time.sleep(0.5)

print("Ready — click twice to activate Pen tool")

deadline = time.time() + 30
while len(clicks) < 2 and time.time() < deadline:
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)

CGEventTapEnable(tap, False)

if len(clicks) >= 2:
    print(f"\nClick 1: ({clicks[0][0]:.0f}, {clicks[0][1]:.0f})")
    print(f"Click 2: ({clicks[1][0]:.0f}, {clicks[1][1]:.0f})")
else:
    print(f"\nOnly got {len(clicks)} clicks")
    for c in clicks:
        print(f"  ({c[0]:.0f}, {c[1]:.0f})")
