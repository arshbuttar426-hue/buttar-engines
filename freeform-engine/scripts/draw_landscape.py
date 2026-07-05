import time, os, subprocess, math
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts):
    for px, py in pts:
        time.sleep(0.008)
        click(px, py)
    time.sleep(0.03)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.01)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    click(404, 55)
    time.sleep(0.18)
    click(395, 509)
    time.sleep(0.3)

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

cx, cy = 330, 420

# =============================================
# MOUNTAIN LANDSCAPE
# =============================================

# ---- 1. Mountain 1 (left, tall, rugged peak) ----
m1_ctrl = [
    (80, cy+40),     # base left
    (90, cy+20),     # foothill
    (120, cy-40),    # lower slope
    (150, cy-100),   # mid slope
    (170, cy-140),   # upper slope
    (180, cy-170),   # shoulder
    (185, cy-180),   # peak left
    (190, cy-190),   # main peak
    (195, cy-182),   # peak right
    (210, cy-150),   # upper slope right
    (230, cy-100),   # mid slope right
    (260, cy-40),    # lower slope right
    (290, cy+10),    # foothill right
    (310, cy+40),    # base right (valley)
]
for dx in [-2, 0, 2]:
    activate_pen()
    stroke(catmull(m1_ctrl, 22))
    time.sleep(0.12)

time.sleep(0.25)

# ---- 2. Mountain 2 (right, taller, more jagged) ----
m2_ctrl = [
    (300, cy+40),     # base left (valley)
    (320, cy),        # foothill
    (340, cy-50),     # lower slope
    (360, cy-120),    # mid slope
    (370, cy-180),    # upper slope
    (375, cy-210),    # shoulder left
    (382, cy-235),    # peak left
    (390, cy-245),    # main peak
    (398, cy-230),    # peak right
    (410, cy-190),    # upper slope right
    (425, cy-130),    # mid slope right
    (450, cy-70),     # lower slope right
    (470, cy-20),     # foothill right
    (500, cy+20),     # base right
    (530, cy+40),     # base far right
]
for dx in [-2, 0, 2]:
    activate_pen()
    stroke(catmull(m2_ctrl, 22))
    time.sleep(0.12)

time.sleep(0.25)

# ---- 3. Mountain 3 (background left, distant) ----
m3_ctrl = [(50, cy+20), (60, cy-30), (80, cy-80), (95, cy-110), (100, cy-100), (115, cy-60), (130, cy-20), (150, cy+20)]
activate_pen()
stroke(catmull(m3_ctrl, 18))
time.sleep(0.2)

# ---- 4. Snow caps on peaks (hatch pattern) ----
# M1 snow field
for y in range(cy-190, cy-150, 3):
    width = int(30 * (1 - ((y-(cy-190))/40)**2))
    if width > 2:
        activate_pen()
        stroke([(190-width, y), (190+width, y)])
        time.sleep(0.02)

time.sleep(0.15)

# M2 snow field
for y in range(cy-245, cy-190, 3):
    width = int(35 * (1 - ((y-(cy-245))/55)**2))
    if width > 2:
        activate_pen()
        stroke([(390-width, y), (390+width, y)])
        time.sleep(0.02)

time.sleep(0.25)

# ---- 5. River flowing from valley between mountains ----
# River starts between the two mountains and flows down, meandering and widening
river_ctrl = [
    (295, cy+35),     # start (between mountains)
    (290, cy+55),     # upper river
    (300, cy+80),     # meander right
    (320, cy+100),    # curve
    (310, cy+130),    # meander left
    (330, cy+160),    # curve right
    (320, cy+190),    # meander left
    (340, cy+220),    # widen
    (330, cy+250),    # meander
    (350, cy+280),    # widen more
    (340, cy+310),    # meander
    (360, cy+340),    # lower river
]

# Left bank
lbank = catmull([(p[0]-3-int(i*0.5), p[1]) for i,p in enumerate(river_ctrl)], 18)
activate_pen()
stroke(lbank)
time.sleep(0.12)

# Right bank
rbank = catmull([(p[0]+3+int(i*0.5), p[1]) for i,p in enumerate(river_ctrl)], 18)
activate_pen()
stroke(rbank)
time.sleep(0.12)

# River flow lines (internal texture)
for i in range(3, len(river_ctrl)-1, 2):
    p = river_ctrl[i]
    w = 3 + i * 0.5
    activate_pen()
    stroke([(p[0]-w+2, p[1]), (p[0]+w-2, p[1])])
    time.sleep(0.02)

time.sleep(0.3)

# ---- 6. Trees (left bank) ----
# Pine tree 1 (left foreground)
def draw_tree(tx, ty, h, w):
    levels = 4
    for i in range(levels):
        level_h = h // levels
        level_w = w * (1 - i * 0.15)
        y0 = ty + i * level_h
        y1 = y0 + level_h - 2
        # Triangle shape
        pts = []
        for t in range(0, 11):
            f = t / 10
            px = tx - level_w/2 + f * level_w
            py = y0 + f * (y1 - y0)
            pts.append((px, py))
        for dx in [-2, 0, 2]:
            activate_pen()
            stroke([(x+dx, y) for (x,y) in pts])
            time.sleep(0.06)
    # Trunk
    activate_pen()
    stroke([(tx-2, ty+h-5), (tx+2, ty+h-5), (tx+2, ty+h+15), (tx-2, ty+h+15)])
    time.sleep(0.08)

draw_tree(140, cy-130, 80, 50)
time.sleep(0.2)
draw_tree(200, cy-80, 60, 35)
time.sleep(0.2)

# ---- 7. Trees (right bank) ----
draw_tree(430, cy-140, 90, 55)
time.sleep(0.2)
draw_tree(480, cy-50, 50, 30)
time.sleep(0.2)
draw_tree(380, cy-20, 40, 25)

time.sleep(0.3)

# ---- 8. Decorative clouds ----
cloud1 = catmull([(100, cy-210), (120, cy-225), (140, cy-230), (160, cy-225), (180, cy-220), (170, cy-215), (155, cy-212), (140, cy-215), (120, cy-215), (100, cy-210)], 12)
activate_pen()
stroke(cloud1)
time.sleep(0.1)

cloud2 = catmull([(380, cy-270), (400, cy-282), (420, cy-285), (440, cy-280), (450, cy-275), (435, cy-270), (420, cy-268), (400, cy-272), (380, cy-270)], 12)
activate_pen()
stroke(cloud2)
time.sleep(0.1)

# ---- 9. Ground/grass line at bottom ----
for x in range(70, 530, 6):
    h = 5 + int(math.sin(x * 0.3) * 3)
    activate_pen()
    stroke([(x, cy+45), (x+2, cy+45-h)])
    time.sleep(0.01)

print("Landscape drawn!")
