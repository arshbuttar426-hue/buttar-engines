import time, os, subprocess, math, random
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *
random.seed(7)

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.003)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts):
    for px, py in pts:
        time.sleep(0.003)
        click(px, py)
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.003)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    click(404, 55); time.sleep(0.07)
    click(395, 509); time.sleep(0.12)

def key_combo(m, c):
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, m, True))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, c, True))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, c, False))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, m, False))

def zi(n=1):
    for _ in range(n): key_combo(0x37, 24); time.sleep(0.03)
def zo(n=1):
    for _ in range(n): key_combo(0x37, 27); time.sleep(0.03)

def catmull(pts, n=15):
    out = []
    for i in range(len(pts)):
        p0=pts[max(0,i-1)]; p1=pts[i]; p2=pts[min(len(pts)-1,i+1)]; p3=pts[min(len(pts)-1,i+2)]
        for t in [j/n for j in range(n)]:
            t2=t*t; t3=t2*t
            x=0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y=0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    return out

def eye_outline(cx, cy, s):
    """Almond-shaped eye. s=1.0 → ~80px on screen."""
    r = 36 * s
    return catmull([
        (cx, cy-0.65*r), (cx-0.88*r, cy-0.28*r), (cx-0.95*r, cy),
        (cx-0.88*r, cy+0.35*r), (cx-0.5*r, cy+0.58*r), (cx, cy+0.68*r),
        (cx+0.5*r, cy+0.58*r), (cx+0.88*r, cy+0.35*r), (cx+0.95*r, cy),
        (cx+0.88*r, cy-0.28*r), (cx, cy-0.65*r),
    ], 20)

def iris_detail(cx, cy, s):
    """Radial iris lines. s=1.0 → ~30px radius."""
    r = 28 * s
    pr = 6 * s
    pts = []
    for a in range(0, 360, 15):
        rad = math.radians(a)
        x1 = cx + pr * math.cos(rad); y1 = cy + pr * math.sin(rad) * 0.7
        x2 = cx + r * math.cos(rad);  y2 = cy + r * math.sin(rad) * 0.7
        pts.append([(x1, y1), (x2, y2)])
    return pts

def pupil_outline(cx, cy, s):
    r = 9 * s
    pts = []
    for a in range(0, 370, 20):
        rad = math.radians(a)
        pts.append((cx + r * math.cos(rad), cy + r * math.sin(rad)))
    return pts

def eyelid_detail(cx, cy, s):
    r = 36 * s
    return catmull([
        (cx-r*0.7, cy-r*0.35), (cx-r*0.35, cy-r*0.7), (cx, cy-r*0.6),
        (cx+r*0.35, cy-r*0.7), (cx+r*0.7, cy-r*0.35),
    ], 10)

subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True); time.sleep(0.8)
subprocess.run(['osascript', '-e', '''
tell app "System Events"
    tell process "Freeform"
        click menu item "New Board" of menu "File" of menu bar 1
    end tell
end tell'''], capture_output=True); time.sleep(1.2)

# =============================================
# INFINITE REGRESSION OF EYES
# Each level draws an eye at screen center.
# Zoom makes each subsequent eye map to a 
# smaller canvas position, nesting inside
# the previous pupil.
# =============================================

# Screen center (where Freeform window centers)
scx, scy = 330, 385

# Face outline (context for the first eye)
activate_pen()
stroke(catmull([
    (scx-120, scy+120), (scx-140, scy+60), (scx-130, scy-20),
    (scx-100, scy-80), (scx-50, scy-120), (scx, scy-130),
    (scx+50, scy-120), (scx+100, scy-80), (scx+130, scy-20),
    (scx+140, scy+60), (scx+120, scy+120),
], 25))
time.sleep(0.06)

# Nose bridge
activate_pen()
stroke(catmull([(scx, scy+20), (scx, scy+60), (scx-10, scy+90), (scx-20, scy+110)], 10))
time.sleep(0.04)

# Eyebrow
activate_pen()
stroke(catmull([
    (scx-90, scy-95), (scx-60, scy-105), (scx-30, scy-108),
    (scx, scy-110), (scx+30, scy-108), (scx+60, scy-105), (scx+90, scy-95),
], 12))
time.sleep(0.06)

# === LEVEL 1: 1x zoom — Outer eye ===
scale = 1.0
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.04)
for line in iris_detail(scx, scy, scale):
    activate_pen(); stroke(line); time.sleep(0.005)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.025)
activate_pen(); stroke(eyelid_detail(scx, scy, scale)); time.sleep(0.03)
time.sleep(0.12)

# === LEVEL 2: Zoom 4x — First inner eye ===
zi(4); time.sleep(0.2)
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.03)
for line in iris_detail(scx, scy, scale):
    activate_pen(); stroke(line); time.sleep(0.004)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.02)
time.sleep(0.1)

# === LEVEL 3: Zoom 5x more (20x total) — Deeper ===
zi(5); time.sleep(0.2)
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.025)
for line in iris_detail(scx, scy, scale):
    activate_pen(); stroke(line); time.sleep(0.003)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.015)
# Add geometric iris pattern for variety
for a in range(0, 360, 60):
    rad = math.radians(a)
    activate_pen()
    stroke([(scx+6*math.cos(rad), scy+6*math.sin(rad)),
            (scx+24*math.cos(rad), scy+24*math.sin(rad))])
    time.sleep(0.008)
time.sleep(0.08)

# === LEVEL 4: Zoom 5x more (100x total) — Deeper still ===
zi(5); time.sleep(0.15)
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.02)
for line in iris_detail(scx, scy, scale):
    activate_pen(); stroke(line); time.sleep(0.003)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.012)
# Dense radial pattern
for a in range(0, 360, 10):
    rad = math.radians(a)
    activate_pen()
    stroke([(scx+2*math.cos(rad), scy+2*math.sin(rad)),
            (scx+22*math.cos(rad), scy+22*math.sin(rad))])
    time.sleep(0.003)
time.sleep(0.08)

# === LEVEL 5: Zoom 5x more (500x total) — Many layers deep ===
zi(5); time.sleep(0.15)
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.015)
for line in iris_detail(scx, scy, scale):
    activate_pen(); stroke(line); time.sleep(0.002)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.01)
# Hexagonal pattern in iris
for i in range(6):
    a1 = math.radians(i*60)
    a2 = math.radians((i+1)*60)
    activate_pen()
    stroke([(scx+8*math.cos(a1), scy+8*math.sin(a1)),
            (scx+8*math.cos(a2), scy+8*math.sin(a2))])
    time.sleep(0.005)
time.sleep(0.06)

# === LEVEL 6: Zoom 5x more (2500x total!) ===
zi(5); time.sleep(0.15)
# At 2500x zoom, this eye is ~0.03 canvas pixels at 1x
# But it fills the screen when zoomed in
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.012)
for line in iris_detail(scx, scy, scale):
    activate_pen(); stroke(line); time.sleep(0.002)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.008)
# Sub-iris - tiny star pattern
for a in range(0, 360, 5):
    rad = math.radians(a)
    activate_pen()
    stroke([(scx, scy), (scx+18*math.cos(rad), scy+18*math.sin(rad))])
    time.sleep(0.002)
time.sleep(0.06)

# === LEVEL 7: Zoom 5x more (12500x total!) ===
zi(5); time.sleep(0.15)
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.01)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.006)
# Micro-filigree
for a in range(0, 360, 3):
    rad = math.radians(a)
    activate_pen()
    stroke([(scx+10*math.cos(rad), scy+10*math.sin(rad)),
            (scx+22*math.cos(rad), scy+22*math.sin(rad))])
    time.sleep(0.002)
time.sleep(0.05)

# === LEVEL 8: Zoom 5x more (62500x total!) — The deepest level ===
zi(5); time.sleep(0.15)
activate_pen(); stroke(eye_outline(scx, scy, scale)); time.sleep(0.008)
activate_pen(); stroke(pupil_outline(scx, scy, scale)); time.sleep(0.005)
# Quantum dots - tiny points
for _ in range(50):
    ox = scx + random.randint(-20, 20)
    oy = scy + random.randint(-20, 20)
    activate_pen()
    stroke([(ox, oy), (ox+1, oy+1)])
    time.sleep(0.001)

time.sleep(0.1)

# === ZOOM BACK OUT — Full reveal ===
zo(35)
time.sleep(0.5)

print("Infinite Regression Eye drawn at 8 levels!")
