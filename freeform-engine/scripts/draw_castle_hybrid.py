"""
Castle — Hybrid: Freeform shapes (rect, triangle) + pen details.
Shapes for structure, pen for ornament.
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

    # Spawn shapes first
    print("Placing shapes...")

    # Keep walls (rect at center)
    spawn_shape(SQUARE, (330, 380))
    # Left tower
    spawn_shape(SQUARE, (200, 400))
    # Right tower
    spawn_shape(SQUARE, (460, 400))
    # Gatehouse
    spawn_shape(SQUARE, (330, 455))
    # Keep roof (triangle)
    spawn_shape(TRIANGLE, (330, 280))
    # Left tower roof
    spawn_shape(TRIANGLE, (200, 340))
    # Right tower roof
    spawn_shape(TRIANGLE, (460, 340))

    # Now pen details
    print("Adding pen details...")
    activate_pen()
    time.sleep(0.3)

    # Crenellations on keep
    from freeform_engine import crenelation
    battlement = crenelation(250, 410, 340, 12, 12)
    for pt in battlement:
        click(*pt)
        time.sleep(0.006)
    keystroke(53)
    time.sleep(0.1)

    # Arched door
    door(305, 470, 355, 430, arch_top=12)

    # Windows on keep
    window_arch(280, 365, 18, 28, mullion_h=1, mullion_v=1)
    window_arch(340, 365, 18, 28, mullion_h=1, mullion_v=1)

    # Arrow slits on towers
    for tx in [190, 210, 450, 470]:
        for ty in [380, 410]:
            activate_pen()
            stroke_soft([(tx, ty - 8), (tx, ty + 8)])

    # Flags
    for fx, fy in [(200, 340), (460, 340), (330, 280)]:
        activate_pen()
        stroke_soft([(fx, fy), (fx, fy - 30)])
        activate_pen()
        stroke_soft([(fx, fy - 30), (fx + 14, fy - 23), (fx, fy - 18)])

    # Moat
    activate_pen()
    stroke_soft([(140, 490), (520, 490), (530, 510), (130, 510)])

    # Drawbridge
    activate_pen()
    stroke_soft([(310, 470), (350, 470), (350, 490), (310, 490)])
    for dx in range(314, 352, 6):
        activate_pen()
        stroke_soft([(dx, 470), (dx, 490)])

    screenshot("/tmp/castle_hybrid.png")
    print("Hybrid castle drawn!")

if __name__ == "__main__":
    main()
