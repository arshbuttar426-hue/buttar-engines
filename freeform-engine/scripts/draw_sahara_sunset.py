#!/usr/bin/env python3
"""Sahara Desert sunset — dunes, haze, palm silhouettes, warm amber sky."""

import sys, math, random
sys.path.insert(0, '/Users/arshbuttar/.opencode_knowledge/scripts')
from freeform_renderer import Canvas

W, H = 660, 700

c = Canvas(W, H)
c.bg(0.95, 0.76, 0.46)

# ─── Sky: dusty Sahara palette ───
sky_colors = [
    (0.15, 0.10, 0.28),   # deep indigo top
    (0.35, 0.15, 0.25),   # dusty magenta
    (0.60, 0.25, 0.12),   # terracotta
    (0.85, 0.50, 0.10),   # deep amber
    (0.95, 0.72, 0.25),   # golden
    (0.98, 0.85, 0.45),   # pale gold horizon
    (0.95, 0.88, 0.60),   # dust haze at horizon
]
c.gradient_linear(0, 0, 0, 490, sky_colors)

# ─── Sun — large, hazy desert sun ───
# Outer glow
c.gs()
glow = [
    (1.0, 0.9, 0.5, 0.0),
    (1.0, 0.85, 0.4, 0.25),
    (1.0, 0.9, 0.5, 0.5),
    (1.0, 1.0, 0.85, 1.0),
]
c.gradient_radial(330, 450, 100, 330, 450, 8, glow)
c.gr()

# Sun disc
c.gs()
c.fc((1.0, 0.92, 0.65))
c.circle(330, 450, 45)
c.gr()

# Bright core
c.gs()
c.fc((1.0, 1.0, 0.92))
c.circle(330, 450, 22)
c.gr()

# ─── Distant dust haze band ───
c.gs()
dust = [(0.95, 0.82, 0.50, 0.0), (0.92, 0.78, 0.45, 0.35), (0.90, 0.75, 0.40, 0.0)]
c.gradient_linear(0, 460, 0, 520, dust)
c.gr()

# ─── Dune function — smooth catmull-rom curves ───
def draw_dune(pts, color):
    c.gs()
    c.fc(color)
    c.fill_curve(pts)
    c.gr()

# Far dunes (lighter, atmospheric)
far_dune = [(0, 490)]
for x in range(0, 661, 5):
    y = 490 - 25 * (1 + math.sin(x * 0.008 + 1.0)) * 0.5 \
          - 15 * (1 + math.sin(x * 0.018 + 2.5)) * 0.5
    far_dune.append((x, y))
far_dune += [(660, 490), (660, 510), (0, 510)]
draw_dune(far_dune, (0.40, 0.22, 0.12, 0.5))

# Mid dunes
mid_dune = [(0, 500)]
for x in range(0, 661, 4):
    y = 500 - 40 * (1 + math.sin(x * 0.01 + 0.3)) * 0.5 \
          - 20 * (1 + math.sin(x * 0.022 + 1.8)) * 0.5 \
          - 10 * (1 + math.sin(x * 0.04 + 3.0)) * 0.5
    mid_dune.append((x, y))
mid_dune += [(660, 500), (660, 520), (0, 520)]
draw_dune(mid_dune, (0.25, 0.14, 0.08, 0.7))

# Near dunes (darkest, most detailed)
near_dune = [(0, 510)]
for x in range(0, 661, 3):
    y = 510 - 55 * (1 + math.sin(x * 0.009 + 1.6)) * 0.5 \
          - 30 * (1 + math.sin(x * 0.019 + 0.7)) * 0.5 \
          - 15 * (1 + math.sin(x * 0.035 + 2.2)) * 0.5 \
          - 8 * (1 + math.sin(x * 0.06 + 4.1)) * 0.5
    near_dune.append((x, y))
near_dune += [(660, 510), (660, 540), (0, 540)]
draw_dune(near_dune, (0.12, 0.07, 0.05))

# ─── Ground dunes ───
ground = [(0, 540)]
for x in range(0, 661, 4):
    y = 540 + 15 * math.sin(x * 0.015 + 0.5) \
          + 8 * math.sin(x * 0.04 + 2.0) \
          + 4 * math.sin(x * 0.08 + 1.0)
    ground.append((x, y))
ground += [(660, 540), (660, H), (0, H)]
c.gs()
c.fc((0.07, 0.05, 0.04))
c.fill_curve(ground)
c.gr()

# ─── Dune ridge highlights (golden edge light from sun) ───
c.gs()
c.lw(1.5)
c.sc((1.0, 0.7, 0.25, 0.2))
for x in range(20, 641, 30):
    ly = 540 + 15 * math.sin(x * 0.015 + 0.5) + 8 * math.sin(x * 0.04 + 2.0) + 4 * math.sin(x * 0.08 + 1.0)
    c.line(x - 5, ly - 1, x + 5, ly - 1)
c.gr()

# ─── Palm tree silhouette ───
def draw_palm(cx, cy, h):
    c.gs()
    c.fc((0.04, 0.03, 0.03))
    # Trunk — curved
    trunk = [(cx, cy)]
    for i in range(1, 11):
        t = i / 10
        tx = cx + 8 * math.sin(t * math.pi * 0.4)
        ty = cy - t * h
        trunk.append((tx, ty))
    c.lw(4)
    c.polyline(trunk)
    # Fronds
    c.lw(2)
    frond_h = h * 0.35
    angles = [-55, -35, -15, 5, 25, 45, 65]
    for a in angles:
        rad = math.radians(a)
        fx = trunk[-1][0]
        fy = trunk[-1][1]
        pts = [(fx, fy)]
        for t in range(1, 9):
            tt = t / 8
            px = fx + tt * frond_h * 0.6 * math.cos(rad)
            py = fy - tt * frond_h * 0.3 * math.sin(abs(rad)) * 0.5
            # droop
            droop = tt * tt * 8
            pts.append((px, py + droop))
            # hang down more at tips
        pts.append((pts[-1][0], pts[-1][1] + 5))
        c.polyline(pts)
    # Extra fronds going other way
    rad2 = math.radians(20)
    for side in [-1, 1]:
        pts = [(trunk[-1][0], trunk[-1][1])]
        for t in range(1, 9):
            tt = t / 8
            px = trunk[-1][0] + side * tt * frond_h * 0.7 * math.cos(rad2)
            py = trunk[-1][1] - tt * frond_h * 0.2
            droop = tt * tt * 10
            pts.append((px, py + droop))
        c.polyline(pts)
    c.gr()

# Draw palm trees at various positions
for px, ph in [(580, 90), (90, 75), (140, 60)]:
    draw_palm(px, 540 + 8 * math.sin(px * 0.02) + 5 * math.sin(px * 0.05 + 1.0), ph)

# ─── Camel silhouette ───
def draw_camel(cx, cy, s):
    """Simple camel silhouette at (cx, cy) with scale s."""
    c.gs()
    c.lw(3 * s)
    # Body
    body = [(cx, cy)]
    for i in range(1, 21):
        t = i / 20
        bx = cx + t * 60 * s
        by = cy - 25 * s * math.sin(t * math.pi)
        if 0.3 < t < 0.7:
            by -= 10 * s * math.sin((t - 0.3) / 0.4 * math.pi)  # hump
        body.append((bx, by))
    c.polyline(body)
    # Neck and head
    neck = [(cx + 55 * s, cy - 5 * s)]
    for i in range(1, 8):
        t = i / 7
        nx = cx + 55 * s - t * 15 * s
        ny = cy - 5 * s - t * 40 * s
        neck.append((nx, ny))
    # Head
    neck.append((cx + 40 * s - 55 * s, cy - 45 * s))  # snout
    c.polyline(neck)
    # Legs
    legs_x = [cx + 10 * s, cx + 20 * s, cx + 40 * s, cx + 50 * s]
    for lx in legs_x:
        ly = cy - 5 * s + 3 * s * math.sin(lx * 0.5)
        c.line(lx, ly, lx, ly + 30 * s)
    c.gr()

draw_camel(340, 565, 1.4)

# ─── Tiny stars beginning to appear ───
c.gs()
c.fc((1.0, 0.95, 0.8, 0.5))
stars = [(80, 50, 1), (180, 30, 0.8), (250, 70, 0.6), (420, 40, 1),
         (530, 60, 0.7), (600, 35, 0.9), (140, 90, 0.5), (490, 80, 0.6),
         (350, 25, 0.4), (560, 95, 0.5)]
for sx, sy, sr in stars:
    c.circle(sx, sy, sr)
c.gr()

# ─── Heat shimmer lines at horizon ───
c.gs()
c.lw(1)
c.sc((1.0, 0.85, 0.5, 0.08))
for i in range(30):
    y = 460 + random.uniform(0, 30)
    x = random.uniform(0, 660)
    c.line(x, y, x + random.uniform(10, 30), y + random.uniform(-2, 2))
c.gr()

path = c.show("/tmp/sahara_sunset.png")
print(f"Sahara sunset drawn → {path}")
