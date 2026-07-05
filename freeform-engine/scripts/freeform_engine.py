"""
Freeform Drawing Engine — Unified Primitives + Composition Library
====================================================================

Persistent module. All drawings import from here. Single source of truth.

Hierarchy:
    L0  Substrate        — Freeform, board, pen activation (raw event injection)
    L1  Input            — click, stroke, key_combo (atomic drawing events)
    L2  Geometry         — catmull, polygon, circle, line, hatch (math primitives)
    L3  Draw primitives  — line, polyline, polygon_outline, hatch_fill, zigzag_fill
    L4  Style            — bold_stroke, parallel_offset, dim_stroke
    L5  Composition      — house, window, door, roof, tree, sun, cloud, eye,
                          fence, wheel, brick_wall, sphere, leaf, star, smoke,
                          arrow_slit, crenellation, tier_block, river, mountain
    L6  Vehicles         — ground, sky, frame, grid
    L7  Verification     — count_ink, screenshot, region_ink

Usage:
    from engine import *
    activate_pen()
    house(cx=330, cy=400)

Calibration: see ~/.opencode_knowledge/pen_calibration.txt (Shape FIRST).
"""

import time, os, subprocess, math, sys, hashlib, inspect
from Quartz.CoreGraphics import *
from Quartz import (
    CFMachPortCreateRunLoopSource, CFRunLoopAddSource,
    CFRunLoopRunInMode, kCFRunLoopDefaultMode
)

# ════════════════════════════════════════════════════════════════════
# L0 — SUBSTRATE
# ════════════════════════════════════════════════════════════════════

CALIBRATION_PATH = os.path.expanduser("~/.opencode_knowledge/pen_calibration.txt")

def _load_calibration():
    """Load Shape/Pen coordinates from pen_calibration.txt.
    Falls back to default if file missing."""
    SHAPE, PEN = (405, 58), (381, 511)
    try:
        for line in open(CALIBRATION_PATH):
            if "=" not in line or line.startswith("#"):
                continue
            key, val = line.split("=", 1)
            x, y = [int(v) for v in val.strip().split(",")]
            if "SHAPE" in key:
                SHAPE = (x, y)
            elif "PEN" in key:
                PEN = (x, y)
    except Exception:
        pass
    return SHAPE, PEN


def activate_freeform():
    """Bring Freeform to the front."""
    subprocess.run(
        ["osascript", "-e", 'tell app "Freeform" to activate'],
        capture_output=True,
    )


def new_board():
    """File → New Board (must wait ≥1.2s for canvas to settle)."""
    subprocess.run(
        ["osascript", "-e", """
            tell app "System Events"
                tell process "Freeform"
                    click menu item "New Board" of menu "File" of menu bar 1
                end tell
            end tell
        """],
        capture_output=True,
    )


# ════════════════════════════════════════════════════════════════════
# L0.5 — ACCESSIBILITY-BASED UI NAVIGATION (replaces hard-coded coords)
# ════════════════════════════════════════════════════════════════════
#
# Uses AppleScript to find and click UI elements by their accessibility
# descriptions. Much more robust than hard-coded pixel coordinates.
#
# Toolbar layout (verified 2026-07-04):
#   (339,39)  Insert Text Box    — AXButton desc="Insert Text Box"
#   (388,39)  Insert Shape       — AXMenuButton desc="Insert Shape"  (opens popover)
#   (434,39)  Insert Sticky Note — AXButton desc="Insert Sticky Note"
#   (479,39)  Insert Table       — AXButton desc="Insert Table"
#   (527,39)  Insert Media       — AXButton desc="Insert Media"
#
# Canvas controls (in split group below toolbar):
#   (14,678)  Show Scene Navigator
#   (22,683)  Decrease zoom
#   (57,683)  Zoom (menu button)
#   (110,683) Increase zoom
#   (572,683) Connectors toggle
#   (607,683) Grid toggle
#

TOOLBAR_ITEMS = {
    "text box":      "Insert Text Box",
    "shape":         "Insert Shape",
    "sticky note":   "Insert Sticky Note",
    "table":         "Insert Table",
    "media":         "Insert Media",
}

CANVAS_CONTROLS = {
    "scene navigator": "Show Scene Navigator",
    "zoom out":        "Decrease zoom",
    "zoom menu":       "Zoom",
    "zoom in":         "Increase zoom",
    "connectors":      "Connectors",
    "grid":            "Grid",
}


def _click_toolbar_button(description):
    """Click a toolbar button by its accessibility description.
    Uses AppleScript for robust element lookup."""
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                set tb to toolbar 1 of window 1
                set btnList to every UI element of tb whose description is "{description}"
                if (count of btnList) > 0 then
                    click first item of btnList
                end if
            end tell
        end tell
    """], capture_output=True)


def click_tool(name):
    """Click a toolbar drawing tool by name (case-insensitive partial match).
    Names: 'text box', 'shape', 'sticky note', 'table', 'media'
    """
    key = name.lower().strip()
    for k, desc in TOOLBAR_ITEMS.items():
        if k == key or key in k or k in key:
            _click_toolbar_button(desc)
            time.sleep(0.3)
            return
    # Fallback: try direct match
    _click_toolbar_button(name)
    time.sleep(0.3)


def click_canvas_control(name):
    """Click a canvas control button by name.
    Names: 'scene navigator', 'zoom out', 'zoom menu', 'zoom in',
           'connectors', 'grid'
    """
    key = name.lower().strip()
    for k, desc in CANVAS_CONTROLS.items():
        if k == key or key in k or k in key:
            _click_canvas_button(desc)
            time.sleep(0.3)
            return


def _click_canvas_button(description):
    """Click a canvas control by accessibility description via AppleScript.
    Canvas controls live in the split group (not the toolbar)."""
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                set sgs to every UI element of window 1 whose role is "AXSplitGroup"
                if (count of sgs) > 0 then
                    set sg to first item of sgs
                    set btnList to every UI element of sg whose description is "{description}"
                    if (count of btnList) > 0 then
                        click first item of btnList
                    end if
                end if
            end tell
        end tell
    """], capture_output=True)


def _click_menu_item(menu_name, item_name):
    """Click a named menu item via AppleScript."""
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                click menu item "{item_name}" of menu "{menu_name}" of menu bar 1
            end tell
        end tell
    """], capture_output=True)


def insert_shape(shape_name):
    """Insert a shape via Insert → Shape menu.
    Shape names: Rectangle, Rounded Rectangle, Oval, Triangle, Right Triangle,
    Arrow, Double Arrow, Diamond, Quote Bubble, Callout, Polygon, Star
    """
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                click menu item "{shape_name}" of menu "Shape" of menu item "Shape" of menu "Insert" of menu bar 1
            end tell
        end tell
    """], capture_output=True)
    time.sleep(0.5)


def insert_text_box():
    """Insert a text box via Insert → Text Box (menu bar)."""
    _click_menu_item("Insert", "Text Box")
    time.sleep(1.5)


def insert_image():
    """Insert an image via Insert → Choose Photo or Video."""
    _click_menu_item("Insert", "Choose Photo or Video")
    time.sleep(1.0)


def insert_sticky_note():
    """Insert a sticky note via toolbar click."""
    click_tool("sticky note")


def insert_table(rows=3, cols=3):
    """Insert a table via Insert → Table."""
    _click_menu_item("Insert", "Table")
    time.sleep(0.8)


def zoom_actual_size():
    """View → Zoom → Actual Size (resets to 100%)."""
    subprocess.run(["osascript", "-e", """
        tell app "System Events"
            tell process "Freeform"
                click menu item "Actual Size" of menu "Zoom" of menu item "Zoom" of menu "View" of menu bar 1
            end tell
        end tell
    """], capture_output=True)
    time.sleep(0.3)


def zoom_to_fit():
    """View → Zoom → Zoom to Fit Content."""
    subprocess.run(["osascript", "-e", """
        tell app "System Events"
            tell process "Freeform"
                click menu item "Zoom to Fit Content" of menu "Zoom" of menu item "Zoom" of menu "View" of menu bar 1
            end tell
        end tell
    """], capture_output=True)
    time.sleep(0.3)


def zoom_to_selection():
    """View → Zoom → Zoom to Selection."""
    subprocess.run(["osascript", "-e", """
        tell app "System Events"
            tell process "Freeform"
                click menu item "Zoom to Selection" of menu "Zoom" of menu item "Zoom" of menu "View" of menu bar 1
            end tell
        end tell
    """], capture_output=True)
    time.sleep(0.3)


def show_grid(show=True):
    """Toggle grid visibility. show=True means grid ON."""
    if show:
        _click_canvas_button("Grid")
    else:
        _click_canvas_button("Grid")


def show_connectors(show=True):
    """Toggle connector visibility."""
    _click_canvas_button("Connectors")


def toggle_guides(guide_type="centre"):
    """Toggle guide type: 'centre' or 'edge'."""
    name = "Centre Guides" if guide_type == "centre" else "Edge Guides"
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                click menu item "{name}" of menu "Guides" of menu item "Guides" of menu "View" of menu bar 1
            end tell
        end tell
    """], capture_output=True)


def select_all():
    """Edit → Select All."""
    _click_menu_item("Edit", "Select All")


def group_items():
    """Arrange → Group."""
    _click_menu_item("Arrange", "Group")


def ungroup_items():
    """Arrange → Ungroup."""
    _click_menu_item("Arrange", "Ungroup")


def lock_items():
    """Arrange → Lock."""
    _click_menu_item("Arrange", "Lock")


def unlock_items():
    """Arrange → Unlock."""
    _click_menu_item("Arrange", "Unlock")


def align_objects(direction="centre"):
    """Align objects. direction: left, centre, right, top, middle, bottom."""
    name_map = {
        "left": "Left", "centre": "Centre", "center": "Centre",
        "right": "Right", "top": "Top", "middle": "Middle", "bottom": "Bottom",
    }
    aligned = name_map.get(direction.lower(), "Centre")
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                click menu item "{aligned}" of menu "Align Objects" of menu item "Align Objects" of menu "Arrange" of menu bar 1
            end tell
        end tell
    """], capture_output=True)


def distribute_objects(direction="horizontally"):
    """Distribute objects evenly. direction: horizontally, vertically, evenly."""
    name_map = {
        "horizontally": "Horizontally", "h": "Horizontally",
        "vertically": "Vertically", "v": "Vertically",
        "evenly": "Evenly",
    }
    dist = name_map.get(direction.lower(), "Horizontally")
    subprocess.run(["osascript", "-e", f"""
        tell app "System Events"
            tell process "Freeform"
                click menu item "{dist}" of menu "Distribute Objects" of menu item "Distribute Objects" of menu "Arrange" of menu bar 1
            end tell
        end tell
    """], capture_output=True)


def show_colors():
    """Format → Show Colours (opens macOS color picker, Shift+Cmd+C)."""
    _click_menu_item("Format", "Show Colours")


def font_bigger():
    """Format → Font → Bigger (Cmd+Shift++)."""
    subprocess.run(["osascript", "-e", """
        tell app "System Events"
            tell process "Freeform"
                click menu item "Bigger" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            end tell
        end tell
    """], capture_output=True)


def font_smaller():
    """Format → Font → Smaller (Cmd+Shift+-)."""
    subprocess.run(["osascript", "-e", """
        tell app "System Events"
            tell process "Freeform"
                click menu item "Smaller" of menu "Font" of menu item "Font" of menu "Format" of menu bar 1
            end tell
        end tell
    """], capture_output=True)


def scene_navigator():
    """Toggle scene navigator sidebar."""
    _click_canvas_button("Show Scene Navigator")


# ════════════════════════════════════════════════════════════════════
# L1 — INPUT ATOMS
# ════════════════════════════════════════════════════════════════════

def click(x, y, slp=0.005):
    """Send a single left-click at (x, y) via Quartz HID event tap."""
    CGEventPost(kCGHIDEventTap,
                CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft))
    time.sleep(slp)
    CGEventPost(kCGHIDEventTap,
                CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft))


def keystroke(keycode):
    """Tap a single key (keycode 53 = Escape on macOS)."""
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keycode, True))
    time.sleep(0.005)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keycode, False))


def key_combo(modifier, keycode):
    """Press modifier+key combo (e.g. Cmd+Plus for zoom in)."""
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, modifier, True))
    time.sleep(0.015)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keycode, True))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, keycode, False))
    time.sleep(0.008)
    CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, modifier, False))


# ════════════════════════════════════════════════════════════════════
# L1.5 — PEN ACTIVATION
# ════════════════════════════════════════════════════════════════════

def activate_pen():
    """Activate the Pen tool via Shape button → "Draw with Pen" popover.
    Uses accessibility-based toolbar click for the Shape button,
    then the calibrated popover coordinate for "Draw with Pen".

    If calibration file is stale, re-run capture_clicks(2)."""
    click_tool("shape")  # accessibility-click the Shape toolbar button
    time.sleep(0.25)
    pen_x, pen_y = PEN_POP
    click(pen_x, pen_y)
    time.sleep(0.5)


SHAPE_BTN, PEN_POP = _load_calibration()  # SHAPE_BTN kept for backward compat


def zoom_in(n=1):
    for _ in range(n):
        key_combo(0x37, 24)  # Cmd+Plus
        time.sleep(0.03)


def zoom_out(n=1):
    for _ in range(n):
        key_combo(0x37, 27)  # Cmd+Minus
        time.sleep(0.03)


# ════════════════════════════════════════════════════════════════════
# L1.6 — STROKE (one full pen drag with Escape commit)
# ════════════════════════════════════════════════════════════════════

def stroke(pts, slp=0.005):
    """Draw a complete stroke: click each point in order, then Escape to commit.
    Calls activate_pen() implicitly (escape deactivates the pen).

    Args:
        pts: list of (x, y) coordinates
        slp: sleep between clicks (default 0.005s)
    """
    activate_pen()
    for px, py in pts:
        time.sleep(slp)
        click(px, py)
    time.sleep(0.02)
    keystroke(53)  # Escape to commit
    time.sleep(0.02)


def stroke_soft(pts, slp=0.005):
    """Like stroke() but assumes pen is already active. NO implicit activation."""
    for px, py in pts:
        time.sleep(slp)
        click(px, py)
    time.sleep(0.015)
    keystroke(53)


# ════════════════════════════════════════════════════════════════════
# L2 — GEOMETRY (pure math, no Freeform dependencies)
# ════════════════════════════════════════════════════════════════════

def catmull(pts, n=40, closed=False):
    """Catmull-Rom spline interpolation.
    Maps N control points to n×(N-1) interpolated points along a smooth curve.

    n:
        20-30 quick curves
        40-50 smooth silhouettes
        60+ deluxe smoothness
    closed:
        True for closed polygon-like shapes
    """
    out = []
    plen = len(pts) - 1 if closed else len(pts)
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
    if closed:
        out.append(out[0])
    return out


def polygon(cx, cy, r, n=60, phase=0, scale_y=1.0):
    """Regular n-sided polygon (= circle approximation).
    n=60 looks like a perfect circle (sub-pixel error).

    scale_y: vertical squash (e.g. 0.7 for ellipse)
    """
    return [
        (cx + r * math.cos(2 * math.pi * i / n + phase),
         cy + r * math.sin(2 * math.pi * i / n + phase) * scale_y)
        for i in range(n + 1)
    ]


def circle(cx, cy, r, n=60):
    """Alias of polygon(cx, cy, r, n)."""
    return polygon(cx, cy, r, n)


def line(x1, y1, x2, y2, n=20):
    """Polyline approximation of a line (n segments).
    Produces n+1 points (n interior + both endpoints)."""
    return [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n + 1)]


def arc(cx, cy, rx, ry, a0, a1, n=30):
    """Elliptical arc from angle a0 to a1 (radians)."""
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts


# ════════════════════════════════════════════════════════════════════
# L3 — DRAW PRIMITIVES (compose pen strokes)
# ════════════════════════════════════════════════════════════════════

def polyline(pts, slp=0.005, bold=False):
    """Draw a single stroke through pts.
    If bold=True, use parallel offsets for thickness (5-pass)."""
    if bold:
        offsets = [-4, -2, 0, 2, 4]
    else:
        offsets = [0]
    for dx in offsets:
        activate_pen()
        for x, y in pts:
            time.sleep(slp)
            click(x + dx, y + dx * 0.3)
        time.sleep(0.02)
        keystroke(53)
        time.sleep(0.03)


def paraline(pts, offsets, slp=0.005):
    """Draw a polyline at every x-offset in offsets."""
    for dx in offsets:
        activate_pen()
        for x, y in pts:
            time.sleep(slp)
            click(x + dx, y + dx * 0.3)
        time.sleep(0.02)
        keystroke(53)
        time.sleep(0.03)


def hatch_lines(x1, x2, y_start, y_end, step=3):
    """Draw vertical hatching at step pitch (uses activate_pen per line)."""
    n_lines = int((y_end - y_start) / step)
    for i in range(n_lines + 1):
        y = y_start + i * step
        activate_pen()
        stroke_soft([(x1, y), (x2, y)], slp=0.001)
        time.sleep(0.005)


def zigzag_fill(x1, x2, y_start, y_end, step=3):
    """Fill a rectangular area with one continuous zigzag stroke.
    Replaces N parallel hatch lines with a single pen drag.
    """
    pts = []
    rows = list(range(y_start, y_end, step))
    for i, y in enumerate(rows):
        if i % 2 == 0:
            pts += [(x1, y), (x2, y)]
        else:
            pts += [(x2, y), (x1, y)]
    if pts:
        stroke(pts, slp=0.002)


def grid_lines(x_start, y_start, x_end, y_end, dx, dy):
    """Draw a rectangular grid of vertical and horizontal lines."""
    for x in range(x_start, x_end + 1, dx):
        stroke([(x, y_start), (x, y_end)], slp=0.002)
    for y in range(y_start, y_end + 1, dy):
        stroke([(x_start, y), (x_end, y)], slp=0.002)


# ════════════════════════════════════════════════════════════════════
# L4 — STYLES (modifiers on top of draw primitives)
# ════════════════════════════════════════════════════════════════════

def bold5(pts, slp=0.005):
    """Standard bold: 5 parallel passes at offsets [-4,-2,0,2,4]."""
    paraline(pts, [-4, -2, 0, 2, 4], slp)


def bold3(pts, slp=0.005):
    """Lighter bold: 3 passes at [-3,0,3]."""
    paraline(pts, [-3, 0, 3], slp)


# ════════════════════════════════════════════════════════════════════
# L5 — COMPOSITION (named elements that drawings are assembled from)
# ════════════════════════════════════════════════════════════════════

def line_simple(x1, y1, x2, y2, bold=False):
    p = line(x1, y1, x2, y2, 20)
    polyline(p, bold=bold)


def rect_outline(x1, y1, x2, y2, bold=False):
    polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], bold=bold)


def rhombus(cx, cy, dx, dy, bold=False):
    polyline(
        catmull([(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy), (cx, cy - dy)], 30),
        bold=bold,
    )


def star4(cx, cy, r, bold=False):
    """4-pointed star / sparkle (plus sign with diagonals)."""
    polyline([(cx - r, cy), (cx + r, cy)], bold=bold)
    polyline([(cx, cy - r), (cx, cy + r)], bold=bold)
    polyline([(cx - r * 0.7, cy - r * 0.7), (cx + r * 0.7, cy + r * 0.7)], bold=bold)
    polyline([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy - r * 0.7)], bold=bold)


def crenelation(x_start, x_end, y_base, tooth_h, tooth_w):
    """Castellated battlement path. Returns pts.
    Pattern: up, across (tooth_w), down, across (tooth_w), up, ...
    Each period is 2*tooth_w. (x_end - x_start) / (2 * tooth_w) teeth per cycle."""
    pts = []
    x = x_start
    up = True
    while x < x_end - tooth_w:
        if up:
            pts.append((x, y_base))
            pts.append((x, y_base - tooth_h))
            pts.append((x + tooth_w, y_base - tooth_h))
            pts.append((x + tooth_w, y_base))
        x += 2 * tooth_w
        up = not up
    return pts


def circle_outline(cx, cy, r, n=60, bold=False):
    polyline(polygon(cx, cy, r, n), bold=bold)


def ellipse_outline(cx, cy, rx, ry, n=60, bold=False):
    """Ellipse outline (oval)."""
    pts = [(cx + rx * math.cos(2 * math.pi * i / n),
            cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    polyline(pts, bold=bold)


# ---- VEHICLE COMPONENTS ----

def roof(peak_x, peak_y, base_left_x, base_y, base_right_x, smooth=40, bold=True):
    """Symmetric pitched roof: two slope curves meeting at peak.
    Default Catmull-Rom interpolation gives an organic curved peak."""
    roof_l = catmull(
        [(peak_x, peak_y),
         (peak_x - 30, peak_y + 15),
         (base_left_x + 30, base_y - 10),
         (base_left_x, base_y)],
        smooth,
    )
    roof_r = catmull(
        [(peak_x, peak_y),
         (peak_x + 30, peak_y + 15),
         (base_right_x - 30, base_y - 10),
         (base_right_x, base_y)],
        smooth,
    )
    polyline(roof_l, bold=bold)
    polyline(roof_r, bold=bold)


def window_pane(x1, y1, x2, y2, dividers_h=1, dividers_v=1, bold=False):
    """Window: rectangle + mullions dividing into panes."""
    rect_outline(x1, y1, x2, y2, bold=bold)
    for i in range(1, dividers_h + 1):
        ym = y1 + (y2 - y1) * i / (dividers_h + 1)
        polyline([(x1, ym), (x2, ym)], bold=bold)
    for i in range(1, dividers_v + 1):
        xm = x1 + (x2 - x1) * i / (dividers_v + 1)
        polyline([(xm, y1), (xm, y2)], bold=bold)


def door(x1, y1, x2, y2, arch_top=8, has_knob=True, bold=False):
    """Door: rectangle with arched top + knob (optional)."""
    trait = y2 - y1
    arch_top = arch_top or trait * 0.08
    pts = [
        (x1, y2),
        (x1, y1 + arch_top),
        ((x1 + x2) / 2, y1),
        (x2, y1 + arch_top),
        (x2, y2),
    ]
    polyline(catmull(pts, 25), bold=bold)
    if has_knob:
        circle_outline((x1 + x2) / 2 + 4, (y1 + y2) / 2, 2, n=12)


def chimney(x, y, w, h):
    """Rectangular chimney with wider cap."""
    rect_outline(x, y + h - 6, x + w, y + h)
    rect_outline(x - 2, y, x + w + 2, y + 6)


def sun(cx, cy, r_inner, r_outer, n_rays=8, ray_length=12):
    """Sun: filled-out circle (concentric rings) + radial rays."""
    circle_outline(cx, cy, r_outer, n=60)
    circle_outline(cx, cy, r_inner, n=60)
    for i in range(n_rays):
        a = 2 * math.pi * i / n_rays
        x0 = cx + (r_outer + 3) * math.cos(a)
        y0 = cy + (r_outer + 3) * math.sin(a)
        x1 = cx + (r_outer + 3 + ray_length) * math.cos(a)
        y1 = cy + (r_outer + 3 + ray_length) * math.sin(a)
        stroke([(x0, y0), (x1, y1)])


def cloud(cx, cy, rx, ry, n_loops=4, bold=False):
    """Cloud: Catmull-Rom blob with multiple bumps."""
    ctrl = []
    import math as m
    for i in range(n_loops * 2):
        ang = 2 * m.pi * i / (n_loops * 2) - m.pi / 2
        bump = 1.0 if i % 2 == 0 else 0.6
        ctrl.append((cx + rx * bump * m.cos(ang), cy + ry * bump * m.sin(ang)))
    ctrl.append(ctrl[0])
    polyline(catmull(ctrl, 35), bold=bold)


def tree_conifer(cx, base_y, height, base_width):
    """Coniferous tree (pine): layered triangle sections."""
    levels = max(3, height // 20)
    for i in range(levels):
        level_h = height // levels
        level_w = base_width * (1 - i * 0.18)
        y0 = base_y + i * level_h
        y1 = y0 + level_h - 2
        polyline(
            catmull(
                [
                    (cx - level_w / 2, y1),
                    (cx - level_w / 2 * 0.2, y1),
                    (cx, y0),
                    (cx + level_w / 2 * 0.2, y1),
                    (cx + level_w / 2, y1),
                ],
                20,
            )
        )
    # trunk
    rect_outline(cx - 3, base_y + height, cx + 3, base_y + height + 14)


def tree_deciduous(cx, base_y, height, canopy_radius):
    """Deciduous tree: trunk + circle foliage."""
    rect_outline(cx - 4, base_y, cx + 4, base_y + height * 0.4)
    circle_outline(
        cx,
        base_y + height * 0.4 - canopy_radius * 0.3,
        canopy_radius,
        n=60,
    )


def raincloud(cx, cy, w, h, drops=12, drop_length=8):
    """Raincloud: cloud + vertical drops below.
    Drops are drawn as `(cx + offset, y_top) → (cx + offset, y_top + drop_length)`."""
    cloud(cx, cy, w, h // 2, bold=True)
    for i in range(drops):
        dx_offset = (i - drops // 2) * (w // (drops + 1))
        stroke(
            [(cx + dx_offset, cy + h * 0.6),
             (cx + dx_offset - 2, cy + h * 0.6 + drop_length)]
        )


def star_twinkle(cx, cy, r, rays=5):
    """5-pointed star."""
    pts = []
    for i in range(rays * 2):
        a = 2 * math.pi * i / (rays * 2) - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    polyline(pts)


def smoke_puff(start_x, start_y, n_puffs=3, drift=4):
    """Curling smoke column from a chimney."""
    pts = []
    y = start_y
    for i in range(n_puffs):
        pts.append((start_x + (i % 2) * drift, y))
        pts.append((start_x + ((i + 1) % 2) * -drift, y - 8))
        y -= 12
    polyline(catmull(pts, 25))


def fence(x_start, x_end, y_base, picket_h, picket_w, rail_count=2):
    """Picket fence: vertical pickets + horizontal rails."""
    x = x_start
    while x < x_end:
        stroke([(x + picket_w / 2, y_base - picket_h),
                (x + picket_w * 0.3, y_base - picket_h + picket_w * 0.4)])
        stroke([(x + picket_w / 2, y_base - picket_h),
                (x + picket_w / 2, y_base)])
        x += picket_w + 3
    for r in range(rail_count):
        ry = y_base - picket_h * (0.25 + r * 0.4)
        stroke([(x_start, ry), (x_end, ry)])


def brick_wall(x1, y1, x2, y2, brick_w, brick_h):
    """Brick wall: staggered grid of rectangular bricks + mortar lines."""
    cols = int((x2 - x1) / brick_w)
    rows = int((y2 - y1) / brick_h)
    for r in range(rows + 1):
        offset = (r % 2) * (brick_w / 2)
        y = y1 + r * brick_h
        stroke(
            [(x1 + offset - brick_w / 2, y), (x2, y)], slp=0.002
        )
        for c in range(cols + 1):
            x = x1 + offset + c * brick_w
            stroke([(x, y), (x, y + brick_h)], slp=0.002)


def window_arch(cx, cy, w, h, mullion_h=1, mullion_v=1, bold=False):
    """Arched window (rounded top)."""
    polyline(
        catmull(
            [
                (cx - w / 2, cy + h / 2),
                (cx - w / 2, cy - h / 4),
                (cx, cy - h / 2),
                (cx + w / 2, cy - h / 4),
                (cx + w / 2, cy + h / 2),
            ],
            30,
        ),
        bold=bold,
    )
    window_pane(cx - w / 2, cy - h / 4, cx + w / 2, cy + h / 2, mullion_h, mullion_v, bold)


def mountain_silhouette(pts, smooth_n=45, bold=True):
    """Mountain range silhouette (returns the stroke)."""
    polyline(catmull(pts, smooth_n), bold=bold)


def river_curve(centerline_pts, w_start, w_end, smooth=18, bold=True):
    """River/wave: meandering center line drawn as two parallel banks."""
    lbank = catmull(
        [(x - w_start - (i * (w_end - w_start) / len(centerline_pts)),
          y)
         for i, (x, y) in enumerate(centerline_pts)],
        smooth,
    )
    rbank = catmull(
        [(x + w_start + (i * (w_end - w_start) / len(centerline_pts)),
          y)
         for i, (x, y) in enumerate(centerline_pts)],
        smooth,
    )
    polyline(lbank, bold=bold)
    polyline(rbank, bold=bold)


def tri_pyramid(cx, base_y, w, h, smooth=20, bold=False):
    """Triangular pyramid/conical shape (e.g. conical roof, tree section)."""
    polyline(
        catmull(
            [
                (cx - w / 2, base_y),
                (cx, base_y - h),
                (cx + w / 2, base_y),
                (cx - w / 2, base_y),
            ],
            smooth,
        ),
        bold=bold,
    )


def wheel(cx, cy, r_tire, r_rim, spokes=5):
    """Wheel: outer tire circle + inner rim + radial spokes."""
    circle_outline(cx, cy, r_tire, n=60)
    # spoke
    for i in range(spokes):
        a = 2 * math.pi * i / spokes
        x0 = cx + r_rim * 0.25 * math.cos(a)
        y0 = cy + r_rim * 0.25 * math.sin(a)
        x1 = cx + r_rim * 0.95 * math.cos(a)
        y1 = cy + r_rim * 0.95 * math.sin(a)
        stroke([(x0, y0), (x1, y1)])
    # hub
    circle_outline(cx, cy, r_rim * 0.25, n=20)


def sphere_grid(cx, cy, r, lat_count=5, lon_count=6, smooth=15):
    """Sphere: 60-gon outline + lat/lon grid (curved longitude lines)."""
    circle_outline(cx, cy, r, n=60)
    for lat in range(-lat_count, lat_count + 1):
        phi = math.pi * lat / (lat_count + 1) / 2
        if abs(lat) == lat_count:
            continue
        y = cy + r * math.sin(phi)
        x_off = r * math.cos(phi)
        stroke([(cx - x_off, y), (cx + x_off, y)])
    for lon in range(-lon_count, lon_count + 1):
        theta = math.pi * lon / (lon_count + 1) / 2
        pts = []
        for i in range(smooth):
            phi = math.pi * (-0.5 + i / (smooth - 1))
            px = cx + r * math.cos(phi) * math.sin(theta)
            py = cy + r * math.sin(phi)
            pts.append((px, py))
        stroke(pts)


def eye(cx, cy, s=1.0, with_iris=True, with_lashes=False):
    """Eye: almond outline + (optional) Iris + (optional) lashes."""
    r = 36 * s
    polyline(
        catmull(
            [
                (cx, cy - 0.65 * r),
                (cx - 0.88 * r, cy - 0.28 * r),
                (cx - 0.95 * r, cy),
                (cx - 0.88 * r, cy + 0.35 * r),
                (cx - 0.5 * r, cy + 0.58 * r),
                (cx, cy + 0.68 * r),
                (cx + 0.5 * r, cy + 0.58 * r),
                (cx + 0.88 * r, cy + 0.35 * r),
                (cx + 0.95 * r, cy),
                (cx + 0.88 * r, cy - 0.28 * r),
                (cx, cy - 0.65 * r),
            ],
            20,
        )
    )
    if with_iris:
        for a in range(0, 360, 15):
            rad = math.radians(a)
            x1 = cx + 6 * s * math.cos(rad)
            y1 = cy + 6 * s * math.sin(rad) * 0.7
            x2 = cx + 28 * s * math.cos(rad)
            y2 = cy + 28 * s * math.sin(rad) * 0.7
            stroke([(x1, y1), (x2, y2)])
        circle_outline(cx, cy, 9 * s, n=30)


def leaf(cx, cy, w, h, lean=0.3, bold=False):
    """Teardrop-shaped leaf."""
    polyline(
        catmull(
            [
                (cx, cy + h / 2),
                (cx - w / 2 + lean * w, cy + h / 4),
                (cx - w / 2, cy),
                (cx - w / 4 - lean * w / 2, cy - h / 2),
                (cx, cy - h / 2),
                (cx + w / 4 + lean * w / 2, cy - h / 2),
                (cx + w / 2, cy),
                (cx + w / 2 - lean * w, cy + h / 4),
                (cx, cy + h / 2),
            ],
            30,
        ),
        bold=bold,
    )


def arrow_slit(cx, cy, h):
    """Arrow loop/narrow window: vertical line + triangle top."""
    polyline([(cx, cy - h / 2), (cx, cy + h / 2)])
    polyline(
        [
            (cx - 2, cy - h / 4),
            (cx + 2, cy - h / 4),
            (cx, cy - h / 2 - 4),
            (cx - 2, cy - h / 4),
        ]
    )


def tier_block(x1, y_base, x2, width, height=8):
    """One of a stack: trapezoidal tier (e.g. Burj Khalifa)."""
    x_top2 = (x1 + x2) / 2 + width / 2
    x_top1 = (x1 + x2) / 2 - width / 2
    polyline(
        [
            (x1, y_base),
            (x_top1, y_base - height),
            (x_top2, y_base - height),
            (x2, y_base),
        ]
    )


# ════════════════════════════════════════════════════════════════════
# L5b — DRAWING FUNDAMENTALS (shading, perspective, form, proportion, warmups)
# ════════════════════════════════════════════════════════════════════
#
# These implement techniques from Proko, RapidFireArt, Ctrl+Paint, and Kesh Art
# drawing fundamentals courses. Each encodes a specific drawing skill as a
# programmatic composition.
#
# Source curriculum:
#   - RapidFireArt free course (10 lessons): line → shape → form → proportion → perspective → shading
#   - Proko Drawing Basics (185 lessons): Line → Shape → Perspective → Value → Edge
#   - Kesh Art Begin Drawing (7 days): Dynamic Lines → Controlled Lines → Shapes → Shape Combos → Forms
#   - Ctrl+Paint Draw 1: visual measuring → gesture → contour → constructive form → negative space
#

# ---- SHADING TECHNIQUES (Value + Edge) ----

def hatch_fill(x1, y1, x2, y2, angle=45, spacing=4, bold=False):
    """Fill area with parallel hatching lines at given angle.
    angle: 0=horizontal, 45=diagonal, 90=vertical
    spacing: pitch between hatch lines in pixels
    """
    import math as _m
    diag = _m.hypot(x2 - x1, y2 - y1) * 1.5
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    ang = _m.radians(angle)
    n_lines = int(diag / spacing)
    for i in range(-n_lines // 2, n_lines // 2 + 1):
        off = i * spacing
        xa = cx + off * _m.cos(ang + _m.pi / 2) - diag * _m.cos(ang)
        ya = cy + off * _m.sin(ang + _m.pi / 2) - diag * _m.sin(ang)
        xb = cx + off * _m.cos(ang + _m.pi / 2) + diag * _m.cos(ang)
        yb = cy + off * _m.sin(ang + _m.pi / 2) + diag * _m.sin(ang)
        # Clip to bbox
        xs = max(x1, min(x2, xa))
        ys = max(y1, min(y2, ya))
        xe = max(x1, min(x2, xb))
        ye = max(y1, min(y2, yb))
        if xs != xe or ys != ye:
            polyline([(xs, ys), (xe, ye)], slp=0.002, bold=bold)


def crosshatch_fill(x1, y1, x2, y2, angle1=45, angle2=-45, spacing=4, bold=False):
    """Cross-hatching: two layers of hatching at different angles.
    angle1 / angle2: hatch directions (default 45/-45 = classic crosshatch)
    """
    hatch_fill(x1, y1, x2, y2, angle=angle1, spacing=spacing, bold=bold)
    hatch_fill(x1, y1, x2, y2, angle=angle2, spacing=spacing, bold=bold)


def stipple_fill(x1, y1, x2, y2, density=0.15, size=2):
    """Fill area with dot stippling pattern.
    density: fraction of points to fill (0.0-1.0)
    size: dot radius in pixels
    """
    import random
    random.seed(42)  # reproducible pattern
    w, h = int(x2 - x1), int(y2 - y1)
    n_dots = int(w * h * density / (size * size))
    for _ in range(min(n_dots, 200)):
        dx = random.randint(2, w - 2)
        dy = random.randint(2, h - 2)
        cntr = (random.random() * 0.5 + 0.25)  # bias toward center for depth feel
        cx = x1 + dx + (w / 2 - dx) * 0.3 * cntr
        cy = y1 + dy + (h / 2 - dy) * 0.3 * cntr
        polyline(circle(cx, cy, size, n=12), slp=0.002)


def form_shading(cx, cy, rx, ry, light_angle=45, n_bands=6):
    """Form shading for ellipsoid shapes: curved contour-hatching that follows
    the surface, getting denser at the terminator (away from light source).
    light_angle: direction light comes from (degrees, 0=right, 90=top)
    n_bands: number of shaded bands
    """
    import math as _m
    la = _m.radians(light_angle)
    for band in range(1, n_bands + 1):
        t = band / (n_bands + 1)
        dist = rx * t
        for side in [-1, 1]:
            xc = cx + side * dist * _m.cos(la)
            yc = cy + side * dist * _m.sin(la)
            if side < 0:
                w = rx * t
                h = ry * (1 - t * 0.5)
            else:
                w = rx * t * 0.4
                h = ry * t * 0.3
            if w < 2 or h < 2:
                continue
            pts = []
            for i in range(20):
                a = 2 * _m.pi * i / 20
                pts.append((xc + w * _m.cos(a) * 0.5, yc + h * _m.sin(a) * 0.5))
            polyline(pts, slp=0.003)


# ---- PERSPECTIVE (Spatial Depth) ----

def perspective_grid(cx, cy, vanishing_x, vanishing_y, horizon_y, n_lines=8, extent=600):
    """Draw perspective construction: horizon + converging lines + transverse lines.
    cx, cy: center point (often center of canvas)
    vanishing_x, vanishing_y: vanishing point location
    horizon_y: y-coordinate of horizon line
    n_lines: number of converging lines
    extent: half-width of the grid
    """
    # Horizon line
    polyline([(cx - extent, horizon_y), (cx + extent, horizon_y)], bold=True)
    # Converging lines from vanishing point
    for i in range(-n_lines // 2, n_lines // 2 + 1):
        if i == 0:
            continue
        x_ground = cx + i * (extent / (n_lines // 2))
        polyline([(vanishing_x, vanishing_y), (x_ground, horizon_y + extent)], slp=0.003)
    # Transverse (horizontal) lines
    for i in range(1, 6):
        y_pos = horizon_y + extent * (1 - 1 / (i + 1))
        w = extent * (1 / (i + 1))
        polyline([(cx - w, y_pos), (cx + w, y_pos)], slp=0.003)


def vanishing_point(x, y, n_rays=12, r=8):
    """Mark a vanishing point with radiating construction lines."""
    for i in range(n_rays):
        a = 2 * math.pi * i / n_rays
        polyline([(x, y), (x + r * 3 * math.cos(a), y + r * 3 * math.sin(a))], slp=0.002)


# ---- FORM CONSTRUCTION (2D → 3D) ----

def contour_rings(cx, cy, rx, ry, n_rings=5, n_pts=20, bold=False):
    """Add contour rings to an ellipsoid form to describe 3D surface.
    Follows the form's curvature — wider rings = rounder form.
    rx, ry: horizontal and vertical radius of the bounding ellipse
    """
    for ring in range(1, n_rings + 1):
        t = ring / (n_rings + 1)
        wr = rx * math.sin(t * math.pi) * 1.0
        hr = ry * math.sin(t * math.pi) * 0.6
        y_off = ry * math.cos(t * math.pi) * 0.8
        if wr < 3:
            continue
        pts = []
        for i in range(n_pts + 1):
            a = 2 * math.pi * i / n_pts
            pts.append((cx + wr * math.cos(a), cy + y_off + hr * math.sin(a)))
        polyline(pts, slp=0.003, bold=bold)


def constructive_box(cx, cy, w, h, depth=60, perspective_angle=15):
    """Draw a 3D box with construction lines (visible back faces).
    Isometric-style: front face + receding edges + back face.
    perspective_angle: foreshortening angle for depth lines (degrees)
    """
    import math as _m
    pa = _m.radians(perspective_angle)
    # Front face
    rect_outline(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    # Depth lines (angled back)
    dx = depth * _m.cos(pa)
    dy = depth * _m.sin(pa)
    corners = [
        (cx - w / 2, cy - h / 2),
        (cx + w / 2, cy - h / 2),
        (cx + w / 2, cy + h / 2),
        (cx - w / 2, cy + h / 2),
    ]
    for c in corners:
        polyline([c, (c[0] + dx, c[1] + dy)], slp=0.002)
    # Back face
    rect_outline(
        cx - w / 2 + dx, cy - h / 2 + dy,
        cx + w / 2 + dx, cy + h / 2 + dy,
    )


def constructive_cylinder(cx, cy, r, h):
    """Draw a 3D cylinder with top/bottom ellipses and side contour lines.
    r: radius, h: height.
    """
    ellipse_outline(cx, cy - h / 2, r, r * 0.3)    # top ellipse
    ellipse_outline(cx, cy + h / 2, r, r * 0.3)    # bottom ellipse
    polyline([(cx - r, cy - h / 2), (cx - r, cy + h / 2)])   # left edge
    polyline([(cx + r, cy - h / 2), (cx + r, cy + h / 2)])   # right edge
    # Contour rings along body
    for i in range(1, 4):
        y = cy - h / 2 + h * i / 4
        wr = r * 0.95
        hr = r * 0.28
        pts = [(cx + wr * math.cos(a), y + hr * math.sin(a)) for a in
               [2 * math.pi * j / 20 for j in range(21)]]
        polyline(pts, slp=0.003)


# ---- PROPORTION TOOLS ----

def proportion_grid(x1, y1, x2, y2, cols=4, rows=4):
    """Draw a proportion measuring grid overlay (like the 'squint and measure' technique).
    Helps map reference photo proportions to canvas.
    """
    for c in range(cols + 1):
        x = x1 + (x2 - x1) * c / cols
        polyline([(x, y1), (x, y2)], slp=0.002)
    for r in range(rows + 1):
        y = y1 + (y2 - y1) * r / rows
        polyline([(x1, y), (x2, y)], slp=0.002)


def visual_measure(start_x, start_y, direction="h", units=8, unit_length=30):
    """Draw a visual measuring 'ruler' — a series of tick marks for
    sight-size or comparative measurement technique (Ctrl+Paint method).
    direction: 'h' for horizontal, 'v' for vertical
    """
    for i in range(units + 1):
        off = i * unit_length
        tick = 8 if i % 2 == 0 else 4
        if direction == "h":
            polyline([(start_x + off, start_y), (start_x + off, start_y + tick)], slp=0.002)
        else:
            polyline([(start_x, start_y + off), (start_x + tick, start_y + off)], slp=0.002)


# ---- WARM-UPS (Line Quality + Muscle Memory Drills) ----

def warmup_lines(n_lines=20, x1=100, x2=500, y_start=300, step=10):
    """Line quality warmup: draw evenly-spaced parallel lines (straight).
    Purpose: train shoulder/elbow movement, line confidence (Proko Line Quality lesson).
    Draw with one continuous motion per line — no slow, wobbly sketching.
    """
    for i in range(n_lines):
        y = y_start + i * step
        polyline([(x1, y), (x2, y)], slp=0.004)


def warmup_ellipses(n=15, cx=330, cy=400, r_min=20, r_max=120):
    """Ellipse warmup: draw concentric ellipses of increasing size.
    Purpose: train elliptical motion, muscle memory for curved strokes.
    The ellipse is the most common shape in drawing (Ctrl+Paint Ellipse Control).
    """
    for i in range(n):
        r = r_min + (r_max - r_min) * i / n
        ellipse_outline(cx, cy, r, r * 0.6, n=40)


def warmup_ghost_boxes(n=6, x1=150, y1=250, w=50, h=40):
    """Ghosting warmup: draw boxes at increasing pace.
    'Ghost' = hover pen above paper, then commit in one stroke.
    Each box is 4 straight strokes (Proko ghosting technique).
    """
    for i in range(n):
        x = x1 + i * (w + 15)
        rect_outline(x, y1, x + w, y1 + h)


def warmup_circles(n=6, cx=330, cy=400, r_min=15, r_max=90):
    """Circle warmup: draw increasingly large circles in one stroke.
    Circle control is a core skill (Drawabox lesson 1, Kesh Art Day 1-2).
    """
    for i in range(n):
        r = r_min + (r_max - r_min) * i / n
        circle_outline(cx, cy + i * (r_max // n), r)


# ---- CONSTRUCTIVE DRAWING WORKFLOW (Shape → Form → Detail) ----

def constructive_draw(shape_pts, form_fn=None, detail_fn=None, slp=0.004):
    """Execute the 3-stage constructive workflow:
    Stage 1: rough bounding shape (the 'overall shape' from RapidFireArt Lesson 2)
    Stage 2: secondary forms / contour lines
    Stage 3: details / defined edges

    shape_pts: control points for the overall structure (Catmull-Rom)
    form_fn: optional function to add form/contour information
    detail_fn: optional function to add final details
    """
    # Stage 1: loose overall shape
    polyline(catmull(shape_pts, 20), slp=slp)
    # Stage 2: form (contour lines, secondary structure)
    if form_fn:
        form_fn()
    # Stage 3: refined detail
    if detail_fn:
        detail_fn()


def still_life_setup():
    """Draw a basic still life composition setup: table surface + backdrop.
    Used as the foundation for still life practice (Ctrl+Paint still life lessons).
    """
    polyline([(80, 500), (580, 500)], bold=True)      # table edge
    polyline([(80, 380), (80, 500)], bold=True)        # left back
    polyline([(580, 380), (580, 500)], bold=True)      # right back
    polyline([(80, 380), (580, 380)], bold=True)       # back edge


# ════════════════════════════════════════════════════════════════════
# L6 — VEHICLES (large-scale compositional aids)
# ════════════════════════════════════════════════════════════════════

def ground(y, x_start, x_end, bold=False):
    polyline(catmull([(x_start, y), ((x_start + x_end) / 2, y - 2), (x_end, y)], 20), bold=bold)


def frame(x1, y1, x2, y2, bold=True):
    """Decorative border rectangle."""
    rect_outline(x1, y1, x2, y2, bold=bold)


def horizon(x_start, x_end, y, n_waves=4, ampx=3):
    polyline(
        catmull(
            [(x_start + (x_end - x_start) * i / (n_waves * 6),
              y + ampx * math.sin(2 * math.pi * i / (n_waves * 6)))
             for i in range(n_waves * 6 + 1)],
            20,
        )
    )


# ════════════════════════════════════════════════════════════════════
# L7 — VERIFICATION
# ════════════════════════════════════════════════════════════════════

def screenshot(path="/tmp/drawing.png"):
    """Save current display to a PNG file."""
    from PIL import Image

    img = CGDisplayCreateImage(CGMainDisplayID())
    w = CGImageGetWidth(img)
    h = CGImageGetHeight(img)
    data = CGDataProviderCopyData(CGImageGetDataProvider(img))
    Image.frombytes("RGBA", (w, h), data, "raw", "BGRA").save(path)
    return path


_cached_w = None
_cached_data = None


def _fresh():
    global _cached_w, _cached_data
    img = CGDisplayCreateImage(CGMainDisplayID())
    _cached_w = CGImageGetWidth(img)
    _cached_data = bytearray(CGDataProviderCopyData(CGImageGetDataProvider(img)))


def count_ink(x1, y1, x2, y2, threshold=80):
    """Count dark pixels in screen-pixel bounding box.
    Threshold distinguishes ink (r,g,b all < threshold) from canvas color."""
    _fresh()
    n = 0
    for y in range(y1, y2):
        for x in range(x1, x2):
            o = (int(y * 2) * _cached_w + int(x * 2)) * 4
            r, g, b = _cached_data[o], _cached_data[o + 1], _cached_data[o + 2]
            if r < threshold and g < threshold and b < threshold:
                n += 1
    return n


def verify_phase(name, x1, y1, x2, y2):
    ink = count_ink(x1, y1, x2, y2)
    print(f"  [Verify] {name}: {ink} ink pixels")
    return ink


def preflight_check(x=330, y=400, threshold=50):
    """Run a small stroke test to verify pen tool is responsive.
    Returns ink count at the test position. Use as a calibration probe."""
    test_pts = [(x + i, y) for i in range(20)]
    stroke(test_pts, slp=0.005)
    time.sleep(0.3)
    ink = count_ink(x - 10, y - 10, x + 30, y + 10)
    return ink


# ════════════════════════════════════════════════════════════════════
# L7 — HOMEOSTATIC DRAW (Domain 7: Medicine — corrective feedback)
# ════════════════════════════════════════════════════════════════════

INK_SET_POINTS = {
    # Calibrated 2026-07-04 from draw_house_homeostatic.py first-attempt measurements.
    # Tolerances set at 0.4 (40%) to absorb normal CGEvent timing variance
    # while catching genuine failures (broken pen, wrong calibration, no ink).
    "door":        {"expected": 1253, "tolerance": 0.4},
    "roof":        {"expected": 3608, "tolerance": 0.4},
    "window_left": {"expected": 224,  "tolerance": 0.4},
    "window_right":{"expected": 400,  "tolerance": 0.4},
    "sun":         {"expected": 3337, "tolerance": 0.4},
    "cloud":       {"expected": 1300, "tolerance": 0.4},
    "tree":        {"expected": 9610, "tolerance": 0.4},
    "house_body":  {"expected": 7922, "tolerance": 0.4},
    "ground":      {"expected": 4442, "tolerance": 0.4},
    "chimney":     {"expected": 587,  "tolerance": 0.4},
    # Generic fallback entries for re-use across drawings
    "window":      {"expected": 300,  "tolerance": 0.5},
    "mountain":    {"expected": 800,  "tolerance": 0.35},
    "river":       {"expected": 450,  "tolerance": 0.4},
    "brick_wall":  {"expected": 1000, "tolerance": 0.3},
}


def homeostatic_draw(name, draw_fn, bbox, expected_ink=None, tolerance=None, **kwargs):
    """Draw with homeostatic correction.

    Draws using draw_fn(**kwargs), measures ink in bbox, and if the
    measured ink deviates from the expected value beyond tolerance,
    re-draws with bold=True as corrective feedback.

    Args:
        name: Element name (for set point lookup and reporting)
        draw_fn: Drawing function to call (e.g. door, roof, sun)
        bbox: (x1, y1, x2, y2) bounding box for ink measurement
        expected_ink: Expected ink pixel count. Falls back to INK_SET_POINTS.
        tolerance: Fractional tolerance (0.0-1.0). Falls back to set point.
        **kwargs: Passed to draw_fn

    Returns:
        int: Final ink count after possible correction
    """
    set_point = INK_SET_POINTS.get(name, {})
    expected = expected_ink if expected_ink is not None else set_point.get("expected")
    tol = tolerance if tolerance is not None else set_point.get("tolerance", 0.4)

    # First attempt
    draw_fn(**kwargs)
    time.sleep(0.3)
    ink = count_ink(*bbox)
    correction_needed = False

    if expected is not None:
        deviation = abs(ink - expected) / max(expected, 1)
        if deviation > tol:
            correction_needed = True
            print(f"  [Homeostat] {name}: {ink}px (expected ~{expected}px, "
                  f"deviation={deviation:.0%}) — re-drawing with bold")

    if correction_needed:
        # Check if function accepts 'bold' before injecting it
        sig = inspect.signature(draw_fn)
        supports_bold = "bold" in sig.parameters

        if supports_bold:
            bold_kwargs = {**kwargs, "bold": True}
            print(f"  [Homeostat] {name}: re-drawing with bold=True")
        else:
            bold_kwargs = {**kwargs}
            print(f"  [Homeostat] {name}: re-drawing (function doesn't support bold)")

        draw_fn(**bold_kwargs)
        time.sleep(0.3)
        ink = count_ink(*bbox)
        deviation = abs(ink - expected) / max(expected, 1) if expected else 0
        if deviation <= tol:
            print(f"  [Homeostat] {name}: corrected to {ink}px (deviation={deviation:.0%}) ✓")
        else:
            print(f"  [Homeostat] {name}: still deviating at {ink}px (deviation={deviation:.0%})")
    else:
        print(f"  [Homeostat] {name}: {ink}px ✓")

    return ink


# ════════════════════════════════════════════════════════════════════
# L7 — INTEGRITY VERIFICATION (Domain 9: Cryptography — hash chains)
# ════════════════════════════════════════════════════════════════════

DRAWING_HASHES = {}  # name → hex digest


def _capture_region_bytes(x1, y1, x2, y2):
    """Capture raw RGBA pixel bytes for a screen region.
    Returns (width, height, bytes) at @2x resolution."""
    img = CGDisplayCreateImage(CGMainDisplayID())
    w = CGImageGetWidth(img)
    h = CGImageGetHeight(img)
    raw = CGDataProviderCopyData(CGImageGetDataProvider(img))
    data = bytearray(raw)

    # Extract the region at @2x
    region_bytes = bytearray()
    for y in range(int(y1 * 2), int(y2 * 2)):
        for x in range(int(x1 * 2), int(x2 * 2)):
            o = (y * w + x) * 4
            region_bytes.extend(data[o:o + 4])
    return (int(x2 - x1) * 2, int(y2 - y1) * 2), bytes(region_bytes)


def verify_drawing_integrity(name, bbox, known_hash=None):
    """Verify drawing integrity via pixel hash.

    Captures the bbox region, hashes it with SHA-256, and compares
    against a known-good hash. Use this to detect calibration drift
    or unexpected pixel changes between draws.

    Args:
        name: Name for this integrity check (e.g. "house_door_verify")
        bbox: (x1, y1, x2, y2) bounding box
        known_hash: Optional known-good hex digest to compare against.
                     If None, looks up DRAWING_HASHES[name].

    Returns:
        (is_intact: bool, current_hash: str)
        - is_intact: True if hash matches known-good (or if no known hash yet)
        - current_hash: 16-char hex prefix of SHA-256 digest
    """
    _size, pixel_bytes = _capture_region_bytes(*bbox)
    current_hash = hashlib.sha256(pixel_bytes).hexdigest()[:16]

    expected = known_hash if known_hash is not None else DRAWING_HASHES.get(name)

    if expected is None:
        # First time — store as known-good
        DRAWING_HASHES[name] = current_hash
        print(f"  [Integrity] {name}: registered hash={current_hash}")
        return (True, current_hash)

    if current_hash == expected:
        print(f"  [Integrity] {name}: intact ✓ (hash={current_hash})")
        return (True, current_hash)
    else:
        print(f"  [Integrity] {name}: BREACH — hash mismatch")
        print(f"    Expected: {expected}")
        print(f"    Got:      {current_hash}")
        return (False, current_hash)


def integrity_report():
    """Print a summary of all registered integrity hashes."""
    if not DRAWING_HASHES:
        print("  [Integrity] No hashes registered.")
        return
    print("  ┌──────────────────────┬──────────────────┐")
    print("  │ Region               │ Hash (SHA256:16) │")
    print("  ├──────────────────────┼──────────────────┤")
    for name, h in sorted(DRAWING_HASHES.items()):
        print(f"  │ {name:<20s} │ {h:<16s} │")
    print("  └──────────────────────┴──────────────────┘")


# ════════════════════════════════════════════════════════════════════
# Capture utility (for re-calibration of Pen tool buttons)
# ════════════════════════════════════════════════════════════════════

def capture_clicks(n=2, timeout=60):
    """Interactive: capture N mouse clicks via CGEventTap."""
    import math as _m

    clicks = []

    def cb(proxy, event_type, event, refcon):
        if event_type == kCGEventLeftMouseDown:
            loc = CGEventGetLocation(event)
            clicks.append((int(loc.x), int(loc.y)))
            print(f"  Click {len(clicks)}: ({int(loc.x)}, {int(loc.y)})")
        return event

    mask = 1 << kCGEventLeftMouseDown
    tap = CGEventTapCreate(
        kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        mask,
        cb,
        None,
    )
    src = CFMachPortCreateRunLoopSource(None, tap, 0)
    CFRunLoopAddSource(CFRunLoopGetCurrent(), src, kCFRunLoopDefaultMode)
    CGEventTapEnable(tap, True)

    print(f"=> Make {n} clicks: Shape button, then 'Draw with Pen'")
    deadline = time.time() + timeout
    while len(clicks) < n and time.time() < deadline:
        CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)
    CGEventTapEnable(tap, False)

    if len(clicks) >= 2:
        SHAPE, PEN = clicks[0], clicks[1]
        with open(CALIBRATION_PATH, "w") as f:
            f.write(f"# Pen tool calibration (recorded {time.strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write(f"SHAPE_X, SHAPE_Y = {SHAPE[0]}, {SHAPE[1]}\n")
            f.write(f"PEN_X, PEN_Y = {PEN[0]}, {PEN[1]}\n")
        global SHAPE_BTN, PEN_POP
        SHAPE_BTN, PEN_POP = SHAPE, PEN
        print(f"  Saved to {CALIBRATION_PATH}")
    return clicks[:n]


# ════════════════════════════════════════════════════════════════════
# Quick-start convenience
# ════════════════════════════════════════════════════════════════════

def setup():
    """Activate Freeform, open a new board, activate Pen tool."""
    activate_freeform()
    time.sleep(1)
    new_board()
    time.sleep(1.5)
    activate_pen()


def setup_with_board(new=True):
    """Flexible setup: activate Freeform and optionally create a new board.
    Does NOT activate pen — lets caller choose the tool.

    Args:
        new: If True, creates a new board. If False, uses current board.
    """
    activate_freeform()
    time.sleep(1)
    if new:
        new_board()
        time.sleep(1.5)
