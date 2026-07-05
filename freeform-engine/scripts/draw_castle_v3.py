"""
Castle #3 — Brick wall composition at zoom + window_arch with mullions.
"""
from freeform_engine import *

def main():
    setup()

    # ── PHASE 1: NORMAL ZOOM — Full castle ──

    ground(470, 100, 560)

    # Main keep (use bold for weight)
    rect_outline(230, 300, 430, 430, bold=True)

    # Crenellations on keep
    from freeform_engine import crenelation
    battlement = crenelation(230, 430, 300, 14, 14)
    polyline(battlement)

    # Keep roof
    polyline([(225, 300), (330, 250), (435, 300)])

    # Left tower — symmetrical with right
    rect_outline(175, 350, 225, 440, bold=True)
    battlement_l = crenelation(175, 225, 350, 10, 10)
    polyline(battlement_l)

    # Right tower — mirror of left
    rect_outline(435, 350, 485, 440, bold=True)
    battlement_r = crenelation(435, 485, 350, 10, 10)
    polyline(battlement_r)

    # Curtain walls
    rect_outline(225, 370, 230, 430)
    rect_outline(430, 370, 435, 440)

    # Gatehouse
    rect_outline(285, 430, 375, 470, bold=True)

    # Arched gate
    door(308, 470, 352, 435, arch_top=14)

    # Window arches on keep
    window_arch(265, 355, 26, 42, mullion_h=1, mullion_v=1, bold=True)
    window_arch(315, 355, 26, 42, mullion_h=1, mullion_v=1, bold=True)
    window_arch(365, 355, 26, 42, mullion_h=1, mullion_v=1, bold=True)

    # Window arches on towers
    window_arch(200, 395, 18, 28, mullion_h=0, mullion_v=0)
    window_arch(460, 395, 18, 28, mullion_h=0, mullion_v=0)

    # Moat — one outline, one fill line
    polyline([(150, 480), (510, 480), (520, 510), (140, 510)])
    polyline([(155, 493), (505, 493)])

    # Drawbridge
    rect_outline(310, 470, 350, 490)
    for dx in range(314, 352, 6):
        stroke([(dx, 470), (dx, 490)])

    # Flags
    for fx, fy in [(200, 350), (460, 350), (330, 300)]:
        stroke([(fx, fy), (fx, fy - 35)])
        polyline([(fx, fy - 35), (fx + 18, fy - 27), (fx, fy - 20)])

    # ── PHASE 2: ZOOM 4x — Brick detail on keep wall ──
    zoom_in(4)

    brick_x, brick_y = 190, 250
    for row in range(4):
        for col in range(5):
            bx = brick_x + col * 44
            by = brick_y + row * 20
            stroke([(bx, by), (bx + 34, by), (bx + 34, by + 14), (bx, by + 14)])

    # Window detail carved into brick
    wx, wy = brick_x + 2 * 44 + 3, brick_y + 1 * 20 + 1
    w_ctrl = [(wx, wy + 34), (wx, wy + 6),
              (wx + 22, wy), (wx + 44, wy + 6), (wx + 44, wy + 34)]
    polyline(w_ctrl)
    stroke([(wx + 22, wy + 3), (wx + 22, wy + 34)])
    stroke([(wx + 3, wy + 18), (wx + 41, wy + 18)])

    # Decorative trefoil above window
    trefoil_ctrl = [(wx + 22, wy - 16), (wx + 20, wy - 10), (wx + 16, wy - 4),
                    (wx + 22, wy - 2), (wx + 28, wy - 4), (wx + 24, wy - 10),
                    (wx + 22, wy - 16)]
    polyline(trefoil_ctrl)

    zoom_out(4)

    # Sun and clouds
    sun(540, 260, 15, 20, n_rays=10, ray_length=12)
    cloud(110, 230, 65, 10, bold=True)
    cloud(200, 215, 40, 7, bold=True)

    screenshot("/tmp/castle_v3.png")
    print("Castle #3 complete: /tmp/castle_v3.png")

if __name__ == "__main__":
    main()
