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

print("Click TWICE to activate Pen tool")
deadline = time.time() + 30
while len(clicks) < 2 and time.time() < deadline:
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)

CGEventTapEnable(tap, False)

if len(clicks) >= 2:
    c1, c2 = clicks[0], clicks[1]
    print(f"\nCaptured clicks:")
    print(f"  C1: ({c1[0]:.0f}, {c1[1]:.0f})")
    print(f"  C2: ({c2[0]:.0f}, {c2[1]:.0f})")
    
    # Now replay them programmatically
    print("\nReplaying...")
    time.sleep(1)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (c1[0], c1[1]), kCGMouseButtonLeft))
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (c1[0], c1[1]), kCGMouseButtonLeft))
    time.sleep(0.3)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (c2[0], c2[1]), kCGMouseButtonLeft))
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (c2[0], c2[1]), kCGMouseButtonLeft))
    
    # Test if pen is active
    time.sleep(0.3)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (330, 400), kCGMouseButtonLeft))
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (330, 400), kCGMouseButtonLeft))
    time.sleep(0.05)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.02)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))
    time.sleep(0.2)
    
    img = CGDisplayCreateImage(CGMainDisplayID())
    w = CGImageGetWidth(img)
    prov = CGImageGetDataProvider(img)
    data = bytearray(CGDataProviderCopyData(prov))
    dark = 0
    for dy in range(390, 410):
        for dx in range(320, 340):
            o = (int(dy*2) * w + int(dx*2)) * 4
            r, g, b = data[o], data[o+1], data[o+2]
            if r < 100 and g < 100 and b < 100:
                dark += 1
    print(f"Dark pixels: {dark}")
else:
    print("Not enough clicks captured.")
