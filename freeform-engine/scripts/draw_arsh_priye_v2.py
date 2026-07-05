"""arsh ❤ priye — adapted from working draw_arsh.py style"""
import time, os, sys, math, subprocess
sys.path.insert(0, os.path.dirname(__file__))
os.environ['PATH'] = f'/tmp/leaf_env/bin:' + os.environ.get('PATH', '')
from Quartz.CoreGraphics import *

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.006)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def stroke(pts, slp=0.006):
    for px, py in pts:
        time.sleep(slp)
        click(px, py)
    time.sleep(0.02)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, True))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, 53, False))

def activate_pen():
    click(405, 58)
    time.sleep(0.15)
    click(381, 511)
    time.sleep(0.3)

def key_combo(mod_key, char_key):
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, True))
    time.sleep(0.03)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, True))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, char_key, False))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, mod_key, False))

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

def bold_stroke(pts, slp=0.005):
    for dx in [-4, -2, 0, 2, 4]:
        activate_pen()
        stroke([(x+dx, y+dx*0.3) for (x,y) in pts], slp)
        time.sleep(0.04)

def vstroke(x, y0, y1, n=20, passes=3):
    for d in range(-(passes//2), passes//2 + 1):
        activate_pen()
        stroke([(x + d*2, y0 + (y1-y0)*i/n) for i in range(n+1)])
        time.sleep(0.04)

# Setup
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

# ── "arsh" ──
# a: left+right diagonal + crossbar
activate_pen(); stroke(catmull([(120,450),(125,410),(135,405),(145,410),(148,450)],25))
activate_pen(); stroke([(122,430),(146,430)])
time.sleep(0.08)

# r: vertical + shoulder
vstroke(165, 410, 450, passes=3)
activate_pen(); stroke(catmull([(165,410),(178,410),(183,415),(180,425)],20))
time.sleep(0.08)

# s: S-curve
bold_stroke(catmull([
    (205,410),(220,408),(225,415),(220,425),
    (210,435),(220,440),(225,448),(220,452)
],30))
time.sleep(0.08)

# h: vertical + arch
vstroke(240, 410, 450, passes=3)
bold_stroke(catmull([(240,410),(255,410),(265,418),(265,435),(262,450)],25))
time.sleep(0.08)

# ── Heart ──
bold_stroke(catmull([
    (295,460), (288,445), (280,430), (285,415), (295,410),
    (305,415), (310,430), (302,445), (295,460),
], 35))
time.sleep(0.08)

# ── "priye" ──
# p: vertical + loop
vstroke(335, 420, 460, passes=3)
bold_stroke(catmull([(335,420),(348,418),(358,425),(358,435),(350,442),(335,440)],25))
time.sleep(0.08)

# r: vertical + shoulder  
vstroke(375, 410, 450, passes=3)
activate_pen(); stroke(catmull([(375,410),(388,410),(393,415),(390,425)],20))
time.sleep(0.08)

# i: vertical + dot
vstroke(405, 410, 450, passes=3)
circle_outline = [(405+6*math.cos(2*math.pi*i/15),410-22+6*math.sin(2*math.pi*i/15)) for i in range(16)]
activate_pen(); stroke(circle_outline)
time.sleep(0.08)

# y: V with tail
bold_stroke(catmull([(425,410),(438,435),(450,410)],20))
activate_pen(); stroke([(438,435),(433,460)])
time.sleep(0.08)

# e: reverse C + bar
bold_stroke(catmull([(470,450),(465,435),(468,418),(480,415),(490,420),(492,435)],30))
activate_pen(); stroke([(468,435),(490,435)])
time.sleep(0.08)

print("arsh ❤ priye done!")
