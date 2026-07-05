"""
Freeform drawing core library.
Persistent toolkit for CGEvent-based Pen tool automation.

Usage:
    from freeform_core import *
    activate_pen()
    stroke([(100,100), (200,200), (300,100)])
"""

import time, os, subprocess, math
from Quartz.CoreGraphics import *

def click(x, y, slp=0.01):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(slp)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts, slp=0.01):
    for px, py in pts:
        time.sleep(slp)
        click(px, py, 0.001)
    time.sleep(0.03)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.01)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    """Click Shape button in toolbar, then 'Draw with Pen' in popover.
    Coordinates calibrated (Calibrated 2026-07-03 13:03).
    Order: Shape FIRST (opens popover), then Pen item within popover."""
    click(405, 58, 0.005)
    time.sleep(0.25)
    click(381, 511, 0.005)
    time.sleep(0.5)

def activate_freeform():
    subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True)
    time.sleep(1)

def new_board():
    subprocess.run(['osascript', '-e', '''
        tell app "System Events"
            tell process "Freeform"
                click menu item "New Board" of menu "File" of menu bar 1
            end tell
        end tell'''], capture_output=True)
    time.sleep(1.5)

def catmull(pts, n=25):
    out = []
    for i in range(len(pts)):
        p0 = pts[max(0,i-1)]; p1 = pts[i]
        p2 = pts[min(len(pts)-1,i+1)]; p3 = pts[min(len(pts)-1,i+2)]
        for t in [j/n for j in range(n)]:
            t2=t*t; t3=t2*t
            x=0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y=0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    return out

def bold_stroke(base_pts, offsets=[-3, 0, 3]):
    for dx in offsets:
        activate_pen()
        stroke([(x+dx, y+dx*0.5) for (x,y) in base_pts])
        time.sleep(0.12)

def count_ink(x1, y1, x2, y2, threshold=80):
    img = CGDisplayCreateImage(CGMainDisplayID())
    w = CGImageGetWidth(img)
    raw = bytearray(CGDataProviderCopyData(CGImageGetDataProvider(img)))
    n = 0
    for y in range(y1, y2):
        for x in range(x1, x2):
            o = (int(y*2)*w + int(x*2))*4
            if raw[o] < threshold and raw[o+1] < threshold and raw[o+2] < threshold:
                n += 1
    return n

def fill_hatch(x1, x2, y1, y2, step=3, horizontal=True):
    if horizontal:
        for y in range(y1, y2, step):
            activate_pen()
            stroke([(x1, y), (x2, y)])
            time.sleep(0.02)
    else:
        for x in range(x1, x2, step):
            activate_pen()
            stroke([(x, y1), (x, y2)])
            time.sleep(0.02)

def capture_clicks(n=2, timeout=30):
    """Interactive: click N times, returns list of (x,y) coordinates."""
    clicks = []
    def cb(proxy, event_type, event, refcon):
        if event_type == kCGEventLeftMouseDown:
            loc = CGEventGetLocation(event)
            clicks.append((loc.x, loc.y))
            print(f"  Click {len(clicks)}: ({loc.x:.0f}, {loc.y:.0f})")
        return event

    from Quartz import CFMachPortCreateRunLoopSource, CFRunLoopAddSource, CFRunLoopRunInMode, kCFRunLoopDefaultMode
    mask = (1 << kCGEventLeftMouseDown)
    tap = CGEventTapCreate(kCGSessionEventTap, kCGHeadInsertEventTap, kCGEventTapOptionDefault, mask, cb, None)
    src = CFMachPortCreateRunLoopSource(None, tap, 0)
    CFRunLoopAddSource(CFRunLoopGetCurrent(), src, kCFRunLoopDefaultMode)
    CGEventTapEnable(tap, True)

    print(f"Click {n} times to capture coordinates...")
    deadline = time.time() + timeout
    while len(clicks) < n and time.time() < deadline:
        CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)
    CGEventTapEnable(tap, False)
    return clicks[:n]
