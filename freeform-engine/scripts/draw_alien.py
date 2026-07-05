import time, os, subprocess, math
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.005)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts):
    for px, py in pts:
        time.sleep(0.005)
        click(px, py)
    time.sleep(0.02)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.005)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    click(404, 55)
    time.sleep(0.1)
    click(395, 509)
    time.sleep(0.2)

def key_combo(mod_key, char_key):
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, True))
    time.sleep(0.02)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, True))
    time.sleep(0.01)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, False))
    time.sleep(0.01)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, False))

def zoom_in(n=1):
    for _ in range(n):
        key_combo(0x37, 24)
        time.sleep(0.05)

def zoom_out(n=1):
    for _ in range(n):
        key_combo(0x37, 27)
        time.sleep(0.05)

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

cx, cy = 330, 400

# =============================================
# ALIEN — Full technique suite
# =============================================

# ---- 1. Head silhouette (large, tapered, organic) ----
head_ctrl = [
    (330, 260),     # top point
    (318, 268),     # upper left taper
    (300, 290),     # left wide
    (295, 310),     # lower left
    (300, 330),     # jaw left
    (310, 345),     # neck left
    (320, 355),     # shoulder left
    (340, 355),     # shoulder right
    (350, 345),     # neck right
    (360, 330),     # jaw right
    (365, 310),     # lower right
    (360, 290),     # right wide
    (342, 268),     # upper right taper
]
activate_pen()
stroke(catmull(head_ctrl, 30))
time.sleep(0.15)

# ---- 2. Body (slender, tapering) ----
body_ctrl = [
    (318, 355),     # left shoulder
    (312, 380),     # left chest
    (310, 410),     # left waist
    (312, 440),     # left hip
    (318, 465),     # left base
    (342, 465),     # right base
    (348, 440),     # right hip
    (350, 410),     # right waist
    (348, 380),     # right chest
    (342, 355),     # right shoulder
]
activate_pen()
stroke(catmull(body_ctrl, 25))
time.sleep(0.12)

# ---- 3. Left arm ----
arm_l_ctrl = [
    (316, 360),
    (298, 375),
    (280, 395),
    (268, 420),
    (262, 445),
    (260, 465),
    (262, 475),
]
activate_pen()
stroke(catmull(arm_l_ctrl, 18))
time.sleep(0.08)

# Left hand (3 fingers)
for fx, fy, fdir in [(260, 475, -8), (265, 478, 0), (272, 474, 8)]:
    activate_pen()
    stroke([(fx, fy), (fx+fdir, fy+14)])
    time.sleep(0.03)

time.sleep(0.1)

# ---- 4. Right arm ----
arm_r_ctrl = [
    (344, 360),
    (362, 375),
    (380, 395),
    (392, 420),
    (398, 445),
    (400, 465),
    (398, 475),
]
activate_pen()
stroke(catmull(arm_r_ctrl, 18))
time.sleep(0.08)

# Right hand (3 fingers)
for fx, fy, fdir in [(398, 475, 8), (395, 478, 0), (388, 474, -8)]:
    activate_pen()
    stroke([(fx, fy), (fx+fdir, fy+14)])
    time.sleep(0.03)

time.sleep(0.15)

# ---- 5. Left eye (large, almond-shaped) ----
eye_l_ctrl = [
    (307, 295),
    (302, 300),
    (300, 308),
    (305, 314),
    (314, 312),
    (318, 305),
    (315, 298),
]
activate_pen()
stroke(catmull(eye_l_ctrl, 15))
time.sleep(0.06)

# Left pupil (filled with zigzag)
for ey in range(302, 310, 3):
    activate_pen()
    stroke([(305, ey), (313, ey)])
    time.sleep(0.015)

time.sleep(0.08)

# ---- 6. Right eye ----
eye_r_ctrl = [
    (353, 295),
    (358, 300),
    (360, 308),
    (355, 314),
    (346, 312),
    (342, 305),
    (345, 298),
]
activate_pen()
stroke(catmull(eye_r_ctrl, 15))
time.sleep(0.06)

# Right pupil
for ey in range(302, 310, 3):
    activate_pen()
    stroke([(347, ey), (355, ey)])
    time.sleep(0.015)

time.sleep(0.12)

# ---- 7. Mouth / breathing slit ----
activate_pen()
stroke([(320, 338), (330, 340), (340, 338)])
time.sleep(0.05)

# ---- 8. Nostril dots ----
for nx, ny in [(324, 325), (336, 325)]:
    activate_pen()
    stroke([(nx-2, ny), (nx+2, ny)])
    time.sleep(0.02)

time.sleep(0.15)

# ---- 9. Zoom in 2.5x for head ridge details ----
zoom_in(3)
time.sleep(0.25)

# Head ridges (bony crest lines on top of head)
for ry in range(266, 292, 6):
    spread = int((ry - 260) / 3)
    activate_pen()
    stroke([(330 - spread, ry), (330 + spread, ry)])
    time.sleep(0.015)

time.sleep(0.1)

# Skin texture lines on head (fine, delicate at zoom)
for sy in range(295, 335, 8):
    offset = int(5 * math.sin(sy * 0.3))
    activate_pen()
    stroke([(302 + offset, sy), (358 + offset, sy)])
    time.sleep(0.015)

time.sleep(0.1)

# ---- 10. Chest emblem (glowing symbol) ----
activate_pen()
stroke(catmull([
    (330, 380), (324, 385), (320, 392), (324, 399),
    (330, 404), (336, 399), (340, 392), (336, 385),
], 10))
time.sleep(0.04)

# Inner emblem detail
activate_pen()
stroke([(327, 392), (330, 396), (333, 392)])
time.sleep(0.04)

# Emblem rays
for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
    ra = math.radians(angle)
    activate_pen()
    stroke([(330 + 10 * math.cos(ra), 392 + 10 * math.sin(ra)),
            (330 + 16 * math.cos(ra), 392 + 16 * math.sin(ra))])
    time.sleep(0.015)

time.sleep(0.1)

# ---- 11. Zoom back out ----
zoom_out(3)
time.sleep(0.25)

print("Alien drawn!")
