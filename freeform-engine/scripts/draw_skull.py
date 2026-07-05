"""
Human skull — complex anatomical composition drawn in Freeform.
================================================================

Each anatomical region is wrapped in homeostatic_draw() for set-point
calibration and integrity verification.

Anatomical regions (front view):
  1. Cranium outline (dome)
  2. Temporal/zygomatic contours
  3. Eye sockets (orbits)
  4. Brow ridges (supraorbital)
  5. Nasal cavity + bridge
  6. Cheekbones (zygomatic arches)
  7. Maxilla (upper jaw)
  8. Teeth (upper + lower)
  9. Mandible (lower jaw)
  10. Cranial sutures + detail

Usage:
    PATH="/tmp/drawenv/bin:$PATH" python3 draw_skull.py
"""

import time, os, sys
sys.path.insert(0, os.path.expanduser('~/.opencode_knowledge/scripts'))
from freeform_engine import *

# Skull center — positioned in the same drawing area as the house
CX, CY = 330, 385

print("=" * 56)
print("  SKULL — ANATOMICAL COMPOSITION")
print("=" * 56)
print()
setup()
time.sleep(1.0)

# ════════════════════════════════════════════════════════════════════
# 1. CRANIUM OUTLINE — full skull silhouette
# ════════════════════════════════════════════════════════════════════
# The characteristic dome shape. Control points traced from anatomical
# reference. Closed Catmull-Rom spline for a seamless contour.

def draw_cranium():
    pts = catmull([
        (CX, 248),          # vertex (top center) — raised for anatom. cranium ratio
        (CX + 20, 252),     # upper right curve
        (CX + 48, 266),     # right parietal
        (CX + 68, 290),     # right upper temple
        (CX + 78, 318),     # right temple (narrowest part)
        (CX + 82, 346),     # right zygomatic process
        (CX + 78, 368),     # right cheekbone peak
        (CX + 70, 385),     # right maxillary area
        (CX + 60, 405),     # right jaw hinge
        (CX + 42, 430),     # right ramus
        (CX + 22, 450),     # right lower mandible
        (CX, 460),          # chin center
        (CX - 22, 450),     # left lower mandible
        (CX - 42, 430),     # left ramus
        (CX - 60, 405),     # left jaw hinge
        (CX - 70, 385),     # left maxillary area
        (CX - 78, 368),     # left cheekbone peak
        (CX - 82, 346),     # left zygomatic process
        (CX - 78, 318),     # left temple (narrowest part)
        (CX - 68, 290),     # left upper temple
        (CX - 48, 266),     # left parietal
        (CX - 20, 252),     # upper left curve
    ], n=55, closed=True)
    polyline(pts, bold=False)

print("[1/10] Cranium outline...")
bb_cranium = (CX - 88, 243, CX + 88, 465)
homeostatic_draw("skull_cranium", draw_cranium, bbox=bb_cranium)


# ════════════════════════════════════════════════════════════════════
# 2. TEMPORAL LINES — subtle contours on the sides of the cranium
# ════════════════════════════════════════════════════════════════════

def draw_temporal_lines():
    # Left temporal line
    polyline(catmull([
        (CX - 18, 260),
        (CX - 32, 278),
        (CX - 38, 300),
        (CX - 35, 320),
    ], 25))
    # Right temporal line
    polyline(catmull([
        (CX + 18, 260),
        (CX + 32, 278),
        (CX + 38, 300),
        (CX + 35, 320),
    ], 25))

print("[2/10] Temporal contours...")
bb_temporal = (CX - 42, 255, CX + 42, 325)
homeostatic_draw("skull_temporal", draw_temporal_lines, bbox=bb_temporal)


# ════════════════════════════════════════════════════════════════════
# 3. EYE SOCKETS (ORBITS) — two large rounded quadrilateral openings
# ════════════════════════════════════════════════════════════════════

def draw_eye_sockets():
    # Left orbit — slightly angled, wider laterally
    ellipse_outline(CX - 32, CY - 34, 22, 16, n=55)
    # Right orbit
    ellipse_outline(CX + 32, CY - 34, 22, 16, n=55)
    # Inner ring (thicker orbital rim effect — smaller concentric ellipse)
    ellipse_outline(CX - 32, CY - 34, 18, 13, n=50)
    ellipse_outline(CX + 32, CY - 34, 18, 13, n=50)

print("[3/10] Eye sockets...")
bb_eyes = (CX - 58, CY - 55, CX + 58, CY - 15)
homeostatic_draw("skull_eyes", draw_eye_sockets, bbox=bb_eyes)


# ════════════════════════════════════════════════════════════════════
# 4. BROW RIDGES (SUPRAORBITAL MARGINS) — thick bone above each eye
# ════════════════════════════════════════════════════════════════════

def draw_brow_ridges():
    # Left brow — glabella to lateral edge
    polyline(catmull([
        (CX, CY - 48),       # glabella (center bridge)
        (CX - 12, CY - 46),
        (CX - 24, CY - 44),
        (CX - 36, CY - 42),
        (CX - 48, CY - 38),
        (CX - 54, CY - 36),
    ], 25))
    # Right brow
    polyline(catmull([
        (CX, CY - 48),
        (CX + 12, CY - 46),
        (CX + 24, CY - 44),
        (CX + 36, CY - 42),
        (CX + 48, CY - 38),
        (CX + 54, CY - 36),
    ], 25))
    # Second pass slightly offset for thickness
    polyline(catmull([
        (CX, CY - 46),
        (CX - 12, CY - 44),
        (CX - 24, CY - 42),
        (CX - 36, CY - 40),
        (CX - 48, CY - 36),
    ], 20))
    polyline(catmull([
        (CX, CY - 46),
        (CX + 12, CY - 44),
        (CX + 24, CY - 42),
        (CX + 36, CY - 40),
        (CX + 48, CY - 36),
    ], 20))

print("[4/10] Brow ridges...")
bb_brow = (CX - 58, CY - 55, CX + 58, CY - 30)
homeostatic_draw("skull_brows", draw_brow_ridges, bbox=bb_brow)


# ════════════════════════════════════════════════════════════════════
# 5. NASAL CAVITY + BRIDGE
# ════════════════════════════════════════════════════════════════════
# Pear-shaped pyriform aperture with bony nasal bridge above

def draw_nasal():
    # Nasal bridge (bony ridge of nose)
    polyline(catmull([
        (CX, CY - 48),
        (CX, CY - 38),
        (CX - 1, CY - 28),
        (CX - 1, CY - 18),
    ], 20))
    # Pyriform aperture (nasal opening) — keyhole/pear shape
    polyline(catmull([
        (CX, CY - 18),       # top of opening (nasal bone)
        (CX - 6, CY - 6),
        (CX - 11, CY + 2),   # widest point
        (CX - 9, CY + 12),
        (CX - 5, CY + 18),
        (CX, CY + 20),       # bottom point (anterior nasal spine)
        (CX + 5, CY + 18),
        (CX + 9, CY + 12),
        (CX + 11, CY + 2),   # widest point right
        (CX + 6, CY - 6),
        (CX, CY - 18),
    ], n=35, closed=True))

print("[5/10] Nasal cavity + bridge...")
bb_nasal = (CX - 15, CY - 50, CX + 15, CY + 25)
homeostatic_draw("skull_nasal", draw_nasal, bbox=bb_nasal)


# ════════════════════════════════════════════════════════════════════
# 6. CHEEKBONES (ZYGOMATIC ARCHES)
# ════════════════════════════════════════════════════════════════════

def draw_cheekbones():
    # Left zygomatic arch
    polyline(catmull([
        (CX - 48, CY - 20),
        (CX - 60, CY - 12),
        (CX - 68, CY - 2),
        (CX - 72, CY + 6),
        (CX - 68, CY + 12),
    ], 25))
    # Right zygomatic arch
    polyline(catmull([
        (CX + 48, CY - 20),
        (CX + 60, CY - 12),
        (CX + 68, CY - 2),
        (CX + 72, CY + 6),
        (CX + 68, CY + 12),
    ], 25))

print("[6/10] Cheekbones...")
bb_cheek = (CX - 78, CY - 25, CX + 78, CY + 17)
homeostatic_draw("skull_cheekbones", draw_cheekbones, bbox=bb_cheek)


# ════════════════════════════════════════════════════════════════════
# 7. MAXILLA (UPPER JAW) — below nasal cavity
# ════════════════════════════════════════════════════════════════════

def draw_maxilla():
    # Upper jaw outline — simplified to direct bold stroke lines
    # Left side
    bold5(catmull([
        (CX - 22, CY + 20), (CX - 28, CY + 28),
        (CX - 30, CY + 33), (CX - 26, CY + 39),
        (CX, CY + 42),
    ], 20))
    # Right side
    bold5(catmull([
        (CX, CY + 42),
        (CX + 26, CY + 39), (CX + 30, CY + 33),
        (CX + 28, CY + 28), (CX + 22, CY + 20),
    ], 20))
    # Alveolar margin (tooth socket base)
    bold5(catmull([
        (CX - 22, CY + 41), (CX, CY + 46), (CX + 22, CY + 41),
    ], 15))

print("[7/10] Maxilla...")
bb_maxilla = (CX - 35, CY + 18, CX + 35, CY + 52)
homeostatic_draw("skull_maxilla", draw_maxilla, bbox=bb_maxilla)
# Immediate diagnostic
ink_check = count_ink(*bb_maxilla)
print(f"  [Diag] maxilla immediate: {ink_check}px")


# ════════════════════════════════════════════════════════════════════
# 8. TEETH — upper and lower rows
# ════════════════════════════════════════════════════════════════════

def draw_teeth():
    # Upper teeth (7 visible incisors) — bold, wider spacing
    for i in range(-3, 4):
        tx = CX + i * 8
        polyline([(tx, CY + 44), (tx, CY + 53)], bold=True)
    # Lower teeth (7 visible)
    for i in range(-3, 4):
        tx = CX + i * 8
        polyline([(tx, CY + 53), (tx, CY + 61)], bold=True)
    # Midline gaps
    polyline([(CX, CY + 44), (CX, CY + 53)], bold=True)
    polyline([(CX, CY + 53), (CX, CY + 61)], bold=True)

print("[8/10] Teeth...")
bb_teeth = (CX - 30, CY + 42, CX + 30, CY + 65)
homeostatic_draw("skull_teeth", draw_teeth, bbox=bb_teeth)
# Immediate diagnostic
ink_check = count_ink(*bb_teeth)
print(f"  [Diag] teeth immediate: {ink_check}px")


# ════════════════════════════════════════════════════════════════════
# 9. MANDIBLE (LOWER JAW) — chin and mental foramina
# ════════════════════════════════════════════════════════════════════

def draw_mandible():
    # Mental protuberance (chin outline)
    polyline(catmull([
        (CX - 18, CY + 58),
        (CX - 24, CY + 62),
        (CX - 22, CY + 68),
        (CX - 12, CY + 76),
        (CX, CY + 78),
        (CX + 12, CY + 76),
        (CX + 22, CY + 68),
        (CX + 24, CY + 62),
        (CX + 18, CY + 58),
    ], 30))
    # Mental foramina (small nerve openings on mandible)
    circle_outline(CX - 16, CY + 66, 2, n=12)
    circle_outline(CX + 16, CY + 66, 2, n=12)

print("[9/10] Mandible...")
bb_mandible = (CX - 28, CY + 55, CX + 28, CY + 82)
homeostatic_draw("skull_mandible", draw_mandible, bbox=bb_mandible)


# ════════════════════════════════════════════════════════════════════
# 10. CRANIAL SUTURES + DETAIL
# ════════════════════════════════════════════════════════════════════
# Coronal, sagittal, and squamosal suture lines

def draw_sutures():
    # Coronal suture (across top of skull)
    polyline(catmull([
        (CX - 55, 278),
        (CX - 40, 282),
        (CX - 25, 276),
        (CX, 273),
        (CX + 25, 276),
        (CX + 40, 282),
        (CX + 55, 278),
    ], 25))
    # Sagittal suture (top center line)
    polyline(catmull([
        (CX, 273),
        (CX, 262),
        (CX - 1, 254),
        (CX, 248),
    ], 15))
    # Left squamosal suture (side)
    polyline(catmull([
        (CX - 42, 282),
        (CX - 48, 295),
        (CX - 42, 306),
    ], 15))
    # Right squamosal suture (side)
    polyline(catmull([
        (CX + 42, 282),
        (CX + 48, 295),
        (CX + 42, 306),
    ], 15))

print("[10/10] Cranial sutures...")
bb_sutures = (CX - 58, 243, CX + 58, 310)
homeostatic_draw("skull_sutures", draw_sutures, bbox=bb_sutures)


# ════════════════════════════════════════════════════════════════════
# INTEGRITY VERIFICATION
# ════════════════════════════════════════════════════════════════════

print()
print("─" * 56)
print("  INTEGRITY VERIFICATION")
print("─" * 56)

verify_drawing_integrity("skull_cranium", bb_cranium)
verify_drawing_integrity("skull_eyes", bb_eyes)
verify_drawing_integrity("skull_nasal", bb_nasal)
verify_drawing_integrity("skull_cheekbones", bb_cheek)
verify_drawing_integrity("skull_maxilla", bb_maxilla)
verify_drawing_integrity("skull_teeth", bb_teeth)
verify_drawing_integrity("skull_mandible", bb_mandible)
verify_drawing_integrity("skull_sutures", bb_sutures)

print()
integrity_report()
print()
print("✓ Skull composition complete.")
print()
print("  ┌─────────────────────────────────────────────────────┐")
print("  │  If the proportions look off, adjust control points │")
print("  │  in draw_skull.py and re-run. The homeostatic ink  │")
print("  │  set points from this run become the new baseline. │")
print("  └─────────────────────────────────────────────────────┘")
