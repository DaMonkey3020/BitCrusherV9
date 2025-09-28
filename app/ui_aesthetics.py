

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, Toplevel
from tkinter import filedialog as fd
from tkinter import colorchooser as tkcolor
from tkinter import simpledialog as tksimple
import tkinter.font as tkfont
import json, colorsys
from typing import Callable
from importlib import import_module


def _noop(*_a, **_k): pass

def _get(host, name, default):
    return getattr(host, name, default)


def _set_font_family(root: tk.Tk, family_order: tuple[str, ...] = ("Segoe UI Variable","Inter","Segoe UI","Arial"),
                     force_family: str | None = None, force_size: int | None = None):
    available = set(tkfont.families(root))
    pick = (force_family if force_family in available else None) or next((f for f in family_order if f in available), "Segoe UI")
    for fam in ("TkDefaultFont","TkTextFont","TkHeadingFont","TkMenuFont","TkTooltipFont","TkFixedFont"):
        try:
            f = tkfont.nametofont(fam)
            sz = f.cget("size")
            if fam == "TkDefaultFont" and (force_size or 0) > 0:
                f.configure(family=pick, size=int(force_size))
            elif fam == "TkDefaultFont" and sz < 10:
                f.configure(family=pick, size=10)
            else:
                f.configure(family=pick)
        except Exception:
            pass

from importlib import import_module

def animated_retheme(host, theme_name: str, fade_ms: int = 0, dim_to: float | None = None):
    """
    Clean theme swap (no invisibility). If you ever want a subtle dim instead of a full fade,
    pass dim_to=0.85 (or similar); default keeps alpha unchanged.
    """
    root: tk.Tk = host.root
    style: ttk.Style = host.style

    try:
        mod = import_module(host.__module__)
    except Exception:
        mod = None

    def _resolve(name, default=_noop):
        if hasattr(host, name):
            return getattr(host, name)
        if mod and hasattr(mod, name):
            return getattr(mod, name)
        return default

    apply_theme_fn     = _resolve("apply_theme")
    retheme_runtime_fn = _resolve("retheme_runtime")
    fade_window_fn     = _resolve("fade_window")

    def _maybe_dim(start_alpha, end_alpha):
        try:
            if dim_to is not None:

                fade_window_fn(root, start=start_alpha, end=dim_to, dur_ms=max(80, int(fade_ms*0.5)))
        except Exception:
            pass

    def _maybe_undim(start_alpha, end_alpha):
        try:
            if dim_to is not None:
                fade_window_fn(root, start=dim_to, end=1.0, dur_ms=max(120, int(fade_ms*0.7)))
        except Exception:
            pass

    try:
        cur_alpha = 1.0
        try:
            cur_alpha = root.attributes("-alpha")
        except Exception:
            pass
        _maybe_dim(cur_alpha, dim_to)
    except Exception:
        pass

    try:
        if retheme_runtime_fn is not _noop:
            retheme_runtime_fn(host, style, theme_name)
        else:
            apply_theme_fn(style, theme_name)
    except Exception:
        pass

    _maybe_undim(dim_to, 1.0)


def make_card(parent: tk.Misc, padding: int = 12) -> ttk.Frame:


    shadow = ttk.Frame(parent, style="TFrame")
    shadow.place_configure()  # noop if used with .pack/.grid

    card = ttk.Frame(shadow, style="Card.TFrame")

    try:

        s = ttk.Style()
        cbg = s.lookup("Card.TFrame", "background") or "#1C1F24"

        try:
            from importlib import import_module as _imp
            _mod = _imp(parent.winfo_toplevel().__class__.__module__)
            _hsl = getattr(_mod, "_hsl_shift", lambda c, **_: c)
        except Exception:
            _hsl = lambda c, **_: c
        backplate = tk.Frame(shadow, bg=_hsl(cbg, l_mul=0.80))

        backplate.place(relx=0, rely=0, x=2, y=3, relwidth=1, relheight=1)
        card.place(in_=shadow, relx=0, rely=0, x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        pass

    shadow.card = card  # type: ignore

    for side in ("top", "bottom", "left", "right"):
        tk.Frame(card, height=padding if side in ("top", "bottom") else 0,
                 width=padding if side in ("left", "right") else 0).pack(
            side=side, fill="x" if side in ("top", "bottom") else "y")
    return card

def wrap_as_card(widget: tk.Widget) -> ttk.Frame:
    """Take an existing widget, reparent it inside a new Card, preserving geometry manager via pack."""
    parent = widget.master
    card = make_card(parent)
    widget.pack_forget()
    widget.master = card  # type: ignore
    widget.pack(fill="both", expand=True)
    return card


def install_button_hover_fx(root: tk.Misc):
    """Scale buttons slightly on hover with a cheap transform via tk.call('scale'...)."""
    def on_enter(e):
        w = e.widget
        try:
            w.tk.call(w, 'scale', 0, 0, 1.02, 1.02)
        except Exception:
            pass
    def on_leave(e):
        w = e.widget
        try:
            w.tk.call(w, 'scale', 0, 0, 1.0, 1.0)
        except Exception:
            pass
    def _bind_recursive(w: tk.Widget):
        if isinstance(w, ttk.Button):
            w.bind("<Enter>", on_enter, add="+")
            w.bind("<Leave>", on_leave, add="+")
        for child in w.winfo_children():
            _bind_recursive(child)
    _bind_recursive(root)

def install_queue_drop_highlight(host):
    
    install_drop_highlight = _get(host, "install_drop_highlight", _noop)
    if hasattr(host, "queue_container"):
        try:
            install_drop_highlight(host.queue_container)  # type: ignore
        except Exception:
            pass

def install_snackbar_hooks(host):
    """Replace common messagebox/info flows with a snackbar for brief status toasts."""
    snackbar = _get(host, "snackbar", _noop)
    def info(msg: str): snackbar(host.root, msg, millis=1800, kind="info")
    def warn(msg: str): snackbar(host.root, msg, millis=2200, kind="warn")
    def err (msg: str): snackbar(host.root, msg, millis=2600, kind="error")
    host.ui_info = info
    host.ui_warn = warn
    host.ui_error = err


def _hex_norm(x: str) -> str:
    try:
        x = (x or "").strip()
        if not x: return "#000000"
        if x[0] != "#": x = "#" + x
        if len(x) == 4:  # #abc → #aabbcc
            x = "#" + "".join(ch*2 for ch in x[1:])
        return x[:7]
    except Exception:
        return "#000000"

def _wcag_ratio(c1: str, c2: str) -> float:
    def _lumin(hex6: str) -> float:
        hex6 = hex6.lstrip("#")
        r = int(hex6[0:2],16)/255.0; g=int(hex6[2:4],16)/255.0; b=int(hex6[4:6],16)/255.0
        def _lin(u): return u/12.92 if u<=0.03928 else ((u+0.055)/1.055)**2.4
        R,G,B = _lin(r),_lin(g),_lin(b)
        return 0.2126*R + 0.7152*G + 0.0722*B
    L1, L2 = sorted([_lumin(_hex_norm(c1)), _lumin(_hex_norm(c2))], reverse=True)
    return (L1 + 0.05) / (L2 + 0.05)

def _ratio_badge(r: float) -> str:
    return "AAA" if r >= 7 else ("AA" if r >= 4.5 else ("A" if r >= 3 else "⚠"))


class ThemeLab(Toplevel):
    def __init__(self, host):
        super().__init__(host.root)
        self.title("Theme Lab")
        self.host = host
        self.style: ttk.Style = host.style
        self.resizable(False, False)
        self.transient(host.root)

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        tab_palette = ttk.Frame(nb)
        nb.add(tab_palette, text="Palette")

        self._build_palette_editor(tab_palette)

        tab_adjust = ttk.Frame(nb)
        nb.add(tab_adjust, text="Adjust")

        self.h = tk.DoubleVar(value=0.0)
        self.s = tk.DoubleVar(value=1.0)
        self.l = tk.DoubleVar(value=1.0)

        self._base_theme_name = self._current_theme()
        self._base_palette_snapshot = dict(self._palette() or {})

        self._debounce_id = None
        self._dragging = False
        self._row_slider(tab_adjust, "Hue Δ",  self.h, 0.0, 1.0, 0.001)
        self._row_slider(tab_adjust, "Sat ×",  self.s, 0.5, 1.5, 0.005)
        self._row_slider(tab_adjust, "Light ×",self.l, 0.7, 1.3, 0.005)

        tab_type = ttk.Frame(nb)
        nb.add(tab_type, text="Typography")
        self._build_typography(tab_type)

        tab_prev = ttk.Frame(nb)
        nb.add(tab_prev, text="Preview")
        self._build_preview(tab_prev)

        btns = ttk.Frame(self, style="Card.TFrame")
        btns.pack(fill="x", padx=10, pady=10)
        ttk.Button(btns, text="Save as JSON…", command=self._save_json).pack(side="left", padx=(0,6))
        ttk.Button(btns, text="Load JSON…", command=self._load_json).pack(side="left", padx=6)
        ttk.Button(btns, text="Save as Named Theme…", command=self._save_named).pack(side="left", padx=6)
        ttk.Button(btns, text="Reset Adjustments", command=self._reset_adjustments).pack(side="left", padx=6)
        ttk.Button(btns, text="Close", command=self.destroy).pack(side="right")

        self.after(30, lambda: animated_retheme(self.host, self._current_theme()))

    def _current_theme(self) -> str:
        try: return self.host.theme_var.get()
        except Exception: return "Dark"

    def _palette(self) -> dict:
        try: mod = import_module(self.host.__module__)
        except Exception: mod = None
        THEMES = getattr(self.host, "THEMES", getattr(mod, "THEMES", {}))
        return THEMES.get(self._current_theme(), {})

    def _reset_adjustments(self):

        try:
            self.h.set(0.0); self.s.set(1.0); self.l.set(1.0)
        except Exception:
            pass

        base_name = getattr(self, "_base_theme_name", None) or self._current_theme()
        base_palette = dict(getattr(self, "_base_palette_snapshot", {}) or {})

        try:
            self.host.theme_var.set(base_name)
        except Exception:
            pass

        try:
            from importlib import import_module
            mod = import_module(self.host.__module__)
        except Exception:
            mod = None
        try:
            THEMES = getattr(self.host, "THEMES", getattr(mod, "THEMES", {}))
            if base_palette:
                THEMES[base_name] = base_palette
        except Exception:
            pass

        try:
            from ui_aesthetics import animated_retheme
            animated_retheme(self.host, base_name)
        except Exception:
            try:
                if hasattr(self.host, "retheme_runtime"):
                    self.host.retheme_runtime(self.host.style, base_name)
                elif hasattr(self.host, "apply_theme"):
                    self.host.apply_theme(self.host.style, base_name)
            except Exception:
                pass

        try:
            self.host.settings = getattr(self.host, "settings", {}) or {}
            self.host.settings["theme"] = base_name
            if hasattr(self.host, "save_settings"):
                self.host.save_settings()
            if hasattr(self.host, "rebuild_themes_menu"):
                self.host.rebuild_themes_menu()
        except Exception:
            pass

        try:
            self._base_theme_name = base_name
            self._base_palette_snapshot = dict(self._palette() or {})
        except Exception:
            pass

    def _build_palette_editor(self, parent):
        order = ("APP_BG","CARD_BG","FG","FG_SUB","ACCENT","ACCENT_2","ERROR","WARN","TITLE")
        cur = self._palette() or {}
        self._vars = {k: tk.StringVar(value=cur.get(k, "#000000")) for k in order}

        grid = ttk.Frame(parent); grid.pack(fill="both", expand=True, padx=12, pady=12)
        for r, key in enumerate(order):
            ttk.Label(grid, text=key, width=10).grid(row=r, column=0, sticky="w", padx=(0,8), pady=4)
            sw = tk.Label(grid, width=3, relief="flat", bd=0, bg=_hex_norm(self._vars[key].get()))
            sw.grid(row=r, column=1, padx=4, pady=4, sticky="w")
            ent = ttk.Entry(grid, textvariable=self._vars[key], width=12, style="Dark.TEntry")
            ent.grid(row=r, column=2, padx=4, pady=4, sticky="w")
            ttk.Button(grid, text="Pick…", command=lambda k=key: self._pick_color(k)).grid(row=r, column=3, padx=4, pady=4)

            ratio = tk.Label(grid, text="", width=4); ratio.grid(row=r, column=4, padx=4, pady=4)
            def _on_change(*_a, k=key, swatch=sw, badge=ratio):
                c = _hex_norm(self._vars[k].get())
                try: swatch.configure(bg=c)
                except Exception: pass
                try:
                    app_bg = _hex_norm(self._vars["APP_BG"].get())
                    badge.configure(text=_ratio_badge(_wcag_ratio(c, app_bg)))
                except Exception: pass
                self._apply_palette_vars()
            self._vars[key].trace_add("write", _on_change)
            _on_change()

    def _pick_color(self, key: str):
        c0 = _hex_norm(self._vars[key].get())
        rgb, hx = tkcolor.askcolor(color=c0, parent=self)
        if hx:
            self._vars[key].set(_hex_norm(hx))

    def _apply_palette_vars(self, persist: bool = True, animate: bool = True, palette: dict | None = None):
        """
        Apply a palette as 'Custom Live'.
        If 'palette' is None we build it from self._vars (Palette tab).
        If persist=False we skip disk writes/settings.
        If animate=False we apply instantly (no fade) for smooth dragging.
        """
        live = dict(palette) if isinstance(palette, dict) else {k: _hex_norm(v.get()) for k, v in self._vars.items()}

        try:
            mod = import_module(self.host.__module__)
        except Exception:
            mod = None

        THEMES = getattr(self.host, "THEMES", getattr(mod, "THEMES", {}))
        THEMES["Custom Live"] = live

        if persist:
            try:
                import os, json
                USER_SETTINGS_DIR = getattr(mod, "USER_SETTINGS_DIR", None)
                if not USER_SETTINGS_DIR:
                    host_file = getattr(mod, "__file__", None)
                    base_dir = os.path.dirname(host_file) if host_file else os.getcwd()
                    USER_SETTINGS_DIR = os.path.join(base_dir, "user_settings")
                thdir = os.path.join(USER_SETTINGS_DIR, "themes"); os.makedirs(thdir, exist_ok=True)
                with open(os.path.join(thdir, "Custom Live.json"), "w", encoding="utf-8") as f:
                    json.dump(live, f, indent=2)
            except Exception:
                pass

        try:
            self.host.theme_var.set("Custom Live")
        except Exception:
            pass

        try:
            if not animate and hasattr(self.host, "retheme_runtime"):
                self.host.retheme_runtime(self.host.style, "Custom Live")
            else:
                animated_retheme(self.host, "Custom Live")
        except Exception:
            try:
                self.host.retheme_runtime(self.host.style, "Custom Live")
            except Exception:
                pass

        if persist:
            try:
                self.host.settings = getattr(self.host, "settings", {}) or {}
                self.host.settings["theme"] = "Custom Live"
                if hasattr(self.host, "save_settings"): self.host.save_settings()
                if hasattr(self.host, "rebuild_themes_menu"): self.host.rebuild_themes_menu()
                saver = getattr(self.host, "_save_theme_choice", None) or (getattr(mod, "_save_theme_choice", None) if mod else None)
                if callable(saver): saver("Custom Live")
            except Exception:
                pass

    def _apply_live(self, preview_only: bool = True):
        """
        Compute live palette from base + H/S/L and apply.
        preview_only=True -> instant apply, no disk writes (for drag).
        preview_only=False -> persist + remember selection.
        """
        base = (getattr(self, "_base_palette_snapshot", None) or self._palette() or {})
        if not base:
            return
        h, s, l = self.h.get(), self.s.get(), self.l.get()
        live = {k: self._hsl_shift_local(v, h_delta=h, s_mul=s, l_mul=l) for k, v in base.items()}

        self._apply_palette_vars(
            persist=not preview_only,
            animate=not preview_only,
            palette=live
        )

        if not preview_only:

            for k, v in (self._vars or {}).items():
                v.set(live.get(k, v.get()))



    def _schedule_preview(self, delay_ms: int = 16):

        if getattr(self, "_debounce_id", None):
            try:
                self.after_cancel(self._debounce_id)
            except Exception:
                pass
        self._debounce_id = self.after(delay_ms, lambda: self._apply_live(preview_only=True))

    def _commit_live_from_adjust(self):
        self._dragging = False
        if getattr(self, "_debounce_id", None):
            try:
                self.after_cancel(self._debounce_id)
            except Exception:
                pass
            self._debounce_id = None

        self._apply_live(preview_only=False)




    def _hsl_shift_local(self, hex_color: str, h_delta=0.0, s_mul=1.0, l_mul=1.0) -> str:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)/255.0; g=int(hex_color[2:4],16)/255.0; b=int(hex_color[4:6],16)/255.0
        h,l,s = colorsys.rgb_to_hls(r,g,b); h=(h+h_delta)%1.0; s=max(0.0,min(1.0,s*s_mul)); l=max(0.0,min(1.0,l*l_mul))
        r,g,b = colorsys.hls_to_rgb(h,l,s); return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def _build_typography(self, parent):
        row = ttk.Frame(parent); row.pack(fill="x", padx=12, pady=12)
        ttk.Label(row, text="Font family:", width=12).pack(side="left")
        fams = sorted(set(tkfont.families(self)))
        self._fam = tk.StringVar(value=self._detect_current_family())
        cb = ttk.Combobox(row, values=fams, textvariable=self._fam, width=24, state="readonly", style="Dark.TCombobox")
        cb.pack(side="left", padx=6); cb.bind("<<ComboboxSelected>>", lambda _e=None: self._apply_typography())
        ttk.Label(row, text="Base size:", width=10).pack(side="left", padx=(16,0))
        self._size = tk.IntVar(value=self._detect_current_size())
        sp = ttk.Spinbox(row, from_=8, to=18, textvariable=self._size, width=5)  # ttk Spinbox if available
        sp.pack(side="left", padx=6)
        for v in (self._size,):
            v.trace_add("write", lambda *_: self._apply_typography())

    def _detect_current_family(self) -> str:
        try: return tkfont.nametofont("TkDefaultFont").cget("family")
        except Exception: return "Segoe UI"

    def _detect_current_size(self) -> int:
        try: return int(tkfont.nametofont("TkDefaultFont").cget("size"))
        except Exception: return 10

    def _apply_typography(self):
        fam = self._fam.get().strip(); size = int(self._size.get())
        try:
            _set_font_family(self.host.root, force_family=fam, force_size=size)
        except Exception:
            pass

        try:
            self.host.settings = getattr(self.host, "settings", {}) or {}
            self.host.settings["ui_font_family"] = fam
            self.host.settings["ui_font_size"]   = size
            if hasattr(self.host, "save_settings"): self.host.save_settings()
        except Exception:
            pass

    def _build_preview(self, parent):
        frm = ttk.Frame(parent); frm.pack(fill="both", expand=True, padx=12, pady=12)
        card = ttk.Frame(frm, style="Card.TFrame"); card.pack(fill="x", pady=6)
        ttk.Label(card, text="Preview: Controls", style="Sub.TLabel").pack(anchor="w", padx=10, pady=(10,0))
        inner = ttk.Frame(card); inner.pack(fill="x", padx=10, pady=10)
        ttk.Entry(inner, width=24, style="Dark.TEntry").pack(side="left", padx=6)
        ttk.Button(inner, text="Primary").pack(side="left", padx=6)
        ttk.Button(inner, text="Ghost", style="Ghost.TButton").pack(side="left", padx=6)
        ttk.Checkbutton(inner, text="Check me").pack(side="left", padx=12)
        pb = ttk.Progressbar(card, mode="indeterminate", style="Accent.Horizontal.TProgressbar", length=260)
        pb.pack(fill="x", padx=10, pady=(6,10)); pb.start(8)

    def _save_named(self):
        name = tksimple.askstring("Save Theme", "Theme name:", parent=self)
        if not name: return

        live = {k: _hex_norm(v.get()) for k, v in self._vars.items()}
        try:
            mod = import_module(self.host.__module__)
        except Exception:
            mod = None
        THEMES = getattr(self.host, "THEMES", getattr(mod, "THEMES", {}))
        THEMES[name] = live
        try:
            import os, json
            USER_SETTINGS_DIR = getattr(mod, "USER_SETTINGS_DIR", None)
            if not USER_SETTINGS_DIR:
                host_file = getattr(mod, "__file__", None)
                base_dir = os.path.dirname(host_file) if host_file else os.getcwd()
                USER_SETTINGS_DIR = os.path.join(base_dir, "user_settings")
            thdir = os.path.join(USER_SETTINGS_DIR, "themes"); os.makedirs(thdir, exist_ok=True)
            with open(os.path.join(thdir, f"{name}.json"), "w", encoding="utf-8") as f:
                json.dump(live, f, indent=2)
        except Exception:
            pass
        try: self.host.theme_var.set(name)
        except Exception: pass
        try: animated_retheme(self.host, name)
        except Exception:
            try: self.host.retheme_runtime(self.host.style, name)
            except Exception: pass
        try:
            self.host.settings = getattr(self.host, "settings", {}) or {}
            self.host.settings["theme"] = name
            if hasattr(self.host, "save_settings"): self.host.save_settings()
            if hasattr(self.host, "rebuild_themes_menu"): self.host.rebuild_themes_menu()
        except Exception:
            pass



    def _palette(self):

        try:
            mod = import_module(self.host.__module__)
        except Exception:
            mod = None
        THEMES = getattr(self.host, "THEMES", getattr(mod, "THEMES", {}))
        name = self._current_theme()
        return THEMES.get(name, next(iter(THEMES.values())) if THEMES else {})


    def _current_theme(self) -> str:

        try:
            return self.host.theme_var.get()
        except Exception:
            return "Dark"

    def _row_slider(self, parent, label, var, mn, mx, res):
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", pady=6)
        ttk.Label(row, text=label, width=10).pack(side="left")
        s = ttk.Scale(row, variable=var, from_=mn, to=mx)
        s.pack(side="left", fill="x", expand=True, padx=8)

        s.bind("<ButtonPress-1>",    lambda _e=None: setattr(self, "_dragging", True))
        s.bind("<B1-Motion>",        lambda _e=None: self._schedule_preview())
        s.bind("<ButtonRelease-1>",  lambda _e=None: self._commit_live_from_adjust())

        var.trace_add("write", lambda *_: self._schedule_preview())
        return s




    def _hsl_shift_local(self, hex_color: str, h_delta=0.0, s_mul=1.0, l_mul=1.0) -> str:
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        h,l,s = colorsys.rgb_to_hls(r,g,b)
        h = (h + h_delta) % 1.0
        s = max(0.0, min(1.0, s * s_mul))
        l = max(0.0, min(1.0, l * l_mul))
        r,g,b = colorsys.hls_to_rgb(h,l,s)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        THEMES = getattr(self.host, "THEMES", getattr(mod, "THEMES", {}))
        name = self._current_theme()
        base = dict(THEMES.get(name, {}))
        if not base:
            return
        h, s, l = self.h.get(), self.s.get(), self.l.get()
        live = {k: self._hsl_shift_local(v, h_delta=h, s_mul=s, l_mul=l) for k, v in base.items()}

        try:
            import os, json
            USER_SETTINGS_DIR = getattr(mod, "USER_SETTINGS_DIR", None)
            if not USER_SETTINGS_DIR:
                host_file = getattr(mod, "__file__", None)
                base_dir = os.path.dirname(host_file) if host_file else os.getcwd()
                USER_SETTINGS_DIR = os.path.join(base_dir, "user_settings")
            themes_dir = os.path.join(USER_SETTINGS_DIR, "themes")
            os.makedirs(themes_dir, exist_ok=True)
            with open(os.path.join(themes_dir, "Custom Live.json"), "w", encoding="utf-8") as f:
                json.dump(live, f, indent=2)
        except Exception:
            pass

        THEMES["Custom Live"] = live
        try:
            self.host.theme_var.set("Custom Live")
        except Exception:
            pass
        try:
            from ui_aesthetics import animated_retheme
            animated_retheme(self.host, "Custom Live")
        except Exception:

            try:
                style = getattr(self.host, "style")
                apply_theme = getattr(self.host, "apply_theme")
                retheme_runtime = getattr(self.host, "retheme_runtime")
                apply_theme(style, "Custom Live")
                retheme_runtime(self.host, style, "Custom Live")
            except Exception:
                pass

        try:
            saver = getattr(self.host, "_save_theme_choice", None) or (getattr(mod, "_save_theme_choice", None) if mod else None)
            if callable(saver):
                saver("Custom Live")
            self.host.settings = getattr(self.host, "settings", {}) or {}
            self.host.settings["theme"] = "Custom Live"
            if hasattr(self.host, "save_settings"):
                self.host.save_settings()
            if hasattr(self.host, "rebuild_themes_menu"):
                self.host.rebuild_themes_menu()
        except Exception:
            pass





    def _save_json(self):
        THEMES = _get(self.host, "THEMES", {})
        name = self._current_theme()
        data = THEMES.get(name, {})
        if not data:
            return
        p = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=f"{name}.json")
        if not p: return
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        _snack = _get(self.host, "snackbar", _noop)
        _snack(self.host.root, f"Saved theme '{name}'", 1400, "info")

    def _load_json(self):
        THEMES = _get(self.host, "THEMES", {})
        p = fd.askopenfilename(filetypes=[("JSON", "*.json")])
        if not p: return
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data:
                key = (p.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]).rsplit(".", 1)[0]
                THEMES[key] = data
                try:
                    self.host.theme_var.set(key)
                except Exception:
                    pass
                animated_retheme(self.host, key)
        except Exception:
            _snack = _get(self.host, "snackbar", _noop)
            _snack(self.host.root, "Invalid theme file", 1800, "error")


def init_aesthetics(host):

    st = getattr(host, "settings", {}) or {}
    _set_font_family(host.root, force_family=st.get("ui_font_family"), force_size=st.get("ui_font_size"))
    install_button_hover_fx(host.root)
    install_snackbar_hooks(host)
    for attr in ("queue_container","log_container","preview_container"):
        if hasattr(host, attr):
            try: wrap_as_card(getattr(host, attr))
            except Exception: pass

def open_theme_lab(host):
    ThemeLab(host)
