#!/usr/bin/env python3
"""Beautiful sunset — rendered via Quartz CGContext, pasted into Freeform."""

import sys, math
sys.path.insert(0, '/Users/arshbuttar/.opencode_knowledge/scripts')
from freeform_renderer import Canvas, hatch_fill

W, H = 660, 700

c = Canvas(W, H)
c.bg(0.95, 0.76, 0.46)  # warm sand bg, will be covered by sky gradient

# ─── Sky gradient: deep purple → orange → gold ───
sky_colors = [
    (0.12, 0.08, 0.25),   # deep purple top
    (0.35, 0.10, 0.30),   # magenta-purple
    (0.70, 0.20, 0.15),   # deep red
    (0.95, 0.45, 0.10),   # orange
    (1.00, 0.70, 0.20),   # golden orange
    (1.00, 0.85, 0.40),   # gold at horizon
]
c.gradient_linear(0, 0, 0, 480, sky_colors)

# ─── Sun glow (radial gradient) ───
c.gs()
glow_colors = [
    (1.0, 1.0, 0.8, 0.0),    # transparent edge
    (1.0, 0.9, 0.5, 0.3),    # soft glow
    (1.0, 0.95, 0.6, 0.6),   # bright glow
    (1.0, 1.0, 0.9, 1.0),    # core
]
c.gradient_radial(330, 440, 80, 330, 440, 5, glow_colors)
c.gr()

# ─── Sun disc ───
c.gs()
c.fc((1.0, 0.95, 0.75))
c.circle(330, 440, 35)
c.gr()

# ─── Sun inner bright core ───
c.gs()
c.fc((1.0, 1.0, 0.95))
c.circle(330, 440, 18)
c.gr()

# ─── Clouds ───
cloud_color = (0.90, 0.50, 0.30, 0.5)
cloud_color2 = (0.95, 0.65, 0.35, 0.4)
cloud_color3 = (0.40, 0.20, 0.45, 0.35)

def draw_cloud(cx, cy, w, h, color):
    c.gs()
    c.fc(color)
    pts = [
        (cx - w * 0.4, cy + h * 0.1),
        (cx - w * 0.35, cy - h * 0.2),
        (cx - w * 0.2, cy - h * 0.4),
        (cx, cy - h * 0.45),
        (cx + w * 0.2, cy - h * 0.35),
        (cx + w * 0.35, cy - h * 0.2),
        (cx + w * 0.4, cy + h * 0.05),
        (cx + w * 0.3, cy + h * 0.2),
        (cx - w * 0.3, cy + h * 0.2),
    ]
    c.fill_curve(pts)
    c.gr()

# Upper clouds (distant, smaller)
draw_cloud(180, 250, 120, 40, cloud_color3)
draw_cloud(470, 220, 100, 35, cloud_color3)
draw_cloud(350, 180, 140, 45, cloud_color3)

# Mid clouds (warm lit)
draw_cloud(150, 360, 150, 50, cloud_color2)
draw_cloud(500, 340, 130, 45, cloud_color2)
draw_cloud(300, 320, 110, 35, cloud_color2)

# Lower clouds (bright orange-gold, near sun)
draw_cloud(200, 400, 100, 30, cloud_color)
draw_cloud(460, 390, 120, 35, cloud_color)

# ─── Horizon haze ───
c.gs()
haze_colors = [(1.0, 0.75, 0.35, 0.0), (1.0, 0.70, 0.30, 0.3), (1.0, 0.65, 0.25, 0.0)]
c.gradient_linear(0, 470, 0, 510, haze_colors)
c.gr()

# ─── Distant mountains ───
def draw_mountains(pts, color):
    c.gs()
    c.fc(color)
    c.fill_path(pts)
    c.gr()

# Far mountain range (lighter, atmospheric)
far_mtn = [(0, 490)] + [
    (x, 490 - 30 * (1 + math.sin(x * 0.015 + 1.3)) * 0.5
       - 20 * (1 + math.sin(x * 0.025 + 0.7)) * 0.5
       - 15 * (1 + math.sin(x * 0.04 + 2.1)) * 0.5)
    for x in range(0, 661, 8)
] + [(660, 490), (660, 500), (0, 500)]
draw_mountains(far_mtn, (0.25, 0.12, 0.20, 0.6))

# Mid mountain range
mid_mtn = [(0, 500)] + [
    (x, 500 - 50 * (1 + math.sin(x * 0.012 + 2.5)) * 0.5
       - 30 * (1 + math.sin(x * 0.022 + 0.1)) * 0.5
       - 20 * (1 + math.sin(x * 0.035 + 1.8)) * 0.5)
    for x in range(0, 661, 6)
] + [(660, 500), (660, 510), (0, 510)]
draw_mountains(mid_mtn, (0.18, 0.08, 0.15, 0.8))

# Near mountain range (darkest)
near_mtn = [(0, 510)] + [
    (x, 510 - 60 * (1 + math.sin(x * 0.01 + 0.5)) * 0.5
       - 40 * (1 + math.sin(x * 0.02 + 3.2)) * 0.5
       - 25 * (1 + math.sin(x * 0.033 + 0.9)) * 0.5)
    for x in range(0, 661, 5)
] + [(660, 510), (660, 530), (0, 530)]
draw_mountains(near_mtn, (0.10, 0.05, 0.08))

# ─── Ground silhouette ───
ground = [(0, 530)] + [
    (x, 530 + 10 * math.sin(x * 0.02 + 1.0)
        + 5 * math.sin(x * 0.05 + 2.5)
        + 3 * math.sin(x * 0.1 + 0.3))
    for x in range(0, 661, 8)
] + [(660, 530), (660, H), (0, H)]
c.gs()
c.fc((0.06, 0.04, 0.05))
c.fill_path(ground)
c.gr()

# ─── Tree silhouettes on ground ───
def draw_tree(x, y, h, w):
    c.gs()
    c.fc((0.04, 0.03, 0.04))
    # trunk
    c.rect(x - w * 0.04, y - h * 0.1, x + w * 0.04, y, f=(0.04, 0.03, 0.04))
    # canopy (multiple overlapping circles)
    c.circle(x, y - h * 0.4, w * 0.25)
    c.circle(x - w * 0.15, y - h * 0.3, w * 0.2)
    c.circle(x + w * 0.15, y - h * 0.3, w * 0.2)
    c.circle(x - w * 0.08, y - h * 0.55, w * 0.18)
    c.circle(x + w * 0.08, y - h * 0.55, w * 0.18)
    c.circle(x, y - h * 0.65, w * 0.15)
    c.gr()

for tx, th, tw in [(80, 70, 30), (150, 55, 22), (550, 65, 28), (600, 50, 20), (480, 40, 16)]:
    draw_tree(tx, 530 + 5 * math.sin(tx * 0.02 + 1.0), th, tw)

# ─── Star/fireflies overlay (tiny dots in sky) ───
c.gs()
c.fc((1.0, 1.0, 0.9, 0.6))
for sx, sy, sr in [(120, 80, 1.5), (540, 60, 1), (450, 100, 1.2), (200, 130, 0.8),
                    (580, 150, 1), (80, 170, 0.8), (620, 90, 0.6), (300, 70, 0.7)]:
    c.circle(sx, sy, sr)
c.gr()

# ─── Water reflection (subtle light streaks on ground) ───
c.gs()
c.lw(1.5)
c.sc((1.0, 0.8, 0.4, 0.15))
for i in range(12):
    rx = 200 + i * 25 + 10 * math.sin(i * 1.5)
    ry = 580 + 20 * math.sin(i * 0.7)
    rw = 15 + 10 * math.sin(i * 0.9)
    c.line(rx - rw, ry, rx + rw, ry)
c.gr()

# ─── Export & show in Freeform ───
path = c.show("/tmp/sunset_drawing.png")
print(f"Sunset drawn → {path}")
