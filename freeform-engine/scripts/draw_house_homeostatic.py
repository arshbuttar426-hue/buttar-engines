"""
House drawing with homeostatic correction and integrity verification.

Each major element is wrapped in homeostatic_draw() for ink-density
correction (Domain 7), then verified via SHA-256 pixel hash (Domain 9).

Usage:
    python3 draw_house_homeostatic.py
"""

import time, os, sys
sys.path.insert(0, os.path.expanduser('~/.opencode_knowledge/scripts'))
from freeform_engine import *

# ════════════════════════════════════════════════════════════════════
# SETUP
# ════════════════════════════════════════════════════════════════════

print("=" * 56)
print("  HOMEOSTATIC DRAW — COTTAGE WITH VERIFICATION")
print("=" * 56)
print()
setup()
time.sleep(1.0)

# ════════════════════════════════════════════════════════════════════
# GROUND
# ════════════════════════════════════════════════════════════════════

print("[1/9] Ground...")
homeostatic_draw("ground", ground,
                 bbox=(100, 470, 570, 485),
                 y=480, x_start=110, x_end=560)

# ════════════════════════════════════════════════════════════════════
# HOUSE BODY
# ════════════════════════════════════════════════════════════════════

print("[2/9] House body...")
homeostatic_draw("house_body", rect_outline,
                 bbox=(175, 375, 485, 475),
                 x1=180, y1=380, x2=480, y2=470)

# ════════════════════════════════════════════════════════════════════
# ROOF
# ════════════════════════════════════════════════════════════════════

print("[3/9] Pitched roof...")
homeostatic_draw("roof", roof,
                 bbox=(175, 285, 485, 370),
                 peak_x=330, peak_y=290,
                 base_left_x=180, base_y=365, base_right_x=480)

# ════════════════════════════════════════════════════════════════════
# DOOR
# ════════════════════════════════════════════════════════════════════

print("[4/9] Door...")
homeostatic_draw("door", door,
                 bbox=(300, 400, 360, 475),
                 x1=305, y1=405, x2=355, y2=470,
                 has_knob=True)

# ════════════════════════════════════════════════════════════════════
# LEFT WINDOW
# ════════════════════════════════════════════════════════════════════

print("[5/9] Left window...")
homeostatic_draw("window_left", window_pane,
                 bbox=(210, 375, 265, 425),
                 x1=215, y1=380, x2=260, y2=420,
                 dividers_h=1, dividers_v=1)

# ════════════════════════════════════════════════════════════════════
# RIGHT WINDOW
# ════════════════════════════════════════════════════════════════════

print("[6/9] Right window...")
homeostatic_draw("window_right", window_pane,
                 bbox=(390, 375, 445, 425),
                 x1=395, y1=380, x2=440, y2=420,
                 dividers_h=1, dividers_v=1)

# ════════════════════════════════════════════════════════════════════
# SUN
# ════════════════════════════════════════════════════════════════════

print("[7/9] Sun...")
homeostatic_draw("sun", sun,
                 bbox=(530, 250, 590, 310),
                 cx=560, cy=280, r_inner=18, r_outer=22,
                 n_rays=8, ray_length=12)

# ════════════════════════════════════════════════════════════════════
# CLOUD
# ════════════════════════════════════════════════════════════════════

print("[8/9] Cloud...")
homeostatic_draw("cloud", cloud,
                 bbox=(85, 225, 180, 265),
                 cx=135, cy=245, rx=40, ry=12,
                 n_loops=4)

# ════════════════════════════════════════════════════════════════════
# TREE
# ════════════════════════════════════════════════════════════════════

print("[9/9] Conifer tree...")
homeostatic_draw("tree", tree_conifer,
                 bbox=(115, 395, 185, 560),
                 cx=148, base_y=400, height=140, base_width=50)

# ════════════════════════════════════════════════════════════════════
# CHIMNEY
# ════════════════════════════════════════════════════════════════════

print("Chimney (via homeostatic_draw)...")
def _raw_chimney(x, y, w, h):
    """Wrap engine's chimney() for homeostatic_draw interface."""
    chimney(x, y, w, h)

homeostatic_draw("chimney", _raw_chimney,
                 bbox=(415, 295, 450, 365),
                 x=420, y=310, w=25, h=50)

# ════════════════════════════════════════════════════════════════════
# INTEGRITY VERIFICATION
# ════════════════════════════════════════════════════════════════════

print()
print("─" * 56)
print("  INTEGRITY VERIFICATION")
print("─" * 56)

verify_drawing_integrity("house_body", (175, 375, 485, 475))
verify_drawing_integrity("roof", (175, 285, 485, 370))
verify_drawing_integrity("door", (300, 400, 360, 475))
verify_drawing_integrity("window_left", (210, 375, 265, 425))
verify_drawing_integrity("window_right", (390, 375, 445, 425))
verify_drawing_integrity("sun", (530, 250, 590, 310))
verify_drawing_integrity("cloud", (85, 225, 180, 265))
verify_drawing_integrity("tree", (115, 330, 180, 485))

print()
integrity_report()
print()
print("✓ House homeostatic draw complete.")
