"""
Castle #1 — Baseline. Pure compositions, no zoom.
"""
from freeform_engine import *

def main():
    setup()

    # Ground
    ground(475, 120, 540)

    # Keep (main tower block)
    rect_outline(240, 310, 420, 430, bold=True)

    # Crenellations on keep
    from freeform_engine import crenelation
    battlement = crenelation(240, 420, 310, 14, 14)
    polyline(battlement)

    # Left tower
    rect_outline(180, 350, 230, 440, bold=True)
    battlement_l = crenelation(180, 230, 350, 12, 12)
    polyline(battlement_l)

    # Right tower
    rect_outline(430, 350, 480, 440, bold=True)
    battlement_r = crenelation(430, 480, 350, 12, 12)
    polyline(battlement_r)

    # Curtain walls (connecting towers to keep)
    polyline([(230, 370), (240, 370), (240, 430)])
    polyline([(420, 370), (430, 370), (430, 440)])

    # Gatehouse
    rect_outline(280, 430, 380, 465, bold=True)

    # Arched door
    door(305, 465, 355, 425, arch_top=12)

    # Windows on keep
    window_arch(270, 355, 24, 40, mullion_h=1, mullion_v=1)
    window_arch(330, 355, 24, 40, mullion_h=1, mullion_v=1)

    # Moat
    polyline([(150, 480), (510, 480), (520, 505), (140, 505)])

    # Drawbridge
    rect_outline(310, 465, 350, 485)
    for dx in range(314, 352, 6):
        stroke([(dx, 465), (dx, 485)])

    # Flags on towers and keep
    for fx, fy in [(205, 350), (455, 350), (330, 310)]:
        stroke([(fx, fy), (fx, fy - 30)])
        stroke([(fx, fy - 30), (fx + 15, fy - 24), (fx, fy - 18)])

    # Sun and clouds
    sun(520, 280, 14, 18, n_rays=8, ray_length=10)
    cloud(100, 240, 60, 10, bold=True)

    screenshot("/tmp/castle_v1.png")
    print("Castle #1 complete: /tmp/castle_v1.png")

if __name__ == "__main__":
    main()
