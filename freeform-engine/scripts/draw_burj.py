import time, os, subprocess, math
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

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

def catmull(pts, n=20):
    out = []
    for i in range(len(pts)):
        p0=pts[max(0,i-1)]; p1=pts[i]; p2=pts[min(len(pts)-1,i+1)]; p3=pts[min(len(pts)-1,i+2)]
        for t in [j/n for j in range(n)]:
            t2=t*t; t3=t2*t
            x=0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y=0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    return out

subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True); time.sleep(0.8)
subprocess.run(['osascript', '-e', '''
tell app "System Events" tell process "Freeform"
    click menu item "New Board" of menu "File" of menu bar 1
end tell'''], capture_output=True); time.sleep(1.2)

cx, cy = 330, 420

# =============================================
# BURJ KHALIFA — The World's Tallest Building
# Stepped, tiered taper with Y-shaped plan
# =============================================

# ---- 1. Main structure: stepped silhouette ----
# Each tier is drawn as a trapezoid, getting narrower
tiers = [
    (240, 465, 420, 465, 420, 425, 240, 425),   # base tier
    (248, 420, 412, 420, 412, 385, 248, 385),    # tier 2
    (256, 380, 404, 380, 404, 348, 256, 348),    # tier 3
    (263, 343, 397, 343, 397, 312, 263, 312),    # tier 4
    (270, 307, 390, 307, 390, 278, 270, 278),    # tier 5
    (277, 273, 383, 273, 383, 245, 277, 245),    # tier 6
    (284, 240, 376, 240, 376, 213, 284, 213),    # tier 7
    (291, 208, 369, 208, 369, 182, 291, 182),    # tier 8
    (298, 177, 362, 177, 362, 152, 298, 152),    # tier 9
    (305, 147, 355, 147, 355, 123, 305, 123),    # tier 10
    (312, 118, 348, 118, 348, 95, 312, 95),      # tier 11
    (319, 90, 341, 90, 341, 68, 319, 68),        # tier 12
]

for (x1, y1, x2, y2, x3, y3, x4, y4) in tiers:
    activate_pen()
    stroke([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    time.sleep(0.02)

time.sleep(0.12)

# ---- 2. Central spine (Y-plan ridge visible from front) ----
activate_pen()
stroke([(330, 465), (330, 68)])
time.sleep(0.04)

# ---- 3. Side wings (3-wing Y-plan creates 2 visible ridges) ----
activate_pen()
stroke([(310, 465), (315, 68)])
time.sleep(0.03)
activate_pen()
stroke([(350, 465), (345, 68)])
time.sleep(0.03)

# ---- 4. Horizontal light bands at each tier top ----
for (x1, y1, x2, y2, x3, y3, x4, y4) in tiers:
    # Top edge of each tier (double line for emphasis)
    activate_pen()
    stroke([(x4, y4), (x3, y3)])
    time.sleep(0.008)
    # Light band below
    band_y = y4 + 2
    band_x1 = x4 + 2
    band_x2 = x3 - 2
    if band_x2 > band_x1:
        activate_pen()
        stroke([(band_x1, band_y), (band_x2, band_y)])
        time.sleep(0.005)

time.sleep(0.1)

# ---- 5. Vertical window lines (suggesting thousands of windows) ----
for wx in range(260, 420, 6):
    for ty in tiers:
        (x1, y1, x2, y2, x3, y3, x4, y4) = ty
        if x4 < wx < x3 and y4 < 465:
            activate_pen()
            stroke([(wx, y4 + 3), (wx, y4 + 15)])
            time.sleep(0.002)

time.sleep(0.1)

# ---- 6. Spire (the top needle) ----
activate_pen()
stroke([(328, 68), (328, 35)])
time.sleep(0.025)
activate_pen()
stroke([(332, 68), (332, 35)])
time.sleep(0.025)
# Spire tip
activate_pen()
stroke([(328, 35), (330, 28), (332, 35)])
time.sleep(0.025)

time.sleep(0.1)

# ---- 7. Base detail (the podium level) ----
# Wide podium base
activate_pen()
stroke([(220, 480), (440, 480), (440, 465), (220, 465)])
time.sleep(0.03)

# Podium vertical lines
for px in range(230, 440, 8):
    activate_pen()
    stroke([(px, 480), (px, 466)])
    time.sleep(0.003)

time.sleep(0.08)

# ---- 8. Ground line ----
activate_pen()
stroke([(170, 485), (490, 485)])
time.sleep(0.025)
activate_pen()
stroke([(170, 490), (490, 490)])
time.sleep(0.025)

# ---- 9. Small surrounding buildings (for scale) ----
# Left buildings
for bx, bw, bh in [(190, 20, 30), (215, 15, 20), (175, 12, 18)]:
    activate_pen()
    stroke([(bx, 485), (bx+bw, 485), (bx+bw, 485-bh), (bx, 485-bh)])
    time.sleep(0.015)

# Right buildings
for bx, bw, bh in [(440, 18, 35), (462, 22, 25), (428, 14, 22)]:
    activate_pen()
    stroke([(bx, 485), (bx+bw, 485), (bx+bw, 485-bh), (bx, 485-bh)])
    time.sleep(0.015)

time.sleep(0.1)

# ---- 10. Zoom in 3x for spire details ----
zi(3); time.sleep(0.2)

# Spire cross-bars / structural details
for sy in range(30, 65, 5):
    spread = 1 + (65 - sy) // 10
    activate_pen()
    stroke([(330 - spread, sy), (330 + spread, sy)])
    time.sleep(0.008)

# Spire antenna
activate_pen()
stroke([(330, 28), (330, 18)])
time.sleep(0.015)

# Top beacon light
activate_pen()
stroke([(328, 17), (332, 17), (332, 15), (328, 15)])
time.sleep(0.015)

time.sleep(0.08)

# ---- 11. Zoom in more for architectural patterns ----
zi(3); time.sleep(0.15)

# At 9x zoom, visible canvas is narrow — draw facade pattern
# Tier transitions (the stepped notches)
for y in range(50, 85, 4):
    activate_pen()
    stroke([(318, y), (342, y)])
    time.sleep(0.005)

# Diamond patterns inspired by Islamic geometry
for dx in range(-12, 14, 8):
    for dy in range(-20, 10, 8):
        px = 330 + dx
        py = 60 + dy
        activate_pen()
        stroke([(px, py-3), (px+3, py), (px, py+3), (px-3, py)])
        time.sleep(0.005)

time.sleep(0.08)

# ---- 12. Zoom back out ----
zo(6); time.sleep(0.3)

print("Burj Khalifa drawn!")
