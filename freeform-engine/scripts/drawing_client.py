"""
TCP client for the Swift DrawingServer on localhost:9876.

Sends JSON commands to the native SwiftUI Canvas renderer.
No CGEvent clicks, no pen calibration, no Freeform dependency.

Usage:
    with DrawingClient() as dc:
        dc.clear()
        dc.circle(cx=330, cy=400, r=50, width=2)
        dc.ink_count(300, 370, 360, 430)
"""

import json
import socket
import time


class DrawingClient:
    """TCP client for the Swift DrawingServer."""

    def __init__(self, host="localhost", port=9876):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        """Connect to the DrawingServer TCP socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.connect((self.host, self.port))
        # Use a file wrapper for line-delimited reading
        self._reader = self.sock.makefile("r", buffering=1)
        return self

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            self._reader = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, *args):
        self.close()

    def send(self, cmd, **params):
        """Send a command and return the parsed JSON response."""
        payload = {"cmd": cmd}
        payload.update(params)
        data = json.dumps(payload) + "\n"
        self.sock.sendall(data.encode())
        response = self._reader.readline()
        return json.loads(response) if response else {}

    # ── Drawing Commands ──────────────────────────────────────

    def clear(self):
        """Clear all strokes from the canvas."""
        return self.send("clear")

    def stroke(self, points, color=None, width=None, filled=None):
        """Draw a polyline through points."""
        params = {"points": [[float(p[0]), float(p[1])] for p in points]}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        if filled is not None:
            params["filled"] = filled
        return self.send("stroke", **params)

    def catmull(self, points, n=40, closed=False, color=None, width=None,
                bold=None, filled=None):
        """Draw a Catmull-Rom spline through control points."""
        params = {
            "points": [[float(p[0]), float(p[1])] for p in points],
            "n": n,
            "closed": closed,
        }
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        if bold is not None:
            params["bold"] = bold
        if filled is not None:
            params["filled"] = filled
        return self.send("catmull", **params)

    def circle(self, cx, cy, r, n=60, color=None, width=None, filled=None):
        """Draw a circle outline."""
        params = {"cx": float(cx), "cy": float(cy), "r": float(r), "n": n}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        if filled is not None:
            params["filled"] = filled
        return self.send("circle", **params)

    def ellipse(self, cx, cy, rx, ry, n=60, color=None, width=None,
                filled=None):
        """Draw an ellipse outline."""
        params = {"cx": float(cx), "cy": float(cy), "rx": float(rx),
                  "ry": float(ry), "n": n}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        if filled is not None:
            params["filled"] = filled
        return self.send("ellipse", **params)

    def line(self, x1, y1, x2, y2, n=20, color=None, width=None):
        """Draw a straight line."""
        params = {"x1": float(x1), "y1": float(y1),
                  "x2": float(x2), "y2": float(y2), "n": n}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        return self.send("line", **params)

    def rect(self, x1, y1, x2, y2, color=None, width=None, filled=None):
        """Draw a rectangle outline."""
        params = {"x1": float(x1), "y1": float(y1),
                  "x2": float(x2), "y2": float(y2)}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        if filled is not None:
            params["filled"] = filled
        return self.send("rect", **params)

    def bold5(self, points, color=None, width=None):
        """Draw with 5 parallel passes for thickness."""
        params = {"points": [[float(p[0]), float(p[1])] for p in points]}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        return self.send("bold5", **params)

    def bold3(self, points, color=None, width=None):
        """Draw with 3 parallel passes (lighter bold)."""
        params = {"points": [[float(p[0]), float(p[1])] for p in points]}
        if color is not None:
            params["color"] = [float(c) for c in color]
        if width is not None:
            params["width"] = float(width)
        return self.send("bold3", **params)

    # ── Verification Commands ────────────────────────────────

    def ink_count(self, x1, y1, x2, y2):
        """Count stroke points in a bounding box."""
        return self.send("ink_count", x1=float(x1), y1=float(y1),
                         x2=float(x2), y2=float(y2))

    def screenshot(self, path="/tmp/drawing_swift.png"):
        """Save a screenshot of the current display."""
        return self.send("screenshot", path=path)
