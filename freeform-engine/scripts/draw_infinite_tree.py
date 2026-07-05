import time, os, subprocess, math, random
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

random.seed(42)

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
    click(404, 55)
    time.sleep(0.08)
    click(395, 509)
    time.sleep(0.15)

def key_combo(mod_key, char_key):
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, True))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, True))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, False))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, False))

def zoom_in(n=1):
    for _ in range(n):
        key_combo(0x37, 24); time.sleep(0.04)

def zoom_out(n=1):
    for _ in range(n):
        key_combo(0x37, 27); time.sleep(0.04)

def catmull(pts, n=20):
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

subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True)
time.sleep(0.8)
subprocess.run(['osascript', '-e', '''
tell app "System Events"
    tell process "Freeform"
        click menu item "New Board" of menu "File" of menu bar 1
    end tell
end tell
'''], capture_output=True)
time.sleep(1.2)

cx, cy = 330, 400

# =============================================
# LEVEL 1: 1x ZOOM — THE COSMIC TREE (full view)
# Every stroke at this level is ~6-8px thick
# =============================================

# Trunk (twisted, organic)
trunk_l = catmull([(318, 395), (315, 370), (312, 345), (310, 320), (312, 300), (316, 285)], 15)
trunk_r = catmull([(342, 395), (345, 370), (348, 345), (350, 320), (348, 300), (344, 285)], 15)
activate_pen(); stroke(trunk_l); time.sleep(0.05)
activate_pen(); stroke(trunk_r); time.sleep(0.05)

# Trunk cross-rings (tree rings = layers of time)
for ty in range(295, 385, 12):
    spread = 3 + (ty - 290) // 10
    activate_pen(); stroke(catmull([(330-spread, ty-2), (330, ty+1), (330+spread, ty-2)], 6))
    time.sleep(0.015)

time.sleep(0.08)

# Main branches
branches = [
    [(330, 300), (315, 280), (295, 265), (270, 250), (248, 238)],
    [(330, 300), (345, 280), (365, 265), (390, 250), (412, 238)],
    [(330, 305), (310, 290), (285, 278), (260, 268)],
    [(330, 305), (350, 290), (375, 278), (400, 268)],
    [(330, 295), (330, 278), (330, 260), (330, 242)],
    [(330, 298), (305, 285), (278, 275), (255, 265)],
    [(330, 298), (355, 285), (382, 275), (405, 265)],
]
for b in branches:
    activate_pen(); stroke(catmull(b, 12)); time.sleep(0.035)

time.sleep(0.1)

# Small twigs
twigs = []
for _ in range(25):
    bx = random.randint(240, 420)
    by = random.randint(235, 295)
    angle = random.uniform(-0.8, 0.8)
    length = random.randint(15, 35)
    twigs.append([(bx, by), (bx + length * math.cos(angle), by + length * math.sin(angle))])
for t in twigs:
    activate_pen(); stroke(t); time.sleep(0.008)

time.sleep(0.08)

# Leaves (canopy - many small teardrops)
for _ in range(60):
    lx = random.randint(230, 430)
    ly = random.randint(210, 300)
    ls = random.randint(4, 9)
    activate_pen()
    stroke(catmull([(lx, ly), (lx-ls//3, ly-ls), (lx+ls//3, ly-ls)], 4))
    time.sleep(0.004)

time.sleep(0.08)

# Roots going deep
roots = [
    [(320, 395), (310, 410), (298, 428), (288, 448), (282, 468)],
    [(340, 395), (350, 410), (362, 428), (372, 448), (378, 468)],
    [(325, 398), (305, 418), (290, 438), (310, 458)],
    [(335, 398), (355, 418), (370, 438), (350, 458)],
    [(330, 398), (330, 420), (325, 445), (318, 465)],
]
for r in roots:
    activate_pen(); stroke(catmull(r, 12)); time.sleep(0.03)

time.sleep(0.1)

# Ground line
activate_pen()
stroke(catmull([(170, 440), (220, 438), (280, 442), (330, 440), (380, 443), (440, 438), (490, 440)], 10))
time.sleep(0.06)

# Stars in the sky
for _ in range(20):
    sx = random.randint(180, 480)
    sy = random.randint(165, 220)
    activate_pen(); stroke([(sx-2, sy), (sx+2, sy)]); time.sleep(0.006)
    activate_pen(); stroke([(sx, sy-2), (sx, sy+2)]); time.sleep(0.006)

time.sleep(0.15)

# =============================================
# LEVEL 2: ZOOM 6x — TRUNK DETAIL (bark, knots)
# Zoomed in, strokes appear thinner (~1-2px canvas)
# Visible canvas: ~245×160 px centered on (330,400)
# =============================================
zoom_in(6)
time.sleep(0.3)

# Bark texture (vertical grain lines on trunk)
for bx in range(308, 352, 3):
    by_start = 310 + int(8 * math.sin(bx * 0.3))
    by_end = 390 + int(8 * math.sin(bx * 0.5 + 1))
    if random.random() > 0.3:
        activate_pen()
        stroke([(bx, by_start), (bx, by_end)])
        time.sleep(0.003)

time.sleep(0.08)

# Bark horizontal fissures
for fy in range(315, 390, 7):
    fwidth = 5 + int(3 * math.sin(fy * 0.5))
    fx = 330 + int(5 * math.sin(fy * 0.7))
    activate_pen()
    stroke([(fx - fwidth, fy), (fx + fwidth, fy)])
    time.sleep(0.008)

time.sleep(0.06)

# Tree knots (whorls in the bark)
knots = [(325, 340), (338, 365), (322, 380), (340, 330)]
for kx, ky in knots:
    for r in range(3, 9, 2):
        pts = []
        for a in range(0, 370, 20):
            rad = math.radians(a)
            pts.append((kx + r * math.cos(rad), ky + r * math.sin(rad) * 0.7))
        activate_pen(); stroke(pts); time.sleep(0.015)

time.sleep(0.08)

# Tiny faces/figures in the bark (pareidolia)
faces = [(328, 350, 6), (336, 375, 5)]
for fx, fy, fs in faces:
    # Eyes
    activate_pen(); stroke([(fx-fs//2, fy-fs//3), (fx-fs//3, fy-fs//3)]); time.sleep(0.01)
    activate_pen(); stroke([(fx+fs//3, fy-fs//3), (fx+fs//2, fy-fs//3)]); time.sleep(0.01)
    # Mouth
    activate_pen(); stroke(catmull([(fx-fs//3, fy+fs//3), (fx, fy+fs//2), (fx+fs//3, fy+fs//3)], 5)); time.sleep(0.01)

time.sleep(0.1)

# Small roots detail at base
for rx in range(300, 360, 5):
    ry = 400 + int(6 * math.sin(rx * 0.4))
    activate_pen(); stroke([(rx, ry), (rx + 2, ry + 8)]); time.sleep(0.004)

time.sleep(0.08)

# =============================================
# LEVEL 3: ZOOM 5x MORE (~30x TOTAL) — WOOD GRAIN
# Strokes now ~0.2-0.3px canvas width (extremely thin)
# Visible canvas: ~50×32 px centered on (330,400)
# =============================================
zoom_in(5)
time.sleep(0.25)

# Wood grain (microscopic cellular pattern)
for gy in range(380, 420, 2):
    gx_off = int(3 * math.sin(gy * 0.8))
    activate_pen()
    stroke([(320 + gx_off, gy), (340 + gx_off, gy)])
    time.sleep(0.004)

time.sleep(0.06)

# Cell structures (tiny honeycomb-like patterns)
for hy in range(385, 415, 4):
    for hx in range(320, 340, 5):
        if random.random() > 0.4:
            activate_pen()
            stroke(catmull([
                (hx, hy), (hx+2, hy-1), (hx+4, hy), (hx+4, hy+2),
                (hx+2, hy+3), (hx, hy+2)
            ], 5))
            time.sleep(0.004)

time.sleep(0.06)

# Tiny spiral formations (like fibonacci in nature)
for sx, sy in [(325, 398), (335, 405), (328, 388), (338, 392)]:
    pts = []
    for angle in range(0, 720, 15):
        rad = math.radians(angle)
        r = angle / 720 * 4
        pts.append((sx + r * math.cos(rad), sy + r * math.sin(rad)))
    activate_pen(); stroke(pts); time.sleep(0.02)

time.sleep(0.08)

# =============================================
# LEVEL 4: ZOOM 5x MORE (~150x TOTAL) — MICRO WORLD
# Strokes now ~0.04-0.06px canvas width (near-invisible at 1x)
# Visible canvas: ~10×6 px centered on (330,400)
# =============================================
zoom_in(5)
time.sleep(0.25)

# At ~150x zoom, the visible canvas area is tiny (~10×6 px)
# Screen coordinates 50-610 map to just a few canvas pixels
# Drawing at full screen range creates micro-filigree

# Crystalline structures (tiny geometric patterns)
for cy_pos in range(390, 410, 2):
    for cx_pos in range(324, 336, 3):
        if random.random() > 0.5:
            size = random.randint(1, 3)
            activate_pen()
            pts = []
            for a in range(0, 360, 30):
                rad = math.radians(a)
                pts.append((cx_pos + size * math.cos(rad), cy_pos + size * math.sin(rad)))
            stroke(pts)
            time.sleep(0.004)

time.sleep(0.06)

# Micro-organisms (tiny curved shapes)
for _ in range(15):
    ox = random.randint(320, 340)
    oy = random.randint(392, 408)
    activate_pen()
    stroke(catmull([
        (ox, oy), (ox+2, oy-1), (ox+4, oy), (ox+2, oy+1)
    ], 5))
    time.sleep(0.006)

time.sleep(0.06)

# Quantum foam / energy patterns (dots and dashes)
for _ in range(40):
    qx = random.randint(318, 342)
    qy = random.randint(390, 410)
    activate_pen()
    stroke([(qx, qy), (qx + int(random.random() * 2), qy + int(random.random() * 2))])
    time.sleep(0.002)

time.sleep(0.06)

# =============================================
# LEVEL 5: ZOOM OUT (16 steps) — FULL REVEAL
# =============================================
zoom_out(16)
time.sleep(0.4)

print("Infinite Cosmic Tree drawn!")
