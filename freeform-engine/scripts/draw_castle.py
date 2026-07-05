import time, os, subprocess, math
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.006)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts):
    for px, py in pts:
        time.sleep(0.006)
        click(px, py)
    time.sleep(0.025)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    click(404, 55)
    time.sleep(0.15)
    click(395, 509)
    time.sleep(0.25)

def key_combo(mod_key, char_key):
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, True))
    time.sleep(0.05)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, True))
    time.sleep(0.02)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, False))
    time.sleep(0.02)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, False))

def zoom_in(n=1):
    for _ in range(n):
        key_combo(0x37, 24)  # Cmd + Plus (= key, keycode 24)
        time.sleep(0.1)

def zoom_out(n=1):
    for _ in range(n):
        key_combo(0x37, 27)  # Cmd + Minus (- key, keycode 27)
        time.sleep(0.1)

def catmull(pts, n=30):
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
time.sleep(1)
subprocess.run(['osascript', '-e', '''
tell app "System Events"
    tell process "Freeform"
        click menu item "New Board" of menu "File" of menu bar 1
    end tell
end tell
'''], capture_output=True)
time.sleep(1.5)

cx, cy = 330, 420

# =============================================
# CASTLE with ZOOM-BASED PERSPECTIVE
# =============================================
# Phase 1: Normal zoom — Main castle structure
# Phase 2: Zoom in 3x — Thin delicate details (windows, flags, stone)
# Phase 3: Zoom out — Thick foreground (moat, drawbridge, ground)

# ---- PHASE 1: NORMAL ZOOM - CASTLE SILHOUETTE ----

# Central keep (main tower block)
keep = [(270, 310), (390, 310), (390, 420), (270, 420)]
activate_pen()
stroke(keep)
time.sleep(0.1)

# Crenellations on keep top
for x in range(268, 395, 14):
    activate_pen()
    stroke([(x, 310), (x, 295)])
    time.sleep(0.04)

time.sleep(0.15)

# Left curtain wall
activate_pen()
stroke([(190, 360), (270, 360), (270, 420), (190, 420)])
time.sleep(0.1)

# Right curtain wall
activate_pen()
stroke([(390, 360), (470, 360), (470, 420), (390, 420)])
time.sleep(0.1)

# Left corner tower (round, indicated by wide rectangle)
activate_pen()
stroke([(180, 340), (210, 340), (210, 430), (180, 430)])
time.sleep(0.08)

# Right corner tower
activate_pen()
stroke([(450, 340), (480, 340), (480, 430), (450, 430)])
time.sleep(0.08)

# Gatehouse (front projection)
gate = [(285, 420), (375, 420), (375, 460), (285, 460)]
activate_pen()
stroke(gate)
time.sleep(0.08)

# Gate arch
arch_ctrl = [(310, 460), (310, 440), (330, 430), (350, 440), (350, 460)]
activate_pen()
stroke(catmull(arch_ctrl, 20))
time.sleep(0.08)

# Portcullis lines (vertical bars in gate)
for x in range(316, 350, 6):
    activate_pen()
    stroke([(x, 460), (x, 440)])
    time.sleep(0.03)

time.sleep(0.2)

# ---- PHASE 2: ZOOM IN 3x - DELICATE DETAILS (thin strokes) ----
zoom_in(3)
time.sleep(0.3)

# Window slits on keep (thin because we're zoomed in)
for wx, wy in [(290, 350), (310, 350), (350, 350), (370, 350), (290, 380), (370, 380)]:
    activate_pen()
    stroke([(wx, wy-12), (wx, wy+12)])
    time.sleep(0.03)

time.sleep(0.12)

# Arrow slits on towers
for wx in [190, 200, 460, 470]:
    for wy in [370, 400]:
        activate_pen()
        stroke([(wx, wy-8), (wx+4, wy-5), (wx, wy+8)])
        time.sleep(0.03)

time.sleep(0.12)

# Flags on towers
for fx, fy in [(195, 340), (465, 340), (330, 310)]:
    # Flag pole
    activate_pen()
    stroke([(fx, fy), (fx, fy-35)])
    time.sleep(0.03)
    # Flag triangle
    activate_pen()
    stroke([(fx, fy-35), (fx+20, fy-28), (fx, fy-22)])
    time.sleep(0.03)

time.sleep(0.12)

# Stone texture lines on keep walls (delicate horizontal lines)
for sy in range(325, 400, 11):
    activate_pen()
    stroke([(275, sy), (385, sy)])
    time.sleep(0.02)

# Stone vertical joints
for sx in range(285, 380, 16):
    for sy in [335, 355, 375]:
        activate_pen()
        stroke([(sx, sy), (sx, sy+8)])
        time.sleep(0.02)

time.sleep(0.2)

# ---- PHASE 3: ZOOM OUT - THICK FOREGROUND ----
zoom_out(5)
time.sleep(0.3)

# Moat (thick strokes because zoomed out)
activate_pen()
stroke([(140, 480), (520, 480), (530, 510), (130, 510)])
time.sleep(0.08)

# Moat water lines
activate_pen()
stroke([(150, 490), (510, 490)])
time.sleep(0.06)
activate_pen()
stroke([(160, 500), (500, 500)])
time.sleep(0.06)

# Drawbridge
activate_pen()
stroke([(310, 460), (350, 460), (350, 490), (310, 490)])
time.sleep(0.06)

# Drawbridge planks
for dx in range(314, 352, 6):
    activate_pen()
    stroke([(dx, 460), (dx, 490)])
    time.sleep(0.03)

# Ground (sweeping curved ground line)
ground_ctrl = [(60, 480), (100, 490), (200, 495), (330, 500), (460, 495), (540, 490), (580, 480)]
activate_pen()
stroke(catmull(ground_ctrl, 20))
time.sleep(0.08)

# Ground grass tufts
for gx in range(80, 560, 40):
    for _ in range(2):
        gh = 5 + int(math.sin(gx * 0.5 + _ * 2) * 3)
        activate_pen()
        stroke([(gx + _ * 10, 490), (gx + _ * 10 + 2, 490 - gh)])
        time.sleep(0.015)

# Reset zoom
zoom_in(2)
time.sleep(0.2)

print("Castle with zoom perspective drawn!")
