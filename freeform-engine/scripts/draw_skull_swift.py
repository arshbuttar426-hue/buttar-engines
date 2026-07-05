"""
Human skull — rendered through the Swift DrawingServer via TCP.
No CGEvent clicks, no pen calibration, no Freeform.
Pure vector strokes on a native SwiftUI Canvas with zoom/pan.

Usage:
    Terminal 1: cd ~/.opencode_knowledge/DrawingServer && .build/debug/DrawingServer
    Terminal 2: python3 draw_skull_swift.py
"""

import time, sys, os, math

sys.path.insert(0, os.path.expanduser("~/.opencode_knowledge/scripts"))
from drawing_client import DrawingClient

# Skull center — same coordinate space as the house
CX, CY = 330, 385

print("=" * 56)
print("  SKULL — SWIFT CANVAS (TCP)")
print("=" * 56)
print()


def catmull(pts, n=40, closed=False):
    """Catmull-Rom spline (same math as the engine, pre-computed locally)."""
    out = []
    plen = len(pts) - 1 if not closed else len(pts)
    for i in range(plen):
        if closed:
            p0 = pts[(i - 1) % len(pts)]
            p1 = pts[i % len(pts)]
            p2 = pts[(i + 1) % len(pts)]
            p3 = pts[(i + 2) % len(pts)]
        else:
            p0 = pts[max(0, i - 1)]
            p1 = pts[i]
            p2 = pts[min(len(pts) - 1, i + 1)]
            p3 = pts[min(len(pts) - 1, i + 2)]
        for j in range(n):
            t = j / n
            t2 = t * t
            t3 = t2 * t
            x = 0.5 * (
                (2 * p1[0])
                + (-p0[0] + p2[0]) * t
                + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
            )
            y = 0.5 * (
                (2 * p1[1])
                + (-p0[1] + p2[1]) * t
                + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
            )
            out.append((x, y))
    if closed and out:
        out.append(out[0])
    return out


def connect_to_server(host="localhost", port=9876, retries=30, delay=1):
    """Retry connection to the DrawingServer until it's ready."""
    for i in range(retries):
        try:
            dc = DrawingClient(host, port)
            dc.connect()
            print(f"  Connected to DrawingServer on attempt {i+1}")
            return dc
        except ConnectionRefusedError:
            if i < retries - 1:
                print(f"  Waiting for DrawingServer... ({i+1}/{retries})")
                time.sleep(delay)
    print("  ERROR: Could not connect to DrawingServer")
    print("  Run: cd ~/.opencode_knowledge/DrawingServer && .build/debug/DrawingServer")
    return None


# ── Connect with retry ─────────────────────────────────────────

dc = connect_to_server()
if dc is None:
    sys.exit(1)

try:
    dc.clear()
    time.sleep(0.2)

    # ── 1. CRANIUM OUTLINE ────────────────────────────────────
    print("[1/10] Cranium outline...")
    cranium_pts = catmull([
        (CX, 248),
        (CX + 20, 252),
        (CX + 48, 266),
        (CX + 68, 290),
        (CX + 78, 318),
        (CX + 82, 346),
        (CX + 78, 368),
        (CX + 70, 385),
        (CX + 60, 405),
        (CX + 42, 430),
        (CX + 22, 450),
        (CX, 460),
        (CX - 22, 450),
        (CX - 42, 430),
        (CX - 60, 405),
        (CX - 70, 385),
        (CX - 78, 368),
        (CX - 82, 346),
        (CX - 78, 318),
        (CX - 68, 290),
        (CX - 48, 266),
        (CX - 20, 252),
    ], n=55, closed=True)
    dc.stroke(cranium_pts, width=2.0)
    r = dc.ink_count(CX - 88, 243, CX + 88, 465)
    print(f"  [Ink] cranium: {r.get('inkCount', '?')} pts")

    # ── 2. TEMPORAL LINES ─────────────────────────────────────
    print("[2/10] Temporal contours...")
    dc.stroke(catmull([
        (CX - 18, 260), (CX - 32, 278), (CX - 38, 300), (CX - 35, 320),
    ], 25), width=1.5)
    dc.stroke(catmull([
        (CX + 18, 260), (CX + 32, 278), (CX + 38, 300), (CX + 35, 320),
    ], 25), width=1.5)
    r = dc.ink_count(CX - 42, 255, CX + 42, 325)
    print(f"  [Ink] temporal: {r.get('inkCount', '?')} pts")

    # ── 3. EYE SOCKETS ────────────────────────────────────────
    print("[3/10] Eye sockets...")
    dc.ellipse(CX - 32, CY - 34, 22, 16, width=2.0)
    dc.ellipse(CX - 32, CY - 34, 18, 13, width=1.5)
    dc.ellipse(CX + 32, CY - 34, 22, 16, width=2.0)
    dc.ellipse(CX + 32, CY - 34, 18, 13, width=1.5)
    r = dc.ink_count(CX - 58, CY - 55, CX + 58, CY - 15)
    print(f"  [Ink] eyes: {r.get('inkCount', '?')} pts")

    # ── 4. BROW RIDGES ────────────────────────────────────────
    print("[4/10] Brow ridges...")
    dc.stroke(catmull([
        (CX, CY - 48), (CX - 12, CY - 46), (CX - 24, CY - 44),
        (CX - 36, CY - 42), (CX - 48, CY - 38), (CX - 54, CY - 36),
    ], 25), width=2.5)
    dc.stroke(catmull([
        (CX, CY - 48), (CX + 12, CY - 46), (CX + 24, CY - 44),
        (CX + 36, CY - 42), (CX + 48, CY - 38), (CX + 54, CY - 36),
    ], 25), width=2.5)
    dc.stroke(catmull([
        (CX, CY - 46), (CX - 12, CY - 44), (CX - 24, CY - 42),
        (CX - 36, CY - 40), (CX - 48, CY - 36),
    ], 20), width=2.0)
    dc.stroke(catmull([
        (CX, CY - 46), (CX + 12, CY - 44), (CX + 24, CY - 42),
        (CX + 36, CY - 40), (CX + 48, CY - 36),
    ], 20), width=2.0)
    r = dc.ink_count(CX - 58, CY - 55, CX + 58, CY - 30)
    print(f"  [Ink] brows: {r.get('inkCount', '?')} pts")

    # ── 5. NASAL CAVITY ───────────────────────────────────────
    print("[5/10] Nasal cavity + bridge...")
    dc.stroke(catmull([
        (CX, CY - 48), (CX, CY - 38), (CX - 1, CY - 28), (CX - 1, CY - 18),
    ], 20), width=2.0)
    dc.stroke(catmull([
        (CX, CY - 18), (CX - 6, CY - 6), (CX - 11, CY + 2),
        (CX - 9, CY + 12), (CX - 5, CY + 18), (CX, CY + 20),
        (CX + 5, CY + 18), (CX + 9, CY + 12), (CX + 11, CY + 2),
        (CX + 6, CY - 6), (CX, CY - 18),
    ], n=35, closed=True), width=2.0)
    r = dc.ink_count(CX - 15, CY - 50, CX + 15, CY + 25)
    print(f"  [Ink] nasal: {r.get('inkCount', '?')} pts")

    # ── 6. CHEEKBONES ─────────────────────────────────────────
    print("[6/10] Cheekbones...")
    dc.stroke(catmull([
        (CX - 48, CY - 20), (CX - 60, CY - 12), (CX - 68, CY - 2),
        (CX - 72, CY + 6), (CX - 68, CY + 12),
    ], 25), width=2.0)
    dc.stroke(catmull([
        (CX + 48, CY - 20), (CX + 60, CY - 12), (CX + 68, CY - 2),
        (CX + 72, CY + 6), (CX + 68, CY + 12),
    ], 25), width=2.0)
    r = dc.ink_count(CX - 78, CY - 25, CX + 78, CY + 17)
    print(f"  [Ink] cheekbones: {r.get('inkCount', '?')} pts")

    # ── 7. MAXILLA ────────────────────────────────────────────
    print("[7/10] Maxilla...")
    dc.stroke(catmull([
        (CX - 22, CY + 20), (CX - 28, CY + 28), (CX - 30, CY + 33),
        (CX - 26, CY + 39), (CX, CY + 42),
    ], 20), width=2.5)
    dc.stroke(catmull([
        (CX, CY + 42), (CX + 26, CY + 39), (CX + 30, CY + 33),
        (CX + 28, CY + 28), (CX + 22, CY + 20),
    ], 20), width=2.5)
    dc.stroke(catmull([
        (CX - 22, CY + 41), (CX, CY + 46), (CX + 22, CY + 41),
    ], 15), width=2.5)
    r = dc.ink_count(CX - 35, CY + 18, CX + 35, CY + 52)
    print(f"  [Ink] maxilla: {r.get('inkCount', '?')} pts")

    # ── 8. TEETH ──────────────────────────────────────────────
    print("[8/10] Teeth...")
    for i in range(-3, 4):
        tx = CX + i * 8
        dc.line(tx, CY + 44, tx, CY + 53, width=2.5)
    for i in range(-3, 4):
        tx = CX + i * 8
        dc.line(tx, CY + 53, tx, CY + 61, width=2.5)
    dc.line(CX, CY + 44, CX, CY + 53, width=2.5)
    dc.line(CX, CY + 53, CX, CY + 61, width=2.5)
    r = dc.ink_count(CX - 30, CY + 42, CX + 30, CY + 65)
    print(f"  [Ink] teeth: {r.get('inkCount', '?')} pts")

    # ── 9. MANDIBLE ───────────────────────────────────────────
    print("[9/10] Mandible...")
    dc.stroke(catmull([
        (CX - 18, CY + 58), (CX - 24, CY + 62), (CX - 22, CY + 68),
        (CX - 12, CY + 76), (CX, CY + 78), (CX + 12, CY + 76),
        (CX + 22, CY + 68), (CX + 24, CY + 62), (CX + 18, CY + 58),
    ], 30), width=2.0)
    dc.circle(CX - 16, CY + 66, 2, n=12, width=1.5)
    dc.circle(CX + 16, CY + 66, 2, n=12, width=1.5)
    r = dc.ink_count(CX - 28, CY + 55, CX + 28, CY + 82)
    print(f"  [Ink] mandible: {r.get('inkCount', '?')} pts")

    # ── 10. SUTURES ───────────────────────────────────────────
    print("[10/10] Cranial sutures...")
    dc.stroke(catmull([
        (CX - 55, 278), (CX - 40, 282), (CX - 25, 276),
        (CX, 273), (CX + 25, 276), (CX + 40, 282), (CX + 55, 278),
    ], 25), width=1.5)
    dc.stroke(catmull([
        (CX, 273), (CX, 262), (CX - 1, 254), (CX, 248),
    ], 15), width=1.5)
    dc.stroke(catmull([
        (CX - 42, 282), (CX - 48, 295), (CX - 42, 306),
    ], 15), width=1.5)
    dc.stroke(catmull([
        (CX + 42, 282), (CX + 48, 295), (CX + 42, 306),
    ], 15), width=1.5)
    r = dc.ink_count(CX - 58, 243, CX + 58, 310)
    print(f"  [Ink] sutures: {r.get('inkCount', '?')} pts")

    # ── FINAL INK REPORT ──────────────────────────────────────
    print()
    print("─" * 56)
    print("  INK REPORT")
    print("─" * 56)
    for name, bbox in [
        ("cranium",    (CX - 88, 243, CX + 88, 465)),
        ("temporal",   (CX - 42, 255, CX + 42, 325)),
        ("eyes",       (CX - 58, CY - 55, CX + 58, CY - 15)),
        ("brows",      (CX - 58, CY - 55, CX + 58, CY - 30)),
        ("nasal",      (CX - 15, CY - 50, CX + 15, CY + 25)),
        ("cheekbones", (CX - 78, CY - 25, CX + 78, CY + 17)),
        ("maxilla",    (CX - 35, CY + 18, CX + 35, CY + 52)),
        ("teeth",      (CX - 30, CY + 42, CX + 30, CY + 65)),
        ("mandible",   (CX - 28, CY + 55, CX + 28, CY + 82)),
        ("sutures",    (CX - 58, 243, CX + 58, 310)),
    ]:
        r = dc.ink_count(*bbox)
        print(f"  {name:<14s} {r.get('inkCount', '?'):>5} pts")

    print()
    print("✓ Skull rendered via Swift DrawingServer.")
    print()
    print("  Zoom with pinch gesture. Pan with drag.")

finally:
    dc.close()
