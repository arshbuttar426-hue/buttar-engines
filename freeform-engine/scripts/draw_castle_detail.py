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
    time.sleep(0.12)
    click(395, 509)
    time.sleep(0.2)

def key_combo(mod_key, char_key):
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, True))
    time.sleep(0.03)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, True))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, False))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, False))

def zoom_in(n=1):
    for _ in range(n):
        key_combo(0x37, 24)
        time.sleep(0.08)

def zoom_out(n=1):
    for _ in range(n):
        key_combo(0x37, 27)
        time.sleep(0.08)

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
# PHASE 1: NORMAL ZOOM — Simple castle structure
# =============================================

# Keep
activate_pen()
stroke([(260, 300), (400, 300), (400, 420), (260, 420)])
time.sleep(0.06)

# Crenellations on keep
for x in range(258, 404, 16):
    activate_pen()
    stroke([(x, 300), (x, 285)])
    time.sleep(0.03)

time.sleep(0.1)

# Keep roof
activate_pen()
stroke([(255, 300), (330, 260), (405, 300)])
time.sleep(0.06)

# Left tower
activate_pen()
stroke([(190, 350), (220, 350), (220, 430), (190, 430)])
time.sleep(0.05)
activate_pen()
stroke([(190, 350), (205, 335), (220, 350)])
time.sleep(0.05)

# Right tower
activate_pen()
stroke([(440, 350), (470, 350), (470, 430), (440, 430)])
time.sleep(0.05)
activate_pen()
stroke([(440, 350), (455, 335), (470, 350)])
time.sleep(0.05)

# Curtain walls left
activate_pen()
stroke([(220, 370), (260, 370), (260, 420)])
time.sleep(0.04)
# Curtain walls right
activate_pen()
stroke([(400, 370), (440, 370), (440, 420)])
time.sleep(0.04)

# Gatehouse
activate_pen()
stroke([(290, 420), (370, 420), (370, 460), (290, 460)])
time.sleep(0.05)

# Gate arch
arch_ctrl = [(314, 460), (314, 442), (330, 435), (346, 442), (346, 460)]
activate_pen()
stroke(catmull(arch_ctrl, 15))
time.sleep(0.05)

# Moat
activate_pen()
stroke([(170, 475), (490, 475), (500, 500), (160, 500)])
time.sleep(0.05)

# Drawbridge
activate_pen()
stroke([(314, 460), (346, 460), (346, 480), (314, 480)])
time.sleep(0.05)

time.sleep(0.2)

# =============================================
# PHASE 2: ZOOM ALL THE WAY IN (10x)
# Draw individual bricks on the keep wall
# =============================================

zoom_in(10)
time.sleep(0.4)

# At 10x zoom, view is centered on the screen
# The keep wall was at canvas x=260-400, y=300-420
# At screen center (330, 420), we're seeing a small portion of the keep

# Draw a grid of individual bricks in the visible area
# Each brick at 10x zoom: 4x10 canvas pixels = 40x100 screen pixels
# Brick grid: offset from view center

brick_start_x = 200   # screen coords
brick_start_y = 250

for row in range(6):
    for col in range(8):
        bx = brick_start_x + col * 48
        by = brick_start_y + row * 22
        # Brick outline (thin stroke at 10x zoom = very delicate in canvas)
        activate_pen()
        stroke([(bx, by), (bx+38, by), (bx+38, by+16), (bx, by+16)])
        time.sleep(0.01)

time.sleep(0.15)

# Add some brick color fill (cross-hatch on every other brick)
for row in range(6):
    for col in range(8):
        if (row + col) % 2 == 0:
            bx = brick_start_x + col * 48 + 4
            by = brick_start_y + row * 22 + 3
            # Single diagonal hatch through the brick
            activate_pen()
            stroke([(bx, by), (bx+30, by+10)])
            time.sleep(0.008)

time.sleep(0.15)

# Mortar lines (horizontal + vertical)
for row in range(6):
    my = brick_start_y + row * 22 + 16
    activate_pen()
    stroke([(brick_start_x, my), (brick_start_x + 8*48 - 10, my)])
    time.sleep(0.015)

for col in range(8):
    mx = brick_start_x + col * 48 + 38
    # Staggered vertical mortar lines
    for row in range(6):
        offset = -6 if (row % 2 == 0) else 6
        my = brick_start_y + row * 22 + offset
        activate_pen()
        stroke([(mx, my), (mx, my + 16)])
        time.sleep(0.008)

time.sleep(0.2)

# Window detail in the brick wall - arch window with mullions
# Positioned within the brick grid area
win_x = brick_start_x + 3 * 48 + 6
win_y = brick_start_y + 1 * 22 + 2

# Window arch outline (thin, delicate at 10x zoom)
w_ctrl = [(win_x, win_y+40), (win_x, win_y+8), (win_x+24, win_y), (win_x+48, win_y+8), (win_x+48, win_y+40)]
activate_pen()
stroke(catmull(w_ctrl, 12))
time.sleep(0.04)

# Window mullions (cross bars)
activate_pen()
stroke([(win_x+24, win_y+4), (win_x+24, win_y+40)])
time.sleep(0.02)
activate_pen()
stroke([(win_x+4, win_y+20), (win_x+44, win_y+20)])
time.sleep(0.02)

# Window glass panes (4 panes created by mullions)
for px, py in [(win_x+4, win_y+6), (win_x+26, win_y+6), (win_x+4, win_y+24), (win_x+26, win_y+24)]:
    activate_pen()
    stroke([(px, py), (px+18, py), (px+18, py+12), (px, py+12)])
    time.sleep(0.015)

time.sleep(0.15)

# Stone texture around window - individual stone blocks
for sx in range(win_x-14, win_x+66, 16):
    for sy in [win_y-8, win_y+46]:
        activate_pen()
        stroke([(sx, sy), (sx+12, sy), (sx+12, sy+6), (sx, sy+6)])
        time.sleep(0.008)

time.sleep(0.15)

# Decorative element above window (a small trefoil/circle)
circle_ctrl = [
    (win_x+24, win_y-18), (win_x+22, win_y-12), (win_x+18, win_y-6),
    (win_x+24, win_y-4), (win_x+30, win_y-6), (win_x+26, win_y-12), (win_x+24, win_y-18)
]
activate_pen()
stroke(catmull(circle_ctrl, 10))
time.sleep(0.04)

# Inner circle
inner_ctrl = [
    (win_x+24, win_y-15), (win_x+26, win_y-11), (win_x+24, win_y-8),
    (win_x+22, win_y-11), (win_x+24, win_y-15)
]
activate_pen()
stroke(catmull(inner_ctrl, 8))
time.sleep(0.04)

# =============================================
# PHASE 3: ZOOM OUT — Reveal the full picture
# =============================================

zoom_out(10)
time.sleep(0.3)

print("Castle with extreme detail drawn!")
