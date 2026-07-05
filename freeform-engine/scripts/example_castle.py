"""
example_castle.py — A castle drawn entirely from engine compositions.

Demonstrates: future drawings compose from L5 primitives, no reinvented code.

Drawn with: setup() + ~12 composition calls.
Approximate time: ~45s.
"""
from freeform_engine import (
    setup, polyline, rect_outline, roof, door, window_arch,
    brick_wall, sun, cloud, ground, count_ink
)


def main():
    setup()

    # Canvas-level scene
    ground(470, 100, 560)
    sun(560, 270, 16, 22, n_rays=10, ray_length=12)
    cloud(120, 240, 70, 12)

    # Main building
    rect_outline(220, 320, 440, 470)         # keep walls
    roof(330, 270, 220, 320, 440, bold=True) # roof
    rect_outline(180, 360, 220, 470)         # left tower
    rect_outline(440, 360, 480, 470)         # right tower
    rect_outline(240, 470, 420, 500)         # gatehouse

    # Door
    door(305, 500, 355, 460, arch_top=15)

    # Windows
    window_arch(260, 380, 30, 50, mullion_h=1, mullion_v=1)
    window_arch(340, 380, 30, 50, mullion_h=1, mullion_v=1)
    window_arch(200, 410, 20, 40, mullion_h=0, mullion_v=0)
    window_arch(460, 410, 20, 40, mullion_h=0, mullion_v=0)

    # Details (Crenellation is a polyline we still need to draw explicitly)
    from freeform_engine import crenelation
    battlement = crenelation(220, 440, 320, 13, 14)
    polyline(battlement)

    # Verify
    print("\nInk count by region:")
    for name, x1, y1, x2, y2 in [
        ("ground", 100, 460, 570, 480),
        ("left_tower", 175, 355, 225, 475),
        ("right_tower", 435, 355, 485, 475),
        ("keep_walls", 215, 315, 445, 475),
        ("roof_peak", 280, 265, 380, 325),
        ("door", 290, 455, 370, 510),
        ("windows", 180, 370, 480, 430),
        ("sun", 530, 230, 595, 310),
        ("cloud", 80, 220, 200, 270),
    ]:
        ink = count_ink(x1, y1, x2, y2)
        print(f"  {name}: {ink} ink pixels")


if __name__ == "__main__":
    main()
