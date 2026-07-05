"""
Castle #4 — Homeostatic drawing + integrity verification + screenshot.
Self-correcting castle with hash-chain integrity and ink-set-point validation.
"""
from freeform_engine import *
import time

def main():
    setup()
    cx, cy = 330, 420

    # ── PHASE 1: Normal zoom — castle structure with homeostatic correction ──

    homeostatic_draw("ground", ground, (100, 460, 570, 480), y=475, x_start=120, x_end=540)

    homeostatic_draw("house_body", rect_outline, (225, 295, 435, 435),
                     x1=240, y1=310, x2=420, y2=430, bold=True)

    # Crenellations on keep — manual (no homeostatic for this)
    from freeform_engine import crenelation
    battlement = crenelation(240, 420, 310, 14, 14)
    polyline(battlement)

    # Left tower
    homeostatic_draw("window", rect_outline, (175, 345, 230, 445),
                     x1=180, y1=350, x2=225, y2=440, bold=True)
    battlement_l = crenelation(180, 225, 350, 10, 10)
    polyline(battlement_l)

    # Right tower
    homeostatic_draw("window", rect_outline, (430, 345, 485, 445),
                     x1=435, y1=350, x2=480, y2=440, bold=True)
    battlement_r = crenelation(435, 480, 350, 10, 10)
    polyline(battlement_r)

    # Curtain walls
    polyline([(225, 370), (240, 370), (240, 430)])
    polyline([(420, 370), (435, 370), (435, 440)])

    # Gatehouse
    homeostatic_draw("window", rect_outline, (275, 425, 385, 470),
                     x1=280, y1=430, x2=380, y2=465, bold=True)

    # Arched door
    door(305, 465, 355, 425, arch_top=12)

    # Windows
    window_arch(270, 355, 24, 40, mullion_h=1, mullion_v=1, bold=True)
    window_arch(325, 355, 24, 40, mullion_h=1, mullion_v=1, bold=True)
    window_arch(380, 355, 24, 40, mullion_h=1, mullion_v=1, bold=True)
    window_arch(195, 390, 18, 28, mullion_h=0, mullion_v=0)
    window_arch(465, 390, 18, 28, mullion_h=0, mullion_v=0)

    # Moat and drawbridge
    polyline([(150, 480), (510, 480), (520, 510), (140, 510)])
    rect_outline(310, 465, 350, 490)
    for dx in range(314, 352, 6):
        stroke([(dx, 465), (dx, 490)])

    # Flags
    for fx, fy in [(202, 350), (458, 350), (330, 310)]:
        stroke([(fx, fy), (fx, fy - 32)])
        polyline([(fx, fy - 32), (fx + 16, fy - 25), (fx, fy - 18)])

    # Sun and clouds
    homeostatic_draw("sun", sun, (510, 240, 580, 320),
                     cx=530, cy=280, r_inner=14, r_outer=18, n_rays=8, ray_length=10)
    cloud(120, 235, 60, 10, bold=True)
    cloud(210, 220, 40, 7, bold=True)

    # ── PHASE 2: Integrity verification ──
    print("\n── Integrity Verification ──")
    integrity_passes = []

    for name, bbox in [
        ("castle_keep", (230, 300, 430, 440)),
        ("castle_towers", (170, 340, 490, 450)),
        ("castle_gate", (270, 420, 390, 475)),
        ("castle_moat", (130, 475, 530, 520)),
        ("castle_sun", (510, 235, 585, 325)),
    ]:
        ok, h = verify_drawing_integrity(name, bbox)
        integrity_passes.append((name, ok, h))

    print("\n── Integrity Report ──")
    integrity_report()

    all_pass = all(ok for _, ok, _ in integrity_passes)
    print(f"\n  Overall integrity: {'✓ PASS' if all_pass else '✗ FAIL'}")
    print(f"  Regions checked: {len(integrity_passes)}")

    # ── Screenshot ──
    screenshot("/tmp/castle_v4.png")
    print("Castle #4 complete: /tmp/castle_v4.png")

if __name__ == "__main__":
    main()
