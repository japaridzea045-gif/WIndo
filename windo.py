"""Windo - Android debloater for Windows (ADB based, Canta-style)."""
import os, sys, subprocess, threading, shutil
import tkinter as tk
from tkinter import ttk, messagebox
from windo_db import DB, FAMILY_NAMES, detect_brand, relevant, counts
from windo_rules import classify
from windo_boot import CATS, CAT_BY_KEY, detect_category

APP = "Windo"
VERSION = "2.1"
NOWIN = 0x08000000 if os.name == "nt" else 0

PROPS = [("Manufacturer", "ro.product.manufacturer"), ("Brand", "ro.product.brand"),
         ("Model", "ro.product.model"), ("Marketing name", "ro.product.marketname"),
         ("Codename", "ro.product.device"), ("Product", "ro.product.name"),
         ("Android version", "ro.build.version.release"), ("SDK / API", "ro.build.version.sdk"),
         ("Security patch", "ro.build.version.security_patch"), ("Build", "ro.build.display.id"),
         ("CPU ABI", "ro.product.cpu.abi"), ("Hardware", "ro.hardware"),
         ("Board", "ro.product.board"), ("Bootloader", "ro.bootloader"),
         ("MIUI/HyperOS", "ro.miui.ui.version.name"), ("One UI", "ro.build.version.oneui"),
         ("ColorOS", "ro.build.version.opporom")]

BG, FG, PANEL, ACC = "#14161a", "#e8eaed", "#1e2127", "#4f8cff"
LV = {"safe": "#3ddc84", "medium": "#ffd60a", "high": "#ff5252"}
FONT_NAME = ("Segoe UI Semibold", 12)
FONT_UI = ("Segoe UI", 10)
GREEN, GREEN_D = "#3ddc84", "#2fb86b"
YELLOW, YELLOW_D = "#ffd60a", "#d9b500"
EDGE, BTN, DARKTXT = "#2a2f38", "#2a2f38", "#06210f"


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def dot_pixels(color, bg, size=18, ss=4):
    """Anti-aliased filled circle as rows of hex colours (None = transparent)."""
    c, r = size / 2.0, size / 2.0 - 1
    fg, bk = _rgb(color), _rgb(bg)
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            hit = sum(1 for sy in range(ss) for sx in range(ss)
                      if (x + (sx + .5) / ss - c) ** 2 + (y + (sy + .5) / ss - c) ** 2 <= r * r)
            if hit == 0:
                row.append(None)
            else:
                a = hit / float(ss * ss)
                row.append("#%02x%02x%02x" % tuple(int(f * a + b * (1 - a)) for f, b in zip(fg, bk)))
        rows.append(row)
    return rows


def make_dot(color, bg, size=18):
    img = tk.PhotoImage(width=size, height=size)
    for y, row in enumerate(dot_pixels(color, bg, size)):
        for x, px in enumerate(row):
            if px:
                img.put(px, (x, y))
            else:
                img.transparency_set(x, y, True)
    return img


def base_dirs():
    d = [os.path.dirname(os.path.abspath(sys.argv[0]))]
    if hasattr(sys, "_MEIPASS"):
        d.insert(0, sys._MEIPASS)
    return d


def find_adb():
    for d in base_dirs():
        for p in (os.path.join(d, "platform-tools", "adb.exe"), os.path.join(d, "adb.exe")):
            if os.path.isfile(p):
                return p
    return shutil.which("adb")


ADB = find_adb()


def find_tool(name):
    for d in base_dirs():
        for p in (os.path.join(d, "platform-tools", name + ".exe"), os.path.join(d, name + ".exe")):
            if os.path.isfile(p):
                return p
    return shutil.which(name)


FASTBOOT = find_tool("fastboot")


def fastboot(args, timeout=30):
    if not FASTBOOT:
        return 1, "fastboot not found"
    try:
        r = subprocess.run([FASTBOOT] + args, capture_output=True, text=True, timeout=timeout, creationflags=NOWIN)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)


def adb(args, serial=None, timeout=60):
    if not ADB:
        return 1, "adb not found"
    cmd = [ADB] + (["-s", serial] if serial else []) + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, creationflags=NOWIN)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)


class Windo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("%s %s" % (APP, VERSION))
        self.geometry("1250x720")
        self.configure(bg=BG)
        self.serial = None
        self.brand = None
        self.dev_state, self.category, self.cat_key = None, None, "oppo"
        self.checked = set()
        self.rows = {}
        self.mode = tk.StringVar(value="remove")
        self.show_unknown = tk.BooleanVar(value=False)
        self.search = tk.StringVar()
        self.level_filter = tk.StringVar(value="all")
        self.installed, self.removed, self.third = set(), set(), set()
        self.style_ui()
        self.build_ui()
        self.search.trace_add("write", lambda *a: self.fill())
        self.say(f'Windo database: {len(DB)} apps known, plus pattern rules that label the rest.')
        self.after(200, self.refresh_devices)

    def style_ui(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", background=BG, foreground=FG, fieldbackground=PANEL, font=FONT_UI,
                    bordercolor=EDGE, lightcolor=EDGE, darkcolor=EDGE, focuscolor=BG)
        s.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=FG, rowheight=36, borderwidth=0, font=FONT_NAME)
        s.configure("Treeview.Heading", background=EDGE, foreground=FG, font=("Segoe UI Semibold", 10), relief="flat")
        s.map("Treeview.Heading", background=[("active", GREEN)], foreground=[("active", DARKTXT)])
        # keeps per-row colours working on Tk 8.6.9 (Python 3.8)
        fg_map = [e for e in s.map("Treeview", query_opt="foreground") if e[:2] != ("!disabled", "!selected")]
        s.map("Treeview", foreground=fg_map, background=[("selected", "#2d4a7a")])
        # buttons: dark, turn green on hover (Uninstall turns yellow)
        s.configure("TButton", background=BTN, foreground=FG, bordercolor=BTN, lightcolor=BTN, darkcolor=BTN,
                    focuscolor=BTN, relief="flat", padding=(14, 8), font=("Segoe UI Semibold", 10))
        s.map("TButton", background=[("pressed", GREEN_D), ("active", GREEN)],
              foreground=[("pressed", DARKTXT), ("active", DARKTXT)],
              bordercolor=[("active", GREEN)], lightcolor=[("active", GREEN)], darkcolor=[("active", GREEN)])
        s.configure("Accent.TButton", background=ACC, foreground="white", bordercolor=ACC, lightcolor=ACC,
                    darkcolor=ACC, focuscolor=ACC, padding=(20, 9), font=("Segoe UI Semibold", 11))
        s.map("Accent.TButton", background=[("pressed", YELLOW_D), ("active", YELLOW)],
              foreground=[("pressed", "#2b2200"), ("active", "#2b2200")],
              bordercolor=[("active", YELLOW)], lightcolor=[("active", YELLOW)], darkcolor=[("active", YELLOW)])
        for w in ("TCheckbutton", "TRadiobutton"):
            s.configure(w, background=BG, foreground=FG, font=FONT_UI)
            s.map(w, background=[("active", BG)], foreground=[("active", GREEN)],
                  indicatorcolor=[("selected", GREEN), ("!selected", PANEL)])
        s.configure("TCombobox", fieldbackground=PANEL, background=BTN, foreground=FG, arrowcolor=FG,
                    bordercolor=EDGE, lightcolor=PANEL, darkcolor=PANEL, padding=6)
        s.map("TCombobox", fieldbackground=[("readonly", PANEL)], foreground=[("readonly", FG)],
              selectbackground=[("readonly", PANEL)], selectforeground=[("readonly", FG)],
              background=[("active", GREEN)], arrowcolor=[("active", DARKTXT)])
        self.option_add("*TCombobox*Listbox.background", PANEL)
        self.option_add("*TCombobox*Listbox.foreground", FG)
        self.option_add("*TCombobox*Listbox.selectBackground", GREEN)
        self.option_add("*TCombobox*Listbox.selectForeground", DARKTXT)
        self.option_add("*TCombobox*Listbox.font", FONT_UI)
        s.configure("TEntry", fieldbackground=PANEL, foreground=FG, insertcolor=FG, bordercolor=EDGE,
                    lightcolor=PANEL, darkcolor=PANEL, padding=6)
        s.map("TEntry", bordercolor=[("focus", GREEN)], lightcolor=[("focus", GREEN)], darkcolor=[("focus", GREEN)])
        s.configure("Vertical.TScrollbar", background=BTN, troughcolor=PANEL, bordercolor=PANEL, arrowcolor=FG,
                    lightcolor=BTN, darkcolor=BTN, gripcount=0)
        s.map("Vertical.TScrollbar", background=[("pressed", GREEN_D), ("active", GREEN)],
              lightcolor=[("active", GREEN)], darkcolor=[("active", GREEN)])
        s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 4, 0, 0))
        s.configure("TNotebook.Tab", background=EDGE, foreground=FG, padding=(20, 9), font=("Segoe UI Semibold", 11), borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", GREEN), ("active", YELLOW)],
              foreground=[("selected", DARKTXT), ("active", "#2b2200")])
        s.configure("Big.TButton", padding=(24, 22), font=("Segoe UI Semibold", 15))
        s.configure("BigY.TButton", padding=(24, 22), font=("Segoe UI Semibold", 15))
        s.map("BigY.TButton", background=[("pressed", YELLOW_D), ("active", YELLOW)],
              foreground=[("pressed", "#2b2200"), ("active", "#2b2200")],
              bordercolor=[("active", YELLOW)], lightcolor=[("active", YELLOW)], darkcolor=[("active", YELLOW)])
        s.configure("TLabelframe", background=BG, bordercolor=EDGE)
        s.configure("TLabelframe.Label", background=BG, foreground=GREEN, font=("Segoe UI Semibold", 10))

    def build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)
        tk.Label(top, text=APP, font=("Segoe UI Semibold", 22), bg=BG, fg=GREEN).pack(side="left")
        tk.Label(top, text="Android debloater  v" + VERSION + "  (Debloat + Boot Modes)", font=("Segoe UI", 10), bg=BG, fg="#8a9099").pack(side="left", padx=(10, 0), pady=(10, 0))
        ttk.Button(top, text="Refresh devices", command=self.refresh_devices).pack(side="right")
        self.dev_box = ttk.Combobox(top, state="readonly", width=38)
        self.dev_box.pack(side="right", padx=8)
        self.dev_box.bind("<<ComboboxSelected>>", lambda e: self.select_device())

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10)
        body = ttk.Frame(self.nb)
        self.nb.add(body, text="  Debloat  ")
        self.build_boot_tab()
        left = ttk.LabelFrame(body, text="Device")
        left.pack(side="left", fill="y", padx=(0, 10))
        self.info = tk.Text(left, width=38, bg=PANEL, fg=FG, relief="flat", wrap="word", font=("Consolas", 10))
        self.info.pack(fill="both", expand=True, padx=6, pady=6)

        right = ttk.LabelFrame(body, text="Apps")
        right.pack(side="left", fill="both", expand=True)
        bar = ttk.Frame(right)
        bar.pack(fill="x", padx=6, pady=4)
        ttk.Radiobutton(bar, text="Remove", variable=self.mode, value="remove", command=self.switch_mode).pack(side="left")
        ttk.Radiobutton(bar, text="Restore removed", variable=self.mode, value="restore", command=self.switch_mode).pack(side="left", padx=6)
        ttk.Checkbutton(bar, text="Show other/unknown apps", variable=self.show_unknown, command=self.fill).pack(side="left", padx=6)
        ttk.Combobox(bar, textvariable=self.level_filter, values=["all", "safe", "medium", "high"], width=8, state="readonly").pack(side="right")
        ttk.Label(bar, text="Level:").pack(side="right", padx=4)
        ttk.Entry(bar, textvariable=self.search, width=20).pack(side="right", padx=6)
        self.level_filter.trace_add("write", lambda *a: self.fill())
        leg = ttk.Frame(right)
        leg.pack(fill="x", padx=8)
        for l, txt in (("safe", "Safe"), ("medium", "Medium"), ("high", "High")):
            tk.Label(leg, text="\u25cf", fg=LV[l], bg=BG, font=("Segoe UI", 14)).pack(side="left")
            tk.Label(leg, text=txt, fg=FG, bg=BG, font=FONT_UI).pack(side="left", padx=(0, 14))
        self.count = tk.Label(leg, text="Selected: 0", fg=GREEN, bg=BG, font=("Segoe UI Semibold", 10))
        self.count.pack(side="right")

        cols = ("sel", "name", "pkg", "level")
        wrap = ttk.Frame(right)
        wrap.pack(fill="both", expand=True, padx=6)
        self.tree = ttk.Treeview(wrap, columns=cols, show="tree headings", selectmode="browse")
        self.tree.heading("#0", text="")
        self.tree.column("#0", width=46, minwidth=46, stretch=False, anchor="center")
        for c, t, w in (("sel", "", 40), ("name", "App", 240), ("pkg", "Package", 340), ("level", "Danger", 110)):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w", stretch=(c == "pkg"))
        self.dots = {l: make_dot(col, PANEL) for l, col in LV.items()}
        for l, col in LV.items():
            self.tree.tag_configure(l, foreground=col, font=FONT_NAME)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.desc = tk.Text(right, height=7, bg=PANEL, fg=FG, relief="flat", wrap="word", font=("Segoe UI", 11), padx=8, pady=6)
        self.desc.pack(fill="x", padx=6, pady=6)
        for l, col in LV.items():
            self.desc.tag_configure(l, foreground=col, font=("Segoe UI Semibold", 11))
        self.desc.tag_configure("h", font=("Segoe UI Semibold", 14))

        btns = ttk.Frame(right)
        btns.pack(fill="x", padx=6, pady=(0, 6))
        ttk.Button(btns, text="Select all Safe", command=lambda: self.select_level("safe")).pack(side="left")
        ttk.Button(btns, text="Clear selection", command=self.clear_sel).pack(side="left", padx=6)
        ttk.Button(btns, text="Export unknown apps", command=self.export_unknown).pack(side="left")
        self.act = ttk.Button(btns, text="Uninstall selected", style="Accent.TButton", command=self.apply)
        self.act.pack(side="right")

        self.log = tk.Text(self, height=5, bg="#0e1013", fg="#9aa0a6", relief="flat", font=("Consolas", 9))
        self.log.pack(fill="x", padx=10, pady=8)

    # ---- boot modes tab
    def build_boot_tab(self):
        tab = ttk.Frame(self.nb)
        self.nb.add(tab, text="  Boot Modes  ")
        left = ttk.LabelFrame(tab, text="Brand")
        left.pack(side="left", fill="y", padx=(0, 10), pady=8)
        self.cards = {}
        for c in CATS:
            lab = tk.Label(left, text=c["label"], font=("Segoe UI Semibold", 13), bg=PANEL, fg=FG,
                           width=16, anchor="w", padx=14, pady=10, cursor="hand2")
            lab.pack(fill="x", padx=8, pady=4)
            lab.bind("<Enter>", lambda e, k=c["key"]: self.card_hover(k, True))
            lab.bind("<Leave>", lambda e, k=c["key"]: self.card_hover(k, False))
            lab.bind("<Button-1>", lambda e, k=c["key"]: self.pick_cat(k))
            self.cards[c["key"]] = lab
        right = ttk.LabelFrame(tab, text="Reboot into")
        right.pack(side="left", fill="both", expand=True, pady=8)
        self.cat_title = tk.Label(right, text="", font=("Segoe UI Semibold", 20), bg=BG, fg=GREEN, anchor="w")
        self.cat_title.pack(fill="x", padx=12, pady=(10, 0))
        self.cat_rom = tk.Label(right, text="", font=FONT_UI, bg=BG, fg="#8a9099", anchor="w")
        self.cat_rom.pack(fill="x", padx=12)
        self.boot_dev = tk.Label(right, text="No phone selected. Connect one and press Refresh devices.",
                                 font=FONT_UI, bg=BG, fg=YELLOW, anchor="w")
        self.boot_dev.pack(fill="x", padx=12, pady=(6, 10))
        row = ttk.Frame(right)
        row.pack(fill="x", padx=12)
        self.btn_rec = ttk.Button(row, text="Recovery Mode", style="Big.TButton", command=lambda: self.boot("recovery"))
        self.btn_rec.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.btn_fb = ttk.Button(row, text="Fastboot", style="BigY.TButton", command=lambda: self.boot("fastboot"))
        self.btn_fb.pack(side="left", fill="x", expand=True, padx=(8, 0))
        row2 = ttk.Frame(right)
        row2.pack(fill="x", padx=12, pady=10)
        ttk.Button(row2, text="Reboot to system", command=self.reboot_system).pack(side="left")
        ttk.Button(row2, text="Check fastboot device", command=self.check_fastboot).pack(side="left", padx=8)
        self.fb_status = tk.Label(row2, text="", font=FONT_UI, bg=BG, fg="#8a9099")
        self.fb_status.pack(side="left", padx=8)
        self.keys_box = tk.Text(right, bg=PANEL, fg=FG, relief="flat", wrap="word", font=("Segoe UI", 11),
                                padx=12, pady=10, height=10)
        self.keys_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.keys_box.tag_configure("h", foreground=GREEN, font=("Segoe UI Semibold", 12))
        self.keys_box.tag_configure("w", foreground=YELLOW)
        self.pick_cat(self.cat_key)

    def card_hover(self, key, on):
        if key != self.cat_key:
            self.cards[key].config(bg=GREEN if on else PANEL, fg=DARKTXT if on else FG)

    def pick_cat(self, key):
        self.cat_key = key
        c = CAT_BY_KEY[key]
        for k, lab in self.cards.items():
            sel = k == key
            lab.config(bg=ACC if sel else PANEL, fg="white" if sel else FG)
        self.cat_title.config(text=c["label"])
        self.cat_rom.config(text=c["rom"])
        self.btn_fb.config(text=c["fb_label"])
        t = self.keys_box
        t.config(state="normal")
        t.delete("1.0", "end")
        t.insert("end", "Phone won't boot or USB debugging is off? Enter the modes by hand\n", "h")
        t.insert("end", "Recovery: " + c["rec_keys"] + "\n")
        t.insert("end", c["fb_label"] + ": " + c["fb_keys"] + "\n\n")
        t.insert("end", "Keys can differ slightly by model.\n", "w")
        t.insert("end", c["notes"] + "\n\n")
        t.insert("end", "Windo only reboots the phone into the mode. It does not flash, unlock or wipe anything.", "w")
        t.config(state="disabled")

    def show_detected(self):
        c = CAT_BY_KEY.get(self.category)
        self.boot_dev.config(text="Connected: %s    |    detected: %s" % (self.serial, c["label"] if c else "unknown brand"), fg=GREEN)
        if c:
            self.pick_cat(c["key"])

    def boot(self, mode):
        if not self.serial or self.dev_state != "device":
            return messagebox.showwarning(APP, "Connect a phone with USB debugging on and press Refresh devices first.")
        cat = CAT_BY_KEY[self.cat_key]
        det = self.category
        same_family = det and {det, cat["key"]} <= {"xiaomi", "poco"}
        if det and det != cat["key"] and not same_family:
            if not messagebox.askyesno(APP, "The connected phone looks like %s, but you selected %s.\n"
                                       "The command may not work. Continue?" % (CAT_BY_KEY[det]["label"], cat["label"]), icon="warning"):
                return
        cmd = cat["rec_cmd"] if mode == "recovery" else cat["fb_cmd"]
        name = "Recovery Mode" if mode == "recovery" else cat["fb_label"]
        if not messagebox.askyesno(APP, "Reboot the phone into %s?\nNothing is flashed or wiped by Windo." % name):
            return
        def work():
            _, out = adb(cmd, self.serial)
            self.ui(lambda: self.say("%s: adb %s -> %s" % (name, " ".join(cmd), out or "sent. Press Refresh devices when the phone is back.")))
            if mode == "fastboot" and cat["key"] != "samsung":
                self.ui(lambda: self.after(7000, self.check_fastboot))
        self.bg(work)

    def reboot_system(self):
        def work():
            if self.serial and self.dev_state == "device":
                cmd = "adb reboot"
                _, out = adb(["reboot"], self.serial)
            else:
                cmd = "fastboot reboot"
                _, out = fastboot(["reboot"])
            self.ui(lambda: self.say("%s: %s" % (cmd, out or "sent")))
        self.bg(work)

    def check_fastboot(self):
        def work():
            if not FASTBOOT:
                self.ui(lambda: messagebox.showerror(APP, "fastboot.exe not found.\nPut the 'platform-tools' folder next to Windo.exe."))
                return
            _, out = fastboot(["devices"])
            devs = [l.split()[0] for l in out.splitlines() if l.split() and "fastboot" in l.lower()]
            if devs:
                txt, col = "Fastboot device: %s" % devs[0], GREEN
            else:
                txt, col = "No fastboot device found. Put the phone in fastboot mode first.", YELLOW
            self.ui(lambda: (self.fb_status.config(text=txt, fg=col), self.say("fastboot devices: " + (out or "(none)"))))
        self.bg(work)

    # ---- helpers
    def say(self, m):
        self.log.insert("end", m + "\n")
        self.log.see("end")

    def bg(self, fn):
        threading.Thread(target=fn, daemon=True).start()

    def ui(self, fn):
        self.after(0, fn)

    # ---- devices
    def refresh_devices(self):
        if not ADB:
            messagebox.showerror(APP, "adb.exe not found.\nPut the 'platform-tools' folder next to Windo.exe.")
            return
        def work():
            adb(["start-server"])
            _, out = adb(["devices", "-l"])
            devs = []
            for ln in out.splitlines()[1:]:
                p = ln.split()
                if len(p) >= 2 and not ln.startswith("*"):
                    devs.append((p[0], p[1]))
            self.ui(lambda: self.set_devices(devs))
        self.bg(work)

    def set_devices(self, devs):
        self.devs = devs
        self.dev_box["values"] = [f"{s}  [{st}]" for s, st in devs]
        if not devs:
            self.info.delete("1.0", "end")
            self.info.insert("end", "No device found.\n\n1. Enable Developer options\n2. Enable USB debugging\n3. Plug in USB, choose File transfer\n4. Accept the RSA prompt on the phone\n5. Press Refresh devices")
            return
        self.dev_box.current(0)
        self.select_device()

    def select_device(self):
        i = self.dev_box.current()
        serial, state = self.devs[i]
        self.serial = serial
        self.dev_state = state
        if state != "device":
            self.info.delete("1.0", "end")
            self.info.insert("end", f"Device state: {state}\nUnlock the phone and accept the USB debugging prompt, then refresh.")
            return
        def work():
            lines, props = [], {}
            for label, prop in PROPS:
                _, v = adb(["shell", "getprop", prop], serial)
                if v.strip():
                    props[prop] = v.strip()
                    lines.append(f"{label}: {v.strip()}")
            self.brand = detect_brand(props.get("ro.product.manufacturer", ""), props.get("ro.product.brand", ""), props.get("ro.product.model", ""))
            lines.append("ROM family: " + FAMILY_NAMES.get(self.brand, "Unknown (showing every known app)"))
            self.category = detect_category(props.get("ro.product.manufacturer", ""), props.get("ro.product.brand", ""), props.get("ro.product.model", ""))
            self.ui(self.show_detected)
            _, sz = adb(["shell", "wm", "size"], serial)
            _, bat = adb(["shell", "dumpsys", "battery"], serial)
            level = next((l.split(":")[1].strip() for l in bat.splitlines() if l.strip().startswith("level")), "?")
            lines.append(f"Screen: {sz.split(':')[-1].strip()}")
            lines.append(f"Battery: {level}%")
            lines.append(f"Serial: {serial}")
            self.ui(lambda: (self.info.delete("1.0", "end"), self.info.insert("end", "\n".join(lines))))
            self.load_packages()
        self.bg(work)

    def load_packages(self):
        def parse(o):
            return {l.split(":", 1)[1].strip() for l in o.splitlines() if l.startswith("package:")}
        _, a = adb(["shell", "pm", "list", "packages", "--user", "0"], self.serial)
        _, b = adb(["shell", "pm", "list", "packages", "-u", "--user", "0"], self.serial)
        self.installed, allp = parse(a), parse(b)
        self.removed = allp - self.installed
        _, c = adb(["shell", "pm", "list", "packages", "-3", "--user", "0"], self.serial)
        self.third = parse(c)
        self.ui(self.fill)
        self.ui(lambda: self.say(f"Found {len(self.installed)} installed apps, {sum(1 for p in self.installed if relevant(p, self.brand))} recognised by Windo."))

    # ---- list
    def app_info(self, p):
        if p in DB:
            n, l, w, e = DB[p]
            return n, l, w, e, "known"
        return classify(p, p in self.third)

    def export_unknown(self):
        unk = sorted(p for p in self.installed if p not in DB)
        if not unk:
            return messagebox.showinfo(APP, "Every installed app is already in Windo's database.")
        path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "windo_unknown_apps.txt")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(unk))
            messagebox.showinfo(APP, "Saved %d unknown package names to:\n%s" % (len(unk), path))
        except OSError as e:
            messagebox.showerror(APP, str(e))

    def pool(self):
        return self.installed if self.mode.get() == "remove" else self.removed

    def fill(self):
        self.tree.delete(*self.tree.get_children())
        q = self.search.get().lower()
        lf = self.level_filter.get()
        items = []
        for p in self.pool():
            name, lvl, _, _, kind = self.app_info(p)
            known = relevant(p, self.brand)
            if not known and not (self.show_unknown.get() or self.mode.get() == "restore"):
                continue
            if lf != "all" and lvl != lf:
                continue
            if q and q not in name.lower() and q not in p.lower():
                continue
            items.append((["safe", "medium", "high"].index(lvl), name.lower(), p, name, lvl, known, kind))
        for _, _, p, name, lvl, known, kind in sorted(items):
            box = "\u2611" if p in self.checked else "\u2610"
            self.tree.insert("", "end", iid=p, values=(box, name, p, lvl.upper() if kind == "known" else "%s (%s)" % (lvl.upper(), kind.upper())), tags=(lvl,), image=self.dots[lvl])
        self.count.config(text="Selected: %d" % len(self.checked))

    def on_click(self, e):
        if self.tree.identify_region(e.x, e.y) != "cell" or self.tree.identify_column(e.x) != "#1":
            return
        r = self.tree.identify_row(e.y)
        if r:
            self.checked.symmetric_difference_update({r})
            self.count.config(text="Selected: %d" % len(self.checked))
            self.tree.set(r, "sel", "\u2611" if r in self.checked else "\u2610")

    def on_select(self, e):
        s = self.tree.selection()
        if not s:
            return
        p = s[0]
        self.desc.delete("1.0", "end")
        n, l, what, res, kind = self.app_info(p)
        self.desc.insert("end", f"{n}  ", ("h", l))
        self.desc.insert("end", f"[{l.upper()}]\n", l)
        self.desc.insert("end", f"What it is: {what}\n", ())
        self.desc.insert("end", f"If removed: {res}\n")
        self.desc.insert("end", p + ("" if kind == "known" else "   (guessed from the package name)"))

    def select_level(self, lvl):
        for p in self.pool():
            if relevant(p, self.brand) and DB[p][1] == lvl:
                self.checked.add(p)
        self.fill()

    def clear_sel(self):
        self.checked.clear()
        self.fill()

    def switch_mode(self):
        self.checked.clear()
        self.act.config(text="Uninstall selected" if self.mode.get() == "remove" else "Restore selected")
        self.fill()

    # ---- apply
    def apply(self):
        if not self.serial:
            return messagebox.showwarning(APP, "No device selected.")
        sel = [p for p in self.checked if p in self.pool()]
        if not sel:
            return messagebox.showinfo(APP, "Nothing selected.")
        remove = self.mode.get() == "remove"
        risky = [p for p in sel if self.app_info(p)[1] == "high"]
        msg = f"{'Uninstall' if remove else 'Restore'} {len(sel)} app(s)?"
        if remove and risky:
            msg += f"\n\nWARNING: {len(risky)} are HIGH danger/unknown and may break your phone:\n" + "\n".join(risky[:8])
        if not messagebox.askyesno(APP, msg, icon="warning" if risky else "question"):
            return
        def work():
            for p in sel:
                if remove:
                    _, o = adb(["shell", "pm", "uninstall", "-k", "--user", "0", p], self.serial)
                else:
                    _, o = adb(["shell", "cmd", "package", "install-existing", p], self.serial)
                self.ui(lambda p=p, o=o: self.say(f"{p}: {o}"))
            self.checked.clear()
            self.load_packages()
        self.bg(work)


if __name__ == "__main__":
    Windo().mainloop()
