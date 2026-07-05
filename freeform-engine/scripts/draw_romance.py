"""
"arsh loves priya" — romantic, pencil only, optimized for speed.
"""
import time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from freeform_engine import *
import math

def main():
    activate_freeform()
    time.sleep(1)
    new_board()
    time.sleep(1.5)
    activate_pen()
    time.sleep(0.3)

    cx, cy = 330, 420

    # ── 1. Big Heart (bold3, n=30 for speed) ──
    r = 120
    h = catmull([
        (cx, cy + r), (cx - r*0.7, cy + r*0.15),
        (cx - r*1.1, cy - r*0.35), (cx - r*0.8, cy - r*0.85),
        (cx - r*0.2, cy - r*1.0), (cx, cy - r*0.55),
        (cx + r*0.2, cy - r*1.0), (cx + r*0.8, cy - r*0.85),
        (cx + r*1.1, cy - r*0.35), (cx + r*0.7, cy + r*0.15),
        (cx, cy + r),
    ], n=30)
    bold5(h)
    time.sleep(0.15)

    # ── 2. "arsh" (left side) ──
    arsh = catmull([
        (180, 440), (175, 420), (182, 410), (192, 415), (195, 430), (190, 440),
        (198, 430), (204, 415), (210, 412),
        (218, 415), (215, 425), (222, 430),
        (230, 425), (235, 410), (240, 405), (248, 415), (252, 430), (258, 435),
    ], n=25)
    bold3(arsh)
    time.sleep(0.1)

    # ── 3. "loves" (center, below) ──
    loves = catmull([
        (205, 465), (210, 450), (215, 448),
        (225, 450), (230, 465), (228, 472),
        (240, 468), (245, 455), (252, 452),
        (260, 455), (262, 465), (265, 470),
        (275, 468), (280, 455), (285, 450), (292, 455), (295, 468),
        (305, 465), (310, 452), (315, 448),
        (325, 455), (328, 465), (332, 470),
    ], n=25)
    bold3(loves)
    time.sleep(0.1)

    # ── 4. "priya" (right side) ──
    priya = catmull([
        (270, 440), (275, 418), (282, 410), (290, 415),
        (300, 410), (305, 415), (308, 430),
        (318, 430), (322, 415), (328, 410),
        (340, 415), (342, 428), (345, 435),
        (352, 432), (355, 418), (362, 412), (370, 418), (372, 430), (378, 435),
        (385, 432), (388, 418), (392, 412), (400, 418), (402, 430), (405, 435),
    ], n=25)
    bold3(priya)
    time.sleep(0.1)

    # ── 5. Small hearts (just 4, top/bottom/left/right) ──
    for hx, hy, hr in [(330, 240, 20), (140, 360, 18), (520, 360, 18), (330, 560, 20)]:
        sh = catmull([
            (hx, hy + hr), (hx - hr*0.7, hy + hr*0.15),
            (hx - hr*1.1, hy - hr*0.35), (hx - hr*0.8, hy - hr*0.85),
            (hx - hr*0.2, hy - hr*1.0), (hx, hy - hr*0.55),
            (hx + hr*0.2, hy - hr*1.0), (hx + hr*0.8, hy - hr*0.85),
            (hx + hr*1.1, hy - hr*0.35), (hx + hr*0.7, hy + hr*0.15),
            (hx, hy + hr),
        ], n=20)
        polyline(sh)

    # ── 6. Decorative swirl bottom ──
    swirl = catmull([
        (130, 560), (180, 545), (230, 565), (280, 550),
        (330, 560), (380, 550), (430, 565), (480, 545), (530, 560),
    ], n=25)
    polyline(swirl)

    screenshot("/tmp/romance.png")
    print("'arsh loves priya' drawn!")

    ink = count_ink(80, 200, 580, 620)
    print(f"Total ink: {ink} px")

if __name__ == "__main__":
    main()
