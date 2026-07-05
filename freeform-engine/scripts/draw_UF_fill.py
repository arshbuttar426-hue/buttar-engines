import time, os, subprocess
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts):
    for px, py in pts:
        time.sleep(0.01)
        click(px, py)
    time.sleep(0.03)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.01)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    click(404, 55)
    time.sleep(0.2)
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

# Fill U with horizontal lines
for y in range(350, 460, 3):
    if y < 445:
        stroke([(240, y), (300, y)])
    else:
        # bottom curve - narrow as we go down
        offset = int(18 * ((y-445)/15))
        stroke([(240 - offset, y), (300 + offset, y)])
    time.sleep(0.02)

time.sleep(0.3)

# Fill F with horizontal lines per region
for y in range(350, 460, 3):
    activate_pen()
    if y < 360:
        stroke([(360, y), (445, y)])
    elif y < 410:
        stroke([(360, y), (385, y)])
    elif y < 420:
        stroke([(360, y), (435, y)])
    else:
        stroke([(360, y), (385, y)])
    time.sleep(0.02)

print("Filled UF done!")
