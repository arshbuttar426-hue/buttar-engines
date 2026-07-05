"""
Castle Hybrid v3 — Select shape ONCE, place multiple times.
"""
import time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from freeform_engine import *
from Quartz.CoreGraphics import *

SHAPE = (403, 57)
SQUARE = (489, 151)
TRIANGLE = (302, 458)

def click(x, y):
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def select_shape(shape_xy):
    """Select a shape tool from the palette (SHAPE button + shape type)."""
    click(*SHAPE)
    time.sleep(0.3)
    click(*shape_xy)
    time.sleep(0.4)

def place_shape(canvas_xy):
    """Place currently selected shape at canvas position."""
    click(*canvas_xy)
    time.sleep(0.4)

def main():
    activate_freeform()
    time.sleep(1)
    new_board()
    time.sleep(2)

    # ── Select SQUARE, place walls ──
    print("Selecting Square tool...")
    select_shape(SQUARE)

    print("Placing keep...")
    place_shape((330, 380))
    print(f"  keep: {count_ink(260, 310, 400, 450)}")

    print("Placing left tower...")
    place_shape((230, 400))
    print(f"  ltower: {count_ink(195, 340, 265, 460)}")

    print("Placing right tower...")
    place_shape((430, 400))
    print(f"  rtower: {count_ink(395, 340, 465, 460)}")

    print("Placing gatehouse...")
    place_shape((330, 455))
    print(f"  gate: {count_ink(285, 425, 375, 480)}")

    # ── Select TRIANGLE, place roofs ──
    print("Selecting Triangle tool...")
    select_shape(TRIANGLE)

    print("Placing keep roof...")
    place_shape((330, 290))
    print(f"  roof: {count_ink(260, 230, 400, 330)}")

    print("Placing left tower roof...")
    place_shape((230, 345))
    print(f"  ltroof: {count_ink(195, 310, 265, 360)}")

    print("Placing right tower roof...")
    place_shape((430, 345))
    print(f"  rtroof: {count_ink(395, 310, 465, 360)}")

    # ── Pen details ──
    print("\nPen details...")
    activate_pen()
    time.sleep(0.5)

    door(308, 470, 352, 435, arch_top=10)
    window_arch(290, 370, 16, 24, mullion_h=0, mullion_v=0)
    window_arch(340, 370, 16, 24, mullion_h=0, mullion_v=0)

    # Flag
    activate_pen()
    stroke_soft([(330, 290), (330, 255)])
    activate_pen()
    stroke_soft([(330, 255), (340, 248), (330, 242)])

    # Moat
    activate_pen()
    stroke_soft([(160, 495), (500, 495), (510, 515), (150, 515)])

    screenshot("/tmp/castle_hybrid3.png")
    print("\nFinal:")
    for name,x1,y1,x2,y2 in [
        ("keep", 260,310,400,450), ("ltower", 195,340,265,460),
        ("rtower", 395,340,465,460), ("roof", 260,230,400,330),
        ("ltroof", 195,310,265,360), ("rtroof", 395,310,465,360),
        ("gate", 285,425,375,480), ("door", 303,430,357,475),
        ("moat", 150,485,520,525), ("windows", 280,355,380,405),
    ]:
        print(f"  {name:8s}: {count_ink(x1,y1,x2,y2)}")

if __name__ == "__main__":
    main()
