"""
Castle #2 — Zoom perspective. Bold at low zoom, delicate at high zoom.
"""
from freeform_engine import *

def main():
    setup()

    # ── PHASE 1: NORMAL ZOOM — Main structure (bold) ──
    cx, cy = 330, 420

    # Keep
    rect_outline(260, 300, 400, 430, bold=True)

    # Crenellations
    from freeform_engine import crenelation
    battlement = crenelation(260, 400, 300, 14, 14)
    polyline(battlement)

    # Keep roof
    polyline([(255, 300), (330, 255), (405, 300)])

    # Left tower
    rect_outline(190, 350, 225, 440, bold=True)
    rect_outline(190, 350, 205, 335)
    rect_outline(205, 335, 225, 350)
    battlement_l = crenelation(190, 225, 350, 10, 10)
    polyline(battlement_l)

    # Right tower
    rect_outline(435, 350, 470, 440, bold=True)
    rect_outline(435, 350, 455, 335)
    rect_outline(455, 335, 470, 350)
    battlement_r = crenelation(435, 470, 350, 10, 10)
    polyline(battlement_r)

    # Curtain walls
    polyline([(225, 370), (260, 370), (260, 430)])
    polyline([(400, 370), (435, 370), (435, 440)])

    # Gatehouse
    rect_outline(290, 430, 370, 465, bold=True)

    # Arched gate
    door(314, 465, 346, 435, arch_top=10)

    # ── PHASE 2: ZOOM IN 3x — Delicate details ──
    zoom_in(3)

    # Arrow slits on towers
    for tx in [197, 218, 442, 463]:
        for ty in [370, 400]:
            stroke([(tx, ty - 10), (tx, ty + 10)])
            stroke([(tx - 2, ty - 5), (tx + 2, ty - 5), (tx, ty - 12)])

    # Window slits on keep (delicate)
    for wx, wy in [(275, 350), (295, 350), (340, 350), (360, 350)]:
        stroke([(wx, wy - 8), (wx, wy + 8)])

    # Stone texture lines on keep
    for sy in range(315, 415, 10):
        stroke([(265, sy), (395, sy)])

    for sx in range(275, 390, 18):
        for sy in [325, 345, 365, 385]:
            stroke([(sx, sy), (sx, sy + 6)])

    # Flags
    for fx, fy in [(207, 335), (453, 335), (330, 300)]:
        stroke([(fx, fy), (fx, fy - 28)])
        stroke([(fx, fy - 28), (fx + 14, fy - 22), (fx, fy - 16)])

    # ── PHASE 3: ZOOM OUT — Thick foreground ──
    zoom_out(5)

    # Moat
    polyline([(140, 480), (520, 480), (530, 510), (130, 510)])
    polyline([(155, 490), (505, 490)])
    polyline([(165, 500), (495, 500)])

    # Drawbridge
    rect_outline(310, 465, 350, 490)
    for dx in range(314, 352, 6):
        stroke([(dx, 465), (dx, 490)])

    # Ground
    polyline([(60, 485), (100, 492), (200, 497), (330, 503),
              (460, 497), (520, 492), (560, 485)])

    # Grass tufts
    for gx in range(90, 550, 35):
        for _ in range(2):
            st = [((gx + _ * 8), 495), ((gx + _ * 8 + 2), 492)]
            stroke(st)

    # Sun
    sun(540, 250, 12, 16, n_rays=8, ray_length=10)

    # Clouds
    cloud(120, 225, 55, 9, bold=True)

    zoom_in(2)

    screenshot("/tmp/castle_v2.png")
    print("Castle #2 complete: /tmp/castle_v2.png")

if __name__ == "__main__":
    main()
