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

# =============================================
# BRUTALIST BUILDING
# =============================================
# Main mass: wide blocky base with cantilevered upper section + tower

cx, cy = 330, 430

# ---- 1. Main building perimeter (heavy concrete edges) ----
# Main rectangular base
main_pts = [
    (180, cy),    # bottom-left
    (180, cy-150), # top-left
    (460, cy-150), # top-right
    (460, cy),    # bottom-right
]

for dx in [-3, 0, 3]:
    activate_pen()
    stroke([(x+dx, y) for (x,y) in main_pts])
    time.sleep(0.1)

time.sleep(0.2)

# ---- 2. Cantilevered upper block (projects out, darker) ----
# Forms a protruding mass above
upper_pts = [
    (200, cy-150),  # top-left (setback from main)
    (440, cy-150),  # top-right
    (440, cy-210),  # bottom of upper block
    (200, cy-210),  # bottom-left
]

for dx in [-2, 0, 2]:
    activate_pen()
    stroke([(x+dx, y) for (x,y) in upper_pts])
    time.sleep(0.1)

time.sleep(0.2)

# ---- 3. Tower (right side, rising above) ----
tower_pts = [
    (420, cy-210),   # bottom-left
    (420, cy-320),   # top-left
    (460, cy-250),   # top-right (slanted top)
    (460, cy-210),   # bottom-right
]

for dx in [-2, 0, 2]:
    activate_pen()
    stroke([(x+dx*0.5, y) for (x,y) in tower_pts])
    time.sleep(0.1)

time.sleep(0.2)

# ---- 4. Stairwell tower (left side) ----
stair_pts = [
    (180, cy-150),
    (180, cy-270),
    (210, cy-270),
    (210, cy-150),
]

for dx in [-2, 0, 2]:
    activate_pen()
    stroke([(x+dx*0.5, y) for (x,y) in stair_pts])
    time.sleep(0.1)

time.sleep(0.2)

# ---- 5. Window grid on main facade ----
# Horizontal bands of windows
for row in range(6):
    y_base = cy - 20 - row * 20
    x_start = 190
    for col in range(7):
        wx = x_start + col * 36
        activate_pen()
        stroke([(wx, y_base-8), (wx+28, y_base-8), (wx+28, y_base), (wx, y_base)])
        time.sleep(0.03)

time.sleep(0.3)

# ---- 6. Window grid on tower ----
for row in range(4):
    y_base = cy - 225 - row * 20
    for col in range(1):
        wx = 428
        activate_pen()
        stroke([(wx, y_base-8), (wx+24, y_base-8), (wx+24, y_base), (wx, y_base)])
        time.sleep(0.03)

time.sleep(0.2)

# ---- 7. Entrance (ground level, recessed) ----
entrance = [
    (280, cy),
    (280, cy-30),
    (340, cy-30),
    (340, cy),
]
activate_pen()
stroke(entrance)
time.sleep(0.1)
activate_pen()
stroke([(310, cy), (310, cy-30)])
time.sleep(0.1)
activate_pen()
stroke([(280, cy-30), (340, cy-30)])
time.sleep(0.2)

# ---- 8. Deep shadow hatching (left side of main block) ----
# Vertical shadows on left edge
for y in range(cy-145, cy-5, 4):
    activate_pen()
    stroke([(180, y), (195, y)])
    time.sleep(0.02)

time.sleep(0.2)

# Shadow under cantilever
for x in range(200, 445, 4):
    activate_pen()
    stroke([(x, cy-150), (x, cy-165)])
    time.sleep(0.02)

time.sleep(0.2)

# ---- 9. Horizontal concrete joint lines ----
for y in [cy-50, cy-100, cy-200, cy-250]:
    activate_pen()
    stroke([(185, y), (455, y)])
    time.sleep(0.05)

time.sleep(0.2)

# ---- 10. Ground line ----
activate_pen()
stroke([(160, cy+5), (480, cy+5)])
time.sleep(0.08)
activate_pen()
stroke([(160, cy+10), (480, cy+10)])

print("Brutalist building drawn!")
