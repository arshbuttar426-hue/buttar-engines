"""
Shape mapping session.
Opens Freeform. Captures clicks. You name them via terminal commands.
"""
import time, os, sys, json, threading
sys.path.insert(0, os.path.dirname(__file__))
from freeform_engine import activate_freeform, new_board
from Quartz.CoreGraphics import *
from Quartz import (
    CFMachPortCreateRunLoopSource, CFRunLoopAddSource,
    CFRunLoopRunInMode, kCFRunLoopDefaultMode
)

MAPPING_FILE = os.path.expanduser("~/.opencode_knowledge/shape_map.txt")
event_queue = []
queue_lock = threading.Lock()
tap_running = True

def save_mapping(entry):
    with open(MAPPING_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def cb(proxy, event_type, event, refcon):
    with queue_lock:
        if event_type == kCGEventLeftMouseDown:
            loc = CGEventGetLocation(event)
            event_queue.append(("click", int(loc.x), int(loc.y)))
        elif event_type == kCGEventKeyDown:
            kc = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
            chars = (CGEventGetString(event) or "").strip()
            if chars:
                event_queue.append(("key", kc, chars))
    return event

def event_tap_loop():
    global tap_running
    mask = (1 << kCGEventLeftMouseDown) | (1 << kCGEventKeyDown)
    tap = CGEventTapCreate(
        kCGSessionEventTap, kCGHeadInsertEventTap,
        kCGEventTapOptionDefault, mask, cb, None,
    )
    src = CFMachPortCreateRunLoopSource(None, tap, 0)
    CFRunLoopAddSource(CFRunLoopGetCurrent(), src, kCFRunLoopDefaultMode)
    CGEventTapEnable(tap, True)
    while tap_running:
        CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.5, False)
    CGEventTapEnable(tap, False)

def drain_queue():
    """Return all pending events."""
    out = []
    with queue_lock:
        while event_queue:
            out.append(event_queue.pop(0))
    return out

def main():
    global tap_running
    print("=" * 60)
    print("SHAPE MAPPING SESSION")
    print("=" * 60)
    print()
    print("I opened Freeform with a new board.")
    print("Click the Shape button + pick a shape + click canvas.")
    print()
    print("Terminal commands:")
    print("  c <name>    = name the last 2 clicks as a shape")
    print("  k <code> <n> = name a key code")
    print("  show        = show saved mappings")
    print("  done        = finish")
    print()

    activate_freeform()
    time.sleep(1)
    new_board()
    time.sleep(2)

    tap_thread = threading.Thread(target=event_tap_loop, daemon=True)
    tap_thread.start()

    pending_clicks = []
    last_key = None

    try:
        while True:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not line:
                # Show pending events
                for ev in drain_queue():
                    if ev[0] == "click":
                        pending_clicks.append((ev[1], ev[2]))
                        print(f"  + Click ({ev[1]}, {ev[2]})  [{len(pending_clicks)} pending]")
                    elif ev[0] == "key":
                        last_key = (ev[1], ev[2])
                        print(f"  + Key: code={ev[1]} char='{ev[2]}'")
                continue

            parts = line.split()
            cmd = parts[0].lower()

            if cmd == "done":
                # Drain remaining events
                for ev in drain_queue():
                    if ev[0] == "click":
                        pending_clicks.append((ev[1], ev[2]))
                if pending_clicks:
                    print(f"  {len(pending_clicks)} unlabeled clicks discarded")
                break

            elif cmd == "show":
                if os.path.exists(MAPPING_FILE):
                    with open(MAPPING_FILE) as f:
                        content = f.read()
                        print(content if content else "  (empty)")
                else:
                    print("  No mappings yet.")
                print(f"  Pending clicks: {pending_clicks}")

            elif cmd == "c" and len(parts) >= 2:
                name = " ".join(parts[1:])
                if len(pending_clicks) >= 2:
                    entry = {"clicks": list(pending_clicks[:2]), "shape": name}
                    save_mapping(entry)
                    print(f"  Saved: {name}")
                    pending_clicks = pending_clicks[2:]
                else:
                    print(f"  Need 2 clicks, have {len(pending_clicks)}")

            elif cmd == "k" and len(parts) >= 3:
                try:
                    kc = int(parts[1])
                    name = " ".join(parts[2:])
                    entry = {"key_code": kc, "shape": name}
                    if last_key and last_key[0] == kc:
                        entry["char"] = last_key[1]
                    save_mapping(entry)
                    print(f"  Saved key {kc} = {name}")
                except ValueError:
                    print("  Usage: k <keycode> <name>")
            else:
                print("  Commands: c <name> | k <code> <name> | show | done")

    finally:
        tap_running = False
        time.sleep(0.3)
        print("\nSaved to:", MAPPING_FILE)
        if os.path.exists(MAPPING_FILE):
            with open(MAPPING_FILE) as f:
                print(f.read() or "  (empty)")

if __name__ == "__main__":
    main()
