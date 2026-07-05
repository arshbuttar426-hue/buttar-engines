import time, os, subprocess, math
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.01)
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

def gen_curve(pts, n=25):
    out = []
    for i in range(len(pts)):
        p0 = pts[max(0, i-1)]; p1 = pts[i]
        p2 = pts[min(len(pts)-1, i+1)]; p3 = pts[min(len(pts)-1, i+2)]
        for t in [j/n for j in range(n)]:
            t2=t*t; t3=t2*t
            x = 0.5*((2*p1[0])+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1])+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
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

# ---- BOLD U: 3 parallel curves ----
u_ctrl = [(260,310),(240,340),(235,350),(235,400),(240,445),(260,460),(280,460),(295,445),(300,400),(300,360),(295,330),(290,320),(285,330),(280,350)]
u_curve = gen_curve(u_ctrl, 18)

for dx in [-5, 0, 5]:
    activate_pen()
    stroke([(x+dx, y) for (x,y) in u_curve])
    time.sleep(0.15)

time.sleep(0.4)

# ---- BOLD F: flourished with filled downstroke ----
# Large loop + thick downstroke + bottom flourish returning up
f_main = gen_curve([
    (390, 290), (380, 310), (360, 320), (340, 340),
    (335, 370), (350, 395), (380, 400), (400, 385),
    (405, 360), (398, 345), (390, 350), (388, 370),
    (388, 400), (388, 440), (382, 460), (370, 468),
    (358, 460), (352, 445), (355, 430),
], 18)

# 3 parallel traces for boldness
for dx in [-5, 0, 5]:
    activate_pen()
    stroke([(x+dx, y+dx*0.5) for (x,y) in f_main])
    time.sleep(0.15)

time.sleep(0.3)

# Top crossbar (bold - 2 parallel)
activate_pen()
stroke([(340, 355), (430, 355)])
time.sleep(0.08)
activate_pen()
stroke([(340, 360), (430, 360)])
time.sleep(0.3)

# Middle crossbar (bold - 2 parallel)
activate_pen()
stroke([(345, 402), (425, 402)])
time.sleep(0.08)
activate_pen()
stroke([(345, 407), (425, 407)])

print("Cursive UF bold v3 done!")
