# Copyright © 2026 Arsh Buttar. All rights reserved. Confidential and proprietary.
# Unauthorized copying, distribution, or use of this work is prohibited.

"""
Freeform CGContext Renderer — direct Quartz bitmap rendering, no mouse events
==============================================================================

Renders drawings into a CGBitmapContext using Apple CoreGraphics, then
imports the finished PNG into Freeform via clipboard paste.

Usage:
    from freeform_renderer import Canvas
    c = Canvas(660, 700)
    c.background()
    c.draw()
    c.show()
"""

import math, os, time, subprocess
from Quartz import (
    CGBitmapContextCreate, CGBitmapContextCreateImage,
    CGColorSpaceCreateDeviceRGB, CGDataProviderCopyData,
    CGImageGetDataProvider, CGImageGetWidth, CGImageGetHeight,
    CGImageCreate, CGDataProviderCreateWithData,
    kCGBitmapByteOrder32Host, kCGImageAlphaPremultipliedFirst,
    CGContextSetRGBStrokeColor, CGContextSetRGBFillColor,
    CGContextSetLineWidth, CGContextSetLineCap, CGContextSetLineJoin,
    CGContextBeginPath, CGContextMoveToPoint, CGContextAddLineToPoint,
    CGContextAddCurveToPoint, CGContextAddArc, CGContextAddArcToPoint,
    CGContextAddRect, CGContextAddEllipseInRect,
    CGContextStrokePath, CGContextFillPath,
    CGContextSaveGState, CGContextRestoreGState,
    CGContextClip, CGContextClosePath, CGContextClipToRect,
    CGContextSetAlpha, CGContextDrawLinearGradient, CGContextDrawRadialGradient,
    CGGradientCreateWithColorComponents,
    kCGGradientDrawsBeforeStartLocation, kCGGradientDrawsAfterEndLocation,
    kCGLineCapRound, kCGLineJoinRound,
    kCGImageAlphaNoneSkipLast,
    CGContextTranslateCTM, CGContextScaleCTM,
    CGContextDrawImage,
)
from PIL import Image

BG_R, BG_G, BG_B = 0.945, 0.761, 0.463
CW, CH = 660, 700


def _norm(c):
    return tuple(x / 255.0 if max(c) > 1 else x for x in c)


class Canvas:
    def __init__(self, w=CW, h=CH, scale=2):
        self.w, self.h, self.scale = int(w * scale), int(h * scale), scale
        self.cs = CGColorSpaceCreateDeviceRGB()
        import ctypes
        self.buf = ctypes.create_string_buffer(self.w * self.h * 4)
        self.ctx = CGBitmapContextCreate(
            self.buf, self.w, self.h, 8, self.w * 4,
            self.cs, kCGBitmapByteOrder32Host | kCGImageAlphaPremultipliedFirst
        )
        self._style()
        CGContextTranslateCTM(self.ctx, 0, self.h)
        CGContextScaleCTM(self.ctx, 1, -1)

    def _style(self, r=0, g=0, b=0, w=1):
        CGContextSetRGBStrokeColor(self.ctx, r, g, b, 1)
        CGContextSetRGBFillColor(self.ctx, r, g, b, 1)
        CGContextSetLineWidth(self.ctx, max(0.5, w * self.scale))
        CGContextSetLineCap(self.ctx, kCGLineCapRound)
        CGContextSetLineJoin(self.ctx, kCGLineJoinRound)

    def gs(self): CGContextSaveGState(self.ctx)
    def gr(self): CGContextRestoreGState(self.ctx)

    def sc(self, c, a=None):
        cn = _norm(c)
        if len(cn) == 4 and a is None:
            a = cn[3]
        CGContextSetRGBStrokeColor(self.ctx, cn[0], cn[1], cn[2], a if a is not None else 1.0)

    def fc(self, c, a=None):
        cn = _norm(c)
        if len(cn) == 4 and a is None:
            a = cn[3]
        CGContextSetRGBFillColor(self.ctx, cn[0], cn[1], cn[2], a if a is not None else 1.0)

    def lw(self, w):
        CGContextSetLineWidth(self.ctx, max(0.5, w * self.scale))

    def bg(self, r=BG_R, g=BG_G, b=BG_B):
        self.gs(); self.fc((r, g, b))
        CGContextAddRect(self.ctx, ((0, 0), (self.w, self.h)))
        CGContextFillPath(self.ctx); self.gr()

    def line(self, x1, y1, x2, y2):
        CGContextBeginPath(self.ctx)
        CGContextMoveToPoint(self.ctx, x1 * self.scale, y1 * self.scale)
        CGContextAddLineToPoint(self.ctx, x2 * self.scale, y2 * self.scale)
        CGContextStrokePath(self.ctx)

    def polyline(self, pts):
        if len(pts) < 2: return
        CGContextBeginPath(self.ctx)
        CGContextMoveToPoint(self.ctx, pts[0][0] * self.scale, pts[0][1] * self.scale)
        for x, y in pts[1:]:
            CGContextAddLineToPoint(self.ctx, x * self.scale, y * self.scale)
        CGContextStrokePath(self.ctx)

    def rect(self, x1, y1, x2, y2, f=None, s=None):
        r = ((x1 * self.scale, y1 * self.scale), ((x2 - x1) * self.scale, (y2 - y1) * self.scale))
        if f is not None:
            self.gs(); self.fc(f); CGContextAddRect(self.ctx, r); CGContextFillPath(self.ctx); self.gr()
        if s is not None or f is None:
            self.gs()
            if s is not None: self.sc(s)
            CGContextAddRect(self.ctx, r); CGContextStrokePath(self.ctx); self.gr()

    def ellipse(self, cx, cy, rx, ry, f=None, s=None):
        r = (((cx - rx) * self.scale, (cy - ry) * self.scale), (rx * 2 * self.scale, ry * 2 * self.scale))
        if f is not None:
            self.gs(); self.fc(f); CGContextAddEllipseInRect(self.ctx, r); CGContextFillPath(self.ctx); self.gr()
        if s is not None or f is None:
            self.gs()
            if s is not None: self.sc(s)
            CGContextAddEllipseInRect(self.ctx, r); CGContextStrokePath(self.ctx); self.gr()

    def circle(self, cx, cy, r, f=None, s=None):
        self.ellipse(cx, cy, r, r, f, s)

    def fill_path(self, pts):
        """Fill a closed polygon defined by point list."""
        if len(pts) < 3: return
        CGContextBeginPath(self.ctx)
        CGContextMoveToPoint(self.ctx, pts[0][0] * self.scale, pts[0][1] * self.scale)
        for x, y in pts[1:]:
            CGContextAddLineToPoint(self.ctx, x * self.scale, y * self.scale)
        CGContextClosePath(self.ctx)
        CGContextFillPath(self.ctx)

    def fill_curve(self, pts, n=30):
        """Fill a closed catmull-rom curve."""
        if len(pts) < 2: return
        if len(pts) == 2: self.fill_path(pts + [(pts[1][0], pts[0][1])]); return
        segs = []
        for i in range(len(pts) - 1):
            p0 = pts[max(0, i - 1)]; p1 = pts[i]; p2 = pts[min(len(pts) - 1, i + 1)]; p3 = pts[min(len(pts) - 1, i + 2)]
            for j in range(n):
                t = j / n; t2 = t * t; t3 = t2 * t
                x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                segs.append((x, y))
            segs.append(pts[i + 1])
        self.fill_path(segs)

    def gradient_linear(self, x1, y1, x2, y2, colors, locations=None):
        """Draw linear gradient between two points.
        colors: list of (r,g,b) or (r,g,b,a) tuples (0-1 range)
        locations: list of floats 0-1 (evenly spaced if None)
        """
        if locations is None:
            locations = [i / (len(colors) - 1) for i in range(len(colors))]
        flat = []
        for c in colors:
            cn = _norm(c)
            if len(cn) == 3:
                flat.extend([cn[0], cn[1], cn[2], 1.0])
            else:
                flat.extend([cn[0], cn[1], cn[2], cn[3]])
        grad = CGGradientCreateWithColorComponents(self.cs, flat, locations, len(colors))
        CGContextDrawLinearGradient(self.ctx, grad,
            (x1 * self.scale, y1 * self.scale),
            (x2 * self.scale, y2 * self.scale),
            kCGGradientDrawsBeforeStartLocation | kCGGradientDrawsAfterEndLocation)

    def gradient_radial(self, cx, cy, r1, cx2, cy2, r2, colors, locations=None):
        """Draw radial gradient between two circles."""
        if locations is None:
            locations = [i / (len(colors) - 1) for i in range(len(colors))]
        flat = []
        for c in colors:
            cn = _norm(c)
            if len(cn) == 3:
                flat.extend([cn[0], cn[1], cn[2], 1.0])
            else:
                flat.extend([cn[0], cn[1], cn[2], cn[3]])
        grad = CGGradientCreateWithColorComponents(self.cs, flat, locations, len(colors))
        CGContextDrawRadialGradient(self.ctx, grad,
            (cx * self.scale, cy * self.scale), r1 * self.scale,
            (cx2 * self.scale, cy2 * self.scale), r2 * self.scale,
            kCGGradientDrawsBeforeStartLocation | kCGGradientDrawsAfterEndLocation)

    def clip_rect(self, x1, y1, x2, y2):
        """Clip drawing to a rectangle."""
        CGContextClipToRect(self.ctx, ((x1 * self.scale, y1 * self.scale),
                                       ((x2 - x1) * self.scale, (y2 - y1) * self.scale)))

    def draw_image(self, path, x=0, y=0, w=None, h=None):
        """Draw an image into the canvas via direct pixel buffer write.
        Writes PIL pixels directly into CGBitmapContext backing store at 2x."""
        from PIL import Image as PILImg
        pil = PILImg.open(path).convert("RGB")
        iw, ih = pil.size
        if w is None: w = iw
        if h is None: h = ih
        if w != iw or h != ih:
            pil = pil.resize((w, h), PILImg.LANCZOS)
        
        import numpy as np
        px = np.array(pil, dtype=np.uint8)  # (h, w, 3)
        hh, ww = px.shape[:2]
        
        # Canvas pixel coordinates (2x scale)
        sx, sy = int(x * self.scale), int(y * self.scale)
        sw, sh = int(w * self.scale), int(h * self.scale)
        
        # Resize to canvas resolution if needed
        if sw != ww or sh != hh:
            px = np.array(
                PILImg.fromarray(px).resize((sw, sh), PILImg.LANCZOS),
                dtype=np.uint8)
        
        # Canvas buffer uses kCGBitmapByteOrder32Host | kCGImageAlphaPremultipliedFirst
        # On little-endian (arm64/x86_64): byte order in memory is B, G, R, A
        buf_arr = np.frombuffer(self.buf, dtype=np.uint8).reshape(self.h, self.w, 4)
        dst = buf_arr[sy:sy+sh, sx:sx+sw]
        dst[:,:,0] = px[:,:,2]  # B
        dst[:,:,1] = px[:,:,1]  # G
        dst[:,:,2] = px[:,:,0]  # R
        dst[:,:,3] = 255        # A

    def catmull(self, pts, n=20):
        if len(pts) < 2: return
        if len(pts) == 2: self.polyline(pts); return
        segs = []
        for i in range(len(pts) - 1):
            p0, p1, p2, p3 = pts[max(0, i - 1)], pts[i], pts[min(len(pts) - 1, i + 1)], pts[min(len(pts) - 1, i + 2)]
            for j in range(n):
                t = j / n
                t2 = t * t
                t3 = t2 * t
                x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                segs.append((x, y))
            segs.append(pts[i + 1])
        self.polyline(segs)

    def bezier(self, p0, p1, p2, p3):
        CGContextBeginPath(self.ctx)
        CGContextMoveToPoint(self.ctx, p0[0] * self.scale, p0[1] * self.scale)
        CGContextAddCurveToPoint(self.ctx, p1[0] * self.scale, p1[1] * self.scale,
                                 p2[0] * self.scale, p2[1] * self.scale,
                                 p3[0] * self.scale, p3[1] * self.scale)
        CGContextStrokePath(self.ctx)

    def arc(self, cx, cy, r, sa, ea):
        CGContextBeginPath(self.ctx)
        CGContextAddArc(self.ctx, cx * self.scale, cy * self.scale, r * self.scale,
                        math.radians(sa), math.radians(ea), 0)
        CGContextStrokePath(self.ctx)

    def save(self, path):
        img = CGBitmapContextCreateImage(self.ctx)
        w, h = CGImageGetWidth(img), CGImageGetHeight(img)
        data = CGDataProviderCopyData(CGImageGetDataProvider(img))
        pil = Image.frombytes("RGBA", (w, h), data, "raw", "BGRA")
        if self.scale > 1:
            pil = pil.resize((self.w // self.scale, self.h // self.scale), Image.LANCZOS)
        pil.save(path)
        return path

    def show(self, path="/tmp/freeform_drawing.png"):
        self.save(path)
        subprocess.run(['osascript', '-e', 'tell app "Freeform" to activate'], capture_output=True)
        time.sleep(0.5)
        subprocess.run(['osascript', '-e', '''
            tell app "System Events"
                tell process "Freeform"
                    click menu item "New Board" of menu "File" of menu bar 1
                end tell
            end tell
        '''], capture_output=True)
        time.sleep(1.5)
        import AppKit
        img = AppKit.NSImage.alloc().initWithContentsOfFile_(path)
        AppKit.NSPasteboard.generalPasteboard().clearContents()
        AppKit.NSPasteboard.generalPasteboard().writeObjects_([img])
        time.sleep(0.2)
        subprocess.run(['osascript', '-e', '''
            tell app "System Events"
                tell process "Freeform"
                    keystroke "v" using command down
                end tell
            end tell
        '''], capture_output=True)
        time.sleep(1)
        return path


# ─── Drawing fundamentals ───

def hatch_fill(c, x1, y1, x2, y2, a=45, sp=4):
    d = math.hypot(x2 - x1, y2 - y1) * 1.5
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    ang = math.radians(a)
    n = int(d / sp)
    for i in range(-n // 2, n // 2 + 1):
        off = i * sp
        xa = cx + off * math.cos(ang + math.pi / 2) - d * math.cos(ang)
        ya = cy + off * math.sin(ang + math.pi / 2) - d * math.sin(ang)
        xb = cx + off * math.cos(ang + math.pi / 2) + d * math.cos(ang)
        yb = cy + off * math.sin(ang + math.pi / 2) + d * math.sin(ang)
        xs, ys = max(x1, min(x2, xa)), max(y1, min(y2, ya))
        xe, ye = max(x1, min(x2, xb)), max(y1, min(y2, yb))
        if xs != xe or ys != ye:
            c.line(xs, ys, xe, ye)


def crosshatch(c, x1, y1, x2, y2, a1=45, a2=-45, sp=4):
    hatch_fill(c, x1, y1, x2, y2, a1, sp)
    hatch_fill(c, x1, y1, x2, y2, a2, sp)


def contour_rings(c, cx, cy, rx, ry, n=5):
    for ring in range(1, n + 1):
        t = ring / (n + 1)
        wr = rx * math.sin(t * math.pi)
        hr = ry * math.sin(t * math.pi) * 0.6
        yo = ry * math.cos(t * math.pi) * 0.8
        if wr < 3: continue
        pts = [(cx + wr * math.cos(2 * math.pi * i / 20), cy + yo + hr * math.sin(2 * math.pi * i / 20))
               for i in range(21)]
        c.polyline(pts)


def form_shading(c, cx, cy, rx, ry, la=45, nb=6):
    la = math.radians(la)
    for band in range(1, nb + 1):
        t = band / (nb + 1)
        for side in [-1, 1]:
            xc = cx + side * rx * t * math.cos(la)
            yc = cy + side * rx * t * math.sin(la)
            w = rx * t * (1.0 if side < 0 else 0.4)
            h = ry * (1 - t * 0.5 if side < 0 else t * 0.3)
            if w < 2 or h < 2: continue
            pts = [(xc + w * 0.5 * math.cos(2 * math.pi * i / 20), yc + h * 0.5 * math.sin(2 * math.pi * i / 20))
                   for i in range(20)]
            c.polyline(pts)


def constructive_box(c, cx, cy, w, h, d=50, pa=15):
    pa = math.radians(pa)
    c.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    dx, dy = d * math.cos(pa), d * math.sin(pa)
    for x, y in [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]:
        c.line(x, y, x + dx, y + dy)
    c.rect(cx - w / 2 + dx, cy - h / 2 + dy, cx + w / 2 + dx, cy + h / 2 + dy)


def cyl(c, cx, cy, r, h):
    c.ellipse(cx, cy - h / 2, r, r * 0.3)
    c.ellipse(cx, cy + h / 2, r, r * 0.3)
    c.line(cx - r, cy - h / 2, cx - r, cy + h / 2)
    c.line(cx + r, cy - h / 2, cx + r, cy + h / 2)
    for i in range(1, 4):
        y = cy - h / 2 + h * i / 4
        pts = [(cx + r * 0.95 * math.cos(2 * math.pi * j / 20), y + r * 0.28 * math.sin(2 * math.pi * j / 20))
               for j in range(21)]
        c.polyline(pts)
