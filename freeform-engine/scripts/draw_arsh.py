"""ARSH in stylish font — sleek, bold, geometric with smooth curves."""
import time, os, subprocess, math, sys
sys.path.insert(0, os.path.expanduser('~/.opencode_knowledge/scripts'))
import math as _math  # ensure math is available
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from freeform_core import *
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.005)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def bold_stroke(pts, slp=0.005):
    """Draw with 5 parallel offset passes."""
    for dx in [-4, -2, 0, 2, 4]:
        activate_pen()
        stroke([(x+dx, y+dx*0.3) for (x,y) in pts], slp)
        time.sleep(0.04)

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


def _unused_junk(): pass  # placeholder to keep edit working


# Setup
print("Setting up Freeform...")
activate_freeform()
new_board()
time.sleep(1.5)

# Each letter center
TOP, BOT = 320, 440
h_bold = 3  # number of bold passes for vertical strokes (denser for verticals)

def vstroke(x, y0, y1, n=20, bold=3):
    activate_pen()
    stroke([(x + i*0, y0 + (y1-y0)*i/n) for i in range(n+1)], 0.005)
    time.sleep(0.05)
    for d in range(bold):
        activate_pen()
        stroke([(x + (d-1)*2, y0 + i*(y1-y0)/n) for i in range(n+1)], 0.005)
        time.sleep(0.04)

def diagonal_stroke(x0, y0, x1, y1, n=30, bold=3):
    pts = [(x0 + (x1-x0)*i/n, y0 + (y1-y0)*i/n) for i in range(n+1)]
    activate_pen()
    stroke(pts, 0.005)
    time.sleep(0.05)
    for d in [-2, 0, 2]:
        activate_pen()
        stroke([(x+d, y + d*0.3) for (x,y) in pts], 0.005)
        time.sleep(0.04)

# ── LETTER A (x=170-220, y=320-440) ──
print("Drawing A...")
diagonal_stroke(170, 440, 195, 320, n=40, bold=2)  # left diagonal
diagonal_stroke(195, 320, 220, 440, n=40, bold=2)  # right diagonal
# Crossbar with bold
vstroke(180, 388, 388, n=20, bold=3)
activate_pen()
stroke([(180, 388), (210, 388)], 0.005)
time.sleep(0.05)
for dx in [-2, 0, 2]:
    activate_pen()
    stroke([(180+dx, 388+dx*0.3), (210+dx, 388+dx*0.3)], 0.005)
    time.sleep(0.04)

time.sleep(0.15)

# ── LETTER R (x=255-310, y=320-440) ──
print("Drawing R...")
# Vertical left stem
vstroke(255, 320, 440, n=40, bold=3)
# Bowl (top: rounded curve from (255,320) right to (305,340) down to (255,365))
bowl_top = catmull([(255, 320), (270, 320), (295, 320), (308, 330), (308, 348), (295, 360), (270, 360), (255, 360)], 40)
bold_stroke(bowl_top, 0.005)
# Inside of bowl
bowl_in = catmull([(258, 323), (270, 323), (290, 328), (300, 335), (300, 345), (290, 355), (270, 357)], 30)
activate_pen(); stroke(bowl_in, 0.005); time.sleep(0.05)
# Leg
diagonal_stroke(280, 360, 310, 440, n=30, bold=2)
time.sleep(0.15)

# ── LETTER S (x=355-440, y=320-440, smooth curve) ──
print("Drawing S...")
# Smooth S using Catmull-Rom for both halves
s_top = catmull([
    (420, 340), (440, 335), (445, 320),
    (425, 320), (390, 320), (370, 335), (360, 350),
    (370, 360), (385, 370), (415, 375), (440, 385), (445, 405),
    (440, 425), (415, 440), (390, 440),
    (370, 438), (355, 425)
], 60)
bold_stroke(s_top, 0.005)
time.sleep(0.15)

# ── LETTER H (x=480-550, y=320-440) ──
print("Drawing H...")
# Left vertical
vstroke(485, 320, 440, n=40, bold=3)
# Right vertical
vstroke(545, 320, 440, n=40, bold=3)
# Crossbar (thick)
crossbar = [(490, 380), (540, 380)]
bold_stroke(crossbar, 0.005)
# Make crossbar thick with 3 lines
for y_off in [-3, 0, 3]:
    activate_pen()
    stroke([(485, 380 + y_off), (545, 380 + y_off)], 0.005)
    time.sleep(0.05)

time.sleep(0.15)

# ── DECORATIVE FLOURISH (underline + small ornaments) ──
print("Adding decorative flourishes...")
# Long underline
underline = catmull([(155, 465), (180, 467), (220, 463), (260, 467),
                     (310, 463), (360, 467), (410, 463), (450, 467),
                     (490, 463), (530, 467), (565, 463)], 30)
bold_stroke(underline, 0.005)

# Small stars at each end
for star_x in [145, 575]:
    activate_pen()
    stroke(circle(star_x, 465, 6, 20), 0.005); time.sleep(0.03)
    activate_pen()
    stroke(circle(star_x, 465, 3, 15), 0.005); time.sleep(0.03)

print("\n✓ ARSH complete!")
time.sleep(0.5)
