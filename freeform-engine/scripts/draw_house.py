"""Small house sketch — charming cottage with Catmull-Rom curves, detail, and atmosphere."""
import time, os, subprocess, math, sys
sys.path.insert(0, os.path.expanduser('~/.opencode_knowledge/scripts'))
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from freeform_core import *
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.005)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def catmull(pts, n=40):
    out = []
    for i in range(len(pts)):
        p0=pts[max(0,i-1)]; p1=pts[i]; p2=pts[min(len(pts)-1,i+1)]; p3=pts[min(len(pts)-1,i+2)]
        for t in [j/n for j in range(n)]:
            t2=t*t; t3=t2*t
            x=0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y=0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    return out

def circle(cx, cy, r, n=30):
    return [(cx+r*math.cos(2*math.pi*i/n), cy+r*math.sin(2*math.pi*i/n)) for i in range(n+1)]

def bold(pts, slp=0.005, offsets=[-3, 0, 3]):
    for dx in offsets:
        activate_pen()
        stroke([(x+dx, y+dx*0.3) for (x,y) in pts], slp)
        time.sleep(0.04)

# Setup
print("Setting up Freeform...")
activate_freeform()
new_board()
time.sleep(1.5)

# ── Ground line ──
print("Ground line...")
activate_pen()
stroke([(110, 480), (560, 480)], 0.005); time.sleep(0.05)
bold([(110, 480), (560, 480)], 0.005)

# ── House body (front wall) ──
print("House body...")
walls = [(180, 470), (180, 380), (480, 380), (480, 470)]
bold(walls, 0.005)
# Subtle texture line
activate_pen(); stroke([(185, 470), (185, 380)], 0.005); time.sleep(0.05)
activate_pen(); stroke([(475, 470), (475, 380)], 0.005); time.sleep(0.05)

# ── Pitched roof (Catmull-Rom curve for elegant peak) ──
print("Roof...")
roof_right = catmull([(330, 290), (370, 305), (430, 335), (470, 358), (480, 365)], 40)
roof_left = catmull([(330, 290), (290, 305), (230, 335), (190, 358), (180, 365)], 40)
# Draw right side
activate_pen(); stroke(roof_right, 0.005); time.sleep(0.05)
bold(roof_right, 0.005)
# Draw left side
activate_pen(); stroke(roof_left, 0.005); time.sleep(0.05)
bold(roof_left, 0.005)

# ── Vertical plank/sheathing lines on roof (texture) ──
print("Roof texture...")
for ridge_x in range(220, 470, 22):
    if ridge_x < 330:
        ratio = (330 - ridge_x) / 150
        y_top = 290 + ratio * 75
        y_bot = 365
    else:
        ratio = (ridge_x - 330) / 150
        y_top = 290 + ratio * 75
        y_bot = 365
    activate_pen()
    stroke([(ridge_x, y_top), (ridge_x, y_bot)], 0.003)
    time.sleep(0.05)

# Horizontal base of roof
activate_pen(); stroke([(180, 365), (480, 365)], 0.005); time.sleep(0.05)
bold([(180, 365), (480, 365)], 0.005)

# ── Door ──
print("Door...")
door = catmull([(305, 470), (305, 410), (310, 405), (350, 405), (355, 410), (355, 470), (305, 470)], 30)
bold(door, 0.005)
# Door knob
activate_pen(); stroke(circle(345, 440, 2.5, 12), 0.003); time.sleep(0.03)
# Door panel lines
for py_off in [-15, 15]:
    activate_pen(); stroke([(310, 440 + py_off), (350, 440 + py_off)], 0.003); time.sleep(0.04)

# ── Windows (left and right) ──
print("Windows...")
# Left window
lw = catmull([(215, 380), (215, 420), (260, 420), (260, 380), (215, 380)], 25)
bold(lw, 0.005)
# Window cross
activate_pen(); stroke([(215, 400), (260, 400)], 0.003); time.sleep(0.03)
activate_pen(); stroke([(237, 380), (237, 420)], 0.003); time.sleep(0.03)
# Window sill
activate_pen(); stroke([(210, 422), (265, 422)], 0.005); time.sleep(0.03)
bold([(210, 422), (265, 422)], 0.004, [-2, 0, 2])

# Right window
rw = catmull([(395, 380), (395, 420), (440, 420), (440, 380), (395, 380)], 25)
bold(rw, 0.005)
activate_pen(); stroke([(395, 400), (440, 400)], 0.003); time.sleep(0.03)
activate_pen(); stroke([(417, 380), (417, 420)], 0.003); time.sleep(0.03)
activate_pen(); stroke([(390, 422), (445, 422)], 0.005); time.sleep(0.03)
bold([(390, 422), (445, 422)], 0.004, [-2, 0, 2])

# ── Chimney (right side) ──
print("Chimney...")
chim = [(420, 310), (420, 360), (445, 360), (445, 305), (420, 310)]
activate_pen(); stroke(chim, 0.005); time.sleep(0.05)
bold(chim, 0.004, [-2, 0, 2])
# Chimney cap
cap = [(418, 305), (418, 300), (447, 300), (447, 305), (418, 305)]
activate_pen(); stroke(cap, 0.005); time.sleep(0.05)
bold(cap, 0.004, [-2, 0, 2])

# ── Smoke (Catmull-Rom curls above chimney) ──
print("Smoke...")
smoke1 = catmull([(432, 290), (438, 280), (435, 270), (430, 265)], 20)
activate_pen(); stroke(smoke1, 0.003); time.sleep(0.04)
smoke2 = catmull([(425, 260), (415, 255), (415, 245), (425, 240)], 20)
activate_pen(); stroke(smoke2, 0.003); time.sleep(0.04)
smoke3 = catmull([(432, 235), (438, 225), (435, 215), (428, 213)], 20)
activate_pen(); stroke(smoke3, 0.003); time.sleep(0.04)

# ── Tree (left of house) ──
print("Tree...")
# Trunk
activate_pen(); stroke([(140, 480), (140, 420)], 0.005); time.sleep(0.04)
activate_pen(); stroke([(155, 480), (155, 425)], 0.005); time.sleep(0.04)
# Foliage (3 circles for triangle effect)
activate_pen(); stroke(circle(148, 395, 28, 30), 0.005); time.sleep(0.05)
bold(circle(148, 395, 28, 30), 0.004, [-2, 0, 2])
activate_pen(); stroke(circle(148, 370, 22, 25), 0.005); time.sleep(0.05)
activate_pen(); stroke(circle(148, 348, 16, 20), 0.005); time.sleep(0.05)
# Some leaf detail
for lx, ly in [(130, 395), (165, 393), (145, 380), (155, 360), (138, 356)]:
    activate_pen(); stroke(circle(lx, ly, 4, 12), 0.003); time.sleep(0.02)

# ── Bushes (right of house) ──
print("Bushes...")
for bx in [490, 510, 530]:
    activate_pen(); stroke(circle(bx, 467, 12, 20), 0.005); time.sleep(0.04)
    bold(circle(bx, 467, 12, 20), 0.004, [-2, 0, 2])
# Small path stones
for px in [510, 535]:
    activate_pen(); stroke(circle(px, 481, 5, 15), 0.003); time.sleep(0.03)

# ── Pathway leading to door ──
print("Pathway...")
path = catmull([(330, 480), (335, 490), (340, 498), (345, 505), (350, 512), (358, 518)], 25)
activate_pen(); stroke(path, 0.005); time.sleep(0.04)
# Path second edge
path2 = catmull([(322, 480), (320, 490), (322, 498), (325, 505), (328, 512), (330, 518)], 25)
activate_pen(); stroke(path2, 0.005); time.sleep(0.04)

# ── Sun in upper right ──
print("Sun...")
activate_pen(); stroke(circle(560, 280, 22, 30), 0.005); time.sleep(0.05)
activate_pen(); stroke(circle(560, 280, 18, 25), 0.005); time.sleep(0.04)
# Sun rays
for ang in range(0, 360, 30):
    a = math.radians(ang)
    x0 = 560 + 25*math.cos(a); y0 = 280 + 25*math.sin(a)
    x1 = 560 + 35*math.cos(a); y1 = 280 + 35*math.sin(a)
    activate_pen(); stroke([(x0, y0), (x1, y1)], 0.003); time.sleep(0.025)

# ── Cloud in upper left ──
print("Cloud...")
cloud = catmull([(95, 240), (110, 232), (135, 234), (155, 240), (170, 245), (160, 252), (135, 255), (110, 252), (95, 248)], 30)
activate_pen(); stroke(cloud, 0.005); time.sleep(0.05)
bold(cloud, 0.005)

# ── Fence (right foreground) ──
print("Fence...")
for fx in range(380, 475, 12):
    activate_pen(); stroke([(fx, 480), (fx, 460)], 0.003); time.sleep(0.02)
activate_pen(); stroke([(378, 462), (475, 462)], 0.003); time.sleep(0.04)
activate_pen(); stroke([(378, 470), (475, 470)], 0.003); time.sleep(0.04)

print("\n✓ House sketch complete!")
time.sleep(0.5)
