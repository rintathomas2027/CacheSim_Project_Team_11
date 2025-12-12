"""
direct_mapped_tk.py

Direct-Mapped Cache Simulator with Tkinter graphics.

Run:
    python direct_mapped_tk.py

Controls:
 - Start: play the access sequence with animation
 - Pause: pause animation
 - Step: perform a single access
 - Reset: clear cache and restart sequence from first access
 - Speed: animation delay in ms
 - Cache Size / Block Size: change and Reset
 - Addresses: comma-separated addresses (e.g. 3,11,3,19) or press "Random" to fill
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random

# ---------------- Default configuration ----------------
DEFAULT_CACHE_SIZE = 8
DEFAULT_BLOCK_SIZE = 1
DEFAULT_ADDRESSES = [3, 11, 3, 19, 11, 27, 35, 3, 43, 11, 59, 67, 3, 75]
MIN_SPEED_MS = 50
MAX_SPEED_MS = 2000
# -------------------------------------------------------

class DirectMappedCacheModel:
    def __init__(self, lines, block_size=1):
        self.lines_count = lines
        self.block_size = block_size
        self.reset()

    def reset(self):
        self.lines = [{"valid": False, "tag": None} for _ in range(self.lines_count)]
        self.hits = 0
        self.misses = 0
        self.history_hits = []
        self.history_misses = []
        self.access_log = []  # (addr, index, tag, hit)

    def access(self, address):
        index = (address // self.block_size) % self.lines_count
        tag = address // (self.block_size * self.lines_count)
        line = self.lines[index]
        hit = (line["valid"] and line["tag"] == tag)
        if hit:
            self.hits += 1
        else:
            self.misses += 1
            line["valid"] = True
            line["tag"] = tag
        self.history_hits.append(self.hits)
        self.history_misses.append(self.misses)
        self.access_log.append((address, index, tag, hit))
        return index, tag, hit

    def snapshot(self, upto_index):
        """
        Return a snapshot list of cache lines (valid/tag) after processing accesses up to upto_index (inclusive).
        If upto_index < 0 return empty initial snapshot.
        """
        tmp = [{"valid": False, "tag": None} for _ in range(self.lines_count)]
        for f in range(min(upto_index + 1, len(self.access_log))):
            addr, idx, tg, h = self.access_log[f]
            tmp[idx]["valid"] = True
            tmp[idx]["tag"] = tg
        return tmp

class DirectMappedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Direct-Mapped Cache Simulator (Tkinter)")
        self.resizable(False, False)

        # State values
        self.cache_size = tk.IntVar(value=DEFAULT_CACHE_SIZE)
        self.block_size = tk.IntVar(value=DEFAULT_BLOCK_SIZE)
        self.speed_ms = tk.IntVar(value=500)
        self.is_running = False
        self.current_frame = 0

        # Addresses string variable
        self.addresses_str = tk.StringVar(value=",".join(map(str, DEFAULT_ADDRESSES)))

        # Build UI
        self._build_controls()
        self._build_canvas_area()

        # Init model
        self._reset_model_and_graphics()

    def _build_controls(self):
        frm = ttk.Frame(self, padding=8)
        frm.grid(row=0, column=0, sticky="ew")

        # Cache size / Block size
        ttk.Label(frm, text="Cache Size").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.cache_size, width=6).grid(row=0, column=1, sticky="w", padx=(4,12))
        ttk.Label(frm, text="Block Size").grid(row=0, column=2, sticky="w")
        ttk.Entry(frm, textvariable=self.block_size, width=6).grid(row=0, column=3, sticky="w", padx=(4,12))

        # Addresses entry and random button
        ttk.Label(frm, text="Addresses (comma-separated)").grid(row=1, column=0, columnspan=2, sticky="w", pady=(6,0))
        ttk.Entry(frm, textvariable=self.addresses_str, width=48).grid(row=1, column=2, columnspan=3, sticky="w", padx=(4,0))
        ttk.Button(frm, text="Random", command=self._fill_random).grid(row=1, column=5, padx=(6,0))

        # Controls: Start, Pause, Step, Reset
        ctrl = ttk.Frame(frm)
        ctrl.grid(row=2, column=0, columnspan=6, pady=(8,0))
        ttk.Button(ctrl, text="Start", command=self.start).grid(row=0, column=0, padx=4)
        ttk.Button(ctrl, text="Pause", command=self.pause).grid(row=0, column=1, padx=4)
        ttk.Button(ctrl, text="Step", command=self.step).grid(row=0, column=2, padx=4)
        ttk.Button(ctrl, text="Reset", command=self.reset).grid(row=0, column=3, padx=4)

        # Speed slider
        ttk.Label(ctrl, text="Speed (ms)").grid(row=0, column=4, padx=(12,2))
        self.speed_slider = ttk.Scale(ctrl, from_=MIN_SPEED_MS, to=MAX_SPEED_MS,
                                      orient="horizontal", command=self._on_speed_change)
        self.speed_slider.set(self.speed_ms.get())
        self.speed_slider.grid(row=0, column=5, padx=(0,6))
        self.speed_label = ttk.Label(ctrl, text=str(self.speed_ms.get()))
        self.speed_label.grid(row=0, column=6)

    def _build_canvas_area(self):
        canv_frame = ttk.Frame(self, padding=8)
        canv_frame.grid(row=1, column=0)

        # Left: cache visualization canvas
        self.cache_canvas_w = 420
        self.cache_canvas_h = 360
        self.cache_canvas = tk.Canvas(canv_frame, width=self.cache_canvas_w, height=self.cache_canvas_h, bg="white", bd=1, relief="solid")
        self.cache_canvas.grid(row=0, column=0, padx=6, pady=6)

        # Right: plot canvas (hits/misses)
        self.plot_canvas_w = 420
        self.plot_canvas_h = 360
        self.plot_canvas = tk.Canvas(canv_frame, width=self.plot_canvas_w, height=self.plot_canvas_h, bg="white", bd=1, relief="solid")
        self.plot_canvas.grid(row=0, column=1, padx=6, pady=6)

        # info label under canvases
        self.info_label = ttk.Label(self, text="", anchor="center")
        self.info_label.grid(row=2, column=0, pady=(0,8))

    def _parse_addresses(self):
        raw = self.addresses_str.get().strip()
        if not raw:
            return []
        try:
            parts = [p.strip() for p in raw.split(",") if p.strip() != ""]
            addrs = [int(p) for p in parts]
            return addrs
        except Exception:
            messagebox.showerror("Invalid addresses", "Addresses must be comma-separated integers.")
            return []

    def _fill_random(self):
        size = 14
        # generate random addresses in some range
        addrs = [random.randint(0, 127) for _ in range(size)]
        self.addresses_str.set(",".join(map(str, addrs)))

    def _reset_model_and_graphics(self):
        # Build model
        cs = max(1, int(self.cache_size.get()))
        bs = max(1, int(self.block_size.get()))
        self.model = DirectMappedCacheModel(cs, block_size=bs)

        # Parse addresses
        self.addresses = self._parse_addresses()
        if not self.addresses:
            self.addresses = DEFAULT_ADDRESSES.copy()
            self.addresses_str.set(",".join(map(str, self.addresses)))

        # Reset model and precompute nothing (we'll apply on the fly)
        self.model.reset()

        # Reset simulation indices
        self.current_frame = 0
        self.is_running = False

        # Clear canvases
        self.cache_canvas.delete("all")
        self.plot_canvas.delete("all")

        # Draw static labels and empty cache lines
        self._draw_cache_static()
        self._draw_plot_static()
        self._update_info()

    def reset(self):
        self._reset_model_and_graphics()

    def start(self):
        # If cache size or addresses changed since last reset, reset model.
        try:
            cs = max(1, int(self.cache_size.get()))
            bs = max(1, int(self.block_size.get()))
        except Exception:
            messagebox.showerror("Invalid Input", "Cache Size and Block Size must be integers.")
            return
        self.is_running = True
        self._schedule_next()

    def pause(self):
        self.is_running = False

    def step(self):
        if self.current_frame >= len(self.addresses):
            return
        self._do_access_at_frame(self.current_frame)
        self.current_frame += 1
        self._update_info()

    def _on_speed_change(self, val):
        self.speed_ms.set(int(float(val)))
        self.speed_label.config(text=str(self.speed_ms.get()))

    def _schedule_next(self):
        if self.is_running and self.current_frame < len(self.addresses):
            self.after(max(MIN_SPEED_MS, self.speed_ms.get()), self._tick)

    def _tick(self):
        if not self.is_running:
            return
        if self.current_frame >= len(self.addresses):
            self.is_running = False
            return
        self._do_access_at_frame(self.current_frame)
        self.current_frame += 1
        self._update_info()
        if self.current_frame < len(self.addresses):
            self._schedule_next()
        else:
            self.is_running = False

    def _do_access_at_frame(self, frame_idx):
        addr = self.addresses[frame_idx]
        index, tag, hit = self.model.access(addr)
        # redraw cache snapshot up to this frame
        snapshot = self.model.snapshot(frame_idx)
        self._draw_cache_snapshot(snapshot, accessed_index=index)
        self._draw_plot(frame_idx)  # frame_idx is last index included
        # small flash or mark for hit/miss could be done via color; we'll show text
        # info label updated elsewhere

    # -------- Drawing functions for cache visualization --------
    def _draw_cache_static(self):
        # Title
        self.cache_canvas.create_text(self.cache_canvas_w/2, 16, text="Cache Lines", font=("Helvetica", 14, "bold"))
        # For each cache line, draw a rectangle and placeholders
        margin_x = 20
        margin_y = 36
        spacing = 24
        rect_w = self.cache_canvas_w - 2*margin_x
        rect_h = 20
        self.cache_line_positions = []
        for i in range(self.model.lines_count):
            y = margin_y + i * spacing
            rect_id = self.cache_canvas.create_rectangle(margin_x, y, margin_x + rect_w, y + rect_h, width=1, fill="white", tags=("line", f"line{i}"))
            # index label
            self.cache_canvas.create_text(margin_x + 12, y + rect_h/2, text=f"{i}", anchor="w", font=("Helvetica", 9))
            # Tag text and Valid text placeholders
            tag_x = margin_x + 40
            valid_x = margin_x + rect_w - 60
            txt_tag = self.cache_canvas.create_text(tag_x, y + rect_h/2, text="Tag: -", anchor="w", font=("Helvetica", 9), tags=(f"tag{i}",))
            txt_valid = self.cache_canvas.create_text(valid_x, y + rect_h/2, text="Valid: 0", anchor="w", font=("Helvetica", 9), tags=(f"valid{i}",))
            self.cache_line_positions.append((rect_id, txt_tag, txt_valid))

    def _draw_cache_snapshot(self, snapshot, accessed_index=None):
        # snapshot: list of {"valid": bool, "tag": value}
        for i, (rect_id, txt_tag, txt_valid) in enumerate(self.cache_line_positions):
            v = snapshot[i]["valid"]
            tg = snapshot[i]["tag"]
            self.cache_canvas.itemconfigure(txt_tag, text=f"Tag: {'-' if tg is None else tg}")
            self.cache_canvas.itemconfigure(txt_valid, text=f"Valid: {1 if v else 0}")
            # highlight accessed line
            if accessed_index is not None and i == accessed_index:
                # orange border when accessed; green fill for hit, red fill for miss
                # Determine if hit by comparing last access_log entry if exists
                last_hit = False
                if self.model.access_log:
                    last_addr, last_idx, last_tag, last_hit = self.model.access_log[-1]
                color = "#FFE8D0"  # neutral background
                if last_idx == i:
                    if last_hit:
                        color = "#DFF7DF"  # pale green for hit
                    else:
                        color = "#FFE1E1"  # pale red for miss
                self.cache_canvas.itemconfigure(rect_id, outline="orange", width=2, fill=color)
            else:
                self.cache_canvas.itemconfigure(rect_id, outline="black", width=1, fill="white")

    # -------- Drawing functions for hits/misses plot --------
    def _draw_plot_static(self):
        self.plot_canvas.create_text(self.plot_canvas_w/2, 16, text="Cumulative Hits vs Misses", font=("Helvetica", 14, "bold"))
        # draw axes
        left = 40
        bottom = self.plot_canvas_h - 40
        top = 40
        right = self.plot_canvas_w - 20
        # store coordinates for plotting area
        self.plot_area = (left, top, right, bottom)
        self.plot_canvas.create_rectangle(left, top, right, bottom, outline="black")
        # axis labels
        self.plot_canvas.create_text((left+right)//2, bottom + 20, text="Access number", font=("Helvetica", 9))
        self.plot_canvas.create_text(12, (top+bottom)//2, text="Count", font=("Helvetica", 9), angle=90)

    def _draw_plot(self, upto_frame):
        left, top, right, bottom = self.plot_area
        w = right - left
        h = bottom - top
        # Clear area inside (but keep border)
        self.plot_canvas.create_rectangle(left+1, top+1, right-1, bottom-1, fill="white", outline="")
        n = upto_frame + 1
        if n <= 0:
            return
        # compute max count for scaling
        max_count = max(1, max(self.model.history_hits[:n] + self.model.history_misses[:n]))
        # draw grid lines (optional)
        steps = min(10, max_count)
        for s in range(steps + 1):
            y = bottom - (s / steps) * h
            self.plot_canvas.create_line(left, y, right, y, fill="#f0f0f0")
            self.plot_canvas.create_text(left - 6, y, text=str(round((s/steps)*max_count)), anchor="e", font=("Helvetica", 7))
        # draw axes ticks on x
        for i in range(n):
            x = left + (i / max(1, len(self.addresses)-1)) * w if len(self.addresses) > 1 else left + w/2
            self.plot_canvas.create_text(x, bottom + 10, text=str(i+1), font=("Helvetica", 7))
        # plot hits as connected points/lines
        prev_x = prev_yh = prev_ym = None
        for i in range(n):
            x = left + (i / max(1, len(self.addresses)-1)) * w if len(self.addresses) > 1 else left + w/2
            yh = bottom - (self.model.history_hits[i] / max_count) * h
            ym = bottom - (self.model.history_misses[i] / max_count) * h
            # draw points
            self.plot_canvas.create_oval(x-3, yh-3, x+3, yh+3, fill="green", outline="")
            self.plot_canvas.create_oval(x-3, ym-3, x+3, ym+3, fill="red", outline="")
            # draw lines from previous
            if prev_x is not None:
                self.plot_canvas.create_line(prev_x, prev_yh, x, yh, fill="green", width=2)
                self.plot_canvas.create_line(prev_x, prev_ym, x, ym, fill="red", width=2)
            prev_x, prev_yh, prev_ym = x, yh, ym
        # legend
        self.plot_canvas.create_rectangle(right-110, top+8, right-10, top+42, outline="#ccc", fill="#fff")
        self.plot_canvas.create_oval(right-100, top+16, right-92, top+24, fill="green", outline="")
        self.plot_canvas.create_text(right-80, top+20, text="Hits", anchor="w", font=("Helvetica", 9))
        self.plot_canvas.create_oval(right-100, top+28, right-92, top+36, fill="red", outline="")
        self.plot_canvas.create_text(right-80, top+32, text="Misses", anchor="w", font=("Helvetica", 9))

    def _update_info(self):
        if self.current_frame == 0:
            info = f"Ready. Total accesses: {len(self.addresses)}"
        else:
            last = self.model.access_log[-1] if self.model.access_log else None
            if last:
                addr, idx, tg, hit = last
                info = f"Last access #{self.current_frame}: Address={addr} (Index={idx}, Tag={tg}) -> {'HIT' if hit else 'MISS'} | Hits: {self.model.hits} Misses: {self.model.misses}"
            else:
                info = f"Hits: {self.model.hits} Misses: {self.model.misses}"
        self.info_label.config(text=info)

# ------------- Run the app -------------
if __name__ == "__main__":
    app = DirectMappedApp()
    app.mainloop()
