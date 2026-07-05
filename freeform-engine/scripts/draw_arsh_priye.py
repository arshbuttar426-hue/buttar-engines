"""arsh ❤ priye — large clear letters"""
import time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from freeform_engine import *

def letter_a(x, y):
    oval = polygon(x+15, y-25, 18, n=40, scale_y=1.3)
    polyline(oval, bold=True)
    stroke([(x+30, y-38), (x+30, y)])

def letter_r(x, y):
    stroke([(x+6, y), (x+6, y-55)])
    polyline(catmull([(x+6, y-55), (x+24, y-55), (x+30, y-48), (x+28, y-40)], 20), bold=True)

def letter_s(x, y):
    polyline(catmull([
        (x+8, y), (x+28, y), (x+32, y-8), (x+28, y-16), (x+8, y-24),
        (x+4, y-32), (x+8, y-40), (x+28, y-48), (x+32, y-55),
    ], 25), bold=True)

def letter_h(x, y):
    stroke([(x+4, y), (x+4, y-55)])
    polyline(catmull([
        (x+4, y-55), (x+24, y-55), (x+34, y-48), (x+34, y-30),
        (x+30, y),
    ], 25), bold=True)

def letter_p(x, y):
    stroke([(x+6, y), (x+6, y-55)])
    polyline(catmull([
        (x+6, y-55), (x+26, y-55), (x+34, y-48), (x+34, y-36),
        (x+30, y-24), (x+6, y-24),
    ], 25), bold=True)

def letter_i(x, y):
    stroke([(x+8, y), (x+8, y-52)])
    circle_outline(x+8, y-62, 6, n=15)

def letter_y(x, y):
    polyline(catmull([(x+4, y-52), (x+16, y-26), (x+28, y-52)], 20), bold=True)
    stroke([(x+16, y-26), (x+12, y+10)])

def letter_e(x, y):
    circle_outline(x+16, y-26, 20, n=40)
    stroke([(x+2, y-26), (x+30, y-26)])

def heart_med(cx, cy, r):
    polyline(catmull([
        (cx, cy + r), (cx - r*0.7, cy + r*0.15),
        (cx - r*1.1, cy - r*0.35), (cx - r*0.8, cy - r*0.85),
        (cx - r*0.2, cy - r*1.0), (cx, cy - r*0.55),
        (cx + r*0.2, cy - r*1.0), (cx + r*0.8, cy - r*0.85),
        (cx + r*1.1, cy - r*0.35), (cx + r*0.7, cy + r*0.15),
        (cx, cy + r),
    ], n=25), bold=True)

def main():
    activate_freeform()
    time.sleep(1)
    new_board()
    time.sleep(1.5)

    # "arsh" — left of center, baseline y=450
    letter_a(80, 450)
    letter_r(130, 450)
    letter_s(175, 450)
    letter_h(225, 450)

    # Heart between
    heart_med(295, 425, 25)

    # "priye" — right of center
    letter_p(340, 450)
    letter_r(395, 450)
    letter_i(440, 450)
    letter_y(465, 450)
    letter_e(510, 450)

    screenshot("/tmp/arsh_priye.png")
    print("arsh ❤ priye done!")

if __name__ == "__main__":
    main()
