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
    click(404, 55,)
    time.sleep(0.15)
    click(395, 509)
    time.sleep(0.25)

def catmull(pts, n=45):
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

def zigzag_fill(x1, y1, x2, y2, step=5):
    pts = []
    for i, y in enumerate(range(y1, y2, step)):
        if i % 2 == 0:
            pts.append((x1, y))
            pts.append((x2, y))
        else:
            pts.append((x2, y))
            pts.append((x1, y))
    stroke(pts)

def triangle_fill(tx, ty, w, h, step=5):
    pts = []
    for y in range(ty, ty+h, step):
        ratio = (y - ty) / h
        half = int(w/2 * (1 - ratio))
        pts.append((tx - half, y))
        pts.append((tx + half, y))
    stroke(pts)

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
# RECALIBRATED: Mountain Lake Scene
# Principles applied: dense single curves, zigzag fills, area-balanced, min strokes
# =============================================

# ---- 1. Mountain silhouette - single dense curve (n=45), NO parallel strokes ----
m_ctrl = [
    (60, cy+20),      # base left
    (80, cy-30),      # foothill
    (110, cy-120),    # first peak climb
    (140, cy-170),    # peak 1
    (170, cy-140),    # valley 1
    (200, cy-195),    # peak 2 (secondary)
    (230, cy-160),    # valley 2
    (280, cy-235),    # peak 3 (main, tallest)
    (330, cy-190),    # valley 3
    (370, cy-220),    # peak 4
    (410, cy-170),    # valley 4
    (440, cy-200),    # peak 5
    (470, cy-150),    # valley 5
    (500, cy-110),    # lower slope
    (530, cy-50),     # foothill right
    (560, cy+20),     # base right
]
m = catmull(m_ctrl)
activate_pen()
stroke(m)
time.sleep(0.2)

# ---- 2. Snow cap on main peak - single dense curve ----
snow_ctrl = [
    (262, cy-210),
    (272, cy-228),
    (280, cy-235),
    (288, cy-228),
    (298, cy-208),
    (292, cy-200),
    (280, cy-195),
    (270, cy-200),
    (262, cy-210),
]
activate_pen()
stroke(catmull(snow_ctrl, 25))
time.sleep(0.15)

# ---- 3. Lake outline - single dense curve ----
lake_ctrl = [
    (100, cy+15),
    (80, cy+40),
    (90, cy+90),
    (130, cy+130),
    (210, cy+145),
    (330, cy+150),
    (450, cy+145),
    (520, cy+130),
    (550, cy+80),
    (540, cy+40),
    (520, cy+15),
]
activate_pen()
stroke(catmull(lake_ctrl, 30))
time.sleep(0.2)

# ---- 4. Lake water fill - ONE zigzag stroke (replaces 50+ hatch lines) ----
activate_pen()
zigzag_fill(110, cy+25, 530, cy+140, step=6)
time.sleep(0.2)

# ---- 5. Lake reflection of mountains - single undulating curve ----
reflect_ctrl = [
    (100, cy+40), (130, cy+60), (170, cy+50), (210, cy+70),
    (260, cy+55), (310, cy+75), (360, cy+60), (410, cy+70),
    (460, cy+55), (500, cy+65), (540, cy+50),
]
activate_pen()
stroke(catmull(reflect_ctrl, 20))
time.sleep(0.15)

# ---- 6. Pine trees - each triangle_fill is ONE stroke ----
# Tree 1 (left shore, large)
activate_pen()
triangle_fill(160, cy+5, 40, 70, 4)
time.sleep(0.08)
activate_pen()
stroke([(158, cy+70), (162, cy+70), (162, cy+90), (158, cy+90)])
time.sleep(0.12)

# Tree 2 (left shore, medium)
activate_pen()
triangle_fill(210, cy+15, 30, 50, 4)
time.sleep(0.08)
activate_pen()
stroke([(208, cy+65), (212, cy+65), (212, cy+80), (208, cy+80)])
time.sleep(0.12)

# Tree 3 (right shore, large)
activate_pen()
triangle_fill(460, cy+5, 45, 75, 4)
time.sleep(0.08)
activate_pen()
stroke([(458, cy+75), (462, cy+75), (462, cy+95), (458, cy+95)])
time.sleep(0.12)

# Tree 4 (right shore, small)
activate_pen()
triangle_fill(500, cy+25, 25, 40, 4)
time.sleep(0.08)
activate_pen()
stroke([(498, cy+65), (502, cy+65), (502, cy+78), (498, cy+78)])
time.sleep(0.15)

# ---- 7. Stars in sky - tiny crosses, efficient short strokes ----
stars = [(150, cy-200), (220, cy-210), (350, cy-225), (420, cy-200), (480, cy-190)]
for sx, sy in stars:
    activate_pen()
    stroke([(sx-3, sy), (sx+3, sy)])
    time.sleep(0.04)
    activate_pen()
    stroke([(sx, sy-3), (sx, sy+3)])
    time.sleep(0.04)

time.sleep(0.15)

# ---- 8. Ground shoreline - single curve ----
shore_ctrl = [(90, cy+18), (160, cy+15), (240, cy+20), (330, cy+18), (420, cy+22), (510, cy+15), (540, cy+18)]
activate_pen()
stroke(catmull(shore_ctrl, 15))

print("Recalibrated landscape drawn!")
