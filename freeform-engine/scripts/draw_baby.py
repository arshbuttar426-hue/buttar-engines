"""
Baby infant drawn in Freeform using CGBitmapContext (new standard).
=======================

A simple, round baby with a bald head and basic body.

This script uses the new CGC rendering pipeline:
  1. Draw to CGBitmapContext 
  2. Export to PNG
  3. Paste into Freeform via clipboard

Usage:
    python3 draw_baby.py
"""

import time, subprocess
from freeform_renderer import Canvas

def setup():
    """Initialize Freeform with new board."""
    subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True)
    time.sleep(1)
    subprocess.run(['osascript', '-e', '''
        tell app "System Events"
            tell process "Freeform"
                click menu item "New Board" of menu "File" of menu bar 1
            end tell
        end tell
    '''], capture_output=True)
    time.sleep(1.5)

# Baby center (matches previous script coordinates)
BX, BY = 330, 500

print("=" * 56)
print("  BABY — INFANT (CGC Renderer)")
print("=" * 56)
print()

setup()
print()

c = Canvas(scale=2)  # 2x scaling

# ════════════════════════════════════════════════════════════════════
# HEAD (round, bald) - pentagonal shape
# ════════════════════════════════════════════════════════════════════
print("[1/8] Drawing head...")
c.sc((0.2, 0.2, 0.8))  # blue-gray color
c.line(BX - 50, BY - 50, BX + 50, BY - 50)
c.line(BX + 50, BY - 50, BX, BY + 70)
c.line(BX, BY + 70, BX - 50, BY - 50)
c.line(BX - 50, BY - 50, BX, BY - 70)
c.line(BX, BY - 70, BX + 50, BY - 50)
time.sleep(0.12)

# ════════════════════════════════════════════════════════════════════
# ARM - LEFT
# ════════════════════════════════════════════════════════════════════
print("[2/8] Drawing left arm...")
c.sc((0.3, 0.3, 0.9))
c.line(BX - 50, BY + 20, BX - 75, BY + 50)
time.sleep(0.08)

# ════════════════════════════════════════════════════════════════════
# ARM - RIGHT
# ════════════════════════════════════════════════════════════════════
print("[3/8] Drawing right arm...")
c.sc((0.3, 0.3, 0.9))
c.line(BX + 50, BY + 20, BX + 75, BY + 50)
time.sleep(0.08)

# ════════════════════════════════════════════════════════════════════
# LEG - LEFT
# ════════════════════════════════════════════════════════════════════
print("[4/8] Drawing left leg...")
c.sc((0.2, 0.2, 0.7))
c.line(BX - 25, BY + 80, BX - 40, BY + 130)
time.sleep(0.08)

# ════════════════════════════════════════════════════════════════════
# LEG - RIGHT
# ════════════════════════════════════════════════════════════════════
print("[5/8] Drawing right leg...")
c.sc((0.2, 0.2, 0.7))
c.line(BX + 25, BY + 80, BX + 40, BY + 130)
time.sleep(0.08)

# ════════════════════════════════════════════════════════════════════
# HAND - LEFT
# ════════════════════════════════════════════════════════════════════
print("[6/8] Drawing left hand...")
c.sc((0.4, 0.4, 0.8))
# Draw triangle hand shape
hand_x1, hand_y1 = BX - 75, BY + 60
hand_x2, hand_y2 = BX - 85, BY + 70
hand_x3, hand_y3 = BX - 65, BY + 70
c.line(hand_x1, hand_y1, hand_x2, hand_y2)
c.line(hand_x2, hand_y2, hand_x3, hand_y3)
c.line(hand_x3, hand_y3, hand_x1, hand_y1)
time.sleep(0.05)

# ════════════════════════════════════════════════════════════════════
# HAND - RIGHT
# ════════════════════════════════════════════════════════════════════
print("[7/8] Drawing right hand...")
c.sc((0.4, 0.4, 0.8))
# Draw triangle hand shape
hand_x1, hand_y1 = BX + 75, BY + 60
hand_x2, hand_y2 = BX + 85, BY + 70
hand_x3, hand_y3 = BX + 65, BY + 70
c.line(hand_x1, hand_y1, hand_x2, hand_y2)
c.line(hand_x2, hand_y2, hand_x3, hand_y3)
c.line(hand_x3, hand_y3, hand_x1, hand_y1)
time.sleep(0.05)

# ════════════════════════════════════════════════════════════════════
# FOOT - LEFT
# ════════════════════════════════════════════════════════════════════
print("[8/8] Drawing left foot...")
c.sc((0.5, 0.5, 0.8))
# Draw triangle foot shape
foot_x1, foot_y1 = BX - 38, BY + 130
foot_x2, foot_y2 = BX - 48, BY + 140
foot_x3, foot_y3 = BX - 28, BY + 140
c.line(foot_x1, foot_y1, foot_x2, foot_y2)
c.line(foot_x2, foot_y2, foot_x3, foot_y3)
c.line(foot_x3, foot_y3, foot_x1, foot_y1)
time.sleep(0.05)

# ════════════════════════════════════════════════════════════════════
# FOOT - RIGHT
# ════════════════════════════════════════════════════════════════════
print("Drawing right foot...")
c.sc((0.5, 0.5, 0.8))
# Draw triangle foot shape
foot_x1, foot_y1 = BX + 38, BY + 130
foot_x2, foot_y2 = BX + 48, BY + 140
foot_x3, foot_y3 = BX + 28, BY + 140
c.line(foot_x1, foot_y1, foot_x2, foot_y2)
c.line(foot_x2, foot_y2, foot_x3, foot_y3)
c.line(foot_x3, foot_y3, foot_x1, foot_y1)

print("\n✓ Baby drawn!")

# Export and paste into Freeform
c.show("/tmp/baby_infant.png")
print("  → Saved and pasted to Freeform")
