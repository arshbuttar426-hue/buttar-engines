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
        time.sleep(0.06)

def zoom_out(n=1):
    for _ in range(n):
        key_combo(0x37, 27)
        time.sleep(0.06)

def polygon(cx, cy, r, n, phase=0):
    pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n + phase
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

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

cx, cy = 330, 380
R = 140

# =============================================
# EARTH — Straight lines only (caterpillar principle)
# =============================================

# ---- 1. Sphere: 60-sided regular polygon (IS a circle) ----
activate_pen()
stroke(polygon(cx, cy, R, 60))
time.sleep(0.15)

# ---- 2. Latitude lines (straight horizontal chords) ----
lat_angles = [-50, -30, 0, 30, 50]  # degrees from equator
for lat_deg in lat_angles:
    phi = math.radians(lat_deg)
    y = cy + R * math.sin(phi)
    x_off = R * math.cos(phi)
    activate_pen()
    stroke([(cx - x_off, y), (cx + x_off, y)])
    time.sleep(0.04)

time.sleep(0.12)

# ---- 3. Longitude lines (polygonal arcs, 14 segments each) ----
lon_angles = [-75, -45, -15, 15, 45, 75]
for lon_deg in lon_angles:
    theta = math.radians(lon_deg)
    pts = []
    for i in range(15):
        phi = math.pi * (-0.5 + i / 14)
        px = cx + R * math.cos(phi) * math.sin(theta)
        py = cy + R * math.sin(phi)
        pts.append((px, py))
    activate_pen()
    stroke(pts)
    time.sleep(0.04)

time.sleep(0.2)

# ---- 4. Continents (low-poly, straight edges only) ----

# North America
na = [(212, 278), (230, 272), (255, 268), (282, 268), (295, 275),
      (304, 298), (305, 315), (300, 330), (295, 352), (282, 362),
      (268, 368), (252, 378), (242, 370), (232, 352), (224, 330),
      (218, 312), (210, 295)]
activate_pen()
stroke(na)
time.sleep(0.08)

# South America
sa = [(246, 388), (265, 382), (284, 384), (300, 392), (310, 412),
      (305, 435), (296, 458), (282, 472), (270, 468), (260, 454),
      (252, 432), (248, 412)]
activate_pen()
stroke(sa)
time.sleep(0.08)

# Europe
eu = [(348, 302), (365, 294), (385, 290), (400, 295), (410, 300),
      (415, 312), (410, 325), (400, 330), (390, 335), (375, 340),
      (360, 338), (350, 328), (345, 315)]
activate_pen()
stroke(eu)
time.sleep(0.08)

# Africa
af = [(358, 348), (378, 340), (400, 342), (418, 350), (430, 365),
      (432, 388), (422, 415), (408, 435), (396, 455), (382, 466),
      (368, 458), (358, 440), (350, 418), (348, 395), (350, 372)]
activate_pen()
stroke(af)
time.sleep(0.08)

# Asia (partial)
asi = [(410, 300), (430, 295), (450, 300), (462, 312), (465, 330),
       (460, 348), (448, 358), (435, 355), (418, 350), (410, 335),
       (408, 322)]
activate_pen()
stroke(asi)
time.sleep(0.08)

# Australia
aus = [(430, 440), (448, 435), (460, 442), (462, 458), (452, 470),
       (438, 468), (428, 456)]
activate_pen()
stroke(aus)
time.sleep(0.08)

# Greenland
gr = [(290, 268), (305, 262), (318, 268), (320, 282), (310, 290),
      (298, 286), (290, 278)]
activate_pen()
stroke(gr)
time.sleep(0.12)

# ---- 5. Zoom in 3x for fine detail (islands, coastal details) ----
zoom_in(3)
time.sleep(0.3)

# Caribbean islands
for ix, iy in [(262, 382), (270, 380), (278, 384), (255, 388)]:
    activate_pen()
    stroke(polygon(ix, iy, 4, 8))
    time.sleep(0.025)

# UK/Ireland
activate_pen()
stroke([(347, 298), (352, 294), (356, 298), (354, 304), (347, 302)])
time.sleep(0.03)
activate_pen()
stroke([(340, 296), (345, 292), (348, 296), (344, 300)])
time.sleep(0.03)

# Madagascar
activate_pen()
stroke([(434, 442), (440, 438), (444, 445), (440, 452), (434, 448)])
time.sleep(0.03)

# Japan
activate_pen()
stroke([(470, 328), (476, 324), (480, 330), (476, 336), (470, 332)])
time.sleep(0.03)

# Indonesia archipelago
for ix, iy in [(448, 412), (456, 410), (464, 414), (452, 418)]:
    activate_pen()
    stroke(polygon(ix, iy, 3, 6))
    time.sleep(0.02)

time.sleep(0.12)

# ---- 6. Zoom out to see full globe ----
zoom_out(3)
time.sleep(0.3)

# ---- 7. Equator line (thicker - 3 parallel, for emphasis) ----
y_eq = cy
for dx in [-3, 0, 3]:
    activate_pen()
    stroke([(cx - R + dx, y_eq + dx), (cx + R + dx, y_eq + dx)])
    time.sleep(0.06)

time.sleep(0.2)

# ---- 8. Axis line (polar axis visual hint) ----
activate_pen()
stroke([(cx, cy - R - 15), (cx, cy + R + 15)])
time.sleep(0.06)

print("Earth drawn with straight lines!")
