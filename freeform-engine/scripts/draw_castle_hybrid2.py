"""
Castle Hybrid v2 — Shapes + pen, better positioning.
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
    time.sleep(0.006)
    CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))

def spawn_shape(shape_xy, canvas_xy):
    click(*SHAPE)
    time.sleep(0.25)
    click(*shape_xy)
    time.sleep(0.3)
    click(*canvas_xy)
    time.sleep(0.4)

def main():
    activate_freeform()
    time.sleep(1)
    new_board()
    time.sleep(1.5)

    print("Placing shapes...")

    # Keep walls — centered
    spawn_shape(SQUARE, (330, 380))
    # Left tower — closer in
    spawn_shape(SQUARE, (230, 395))
    # Right tower — symmetric
    spawn_shape(SQUARE, (430, 395))
    # Gatehouse
    spawn_shape(SQUARE, (330, 450))
    # Keep roof
    spawn_shape(TRIANGLE, (330, 290))
    # Tower roofs
    spawn_shape(TRIANGLE, (230, 340))
    spawn_shape(TRIANGLE, (430, 340))

    print("Adding pen details...")
    activate_pen()
    time.sleep(0.3)

    # Crenellations on keep (along top of keep wall)
    from freeform_engine import crenelation
    battlement = crenelation(270, 390, 330, 10, 10)
    for pt in battlement:
        click(*pt)
        time.sleep(0.006)
    keystroke(53)
    time.sleep(0.1)

    # Arched door
    door(308, 460, 352, 425, arch_top=10)

    # Windows — arched
    window_arch(290, 365, 16, 24, mullion_h=1, mullion_v=1)
    window_arch(340, 365, 16, 24, mullion_h=1, mullion_v=1)

    # Single flag on keep peak only (not on towers to avoid overlap)
    activate_pen()
    stroke_soft([(330, 290), (330, 260)])
    activate_pen()
    stroke_soft([(330, 260), (340, 254), (330, 248)])

    # Moat — single outline, no fill lines
    activate_pen()
    stroke_soft([(160, 490), (500, 490), (510, 510), (150, 510)])

    # Drawbridge
    activate_pen()
    stroke_soft([(312, 460), (348, 460), (348, 485), (312, 485)])

    screenshot("/tmp/castle_hybrid2.png")
    print("Castle hybrid v2 drawn!")

if __name__ == "__main__":
    main()
