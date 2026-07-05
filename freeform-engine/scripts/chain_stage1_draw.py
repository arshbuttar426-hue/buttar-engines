#!/usr/bin/env python3
"""Stage 1: Quartz cityscape → Canny edges → ControlNet SD 1.5 → output."""

import sys, math, random
sys.path.insert(0, '/Users/arshbuttar/.opencode_knowledge/scripts')
from freeform_renderer import Canvas

W, H = 660, 700
c = Canvas(W, H)
c.bg(0.95, 0.76, 0.46)

# ─── Twilight sky ───
sky = [
    (0.05, 0.02, 0.12), (0.08, 0.05, 0.20), (0.12, 0.10, 0.30),
    (0.20, 0.18, 0.40), (0.40, 0.25, 0.35), (0.70, 0.35, 0.20),
    (0.90, 0.55, 0.20),
]
c.gradient_linear(0, 0, 0, 500, sky)

# ─── Moon ───
c.gs(); c.fc((0.95, 0.92, 0.80, 0.9)); c.circle(520, 90, 28); c.gr()
c.gs()
moon_glow = [(0.95, 0.92, 0.80, 0.0), (0.90, 0.85, 0.70, 0.15), (0.85, 0.80, 0.60, 0.0)]
c.gradient_radial(520, 90, 60, 520, 90, 28, moon_glow); c.gr()

# ─── Stars ───
c.gs(); c.fc((1.0, 1.0, 0.95, 0.7))
random.seed(42)
for _ in range(80):
    c.circle(random.uniform(5, 655), random.uniform(5, 260), random.uniform(0.4, 1.8))
c.gr()

# ─── Buildings ───
buildings = [
    (20, 30, 120, 'flat'), (55, 25, 90, 'flat'), (85, 35, 160, 'pointed'),
    (125, 20, 100, 'flat'), (150, 28, 140, 'stepped'), (182, 22, 110, 'antenna'),
    (208, 40, 200, 'flat'), (252, 18, 85, 'flat'), (274, 32, 175, 'pointed'),
    (310, 25, 150, 'spire'), (340, 20, 95, 'flat'), (364, 45, 230, 'stepped'),
    (414, 22, 130, 'antenna'), (440, 35, 190, 'flat'), (480, 18, 80, 'flat'),
    (502, 30, 165, 'pointed'), (536, 24, 110, 'antenna'), (564, 35, 185, 'stepped'),
    (604, 20, 95, 'flat'), (628, 28, 140, 'pointed'),
]

def draw_building(c, x, w, h, base_y, style, color, window_color):
    c.gs(); c.fc(color)
    if style == 'flat':
        c.rect(x, base_y - h, x + w, base_y, f=color)
    elif style == 'pointed':
        c.rect(x, base_y - h * 0.7, x + w, base_y, f=color)
        c.fill_path([(x, base_y - h * 0.7), (x + w / 2, base_y - h), (x + w, base_y - h * 0.7)])
    elif style == 'stepped':
        levels = [(x, base_y - h), (x + w * 0.15, base_y - h * 0.85),
                  (x + w * 0.3, base_y - h * 0.85), (x + w * 0.3, base_y - h * 0.65),
                  (x + w * 0.5, base_y - h * 0.65), (x + w * 0.5, base_y - h * 0.5),
                  (x + w, base_y - h * 0.5)]
        for i in range(len(levels) - 1):
            c.rect(levels[i][0], levels[i][1], levels[i + 1][0], base_y, f=color)
        c.rect(x, base_y - h, x + w * 0.15, base_y, f=color)
    elif style == 'antenna':
        c.rect(x, base_y - h * 0.85, x + w, base_y, f=color)
        c.lw(1.5); c.sc((0.3, 0.3, 0.35))
        c.line(x + w / 2, base_y - h * 0.85, x + w / 2, base_y - h)
        c.line(x + w / 2, base_y - h, x + w / 2 - 3, base_y - h * 0.92)
        c.line(x + w / 2, base_y - h, x + w / 2 + 3, base_y - h * 0.92)
    elif style == 'spire':
        c.rect(x, base_y - h * 0.6, x + w, base_y, f=color)
        c.fill_path([(x, base_y - h * 0.6), (x + w / 2, base_y - h), (x + w, base_y - h * 0.6)])
    c.gr()
    if window_color:
        c.gs(); c.fc(window_color)
        n_cols = max(2, int(w / 12))
        n_rows = max(2, int(h * 0.7 / 14))
        for row in range(n_rows):
            for col in range(n_cols):
                if random.random() < 0.55:
                    wx = x + 3 + col * (w - 6) / n_cols
                    wy = base_y - h * 0.75 + row * 14
                    c.rect(wx, wy, wx + 4, wy + 6, f=window_color)
        c.gr()

for x, w, h, style in buildings:
    color = (0.06, 0.05, 0.10)
    win_color = (0.95, 0.85, 0.40, 0.7) if random.random() < 0.6 else (0.85, 0.75, 0.30, 0.4)
    draw_building(c, x, w, h, 510, style, color, win_color)

# ─── Water ───
c.gs()
water = [(0.05, 0.04, 0.12), (0.08, 0.06, 0.18), (0.10, 0.08, 0.15)]
c.gradient_linear(0, 510, 0, H, water); c.gr()

# ─── Reflection streaks ───
c.gs(); c.lw(1.5)
random.seed(99)
for _ in range(40):
    rx = random.uniform(10, 650); rw = random.uniform(4, 20)
    ry = random.uniform(520, 650); rh = random.uniform(2, 8)
    alpha = random.uniform(0.05, 0.15)
    c.sc((0.90, 0.70, 0.30, alpha))
    c.line(rx, ry, rx + rw * random.uniform(-1, 1), ry + rh)
c.gr()

# ─── Bridge ───
bridge_y = 580
c.gs(); c.fc((0.03, 0.025, 0.04))
c.rect(0, bridge_y, W, bridge_y + 8, f=(0.03, 0.025, 0.04))
for px in [80, 200, 330, 460, 580]:
    c.rect(px - 4, bridge_y - 40, px + 4, bridge_y, f=(0.03, 0.025, 0.04))
c.lw(1.5); c.sc((0.05, 0.04, 0.06))
for px in [80, 200, 330, 460, 580]:
    for side in [-1, 1]:
        pts = [(px, bridge_y - 40)]
        for t in range(1, 6):
            tt = t / 5
            pts.append((px + side * tt * 100, bridge_y - 40 + tt * tt * 45))
        c.polyline(pts)
c.gr()

# ─── Shore ───
c.gs(); c.fc((0.035, 0.03, 0.04))
shore = [(0, 630)]
for x in range(0, 661, 6):
    shore.append((x, 630 + 3 * math.sin(x * 0.03 + 0.5) + 2 * math.sin(x * 0.07 + 1.2)))
shore += [(660, 630), (660, H), (0, H)]
c.fill_curve(shore); c.gr()

path = c.save("/tmp/chain_input.png")
print(f"Input: {path}")
