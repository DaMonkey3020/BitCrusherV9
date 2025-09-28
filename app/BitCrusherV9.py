
import io
import sys
import json
import logging
import math
import os
import platform
import re
import shutil
import subprocess
import tempfile
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path
from tkinterdnd2 import TkinterDnD, DND_FILES
from ui_aesthetics import init_aesthetics, animated_retheme, open_theme_lab
from ui_aesthetics import init_aesthetics, open_theme_lab, animated_retheme
import yt_dlp
import tempfile
import queue
import webbrowser

import numpy as np
import psutil
import requests
from PIL import Image, ImageTk
from plyer import notification
from win10toast import ToastNotifier
from datetime import datetime
import argparse
from glob import glob

try:
    os.makedirs("logs", exist_ok=True)
except Exception:
    pass
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(os.path.join("logs", "bitcrusher.log"),
                            encoding="utf-8",
                            mode="a")
    ]
)


import sys, os, traceback

def resource_path(rel_path: str) -> str:
    
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


_BOOT_PHASE = True  # only show popup during true startup failures

def _install_crash_handler():

    try:
        os.makedirs("logs", exist_ok=True)
    except Exception:
        pass

    def _hook(exctype, value, tb):

        try:
            with open(os.path.join("logs", "startup_error.log"), "w", encoding="utf-8") as f:
                import traceback as _tb
                _tb.print_exception(exctype, value, tb, file=f)
        except Exception:
            pass

        try:
            if _BOOT_PHASE:
                from tkinter import Tk, messagebox as mbox
                root = Tk(); root.withdraw()
                mbox.showerror("BitCrusher crashed", "See logs/startup_error.log for details.")
                root.destroy()
        except Exception:
            pass

    sys.excepthook = _hook

_install_crash_handler()




print("[DEBUG] top of file reached")

def _ui_json_path():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        base = os.getcwd()
    p = os.path.join(base, "user_settings")
    os.makedirs(p, exist_ok=True)
    return os.path.join(p, "ui.json")

import os, sys, json, subprocess

def _i18n_dir():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        base = os.getcwd()
    d = os.path.join(base, "user_settings", "i18n")
    os.makedirs(d, exist_ok=True)
    return d

def _open_folder(path: str):
    try:
        if os.name == "nt":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass

LANG_BUILTIN = {
    "en": {
        "menu_language": "Language",
        "menu.file":"File","menu.settings":"Settings","menu.themes":"Themes","menu.guide":"Guide","menu.view":"View",
        "menu.exit":"Exit","menu.configure_paths":"Configure Paths","menu.save_profile":"Save Profile","menu.load_profile":"Load Profile",
        "menu.clear_queue":"Clear Queue","menu.dashboard":"Dashboard","menu.user_guide":"User Guide",
        "menu.theme_lab":"Theme Lab…","menu.save_theme":"Save Current Theme…","menu.load_theme":"Load Theme JSON…",
        "menu.open_i18n_folder":"Open i18n Folder…","menu.export_lang_templates":"Export Language Templates…",

        "lbl.preset":"Preset:","lbl.target_size":"Target Size (MB):","lbl.queue":"Queue","lbl.preview":"Preview",
        "lbl.save_to":"Save to:",
        "panel.webhook":"Webhook","lbl.webhook_url":"Discord/Webhook URL",
        "panel.watcher":"Folder Watcher","lbl.enable_watcher":"Enable watcher","panel.profiles":"Profiles",
        "panel.advanced":"Advanced Options",
        "lbl.encoder":"Encoder:","lbl.manual_crf":"Manual CRF:","lbl.prefix":"Prefix:","lbl.audio":"Audio:",

        "btn.add_files":"Add Files…","btn.remove_selected":"Remove Selected","btn.remove":"Remove Selected","btn.clear":"Clear",
        "btn.move_up":"Move ↑","btn.move_down":"Move ↓",
        "btn.start":"Start Compression","btn.stop":"Stop","btn.open_save":"Open Save Folder",
        "btn.user_guide":"User Guide","btn.browse":"Browse…","btn.save":"Save","btn.load":"Load",

        "title.open_save_folder":"Open Save Folder","title.cancel":"Cancel",

        "unreal.title": "Unrealistic target size",
        "unreal.header": "Requested size is too small for acceptable quality.",
        "unreal.original": "Original","unreal.target": "Target",
        "unreal.why": "Why this breaks quality:",
        "unreal.why.v": "• Video bitrate plummets → blocky macro-artifacts & smearing",
        "unreal.why.a": "• Audio starved of bits → metallic/warbly sound",
        "unreal.why.m": "• High motion or film grain needs more bits than static scenes",
        "unreal.better": "Better options:",
        "unreal.opt.aim": "• Aim for 10–20% of the original size (not 1–2%)",
        "unreal.opt.scale": "• Downscale resolution and/or reduce frame rate",
        "unreal.opt.codec": "• Use HEVC (x265) or AV1 with a sensible CRF",
    }
}

LANG_BUILTIN.update({
    "es": { "menu_language":"Idioma","menu.file":"Archivo","menu.settings":"Ajustes","menu.themes":"Temas","menu.guide":"Guía","menu.view":"Vista",
            "menu.exit":"Salir","menu.configure_paths":"Configurar rutas","menu.save_profile":"Guardar perfil","menu.load_profile":"Cargar perfil",
            "menu.clear_queue":"Vaciar cola","menu.dashboard":"Panel","menu.user_guide":"Guía del usuario",
            "menu.theme_lab":"Laboratorio de temas…","menu.save_theme":"Guardar tema actual…","menu.load_theme":"Cargar tema JSON…",
            "menu.open_i18n_folder":"Abrir carpeta i18n…","menu.export_lang_templates":"Exportar plantillas de idioma…",
            "lbl.preset":"Preajuste:","lbl.target_size":"Tamaño objetivo (MB):","lbl.queue":"Cola","lbl.preview":"Vista previa","lbl.save_to":"Guardar en:",
            "panel.webhook":"Webhook","lbl.webhook_url":"URL de Discord/Webhook","panel.watcher":"Monitor de carpeta","lbl.enable_watcher":"Activar monitor",
            "panel.profiles":"Perfiles","panel.advanced":"Opciones avanzadas","lbl.encoder":"Codificador:","lbl.manual_crf":"CRF manual:",
            "lbl.prefix":"Prefijo:","lbl.audio":"Audio:","btn.add_files":"Añadir archivos…","btn.remove_selected":"Eliminar seleccionados",
            "btn.clear":"Limpiar","btn.move_up":"Mover ↑","btn.move_down":"Mover ↓","btn.start":"Comenzar compresión","btn.stop":"Detener",
            "btn.open_save":"Abrir carpeta de salida","btn.user_guide":"Guía de usuario","btn.browse":"Examinar…","btn.save":"Guardar","btn.load":"Cargar",
            "title.open_save_folder":"Abrir carpeta de salida","title.cancel":"Cancelar",
            "unreal.title":"Tamaño objetivo irreal","unreal.header":"El tamaño solicitado es demasiado pequeño para una calidad aceptable.",
            "unreal.original":"Original","unreal.target":"Objetivo","unreal.why":"Por qué arruina la calidad:",
            "unreal.why.v":"• El bitrate de vídeo cae → bloques y manchas","unreal.why.a":"• Pocos bits para el audio → sonido metálico/robótico",
            "unreal.why.m":"• Mucho movimiento o grano requiere más bits","unreal.better":"Opciones mejores:",
            "unreal.opt.aim":"• Apunta al 10–20% del original (no 1–2%)","unreal.opt.scale":"• Reduce resolución y/o fotogramas",
            "unreal.opt.codec":"• Usa HEVC (x265) o AV1 con CRF razonable"},
    "fr": { "menu_language":"Langue","menu.file":"Fichier","menu.settings":"Paramètres","menu.themes":"Thèmes","menu.guide":"Guide","menu.view":"Affichage" },
    "de": { "menu_language":"Sprache","menu.file":"Datei","menu.settings":"Einstellungen","menu.themes":"Themen","menu.guide":"Anleitung","menu.view":"Ansicht" },
    "pt": { "menu_language":"Idioma","menu.file":"Arquivo","menu.settings":"Ajustes","menu.themes":"Temas","menu.guide":"Guia","menu.view":"Exibir" },
    "it": { "menu_language":"Lingua","menu.file":"File","menu.settings":"Impostazioni","menu.themes":"Temi","menu.guide":"Guida","menu.view":"Vista" },
    "nl": { "menu_language":"Taal","menu.file":"Bestand","menu.settings":"Instellingen","menu.themes":"Thema's","menu.guide":"Handleiding","menu.view":"Beeld" },
    "pl": { "menu_language":"Język","menu.file":"Plik","menu.settings":"Ustawienia","menu.themes":"Motywy","menu.guide":"Przewodnik","menu.view":"Widok" },
    "tr": { "menu_language":"Dil","menu.file":"Dosya","menu.settings":"Ayarlar","menu.themes":"Temalar","menu.guide":"Kılavuz","menu.view":"Görünüm" },
    "ru": { "menu_language":"Язык","menu.file":"Файл","menu.settings":"Настройки","menu.themes":"Темы","menu.guide":"Справка","menu.view":"Вид" },
    "uk": { "menu_language":"Мова","menu.file":"Файл","menu.settings":"Налаштування","menu.themes":"Теми","menu.guide":"Довідник","menu.view":"Вигляд" },
    "ar": { "menu_language":"اللغة","menu.file":"ملف","menu.settings":"الإعدادات","menu.themes":"الثيمات","menu.guide":"الدليل","menu.view":"عرض" },
    "he": { "menu_language":"שפה","menu.file":"קובץ","menu.settings":"הגדרות","menu.themes":"ערכות נושא","menu.guide":"מדריך","menu.view":"תצוגה" },
    "fa": { "menu_language":"زبان","menu.file":"فایل","menu.settings":"تنظیمات","menu.themes":"تم‌ها","menu.guide":"راهنما","menu.view":"نمایش" },
    "hi": { "menu_language":"भाषा","menu.file":"फ़ाइल","menu.settings":"सेटिंग्स","menu.themes":"थीम्स","menu.guide":"मार्गदर्शिका","menu.view":"दृश्य" },
    "bn": { "menu_language":"ভাষা","menu.file":"ফাইল","menu.settings":"সেটিংস","menu.themes":"থিম","menu.guide":"গাইড","menu.view":"ভিউ" },
    "id": { "menu_language":"Bahasa","menu.file":"Berkas","menu.settings":"Pengaturan","menu.themes":"Tema","menu.guide":"Panduan","menu.view":"Tampilan" },
    "ms": { "menu_language":"Bahasa","menu.file":"Fail","menu.settings":"Tetapan","menu.themes":"Tema","menu.guide":"Panduan","menu.view":"Paparan" },
    "vi": { "menu_language":"Ngôn ngữ","menu.file":"Tệp","menu.settings":"Cài đặt","menu.themes":"Chủ đề","menu.guide":"Hướng dẫn","menu.view":"Xem" },
    "th": { "menu_language":"ภาษา","menu.file":"ไฟล์","menu.settings":"การตั้งค่า","menu.themes":"ธีม","menu.guide":"คู่มือ","menu.view":"มุมมอง" },
    "ja": { "menu_language":"言語","menu.file":"ファイル","menu.settings":"設定","menu.themes":"テーマ","menu.guide":"ガイド","menu.view":"表示" },
    "ko": { "menu_language":"언어","menu.file":"파일","menu.settings":"설정","menu.themes":"테마","menu.guide":"가이드","menu.view":"보기" },
    "zh": { "menu_language":"语言","menu.file":"文件","menu.settings":"设置","menu.themes":"主题","menu.guide":"指南","menu.view":"视图" },
    "zh_TW": { "menu_language":"語言","menu.file":"檔案","menu.settings":"設定","menu.themes":"主題","menu.guide":"指南","menu.view":"檢視" },
})

LANG_CODES = [
    ("en","English"),("es","Español"),("fr","Français"),("de","Deutsch"),("pt","Português"),
    ("it","Italiano"),("nl","Nederlands"),("pl","Polski"),("tr","Türkçe"),("ru","Русский"),
    ("uk","Українська"),("ar","العربية"),("he","עברית"),("fa","فارسی"),("hi","हिन्दी"),
    ("bn","বাংলা"),("id","Bahasa Indonesia"),("ms","Bahasa Melayu"),("vi","Tiếng Việt"),("th","ไทย"),
    ("ja","日本語"),("ko","한국어"),("zh","中文(简体)"),("zh_TW","中文(繁體)")
]

LANG = {}

def _load_language_choice(default_code: str = "en") -> str:
    path = _ui_json_path()
    try:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
            v = data.get("language")
            if isinstance(v, str) and v:
                return v
    except Exception:
        pass
    return str(default_code or "en")

def _save_language_choice(code: str) -> None:
    path = _ui_json_path()
    try:
        data = {}
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        if not isinstance(data, dict):
            data = {}
        data["language"] = str(code or "en")
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        pass

def _export_lang_templates(codes=None):
    
    if not codes:
        codes = [c for c,_ in LANG_CODES if c != "en"]
    base = LANG_BUILTIN["en"]
    outdir = _i18n_dir()
    for code in codes:
        try:
            path = os.path.join(outdir, f"{code}.json")
            if not os.path.isfile(path):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(base, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

def _load_lang_packs():
    
    LANG.clear()
    LANG.update(LANG_BUILTIN)  # always include built-ins
    d = _i18n_dir()
    try:
        for fn in os.listdir(d):
            if not fn.lower().endswith(".json"):
                continue
            code = os.path.splitext(fn)[0]
            with open(os.path.join(d, fn), "r", encoding="utf-8") as f:
                pack = json.load(f) or {}
            if isinstance(pack, dict):
                LANG[code] = pack
    except Exception:
        pass



def _save_theme_choice(name: str) -> None:
    
    path = _ui_json_path()
    try:
        data = {}
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        if not isinstance(data, dict):
            data = {}
        data["theme"] = str(name)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except Exception:

        pass

def _load_theme_choice(default_name: str = "Dark") -> str:
    
    path = _ui_json_path()
    try:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
            v = data.get("theme")
            if isinstance(v, str) and v:
                return v
    except Exception:
        pass
    return str(default_name or "Dark")

import os, sys, time, platform, traceback, logging, threading, subprocess
from logging.handlers import RotatingFileHandler
from smart_rate import choose_bitrates, learn_from_result, guardrail_adjust

def _ensure_dir(p):
    try: os.makedirs(p, exist_ok=True)
    except Exception: pass
    return p

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_LOG_DIR = _ensure_dir(os.path.join(_SCRIPT_DIR, "logs"))

def _mk_logger():
    level_name = os.environ.get("BITCRUSHER_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logger = logging.getLogger("BitCrusher")
    logger.setLevel(level)
    logger.propagate = False

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fh = logging.handlers.RotatingFileHandler(os.path.join("logs", "bitcrusher.log"),
                                              maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(level)
    logger.addHandler(fh)

    if os.environ.get("BITCRUSHER_LOG_CONSOLE", "0") == "1":
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        ch.setLevel(level)
        logger.addHandler(ch)

    return logger


LOG = _mk_logger()

class _WPARAMFilter(logging.Filter):
    def filter(self, record):
        msg = str(record.getMessage())
        return False if "WPARAM is simple" in msg else True

try:
    LOG.addFilter(_WPARAMFilter())
except Exception:
    pass


def _log_env_banner():
    try:
        LOG.info("======== BitCrusher start ========")
        LOG.info("Python: %s", sys.version.replace("\n", " "))
        LOG.info("Platform: %s %s (%s)", platform.system(), platform.release(), platform.machine())
        LOG.info("Executable: %s", sys.executable)
        LOG.info("CWD: %s", os.getcwd())
        def _first_line(cmd):
            try:
                p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, timeout=4)
                out = (p.stdout or "").splitlines()
                return out[0] if out else ""
            except Exception:
                return ""
        for tool in ("HandBrakeCLI", "ffmpeg", "ffprobe"):
            v = _first_line([tool, "-h"]) or _first_line([tool, "-version"])
            if v:
                LOG.info("%s: %s", tool, v)
    except Exception:
        LOG.exception("Failed to log environment banner")

_log_env_banner()

def _format_exc(exc_type, exc, tb):
    return "".join(traceback.format_exception(exc_type, exc, tb))

def _excepthook(exc_type, exc, tb):
    if exc_type is TypeError and "WPARAM is simple" in str(exc):

        LOG.debug("Suppressed benign WPARAM TypeError")
        return
    LOG.critical("UNHANDLED EXCEPTION\n%s", _format_exc(exc_type, exc, tb))
    try:
        sys.__excepthook__(exc_type, exc, tb)
    except Exception:
        pass

sys.excepthook = _excepthook


def _thread_excepthook(args):
    try:
        name = getattr(args.thread, "name", "") or ""
        msg  = str(getattr(args, "exc_value", ""))

        if ("_show_toast" in name) or ("win10toast" in (getattr(args.thread, "__module__", "") or "")) \
           or ("Shell_NotifyIcon" in msg) or ("DestroyWindow" in msg) \
           or ("WPARAM is simple" in msg):
            LOG.debug("Suppressed toast/thread noise: %s | %s", name, msg)
            return

        LOG.critical(
            "UNHANDLED THREAD EXCEPTION (name=%s)\n%s",
            name,
            _format_exc(args.exc_type, args.exc_value, args.exc_traceback),
        )
    except Exception:
        pass


def _patch_tk_report_callback_exception():
    try:
        import tkinter as _tk
        _orig = _tk.Tk.report_callback_exception
        def _report(self, exc, val, tb):
            try:
                if exc is TypeError and "WPARAM is simple" in str(val):
                    LOG.debug("Suppressed benign WPARAM TypeError in Tk callback")
                    return
                LOG.error("Tkinter callback exception\n%s", _format_exc(exc, val, tb))
            except Exception:
                pass
            try:
                return _orig(self, exc, val, tb)
            except Exception:
                pass
            except Exception:
                pass
        _tk.Tk.report_callback_exception = _report
    except Exception:
        LOG.debug("Tkinter not available or already patched", exc_info=True)

_patch_tk_report_callback_exception()

_orig_run = subprocess.run
_orig_check_output = subprocess.check_output

def _render_cmd(cmd):
    try:
        return " ".join(str(c) for c in cmd)
    except Exception:
        return repr(cmd)

def _tail(txt, n=80):
    try:
        lines = (txt or "").splitlines()
        if len(lines) <= n: return txt or ""
        return "\n".join(lines[-n:])
    except Exception:
        return txt or ""

def _run_logged(cmd, *args, **kwargs):
    t0 = time.time()
    text_mode = kwargs.get("text", False)
    capture = (kwargs.get("stdout") is subprocess.PIPE
               or kwargs.get("stderr") is subprocess.PIPE
               or kwargs.get("capture_output") is True
               or text_mode)
    try:
        res = _orig_run(cmd, *args, **kwargs)
    except Exception as e:
        LOG.error("subprocess.run raised exception for: %s\n%s", _render_cmd(cmd), repr(e))
        raise
    dt = time.time() - t0
    try:
        LOG.debug("CMD: %s", _render_cmd(cmd))
        LOG.debug("RET: %s in %.2fs", res.returncode, dt)
        if capture:
            if hasattr(res, "stdout") and res.stdout:
                LOG.debug("STDOUT (tail):\n%s", _tail(res.stdout if isinstance(res.stdout, str)
                                                     else res.stdout.decode("utf-8", "ignore"), 50))
            if hasattr(res, "stderr") and res.stderr:
                LOG.debug("STDERR (tail):\n%s", _tail(res.stderr if isinstance(res.stderr, str)
                                                     else res.stderr.decode("utf-8", "ignore"), 120))
        if res.returncode != 0:
            LOG.error("Command failed (rc=%s): %s", res.returncode, _render_cmd(cmd))
    except Exception:
        pass
    return res

def _check_output_logged(cmd, *args, **kwargs):
    t0 = time.time()
    try:
        out = _orig_check_output(cmd, *args, **kwargs)
        LOG.debug("CHECK_OUTPUT OK (%.2fs): %s", time.time() - t0, _render_cmd(cmd))
        return out
    except subprocess.CalledProcessError as e:
        so = getattr(e, 'stdout', b'')
        se = getattr(e, 'stderr', b'')
        try:
            so = so if isinstance(so, str) else so.decode('utf-8', 'ignore')
        except Exception:
            so = ""
        try:
            se = se if isinstance(se, str) else se.decode('utf-8', 'ignore')
        except Exception:
            se = ""
        LOG.error("CHECK_OUTPUT FAILED (rc=%s) for: %s\nSTDOUT tail:\n%s\nSTDERR tail:\n%s",
                  e.returncode, _render_cmd(cmd), _tail(so, 60), _tail(se, 120))
        raise
    except Exception as e:
        LOG.error("CHECK_OUTPUT EXCEPTION for: %s\n%s", _render_cmd(cmd), repr(e))
        raise

subprocess.run = _run_logged
subprocess.check_output = _check_output_logged

def bridge_gui_logger(widget):
    
    class _TkHandler(logging.Handler):
        def emit(self, record):
            try:
                msg = self.format(record)
                widget.configure(state="normal")
                widget.insert("end", msg + "\n")
                widget.see("end")
                widget.configure(state="disabled")
            except Exception:
                pass
    h = _TkHandler()
    h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S"))
    h.setLevel(logging.INFO)
    LOG.addHandler(h)
    return h

def log_info(msg): LOG.info(msg)
def log_warn(msg): LOG.warning(msg)
def log_err(msg): LOG.error(msg)
def log_exc(msg="Unhandled exception"): LOG.exception(msg)

def log_tool_paths(handbrake, ffmpeg, ffprobe):
    LOG.info("Tool paths — HandBrakeCLI=%s | ffmpeg=%s | ffprobe=%s", handbrake, ffmpeg, ffprobe)

class DiscordWebhookClient:
    def __init__(self, url: str | None = None, name: str = "BitCrusher"):
        self._url = (url or "").strip()
        self._name = name
        self._q = queue.Queue()
        self._stop = threading.Event()
        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    def set_url(self, url: str | None):
        self._url = (url or "").strip()

    def close(self):
        self._stop.set()
        try: self._q.put_nowait(None)
        except Exception: pass

    def send_text(self, content: str, username: str | None = None):
        if not self._url or not content: return
        self._q.put(("text", {"content": str(content)[:1900], "username": username or self._name}))

    def send_file(self, path: str, description: str = "", username: str | None = None):
        if not self._url or not os.path.isfile(path): return
        self._q.put(("file", {"path": path, "description": description, "username": username or self._name}))

    def _loop(self):
        s = requests.Session()
        while not self._stop.is_set():
            try:
                item = self._q.get(timeout=0.5)
            except Exception:
                continue
            if item is None: break
            kind, payload = item
            try:
                self._send_one(s, kind, payload)
            except Exception as e:
                LOG.warning("Webhook send failed: %r", e)

    def _send_one(self, s: requests.Session, kind: str, payload: dict):
        url = self._url
        if not url: return
        backoff = 1.0
        for attempt in range(5):
            try:
                if kind == "text":
                    data = {"content": payload["content"], "username": payload.get("username", self._name)}
                    r = s.post(url, json=data, timeout=10)
                else:
                    p = payload["path"]

                    if os.path.getsize(p) > 25 * 1024 * 1024:
                        msg = f'{payload.get("description","")}\n`{os.path.basename(p)}` too large to attach ({os.path.getsize(p)} bytes).'
                        r = s.post(url, json={"content": msg, "username": payload.get("username", self._name)}, timeout=10)
                    else:
                        with open(p, "rb") as f:
                            files = {"files[0]": (os.path.basename(p), f)}
                            data = {"content": payload.get("description",""), "username": payload.get("username", self._name)}
                            r = s.post(url, data=data, files=files, timeout=20)

                if r.status_code == 429:
                    wait = float(r.json().get("retry_after", 1.0))
                    time.sleep(max(1.0, wait))
                    continue
                if 200 <= r.status_code < 300:
                    return

                if r.status_code in (500, 502, 503, 504):
                    time.sleep(backoff); backoff = min(8.0, backoff * 2.0); continue

                LOG.warning("Webhook HTTP %s: %s", r.status_code, r.text[:200])
                return
            except requests.RequestException as e:
                time.sleep(backoff); backoff = min(8.0, backoff * 2.0)
            except Exception:
                return

def bridge_gui_logger_color(widget):
    

    try:
        widget.tag_configure("INFO",    foreground=FG)
        widget.tag_configure("DEBUG",   foreground="#7aa2f7")
        widget.tag_configure("WARNING", foreground=WARN)
        widget.tag_configure("ERROR",   foreground=ERROR)
        widget.tag_configure("CRITICAL",foreground="#ffffff", background="#b00020")
        widget.configure(background=_hsl_shift(CARD_BG, l_mul=0.98), fg=FG, insertbackground=FG)
    except Exception:
        pass

    class _TkColorHandler(logging.Handler):
        def emit(self, record):
            try:
                msg = self.format(record)
                lvl = record.levelname.upper()
                widget.configure(state="normal")
                widget.insert("end", msg + "\n", (lvl,))
                widget.see("end")
                widget.configure(state="disabled")
            except Exception:
                pass

    h = _TkColorHandler()
    h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S"))
    h.setLevel(logging.INFO)
    LOG.addHandler(h)
    return h

_TOASTER = None
def notify_info(title, msg, duration=3):
    
    global _TOASTER
    try:
        from win10toast import ToastNotifier
        if _TOASTER is None:
            _TOASTER = ToastNotifier()
        _TOASTER.show_toast(str(title or "BitCrusher"),
                            str(msg or ""),
                            duration=int(duration or 3),
                            threaded=True,
                            icon_path=None)
    except Exception as e:
        try:
            LOG.warning(f"Toast suppressed: {e} | {title}: {msg}")
        except Exception:
            pass

def notify_warn(title, msg, duration=4):
    notify_info(title, msg, duration)

def notify_error(title, msg, duration=5):
    try:
        notify_info(title, msg, duration)
    except Exception:
        pass
    try:
        LOG.error(str(msg))
    except Exception:
        pass




def _bin_ok(bin_path, args=("-version",)):
    try:
        p = subprocess.run([bin_path, *args], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, startupinfo=si, creationflags=NO_WIN)
        return p.returncode == 0
    except Exception:
        return False

import csv as _csv
import math
import threading as _th

class EnsembleRegressor:
    
    def __init__(self, gb=None, alpha=0.5, w=None, b=0.0, mu=None, sigma=None, clip=(16,40)):
        self.gb = gb  # may be None
        self.alpha = float(alpha)
        self.w = None if w is None else np.asarray(w, dtype=float).copy()
        self.b = float(b or 0.0)
        self.mu = None if mu is None else np.asarray(mu, dtype=float).copy()
        self.sigma = None if sigma is None else np.asarray(sigma, dtype=float).copy()
        self.clip = tuple(clip or (16,40))

    def _phi(self, X):

        X = np.asarray(X, dtype=float)
        if X.ndim == 1: X = X.reshape(1,-1)
        n, d = X.shape
        k = min(d, 6)
        feats = [X, X*X, np.log1p(np.abs(X))]

        pair = []
        if k >= 2:
            for i in range(k):
                for j in range(i+1, k):
                    pair.append((X[:,i] * X[:,j]).reshape(n,1))
        if pair:
            feats.append(np.hstack(pair))
        Z = np.hstack(feats)

        if self.mu is None or self.sigma is None:
            self.mu = Z.mean(axis=0)
            self.sigma = Z.std(axis=0) + 1e-8
        Zs = (Z - self.mu) / self.sigma
        return Zs

    def predict(self, X_raw):
        X_raw = np.asarray(X_raw, dtype=float)
        if X_raw.ndim == 1: X_raw = X_raw.reshape(1,-1)

        gb_pred = 0.0
        if self.gb is not None:
            try:
                gb_pred = self.gb.predict(X_raw)
            except Exception:
                gb_pred = 0.0
        else:
            gb_pred = 0.0

        Zs = self._phi(X_raw)
        lin = Zs.dot(self.w) + self.b if self.w is not None else np.zeros((X_raw.shape[0],), dtype=float)

        y = self.alpha * np.asarray(gb_pred).reshape(-1) + (1.0 - self.alpha) * lin.reshape(-1)

        y = np.clip(y, float(self.clip[0]), float(self.clip[1]))
        return y

class CRFPredictor:
    def __init__(self, store_dir=None):
        if store_dir is None:
            store_dir = HEURISTICS_DIR
        os.makedirs(store_dir, exist_ok=True)
        self.csv_path = os.path.join(store_dir, "encodes.csv")
        self.model_path = os.path.join(store_dir, "crf_model.pkl")
        self.model = None  # EnsembleRegressor
        self.lock = _th.Lock()
        self._load()

    def _load(self):
        try:
            import joblib
            if os.path.exists(self.model_path):
                obj = joblib.load(self.model_path)
                if isinstance(obj, EnsembleRegressor):
                    self.model = obj
                elif hasattr(obj, "predict"):

                    self.model = EnsembleRegressor(gb=obj, alpha=1.0)
                else:
                    self.model = None
        except Exception:
            self.model = None

    def _save(self):
        try:
            import joblib
            if self.model is not None:
                joblib.dump(self.model, self.model_path)
        except Exception:
            pass

    @staticmethod
    def _feat_vec(dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps):

        dur = float(max(0.01, dur))
        w = float(max(1.0, w)); h = float(max(1.0, h)); fps = float(max(0.1, fps))
        area = w * h
        ar = w / max(1.0, h)
        in_bps = float(max(1.0, in_bps))
        target_v_bps = max(100_000.0, (target_bytes * 8.0) / dur)
        bppf_in = in_bps / max(1.0, area * fps)              # input bits per pixel-frame
        bppf_tg = target_v_bps / max(1.0, area * fps)        # target bits per pixel-frame
        den = in_bps / max(1.0, area)                        # spatial density proxy
        s_kbps = float(sample_kbps)

        return [
            dur, w, h, fps, area, math.sqrt(area), ar,
            in_bps, target_bytes, target_v_bps, bppf_in, bppf_tg, den,
            float(tune_code), s_kbps
        ]

    @staticmethod
    def _rule_crf(dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps):

        dur = float(max(0.01, dur))
        area = max(1.0, float(w) * float(h))
        fps = float(max(0.1, fps))
        target_v_bps = max(100_000.0, (target_bytes * 8.0) / dur)
        bppf = target_v_bps / (area * fps)

        if bppf >= 0.35: base = 19
        elif bppf >= 0.18: base = 22
        elif bppf >= 0.10: base = 24
        elif bppf >= 0.06: base = 27
        elif bppf >= 0.035: base = 29
        else: base = 32

        if int(tune_code) == 2:      # grain
            base -= 2
        elif int(tune_code) == 1:    # animation
            base += 1
        if float(sample_kbps) > 0:   # size targeting → bias toward quality
            base -= 1
        return int(min(max(base, 16), 40))

    def predict(self, dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps, default_crf=22):

        fvec = self._feat_vec(dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps)
        rule = self._rule_crf(dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps)
        with self.lock:
            mdl = self.model
        if mdl is None:
            return int(rule if rule else default_crf)
        try:
            import numpy as _np
            X = _np.asarray([fvec], dtype=float)
            pred = float(mdl.predict(X)[0])
        except Exception:
            pred = float(rule)
        out = 0.30 * float(rule) + 0.70 * pred
        return int(min(max(round(out), 16), 40))

    def log_example(self, dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps, used_crf):
        header = ["dur","w","h","fps","in_bps","target_bytes","tune","sample_kbps","crf"]
        try:
            new_file = not os.path.exists(self.csv_path)
            with open(self.csv_path, "a", newline="") as f:
                wr = _csv.writer(f)
                if new_file: wr.writerow(header)
                wr.writerow([dur, w, h, fps, in_bps, target_bytes, tune_code, sample_kbps, used_crf])
        except Exception:
            pass

    def fit_from_disk(self):

        if not os.path.exists(self.csv_path):
            return
        X_raw, y = [], []
        try:
            with open(self.csv_path, "r", newline="") as f:
                rd = _csv.DictReader(f)
                for r in rd:
                    X_raw.append(self._feat_vec(
                        float(r["dur"]), float(r["w"]), float(r["h"]), float(r["fps"]),
                        float(r["in_bps"]), float(r["target_bytes"]), float(r["tune"]), float(r["sample_kbps"])
                    ))
                    y.append(float(r["crf"]))
            if not X_raw: return
            import numpy as _np
            X_raw = _np.asarray(X_raw, dtype=float)
            y = _np.asarray(y, dtype=float)

            n = len(y)
            idx_split = max(1, int(n * 0.8))
            X_tr, X_va = X_raw[:idx_split], X_raw[idx_split:]
            y_tr, y_va = y[:idx_split], y[idx_split:]

            gb = None
            if _SkHGBR is not None and X_tr.shape[0] >= 30:
                try:
                    gb = _SkHGBR(max_depth=4, learning_rate=0.08, max_iter=400, min_samples_leaf=12)
                    gb.fit(X_tr, y_tr)
                except Exception:
                    gb = None

            tmp = EnsembleRegressor(gb=None, alpha=1.0)
            Z_tr = tmp._phi(X_tr)
            lam = 1e-2
            I = _np.eye(Z_tr.shape[1], dtype=float)
            A = Z_tr.T @ Z_tr + lam * I
            b = Z_tr.T @ y_tr
            coefs = _np.linalg.pinv(A) @ b
            bias = 0.0  # centered by standardization
            mu, sigma = tmp.mu, tmp.sigma

            def _pred_mix(alpha):
                model = EnsembleRegressor(gb=gb, alpha=alpha, w=coefs, b=bias, mu=mu, sigma=sigma)
                return model.predict(X_va)
            best_alpha = 0.5
            if len(y_va) >= 5:
                alphas = _np.linspace(0.0, 1.0, 11)
                errs = []
                for a in alphas:
                    pred = _pred_mix(a)
                    mse = float(_np.mean((pred - y_va)**2))
                    errs.append(mse)
                best_alpha = float(alphas[int(_np.argmin(_np.asarray(errs)))])

            final_tmp = EnsembleRegressor(gb=None, alpha=1.0)
            Z_all = final_tmp._phi(X_raw)
            mu_all, sigma_all = final_tmp.mu, final_tmp.sigma
            A = Z_all.T @ Z_all + 1e-2 * _np.eye(Z_all.shape[1], dtype=float)
            b = Z_all.T @ y
            coefs_all = _np.linalg.pinv(A) @ b
            mdl = EnsembleRegressor(gb=gb, alpha=best_alpha, w=coefs_all, b=0.0, mu=mu_all, sigma=sigma_all)
            self.model = mdl
            self._save()
        except Exception:

            pass

_CRF_PREDICTOR = None
def get_crf_predictor():
    global _CRF_PREDICTOR
    if _CRF_PREDICTOR is None:
        _CRF_PREDICTOR = CRFPredictor()
    return _CRF_PREDICTOR

def _tune_to_code(tune_str: str) -> int:
    t = (tune_str or "film").lower()
    if "anim" in t: return 1
    if "grain" in t: return 2
    return 0  # film/none

def train_crf_offline_async():
    _th.Thread(target=lambda: get_crf_predictor().fit_from_disk(), daemon=True).start()

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None

import pystray

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Toplevel, Label
from tkinter.scrolledtext import ScrolledText


import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    _fix_bad_logging_formatters()
    return logging.getLogger('BitCrusher')

def _jsonl_log(event: str, data: dict | None = None):
    try:
        os.makedirs("logs", exist_ok=True)
        path = os.path.join("logs", f"run_{datetime.now().strftime('%Y%m%d')}.jsonl")
        rec = {"ts": datetime.now().isoformat(timespec="seconds"), "event": event}
        if data:
            rec.update(data)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass

def _privacy_args(preset: str | None):
    p = str(preset or "default").lower()
    if p == "strict":
        return [
            "-map_metadata", "-1",
            "-map_chapters", "-1",
            "-write_tmcd", "0",
            "-fflags", "+bitexact",
            "-flags:v", "+bitexact",
            "-flags:a", "+bitexact",
        ]
    elif p == "keep":
        return []
    else:  # default
        return ["-map_metadata", "-1"]

def _post_webhook_hardened(url: str, *, file_path: str | None = None,
                           json_payload: dict | None = None, max_mb: int = 25):
    try:
        import time as _t
        if json_payload:
            for delay in (0, 2, 4):
                try:
                    requests.post(url, json=json_payload, timeout=15)
                    break
                except Exception:
                    _t.sleep(delay)
        if file_path and os.path.exists(file_path):
            sz = os.path.getsize(file_path)
            if sz <= max_mb * 1024 * 1024:
                for delay in (0, 2, 4):
                    try:
                        with open(file_path, "rb") as f:
                            requests.post(url, files={"file": f}, timeout=60)
                        break
                    except Exception:
                        _t.sleep(delay)
    except Exception:
        pass

def _remux_copy(src: str, dst: str, extra_args: list[str] | None = None) -> bool:
    cmd = [FFMPEG, "-y", "-i", src, "-c", "copy"]
    if extra_args:
        cmd += list(extra_args)
    cmd.append(dst)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True, startupinfo=si, creationflags=NO_WIN)
    return p.returncode == 0


def _fix_bad_logging_formatters():
    
    safe_fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    root = logging.getLogger()
    for h in list(root.handlers):
        try:
            f = getattr(h, "formatter", None)
            if f and isinstance(getattr(f, "_fmt", None), str) and "%H" in f._fmt and "%(asctime)s" not in f._fmt:
                h.setFormatter(safe_fmt)
        except Exception:

            try:
                h.setFormatter(safe_fmt)
            except Exception:
                pass

try:
    from sklearn.linear_model import SGDRegressor as _SkSGD
except Exception:
    _SkSGD = None
try:
    from sklearn.ensemble import HistGradientBoostingRegressor as _SkHGBR
except Exception:
    _SkHGBR = None

def _make_sgd_model():
    
    if _SkSGD is not None:

        return _SkSGD(
            loss="squared_error",
            penalty="l2",
            alpha=1e-4,
            learning_rate="invscaling",
            eta0=0.05,
            power_t=0.25,
            random_state=42,
            max_iter=1000,
            tol=1e-3,
        )

    class _TinyRidge:
        def __init__(self, lam=1e-2):
            self.w = None
            self.b = 0.0
            self.lam = float(lam)

        def fit(self, X, y):
            X = np.asarray(X, dtype=float)
            y = np.asarray(y, dtype=float).reshape(-1)
            if X.ndim == 1:
                X = X.reshape(1, -1)
            Xb = np.hstack([X, np.ones((X.shape[0], 1))])
            A = Xb.T @ Xb + self.lam * np.eye(Xb.shape[1], dtype=float)
            sol = np.linalg.pinv(A) @ (Xb.T @ y)
            self.w = sol[:-1]
            self.b = float(sol[-1])
            return self

        def partial_fit(self, X, y):
            return self.fit(X, y)

        def predict(self, X):
            X = np.asarray(X, dtype=float)
            if X.ndim == 1:
                X = X.reshape(1, -1)
            if self.w is None:
                self.w = np.zeros((X.shape[1],), dtype=float)
            return X @ self.w + self.b

    return _TinyRidge()

class HeuristicLearner:
    def __init__(self, model_path="learner_model.pkl", degree=2, max_pairs=6, crf_clip=(16,40)):
        self.model_path = model_path
        self.degree = int(degree)
        self.max_pairs = int(max_pairs)
        self.crf_clip = tuple(crf_clip)
        self.model = _make_sgd_model()
        self.is_fitted = False
        self.mu = None
        self.sigma = None
        self._load()

        if self.model is None:
            self.model = _make_sgd_model()
        self.X_train, self.y_train = [], []

    def _transform(self, Xrow):
        import numpy as np
        x = np.asarray(Xrow, dtype=float).reshape(-1)

        pieces = [x, x*x, np.log1p(np.abs(x))]

        k = min(len(x), self.max_pairs)
        pair = []
        for i in range(k):
            for j in range(i+1, k):
                pair.append(x[i]*x[j])
        if pair:
            pieces.append(np.asarray(pair, dtype=float))
        z = np.concatenate(pieces)

        if self.mu is None or self.sigma is None:
            self.mu = z.copy()
            self.sigma = np.ones_like(z)
        zs = (z - self.mu) / (self.sigma + 1e-8)
        return zs

    def update(self, target_size, features, used_crf):
        
        try:
            import numpy as np

            if isinstance(features, dict):
                keys = sorted(features.keys())
                x = np.array([features[k] for k in keys], dtype=float)
            else:
                x = np.array(list(features), dtype=float)
            y = float(used_crf)

            z = self._transform(x)
            if self.X_train:
                Z_stack = np.vstack([np.vstack(self.X_train), z.reshape(1,-1)])
                self.mu = Z_stack.mean(axis=0)
                self.sigma = Z_stack.std(axis=0) + 1e-8
            else:
                self.mu = z.copy()
                self.sigma = np.ones_like(z)

            self.X_train.append(((z - self.mu) / (self.sigma + 1e-8)).astype(float))
            self.y_train.append(y)

            X_arr = np.vstack(self.X_train)
            y_arr = np.array(self.y_train)
            if self.is_fitted:
                self.model.partial_fit(X_arr, y_arr)
            else:
                self.model.fit(X_arr, y_arr)
                self.is_fitted = True
            self.save()
        except Exception:
            pass

    def predict(self, X):
        
        import numpy as np
        if isinstance(X, dict):
            keys = sorted(X.keys())
            arr = np.array([X[k] for k in keys], dtype=float)
        else:
            arr = np.array(X, dtype=float)
        z = self._transform(arr)
        if z.ndim == 1: z = z.reshape(1, -1)
        y = float(self.model.predict(z)[0])
        return int(min(max(round(y), self.crf_clip[0]), self.crf_clip[1]))

    def save(self):
        try:
            import joblib
            obj = {"model": self.model, "mu": self.mu, "sigma": self.sigma,
                   "degree": self.degree, "max_pairs": self.max_pairs,
                   "crf_clip": self.crf_clip, "is_fitted": self.is_fitted}
            joblib.dump(obj, self.model_path)
        except Exception:
            pass

    def _load(self):
        try:
            import joblib
            if os.path.exists(self.model_path):
                obj = joblib.load(self.model_path)
                if isinstance(obj, dict):
                    self.model = obj.get("model", _make_sgd_model())
                    self.mu = obj.get("mu", None)
                    self.sigma = obj.get("sigma", None)
                    self.degree = obj.get("degree", 2)
                    self.max_pairs = obj.get("max_pairs", 6)
                    self.crf_clip = tuple(obj.get("crf_clip", (16,40)))
                    self.is_fitted = bool(obj.get("is_fitted", False))
                else:

                    self.model = obj
                    self.is_fitted = True
        except Exception:
            self.model = _make_sgd_model()
            self.is_fitted = False








       
from tkinter import simpledialog
import json
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import pystray
from PIL import Image
import sys
import platform
import threading
from PIL import Image
import pystray
from tkinterdnd2 import DND_FILES, TkinterDnD
from win10toast import ToastNotifier
from win10toast import ToastNotifier

try:
    from win10toast import ToastNotifier as _TN
    _orig_toast = _TN.show_toast
    def _safe_toast(self, title, msg, duration=5, icon_path=None, threaded=True):
        try:
            _orig_toast(self, str(title or "BitCrusher"), str(msg or ""),
                        duration=int(duration or 5), icon_path=icon_path, threaded=True)
            return 1
        except Exception as e:
            try: LOG.warning("Toast suppressed: %r", e)
            except Exception: pass
            return 1
    _TN.show_toast = _safe_toast
except Exception:
    pass


import threading
from plyer import notification

import subprocess, platform

if platform.system() == "Windows":

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    NO_WIN = subprocess.CREATE_NO_WINDOW
else:
    si = None
    NO_WIN = 0


import os

def ensure_runtime_dirs():
    base_path = os.path.expanduser("~")  # Or wherever you want them
    settings_path = os.path.join(base_path, "BitCrusherSettings", "user_settings")
    heuristic_path = os.path.join(base_path, "BitCrusherSettings", "heuristics")

    os.makedirs(settings_path, exist_ok=True)
    os.makedirs(heuristic_path, exist_ok=True)

    return settings_path, heuristic_path



    def start(self): pass
    def stop(self): pass

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    TkinterDnD = None
    DND_FILES = None


import os
import json
import platform

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

HEURISTICS_DIR    = os.path.join(SCRIPT_DIR, "heuristics")
USER_SETTINGS_DIR = os.path.join(SCRIPT_DIR, "user_settings")
os.makedirs(HEURISTICS_DIR, exist_ok=True)
os.makedirs(USER_SETTINGS_DIR, exist_ok=True)


def default_handbrake():
    return "HandBrakeCLI.exe" if platform.system() == "Windows" else "HandBrakeCLI"

def default_ffprobe():
    return "ffprobe.exe"    if platform.system() == "Windows" else "ffprobe"

def default_ffmpeg():
    return "ffmpeg.exe"     if platform.system() == "Windows" else "ffmpeg"

def load_paths():
    print(f"🔍 Looking for config.json at: {CONFIG_PATH}")

    if os.path.exists(CONFIG_PATH):
        print("✅ Found config.json, contents:")
        with open(CONFIG_PATH, "r") as f:
            cfg = json.load(f)
        print(json.dumps(cfg, indent=2))
        hb = cfg.get("handbrake") or default_handbrake()
        fp = cfg.get("ffprobe")   or default_ffprobe()
        ff = cfg.get("ffmpeg")    or default_ffmpeg()
        return hb, fp, ff

    print("⚠️  config.json not found; checking tools/ folder…")
    tools_dir = os.path.join(SCRIPT_DIR, "tools")

    hb_name = "HandBrakeCLI.exe" if platform.system() == "Windows" else "HandBrakeCLI"
    fp_name = "ffprobe.exe"    if platform.system() == "Windows" else "ffprobe"
    ff_name = "ffmpeg.exe"     if platform.system() == "Windows" else "ffmpeg"

    hb_path = os.path.join(tools_dir, hb_name)
    fp_path = os.path.join(tools_dir, fp_name)
    ff_path = os.path.join(tools_dir, ff_name)

    hb = hb_path if os.path.isfile(hb_path) else default_handbrake()
    fp = fp_path if os.path.isfile(fp_path) else default_ffprobe()
    ff = ff_path if os.path.isfile(ff_path) else default_ffmpeg()

    print(f"🚨 Using HandBrakeCLI at: {hb}")
    print(f"🚨 Using ffprobe    at: {fp}")
    print(f"🚨 Using ffmpeg     at: {ff}")

    return hb, fp, ff

HANDBRAKE_CLI, FFPROBE, FFMPEG = load_paths()
log_tool_paths(HANDBRAKE_CLI, FFMPEG, FFPROBE)

def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)

TOOLS_DIR          = resource_path("tools")
DEFAULT_HANDBRAKE  = os.path.join(TOOLS_DIR, "HandBrakeCLI.exe")
DEFAULT_FFMPEG     = os.path.join(TOOLS_DIR, "ffmpeg.exe")
DEFAULT_FFPROBE    = os.path.join(TOOLS_DIR, "ffprobe.exe")

MAX_SIZE_MB_DEFAULT = 10

SIZE_UNITS = {"KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}

def bytes_from_value_unit(val, unit):
    
    try:
        v = float(str(val).strip())
    except Exception:
        v = 0.0
    u = (str(unit or "MB").strip().upper())
    mul = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
    }.get(u, 1024**2)

    b = int(max(0, v) * mul)
    return b



def human_bytes(n: int) -> str:
    n = int(max(0, n))
    for unit, mul in [("TB", 1024**4), ("GB", 1024**3), ("MB", 1024**2), ("KB", 1024)]:
        if n >= mul:
            return f"{n / mul:.2f} {unit}"
    return f"{n} B"


def _sanitize_int(s, default=0):
    try:
        return int(float(str(s).strip()))
    except Exception:
        return int(default)

DEFAULT_AUDIO_BITRATE = 128 * 1000
DEFAULT_CRF = 22
MIN_ACCEPTABLE_CRF = 28
ITERATIVE_MAX_ATTEMPTS = 6  # maximum iterations if binary search fails

PRESETS = {
    "Custom (use size below)": None,
    "Discord Turbo (Max 10MB)": 10,
    "Best Quality (Max 50MB)": 50,
    "Speed Demon (Max 25MB)": 25,
    "Tiny File (Max 5MB)": 5,
}


ADVANCED_DEFAULTS = {
    "auto_retry": True,
    "overshoot_ratio": 1.00,
    "two_pass_fallback": True,
    "grain_filter": True,
    "auto_retry_done": False,
    "two_pass_forced": False,   # ← COMMA HERE
    "encoder": "x264",
    "iterative": False,
    "two_pass": False,
    "manual_crf": "",
    "manual_bitrate": "",
    "output_prefix": "",
    "output_suffix": "_discord_ready",
    "audio_format": "aac",
    "image_format": "jpg",
    "concurrent": False,
    "auto_output_folder": False,
    "guetzli": False,
    "pngopt": False,
    "auto_jpeg": False
}


def _normalize_drop_path(p: str) -> str:
    
    try:
        s = str(p).strip()
        if (s.startswith("{") and s.endswith("}")) or (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        return os.path.normpath(s)
    except Exception:
        return str(p)





from functools import lru_cache

def install_drop_highlight(frame):
    normal_bg = frame.cget("background") if str(frame.cget("style")) == "" else None
    def _enter(_e=None):
        try:
            frame.configure(style="Card.TFrame")
        except Exception:
            if normal_bg is not None:
                frame.configure(background=_hsl_shift(CARD_BG, l_mul=1.08))
    def _leave(_e=None):
        try:
            frame.configure(style="Card.TFrame")
        except Exception:
            if normal_bg is not None:
                frame.configure(background=CARD_BG)
    frame.bind("<Enter>", _enter)
    frame.bind("<Leave>", _leave)
    return frame



@lru_cache(maxsize=64)
def _cached_thumb(path, maxsize=(512, 288)):
    im = Image.open(path)
    im.thumbnail(maxsize, Image.LANCZOS)
    return ImageTk.PhotoImage(im)

def update_preview(self, *_):
    sel = self.queue_box.curselection()
    if not sel:
        self.preview_label.configure(text="No file selected", image="", compound="none")
        return
    fpath = self.queue_box.get(sel[0])
    ext = os.path.splitext(fpath)[1].lower()
    if ext in {'.jpg','.jpeg','.png','.gif','.bmp','.tiff'}:
        img_obj = _cached_thumb(fpath)
        self.preview_label.configure(image=img_obj, text=os.path.basename(fpath), compound='bottom')
        self.preview_label.image = img_obj
    else:
        self.preview_label.configure(text=os.path.basename(fpath), image="", compound='none')

import colorsys, json, tkinter as tk, tkinter.filedialog as fd
from tkinter import ttk
from tkinter import simpledialog as sd

THEMES = {
    "Dark": {
        "APP_BG":"#14161A", "CARD_BG":"#1C1F24",
        "FG":"#E6E8EB", "FG_SUB":"#A6ABB3",
        "ACCENT":"#7C5CFF", "ACCENT_2":"#3DDC97",
        "ERROR":"#FF6B6B", "WARN":"#FFB020",
        "TITLE":"#C9B8FF"
    },
    "Light": {  # high-contrast light, no “blown” whites
        "APP_BG":"#F4F6F9", "CARD_BG":"#FFFFFF",
        "FG":"#1F2328", "FG_SUB":"#5A6470",
        "ACCENT":"#4C5BD4", "ACCENT_2":"#139D6F",
        "ERROR":"#C62828", "WARN":"#B46913",
        "TITLE":"#3949AB"
    },
    "Autumn": {
        "APP_BG":"#1E1510", "CARD_BG":"#2A1C14",
        "FG":"#F3E9DC", "FG_SUB":"#D8C7B6",
        "ACCENT":"#E07A5F", "ACCENT_2":"#F2CC8F",
        "ERROR":"#FF6B6B", "WARN":"#F4A261",
        "TITLE":"#F2A679"
    },
    "Winter": {
        "APP_BG":"#0E141B", "CARD_BG":"#15202B",
        "FG":"#E4F1FF", "FG_SUB":"#A8C0D6",
        "ACCENT":"#58A6FF", "ACCENT_2":"#7EE1D2",
        "ERROR":"#FF6B6B", "WARN":"#FFB020",
        "TITLE":"#9AD1FF"
    },
}

def _themes_dir():
    d = os.path.join(USER_SETTINGS_DIR, "themes")
    os.makedirs(d, exist_ok=True)
    return d

def _validate_theme_dict(d: dict) -> bool:
    req = {"APP_BG","CARD_BG","FG","FG_SUB","ACCENT","ACCENT_2","ERROR","WARN","TITLE"}
    return isinstance(d, dict) and req.issubset(d.keys()) and all(isinstance(d[k], str) for k in req)

def load_user_themes_at_startup():
    
    d = _themes_dir()
    try:
        for fn in os.listdir(d):
            if not fn.lower().endswith(".json"):
                continue
            p = os.path.join(d, fn)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if _validate_theme_dict(data):
                    name = os.path.splitext(fn)[0]
                    THEMES[name] = data
            except Exception:
                pass
    except Exception:
        pass

load_user_themes_at_startup()

APP_BG=CARD_BG=FG=FG_SUB=ACCENT=ACCENT_2=ERROR=WARN=TITLE=None

def _hsl_shift(hex_color: str, h_delta=0.0, s_mul=1.0, l_mul=1.0) -> str:
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

def _use_palette(name: str):
    
    global APP_BG, CARD_BG, FG, FG_SUB, ACCENT, ACCENT_2, ERROR, WARN, TITLE
    p = THEMES.get(name, THEMES["Dark"])
    APP_BG, CARD_BG = p["APP_BG"], p["CARD_BG"]
    FG, FG_SUB      = p["FG"], p["FG_SUB"]
    ACCENT, ACCENT_2= p["ACCENT"], p["ACCENT_2"]
    ERROR, WARN     = p["ERROR"], p["WARN"]
    TITLE           = p["TITLE"]

def apply_theme(style: ttk.Style, theme_name: str="Dark"):
    
    _use_palette(theme_name)
    style.theme_use("clam")

    style.configure(".", background=APP_BG, foreground=FG)
    style.configure("TFrame", background=APP_BG)
    style.configure("Card.TFrame", background=CARD_BG)
    style.configure("TLabel", background=APP_BG, foreground=FG)
    style.configure("Sub.TLabel", background=APP_BG, foreground=FG_SUB)
    style.configure("Title.TLabel", background=APP_BG, foreground=TITLE, font=("Segoe UI Semibold", 20))

    btn_bg  = _hsl_shift(ACCENT, l_mul=0.88)
    btn_bg2 = ACCENT
    style.configure("TButton",
        font=("Segoe UI", 10, "bold"), padding=(12,8),
        background=btn_bg, foreground="#ffffff", borderwidth=0)
    style.map("TButton",
        background=[("active", btn_bg2), ("disabled", "#2B2F36")],
        foreground=[("disabled", "#7a8088")])

    style.configure("Ghost.TButton",
        font=("Segoe UI", 10), padding=(10,6),
        background=CARD_BG, foreground=FG, bordercolor="#2A2E34", relief="flat")
    style.map("Ghost.TButton",
        background=[("active", _hsl_shift(CARD_BG, l_mul=1.06))])

    entry_bg    = _hsl_shift(CARD_BG, l_mul=1.06 if CARD_BG != "#FFFFFF" else 0.98)
    entry_bg_ro = _hsl_shift(CARD_BG, l_mul=1.02 if CARD_BG != "#FFFFFF" else 0.97)
    entry_fg_dis= "#7a8088"

    style.configure("Dark.TEntry",
        fieldbackground=entry_bg, foreground=FG, padding=6,
        bordercolor="#2A2E34", relief="flat")
    style.map("Dark.TEntry",
        fieldbackground=[("focus", entry_bg), ("!focus", entry_bg), ("disabled", _hsl_shift(CARD_BG, l_mul=1.0))],
        foreground=[("disabled", entry_fg_dis)])

    style.configure("Dark.TCombobox",
        fieldbackground=entry_bg, background=CARD_BG, foreground=FG,
        padding=4, bordercolor="#2A2E34", relief="flat")
    style.map("Dark.TCombobox",
        fieldbackground=[("readonly", entry_bg_ro), ("!readonly", entry_bg)],
        foreground=[("disabled", entry_fg_dis)])

    style.configure("Accent.Horizontal.TProgressbar",
        troughcolor=CARD_BG, background=ACCENT, bordercolor=CARD_BG,
        lightcolor=ACCENT, darkcolor=_hsl_shift(ACCENT, l_mul=0.8))

    style.configure("TCheckbutton", background=APP_BG, foreground=FG)
    style.map("TCheckbutton", foreground=[("disabled", FG_SUB)])

    style.configure("Card.TLabelframe", background=CARD_BG, borderwidth=0, relief="flat")
    style.configure("Card.TLabelframe.Label", background=CARD_BG, foreground=FG_SUB, padding=(6,0))
    style.layout("Card.TLabelframe", [
        ('Labelframe.padding', {'sticky': 'nswe', 'children': [
            ('Labelframe.label',  {'side': 'top', 'sticky': ''}),
            ('Labelframe.client', {'sticky': 'nswe'})
        ]})
    ])

def retheme_runtime(self, style: ttk.Style, theme_name: str):
    
    apply_theme(style, theme_name)

    try:
        self.root.configure(bg=APP_BG)
    except Exception:
        pass

    try:
        if hasattr(self, "title_label"):
            self.title_label.configure(style="Title.TLabel")
    except Exception:
        pass
    try:
        self.queue_box.configure(
            bg=_hsl_shift(CARD_BG, l_mul=1.0), fg=FG,
            highlightthickness=0, borderwidth=0,
            selectbackground=_hsl_shift(ACCENT, l_mul=1.0),
            selectforeground="#ffffff"
        )
    except Exception:
        pass
    try:
        self.log_text.configure(
            background=_hsl_shift(CARD_BG, l_mul=0.98),
            foreground=FG, insertbackground=FG,
            highlightthickness=0, borderwidth=0
        )
    except Exception:
        pass
    try:
        self.preview_label.configure(bg=_hsl_shift(CARD_BG, l_mul=0.98), fg=FG)
    except Exception:
        pass

    import tkinter as tk
    entry_bg    = _hsl_shift(CARD_BG, l_mul=1.06 if CARD_BG != "#FFFFFF" else 0.98)
    entry_bg_ro = _hsl_shift(CARD_BG, l_mul=1.02 if CARD_BG != "#FFFFFF" else 0.97)

    def _retint(w):
        try:

            if isinstance(w, (tk.Frame, tk.Toplevel, tk.Canvas)):
                try: w.configure(bg=APP_BG)
                except Exception: pass
            if isinstance(w, tk.Label):
                try: w.configure(bg=APP_BG, fg=FG)
                except Exception: pass
            if isinstance(w, tk.LabelFrame):
                try: w.configure(bg=CARD_BG, fg=FG)
                except Exception: pass

            if isinstance(w, tk.Entry):
                try:
                    w.configure(bg=entry_bg, fg=FG, insertbackground=FG,
                                disabledbackground=entry_bg_ro,
                                highlightthickness=0, borderwidth=1, relief="flat")
                except Exception: pass
            if isinstance(w, tk.Checkbutton):
                try:
                    w.configure(bg=CARD_BG, fg=FG,
                                activebackground=CARD_BG, activeforeground=FG,
                                selectcolor=CARD_BG, highlightthickness=0, borderwidth=0)
                except Exception: pass
        except Exception:
            pass

        for c in w.winfo_children():
            _retint(c)

    try:
        _retint(self.root)
    except Exception:
        pass

def _validate_theme_dict(d: dict) -> bool:
    req = {"APP_BG","CARD_BG","FG","FG_SUB","ACCENT","ACCENT_2","ERROR","WARN","TITLE"}
    return isinstance(d, dict) and req.issubset(d.keys()) and all(isinstance(d[k], str) for k in req)

def save_current_theme_as(self):
    
    name = getattr(self, "theme_var", None).get() if hasattr(self, "theme_var") else "Dark"
    try:
        p = fd.asksaveasfilename(defaultextension=".json",
                                 filetypes=[("JSON", "*.json")],
                                 initialfile=f"{name}.json",
                                 title="Save Current Theme As…")
        if not p: return
        with open(p, "w", encoding="utf-8") as f:
            json.dump(THEMES[name], f, indent=2)
        log_info(f"Saved theme '{name}' to: {p}")
    except Exception:
        log_exc("Failed to save theme")

def load_custom_theme(self):
    
    try:
        p = fd.askopenfilename(filetypes=[("JSON", "*.json")], title="Load Theme JSON")
        if not p: return
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not _validate_theme_dict(data):
            log_err("Invalid theme file. Missing required keys.")
            return

        import os
        name = os.path.splitext(os.path.basename(p))[0]
        THEMES[name] = data

        if hasattr(self, "rebuild_themes_menu"): self.rebuild_themes_menu()
        self.theme_var.set(name)
        animated_retheme(self, name)
        log_info(f"Loaded custom theme '{name}' from: {p}")
    except Exception:
        log_exc("Failed to load theme")


def pulsate(widget, base=1.0, delta=0.05, period=16, _dir=1):
    try:
        scale = base + delta*_dir
        widget.tk.call(widget, 'scale', 0, 0, scale, scale)
    except Exception:
        pass  # not every widget supports tk scale; safe to ignore
    widget.after(period, lambda: pulsate(widget, base, delta, period, -_dir))


def shimmer_progressbar(pb):

    def _loop():
        try:
            pb.step(1)
        except Exception:
            return
        pb.after(15, _loop)
    _loop()


def fade_window(win, start=0.0, end=1.0, dur_ms=220):
    steps = max(1, int(dur_ms/16))
    delta = (end-start)/steps
    def _step(i=0, val=start):
        try:
            win.wm_attributes('-alpha', max(0.0, min(1.0, val)))
        except Exception:
            return
        if i < steps:
            win.after(16, _step, i+1, val+delta)
    _step()


def snackbar(root, text, millis=1800, kind="info"):
    bg = {"info": _hsl_shift(CARD_BG, l_mul=1.15), "warn": WARN, "error": ERROR}.get(kind, CARD_BG)
    bar = tk.Label(root, text=text, bg=bg, fg="#101215", font=("Segoe UI", 10, "bold"))
    bar.place(relx=0.5, rely=1.0, anchor="s", relwidth=0.6, y=-10)

    def kill():
        try: bar.destroy()
        except: pass
    root.after(millis, kill)


def _probe_audio_meta(input_path: str) -> dict:
    

    if not FFPROBE:
        return {
            "duration": 0.0,
            "bitrate": DEFAULT_AUDIO_BITRATE,
            "sr": 48000,
            "ch": 2,
            "codec": "",
        }

    cmd = [
        FFPROBE, "-v", "error",
        "-select_streams", "a:0",
        "-show_entries",
        "format=duration,bit_rate:stream=codec_name,bit_rate,sample_rate,channels",
        "-of", "json", input_path
    ]

    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, startupinfo=si, creationflags=NO_WIN
        )
    except Exception as e:
        log_err(f"ffprobe exec failed: {e}")
        return {
            "duration": 0.0,
            "bitrate": DEFAULT_AUDIO_BITRATE,
            "sr": 48000,
            "ch": 2,
            "codec": "",
        }

    if p.returncode != 0:
        log_err(f"ffprobe failed (rc={p.returncode}): {' '.join(str(x) for x in cmd)}")
        if p.stderr:
            log_err(p.stderr.strip())
        return {
            "duration": 0.0,
            "bitrate": DEFAULT_AUDIO_BITRATE,
            "sr": 48000,
            "ch": 2,
            "codec": "",
        }

    try:
        js = json.loads(p.stdout or "{}")
    except Exception:
        js = {}

    fmt = js.get("format", {}) or {}
    streams = js.get("streams", []) or []
    s = streams[0] if streams else {}

    def _int(x, d):
        try:
            return int(x)
        except Exception:
            return d

    def _float(x, d):
        try:
            return float(x)
        except Exception:
            return d

    return {
        "duration": _float(fmt.get("duration"), 0.0),
        "bitrate":  _int(fmt.get("bit_rate") or s.get("bit_rate"), DEFAULT_AUDIO_BITRATE),
        "sr":       _int(s.get("sample_rate"), 48000),
        "ch":       _int(s.get("channels"), 2),
        "codec":    (s.get("codec_name") or "").lower(),
    }



def _should_copy_audio(target_bytes:int, dur:float, meta:dict) -> bool:
    
    try:
        if not target_bytes or not dur or dur <= 0:
            return False
        codec = (meta.get("codec") or "").lower()
        if codec not in {"aac", "opus", "vorbis"}:
            return False
        a_bits = int(meta.get("bitrate") or 0) * float(dur)
        return a_bits / 8.0 < 0.10 * target_bytes
    except Exception:
        return False

def _adaptive_two_pass(new_w:int, target_bitrate:int, force:bool=False) -> bool:
    
    if force:
        return True
    if new_w >= 1280:
        return target_bitrate > 0 and target_bitrate < 2_000_000
    else:
        return target_bitrate > 0 and target_bitrate < 1_000_000


def _encode_audio_once(input_path: str, output_path: str, *,
                       encoder: str, bitrate_bps: int, sr: int,
                       channels: int, vbr_mode: str, loudnorm: bool,
                       highpass_hz: int | None, lowpass_hz: int | None,
                       extra_filters: list[str] | None = None,
                       privacy_preset: str | None = None) -> tuple[bool, int, str]:
    

    af = []

    if highpass_hz and highpass_hz > 0:
        af.append(f"highpass=f={highpass_hz}")
    if lowpass_hz and lowpass_hz > 0:
        af.append(f"lowpass=f={lowpass_hz}")

    if loudnorm:
        af.append("dynaudnorm=p=1")

    if extra_filters:
        af.extend(extra_filters)

    af_chain = ",".join(af) if af else None

    cmd = [
        FFMPEG, "-y",
        "-i", input_path,
        "-vn",
        "-c:a", encoder,
    ]

    if encoder == "libopus":
        if vbr_mode == "off":
            cmd += ["-vbr", "off"]
        elif vbr_mode == "constrained":
            cmd += ["-vbr", "constrained"]
        else:
            cmd += ["-vbr", "on"]
        cmd += ["-compression_level", "10", "-application", "audio"]

    if channels in (1, 2):
        cmd += ["-ac", str(channels)]
    if sr:
        cmd += ["-ar", str(sr)]

    cmd += ["-b:a", str(int(bitrate_bps))]

    if af_chain:
        cmd += ["-af", af_chain]

    cmd += _privacy_args(privacy_preset) + [output_path]


    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, startupinfo=si, creationflags=NO_WIN)
    ok = (proc.returncode == 0) and os.path.exists(output_path)
    size = os.path.getsize(output_path) if ok else 0
    tail = "\n".join((proc.stderr or "").splitlines()[-15:])
    return ok, size, tail



def log_message(log_widget, msg, level="INFO"):
    timestamp = time.strftime("%H:%M:%S")
    full_msg = f"[{timestamp}] [{level}] {msg}\n"
    logging.log(getattr(logging, level.upper(), logging.INFO), msg)
    if log_widget:
        log_widget.configure(state="normal")
        log_widget.insert("end", full_msg)
        log_widget.see("end")
        log_widget.configure(state="disabled")


def log_message(log_widget, msg, level="INFO"):
    timestamp = time.strftime("%H:%M:%S")
    full_msg = f"[{timestamp}] [{level}] {msg}\n"
    logging.log(getattr(logging, level.upper(), logging.INFO), msg)
    if log_widget:
        log_widget.configure(state="normal")
        log_widget.insert("end", full_msg)
        log_widget.see("end")
        log_widget.configure(state="disabled")


def format_bytes(size: int) -> str:
    power = 2 ** 10
    n = 0
    units = ["B", "KB", "MB", "GB"]
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"

def get_video_metadata(filepath: str):
    cmd = [
        FFPROBE, "-v", "error", "-select_streams", "v:0",
        "-show_entries", "format=duration:stream=width,height,bit_rate,avg_frame_rate",
        "-of", "json", filepath
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=si, creationflags=NO_WIN)
    data = json.loads(result.stdout or "{}")
    fmt_info = data.get("format", {})
    stream_info = data.get("streams", [{}])[0]
    duration = float(fmt_info.get("duration", 0))
    width = int(stream_info.get("width", 1280))
    height = int(stream_info.get("height", 720))
    bitrate = int(stream_info.get("bit_rate", 5_000_000))
    framerate_raw = stream_info.get("avg_frame_rate", "30/1")
    try:
        framerate = float(Fraction(framerate_raw))
    except Exception:
        framerate = 30.0
    return duration, width, height, bitrate, framerate

def extract_video_duration(path):
    
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        path
    ]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
        return float(out)
    except Exception:
        return None

def calculate_bitrate(duration, target_bytes, audio_bitrate, input_path=None):
    

    if not duration or duration <= 0:
        if input_path:
            probed = extract_video_duration(input_path)
            if probed and probed > 0:
                duration = probed

    if not duration or duration <= 0:
        duration = 60.0

    video_bits = (target_bytes * 8) - (audio_bitrate * duration)
    video_bits = max(video_bits, 0)

    return max(int(video_bits / duration), 100_000)


def determine_audio_bitrate(input_bitrate: int) -> int:
    if input_bitrate < 1_000_000:
        return 64 * 1000
    elif input_bitrate < 1_500_000:
        return 96 * 1000
    return DEFAULT_AUDIO_BITRATE

def determine_tune_profile(width: int, height: int, filename: str) -> str:
    lower = filename.lower()
    if "anime" in lower or "cartoon" in lower:
        return "animation"
    elif "cam" in lower or "grain" in lower:
        return "grain"
    return "film"

def determine_frame_rate(framerate: float, width: int, duration: float):
    if framerate > 29 and width <= 1280 and duration > 10:
        return 24
    return None

def determine_resolution(width: int, target_bitrate: int) -> int:
    if width > 1920 and target_bitrate < 1_800_000:
        return 1280
    elif width > 1280 and target_bitrate < 1_000_000:
        return 854
    return width

def compress_with_handbrake(input_path: str, output_path: str,
                            audio_bitrate: int, encoder: str="x264",
                            crf: int=None, bitrate: int=None,
                            width: int=None, fps: int=None, tune: str=None,
                            two_pass: bool=False, vf: str=None,
                            hwaccel: str="CPU", audio_copy: bool=False,
                            advanced_options: dict | None = None):

    
    enc = (encoder or "x264").lower()
    use_ffmpeg = enc in {"av1", "nvenc", "hevc_nvenc", "h264_nvenc", "qsv", "amf"} or (two_pass and platform.system() == "Windows")
    adv = advanced_options or {}


    if not use_ffmpeg and enc in {"x264", "x265"}:

        try:
            hb_cmd = [
                HANDBRAKE_CLI, "-i", input_path, "-o", output_path,
                "-e", enc, "--aencoder", "av_aac", "--audio", "1",
                "--ab", str(int(max(1, audio_bitrate) // 1000)),
                "--encoder-preset", "medium",  # faster than "slow"
                "--optimize"
            ]

            if crf is not None and str(crf).strip():
                hb_cmd += ["-q", str(crf)]
            elif bitrate is not None:
                hb_cmd += ["-b", str(int(bitrate // 1000))]
                if platform.system() != "Windows" and two_pass:
                    hb_cmd += ["--two-pass"]

            if width:
                hb_cmd += ["--width", str(width)]
            if fps:
                hb_cmd += ["--rate", str(fps)]
            if tune and tune != "none" and enc == "x264":
                hb_cmd += ["--encoder-tune", tune]

            if vf:
                hb_cmd += ["--vf", vf]
            subprocess.run(hb_cmd, check=True, capture_output=True, text=True, startupinfo=si, creationflags=NO_WIN)
            return True
        except subprocess.CalledProcessError:
            return False

    if enc in {"nvenc", "hevc_nvenc"}:
        vcodec = "hevc_nvenc"
    elif enc == "h264_nvenc":
        vcodec = "h264_nvenc"
    elif enc in {"qsv", "hevc_qsv"}:
        vcodec = "hevc_qsv"
    elif enc == "h264_qsv":
        vcodec = "h264_qsv"
    elif enc in {"amf", "hevc_amf"}:
        vcodec = "hevc_amf"
    elif enc == "h264_amf":
        vcodec = "h264_amf"
    elif enc == "av1":
        vcodec = "libaom-av1"
    elif enc == "x265":
        vcodec = "libx265"
    else:
        vcodec = "libx264"

    ff_cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error"]

    if (hwaccel or "").upper() == "NVENC":
        ff_cmd += ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]
    ff_cmd += ["-i", input_path]

    ff_cmd += ["-threads", str(max(2, (os.cpu_count() or 4) - 1))]

    if audio_copy:
        ff_cmd += ["-c:a", "copy"]
    else:
        ff_cmd += ["-c:a", "aac", "-b:a", str(int(max(1, audio_bitrate)))]

    ff_cmd += ["-c:v", vcodec]

    if "nvenc" in vcodec:
        ff_cmd += ["-rc", "vbr_hq",
                   "-cq", str(crf if crf is not None else 19),
                   "-rc-lookahead", "32",
                   "-spatial_aq", "1", "-temporal_aq", "1",
                   "-aq-strength", "8",
                   "-b_ref_mode", "middle",
                   "-preset", "p5"]

        ff_cmd += ["-movflags", "+faststart"]

        if two_pass and bitrate is not None:
            ff_cmd += ["-multipass", "2pass-fullres"]

        if bitrate is not None:
            ff_cmd += ["-b:v", str(int(bitrate)),
                       "-maxrate", str(int(bitrate*1.45)),
                       "-bufsize", str(int(bitrate*2))]
    else:
        preset = "medium"
        if vcodec == "libaom-av1":
            preset = "3"  # keep AV1 sane
        ff_cmd += ["-preset", preset]
        if crf is not None and str(crf).strip():
            if vcodec == "libx265":
                ff_cmd += ["-x265-params", f"crf={int(crf)}"]
            elif vcodec == "libaom-av1":
                ff_cmd += ["-crf", str(int(crf))]
            else:
                ff_cmd += ["-crf", str(int(crf))]
        elif bitrate is not None:
            ff_cmd += ["-b:v", str(int(bitrate))]

    if width:
        if (hwaccel or "").upper() == "NVENC":

            ff_cmd += ["-vf", f"scale_cuda={int(width)}:-2" + ((","+vf) if vf else "")]
        else:
            scale_expr = f"scale={int(width)}:-2"
            if vf:
                scale_expr = vf + "," + scale_expr
            ff_cmd += ["-vf", scale_expr]
    elif vf:
        ff_cmd += ["-vf", vf]
    if fps:
        ff_cmd += ["-r", str(fps)]

    if two_pass and "nvenc" not in vcodec and bitrate is not None:
        passlog = output_path + ".log"
        cmd1 = ff_cmd + ["-pass", "1", "-an", "-f", "mp4", os.devnull]
        subprocess.run(cmd1, check=True, capture_output=True, text=True, startupinfo=si, creationflags=NO_WIN)
        cmd2 = ff_cmd + ["-pass", "2", "-movflags", "+faststart", output_path]
        subprocess.run(cmd2, check=True, capture_output=True, text=True, startupinfo=si, creationflags=NO_WIN)
        try:
            for x in [passlog, passlog+".mbtree", "ffmpeg2pass-0.log", "ffmpeg2pass-0.log.mbtree"]:
                if os.path.exists(x): os.remove(x)
        except:
            pass
        return True
    else:
        ff_cmd += _privacy_args(adv.get("privacy_preset")) + ["-movflags", "+faststart", output_path]
        subprocess.run(ff_cmd, check=True, capture_output=True, text=True, startupinfo=si, creationflags=NO_WIN)
        return True







def get_media_type(input_path: str) -> str:
    ext = os.path.splitext(input_path)[1].lower()
    video_exts = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".3g2", ".mpeg", ".mpg"}
    audio_exts = {".mp3", ".wav", ".aac", ".ogg", ".flac", ".wma", ".m4a", ".opus", ".alac", ".aiff", ".aif"}
    image_exts = {".jpg", ".jpeg", ".jfif", ".png", ".webp", ".gif", ".bmp", ".tiff", ".tif", ".heic", ".heif", ".jxl", ".raw"}

    if ext in video_exts:
        return "video"
    elif ext in audio_exts:
        return "audio"
    elif ext in image_exts:
        return "image"
    else:
        return "unknown"

def parse_dnd_files(data: str) -> list:
    data = data.strip()
    files = re.findall(r'\{([^}]+)\}', data)
    if not files:
        files = data.replace("\r", "\n").split("\n")
    cleaned = []
    for f in files:
        f = f.strip().strip("{}")
        if f.startswith("file:///"):
            f = f[8:]
        elif f.startswith("file://"):
            f = f[7:]
        if os.name == "nt":
            f = f.replace("/", "\\")
        cleaned.append(os.path.normpath(f))
    return cleaned

def binary_search_video_crf(input_path: str, temp_output: str, audio_bitrate: int,
                            encoder: str, width: int, fps: int, tune: str, two_pass: bool,
                            target_size_bytes: int, low: int, high: int,
                            status_callback, cancel_callback) -> int:
    best_crf = None
    while low <= high:
        mid = (low + high) // 2
        if cancel_callback():
            status_callback("Video compression cancelled during binary search.", level="WARNING")
            return None
        status_callback(f"Testing CRF={mid}...")
        if os.path.exists(temp_output):
            os.remove(temp_output)
        try:
            compress_with_handbrake(
                input_path, temp_output, audio_bitrate,
                encoder=encoder, crf=mid, width=width,
                fps=fps, tune=tune, two_pass=two_pass
            )
        except Exception as err:
            status_callback(f"Error at CRF {mid}: {err}", level="ERROR")
            return None
        if not os.path.exists(temp_output):
            status_callback("No output produced for CRF " + str(mid), level="ERROR")
            return None
        size = os.path.getsize(temp_output)
        status_callback(f"CRF {mid} produced {format_bytes(size)}")
        if size > target_size_bytes:
            low = mid + 1
        else:
            best_crf = mid
            if size >= target_size_bytes * 0.9:
                return mid
            high = mid - 1
    return best_crf

def binary_search_audio_bitrate(input_path: str, temp_output: str, audio_encoder: str,
                                low: int, high: int, target_size_bytes: int,
                                status_callback, cancel_callback) -> int:
    best_bitrate = None
    while low <= high:
        mid = (low + high) // 2
        if cancel_callback():
            status_callback("Audio compression cancelled during binary search.", level="WARNING")
            return None
        status_callback(f"Testing bitrate: {mid}bps...")
        if os.path.exists(temp_output):
            os.remove(temp_output)
        cmd = [FFMPEG, "-y", "-i", input_path, "-vn", "-c:a", audio_encoder, "-b:a", str(mid), temp_output]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=si, creationflags=NO_WIN)
        if result.returncode != 0:
            status_callback(f"ffmpeg error at bitrate {mid}: {result.stderr.strip()}", level="ERROR")
            return None
        if not os.path.exists(temp_output):
            status_callback("No output produced for bitrate " + str(mid), level="ERROR")
            return None
        size = os.path.getsize(temp_output)
        status_callback(f"Bitrate {mid} produced {format_bytes(size)}")
        if size > target_size_bytes:
            high = mid - 1
        else:
            best_bitrate = mid
            if size >= target_size_bytes * 0.9:
                return mid
            low = mid + 1
    return best_bitrate


def compress_audio_files(self):
    files = [f for f in self.file_queue if f.lower().endswith(self.supported_audio_formats)]
    if not files:
        self.log_info("🎵 No audio files to compress.")
        return

    self.log_info(f"🎵 Starting audio compression: {len(files)} files.")
    with ThreadPoolExecutor(max_workers=cpu_count() - 1 or 1) as pool:
        futures = [pool.submit(self.compress_audio, f) for f in files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                self.log_exception(f"Audio compression crash: {e}")



def compress_image_files(self):
    files = [f for f in self.file_queue if f.lower().endswith(self.supported_image_formats)]
    if not files:
        self.log_info("📸 No image files to compress.")
        return

    self.log_info(f"📸 Starting image compression: {len(files)} files.")
    with ThreadPoolExecutor(max_workers=cpu_count() - 1 or 1) as pool:
        futures = [pool.submit(self.compress_image, f) for f in files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                self.log_exception(f"Image compression crash: {e}")


from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

def compress_video_files(self):
    files = [f for f in self.file_queue if f.lower().endswith(self.supported_video_formats)]
    if not files:
        self.log_info("🎥 No video files to compress.")
        return

    self.log_info(f"🎥 Starting video compression: {len(files)} files.")
    with ThreadPoolExecutor(max_workers=cpu_count() - 1 or 1) as pool:

        out_dir = (self.save_path.get() if hasattr(self, "save_path") else os.path.dirname(files[0]) or os.getcwd())
        tgt     = (self._get_target_bytes() if hasattr(self, "_get_target_bytes") else 10 * 1024 * 1024)
        adv     = (self.gather_advanced_options() if hasattr(self, "gather_advanced_options") else {})
        wh      = (self.webhook_url.get() if hasattr(self, "webhook_url") and getattr(self, "use_webhook", None) and self.use_webhook.get() else "")

        futures = [pool.submit(self.compress_file_task, f, out_dir, tgt, wh, adv) for f in files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                self.log_exception(f"Video compression crash: {e}")


import math

def _build_vf_chain_for_noise(input_path, w, h, new_w, new_h, advanced_options):
    filters = []
    if new_w and new_h:
        filters.append(f"scale={new_w}:{new_h}:flags=lanczos")

    fn_low = os.path.basename(input_path).lower()
    looks_grainy = (
        "grain" in fn_low or "noise" in fn_low or "iso" in fn_low
        or determine_tune_profile(w, h, input_path) == "grain"
    )
    if advanced_options.get("grain_filter", True) and looks_grainy:
        filters.append("hqdn3d=1.5:1.5:6:6")

    return ",".join(filters) if filters else None



def compress_video(input_path: str, save_path: str, status_cb,
                   target_size_mb: int, webhook_url: str,
                   advanced_options: dict, cancel_cb) -> dict:
    

    status_cb(f"🚀 Compressing video: {input_path}")

    bitrate = None
    audio_br = None
    audio_copy = False
    t_start = time.time()
    target_bytes = int(float(target_size_mb) * 1024 * 1024)

    _jsonl_log("start_job", {"type": "video", "input": input_path, "target_bytes": target_bytes})

    try:
        if target_bytes > 0 and os.path.getsize(input_path) <= int(target_bytes * 0.99):
            suffix = datetime.now().strftime("%H%M%S")
            out_file = os.path.join(save_path, f"{Path(input_path).stem}_compressed_{suffix}.mp4")
            tmp_final = out_file + ".partial"
            if os.path.exists(tmp_final):
                os.remove(tmp_final)

            preset = advanced_options.get("privacy_preset")
            ok = _remux_copy(input_path, tmp_final, _privacy_args(preset))
            if not ok:
                status_cb("⚠️ Passthrough remux failed; proceeding with re-encode.", level="WARNING")
            else:
                shutil.move(tmp_final, out_file)
                final_size = os.path.getsize(out_file)

            try:
                _container = (os.path.splitext(out_file)[1] or ".mp4").lstrip(".").lower() or "mp4"
                _encoder   = (advanced_options.get("encoder") or "x264")
                _stats_dir = os.path.join(USER_SETTINGS_DIR, "stats")
                learn_from_result(_stats_dir, _encoder, _container, int(target_bytes), int(final_size))
                _jsonl_log("learned", {"encoder": _encoder, "container": _container,
                                       "target_bytes": int(target_bytes), "actual_bytes": int(final_size)})
                _adj = guardrail_adjust(int(final_size), int(target_bytes))
                if _adj is not None:
                    _jsonl_log("guardrail_suggest", {"scale": float(_adj)})
            except Exception:
                pass

                stats = {
                    "original_size": os.path.getsize(input_path),
                    "compressed_size": final_size,
                    "used_crf": None,
                    "duration": None,
                    "width": None,
                    "height": None,
                    "bitrate": None,
                    "framerate": None,
                    "output_path": out_file,
                    "passthrough": True,
                }
                _jsonl_log("encode_end", {"type": "video", **stats})
                
                if webhook_url:
                    _post_webhook_hardened(webhook_url, json_payload=stats, file_path=out_file)
                return stats
    except Exception:
        pass

    try:
        dur, w, h, br, fr = get_video_metadata(input_path)
    except Exception:
        status_cb("⚠️ Failed to extract metadata; using defaults", level="WARNING")
        dur, w, h, br, fr = 10.0, 1280, 720, 5_000_000, 30.0
    if not dur or dur <= 0:
        probed = extract_video_duration(input_path)
        dur = probed if probed and probed > 0 else 10.0

    sample_dur = min(10.0, max(5.0, 0.07 * float(dur)))

    base_crf = None
    mc = str(advanced_options.get("manual_crf") or "").strip()
    if mc.isdigit():
        base_crf = int(mc)
    else:
        base_crf = DEFAULT_CRF

    est_total = 0
    try:
        est_total = quick_size_estimate(input_path, base_crf, sample_dur, status_cb)
    except Exception:
        est_total = 0

    suggested_crf = base_crf
    try:
        if target_bytes > 0 and est_total > 0:
            ratio = est_total / float(target_bytes)
            crf_adj = int(round(6 * math.log2(ratio))) if ratio > 0 else 0
            suggested_crf = max(18, min(51, base_crf + crf_adj))
    except Exception:
        pass

    audio_meta = _probe_audio_meta(input_path)
    ch = (audio_meta or {}).get("ch") or 2
    sr = (audio_meta or {}).get("sr") or 48000
    enc_name = (advanced_options.get("encoder") or "x264")

    if _should_copy_audio(target_bytes, dur, audio_meta):
        audio_copy = True

        v_bps, a_bps_suggest, ov = choose_bitrates(
            duration_s=dur,
            target_bytes=target_bytes,
            encoder=enc_name,
            container="mp4",
            channels=ch,
            sample_rate=sr,
            audio_fmt=(advanced_options.get("audio_format") or "aac"),
            stats_dir=os.path.join(USER_SETTINGS_DIR, "stats"),
        )
        audio_br = 0
    else:
        audio_copy = False
        v_bps, a_bps_suggest, ov = choose_bitrates(
            duration_s=dur,
            target_bytes=target_bytes,
            encoder=enc_name,
            container="mp4",
            channels=ch,
            sample_rate=sr,
            audio_fmt=(advanced_options.get("audio_format") or "aac"),
            stats_dir=os.path.join(USER_SETTINGS_DIR, "stats"),
        )
        audio_br = a_bps_suggest

    target_bitrate = int(v_bps)
    bitrate = target_bitrate  # ensure guardrails can read a base VBR


    new_w = determine_resolution(w, target_bitrate)
    fps = determine_frame_rate(fr, w, dur) or fr
    tune = determine_tune_profile(w, h, input_path)
    encoder = (advanced_options.get("encoder") or "x264").lower()
    hwaccel = (advanced_options.get("hwaccel") or "CPU").upper()

    force_two = bool(advanced_options.get("two_pass") or advanced_options.get("two_pass_forced"))
    two_pass = _adaptive_two_pass(new_w, target_bitrate, force=force_two)

    tmp_final = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    status_cb(f"🎬 Encoding BITRATE={target_bitrate} bps (two-pass={two_pass}), width={new_w}, encoder={encoder}, hw={hwaccel}")

    manual_bps = int(target_bitrate)

    try:
        if advanced_options and advanced_options.get("manual_bitrate"):
            manual_bps = int(float(advanced_options["manual_bitrate"]))
    except Exception:
        pass

    two_pass = True


    ok = compress_with_handbrake(
        input_path, tmp_final,
        audio_bitrate=audio_br if audio_br else DEFAULT_AUDIO_BITRATE,
        encoder=encoder,
        crf=None if manual_bps is not None else suggested_crf,
        bitrate=manual_bps,
        width=new_w, fps=fps, tune=tune,
        two_pass=two_pass,
        vf=None,
        hwaccel=hwaccel,
        audio_copy=audio_copy,
        advanced_options=advanced_options
    )


    if not ok:
        raise RuntimeError("Encode failed")

    suffix = datetime.now().strftime("%H%M%S")
    out_file = os.path.join(save_path, f"{Path(input_path).stem}_compressed_{suffix}.mp4")
    shutil.move(tmp_final, out_file)

    final_size = os.path.getsize(out_file)

    if target_bytes and final_size > int(target_bytes * 1.02) and (bitrate or target_bitrate):
        try:

            _scale = max(0.50, min(0.95, (target_bytes / float(final_size)) * 0.97))
            _base_vbr = int(bitrate or target_bitrate)
            _new_v_bitrate = max(160_000, int(_base_vbr * _scale))

            _new_a_bitrate = None if audio_copy else max(64_000, int(((audio_br or 128_000)) * _scale))
            status_cb(f"⚖️ Overshot target ({final_size} > {target_bytes}). Retrying with {_new_v_bitrate} bps.", "WARNING")

            _retry_tmp = out_file + ".retry"
            if os.path.exists(_retry_tmp):
                os.remove(_retry_tmp)

            _ok_retry = compress_with_handbrake(
                input_path=input_path,
                output_path=_retry_tmp,
                vcodec=vcodec,
                acodec=acodec,
                bitrate=_new_v_bitrate,
                crf=None,                   # force true bitrate retry
                two_pass=True,              # tighten allocation on retry
                width=new_w,
                height=new_h,
                fps=fr,
                audio_bitrate=_new_a_bitrate,
                audio_copy=audio_copy,
                advanced_options=advanced_options,
                status_cb=status_cb
            )

            if _ok_retry and os.path.exists(_retry_tmp):
                os.replace(_retry_tmp, out_file)
                final_size = os.path.getsize(out_file)
                _jsonl_log("retry_success", {
                    "scale": float(_scale),
                    "new_video_bitrate": int(_new_v_bitrate),
                    "new_audio_bitrate": None if audio_copy else int(_new_a_bitrate),
                    "final_bytes": int(final_size)
                })
            else:
                _jsonl_log("retry_failed", {
                    "scale": float(_scale),
                    "new_video_bitrate": int(_new_v_bitrate)
                })
        except Exception as _e:
            _jsonl_log("retry_error", {"error": str(_e)})

    try:
        _container = (os.path.splitext(out_file)[1] or ".mp4").lstrip(".").lower() or "mp4"
        _encoder   = (advanced_options.get("encoder") or "x264")
        _stats_dir = os.path.join(USER_SETTINGS_DIR, "stats")
        learn_from_result(_stats_dir, _encoder, _container, int(target_bytes), int(final_size))
        _jsonl_log("learned", {"encoder": _encoder, "container": _container,
                               "target_bytes": int(target_bytes), "actual_bytes": int(final_size)})
        _adj = guardrail_adjust(int(final_size), int(target_bytes))
        if _adj is not None:
            _jsonl_log("guardrail_suggest", {"scale": float(_adj)})
    except Exception:
        pass

    stats = {
        "original_size": os.path.getsize(input_path),
        "compressed_size": final_size,
        "used_crf": suggested_crf,
        "duration": dur,
        "width": new_w,
        "height": int(round(h * new_w / w)) if w else h,
        "bitrate": br,
        "frame_rate": fr,
        "output_path": out_file
    }


    if webhook_url:
        _post_webhook_hardened(webhook_url, json_payload=stats, file_path=out_file)


    status_cb(f"✅ Compress done in {time.time()-t_start:.1f}s")
    return stats





def compress_audio(input_path: str, save_path: str, status_callback,
                   target_size_mb: int, webhook_url: str,
                   advanced_options: dict, cancel_callback) -> dict:
    
    status_callback(f"🚀 Compressing audio: {input_path}")
    t0 = time.time()

    try:

        target_bytes = int(target_size_mb) if float(target_size_mb) >= (2 * 1024 * 1024) else int(float(target_size_mb) * 1024 * 1024)
        target_bytes = max(1, target_bytes)
    except Exception:
        target_bytes = 10 * 1024 * 1024  # 10 MB fallback

    _jsonl_log("start_job", {"type": "audio", "input": input_path, "target_bytes": target_bytes})

    meta = _probe_audio_meta(input_path)
    duration = max(1.0, meta["duration"])  # avoid division by zero
    orig_bps = max(32_000, meta["bitrate"])

    fmt = (advanced_options.get("audio_format", "opus") or "opus").lower()
    audio_mode = (advanced_options.get("audio_mode", "auto") or "auto").lower()   # auto|music|speech
    vbr_mode   = (advanced_options.get("audio_vbr", "on") or "on").lower()        # on|constrained|off
    loudnorm   = bool(advanced_options.get("audio_loudnorm", False))
    downmix    = bool(advanced_options.get("audio_downmix_mono", audio_mode == "speech"))
    max_sr     = int(advanced_options.get("audio_max_sr", 48000))                 # cap SR to 48k by default

    if fmt == "mp3":
        encoder, ext = "libmp3lame", "mp3"
    elif fmt == "aac" or fmt == "m4a":
        encoder, ext = "aac", "m4a"
    else:

        encoder, ext = "libopus", "opus"

    out_ch = 1 if downmix else min(2, meta["ch"] or 2)

    in_sr  = meta["sr"] or 48000
    out_sr = min(max_sr, 48000 if in_sr >= 44100 else 44100)

    hp = 80 if out_ch == 1 else None
    lp = 20000

    headroom = 1.03
    init_bps = int((target_bytes * 8 / duration) / headroom)

    if encoder == "libopus":

        lo = 24_000 if out_ch == 1 else 32_000
        hi = 192_000 if out_ch == 1 else 256_000
    elif encoder == "aac":
        lo, hi = (64_000 if out_ch == 1 else 96_000), (224_000 if out_ch == 1 else 320_000)
    else:  # mp3
        lo, hi = (80_000 if out_ch == 1 else 128_000), (256_000 if out_ch == 1 else 320_000)

    if encoder == "libopus":

        max_cap = 510_000
    elif encoder == "aac":

        max_cap = 512_000
    else:

        max_cap = 320_000

    calc_hi = max(hi, int(init_bps * 1.25))
    hi = min(calc_hi, max_cap)

    if lo >= hi:
        lo = max(16_000, hi - 32_000)

    if audio_mode == "speech":
        lo = max(lo - 16_000, 16_000)
        hi = max(hi - 32_000, lo + 16_000)
    elif audio_mode == "music":
        lo = min(lo + 16_000, hi - 16_000)

    target_bps = max(lo, min(init_bps, hi))

    base = os.path.splitext(os.path.basename(input_path))[0]
    prefix = advanced_options.get("output_prefix", "")
    suffix = advanced_options.get("output_suffix", "")
    final_out = os.path.join(save_path, f"{prefix}{base}{suffix}.{ext}")

    tmp_out = os.path.join(save_path, f"._tmp_audio_encode_.{ext}")
    if os.path.exists(tmp_out):
        os.remove(tmp_out)

    tries = 0
    max_tries = 6
    best_ok = None  # (size, bitrate, path_is_tmp_bool)

    low_bps, high_bps = lo, hi
    current_bps = target_bps

    while tries < max_tries:
        if cancel_callback():
            status_callback("⏹️ Audio compression cancelled.", level="WARNING")
            if os.path.exists(tmp_out):
                os.remove(tmp_out)
            return {}

        tries += 1
        if os.path.exists(tmp_out):
            os.remove(tmp_out)

        status_callback(f"🎚️ Try {tries}/{max_tries}: {current_bps//1000} kbps, "
                        f"{out_sr} Hz, {'mono' if out_ch==1 else 'stereo'} "
                        f"(encoder={encoder}, vbr={vbr_mode})")

        ok, size, err_tail = _encode_audio_once(
            input_path, tmp_out,
            encoder=encoder,
            bitrate_bps=current_bps,
            sr=out_sr,
            channels=out_ch,
            vbr_mode=vbr_mode,
            loudnorm=loudnorm,
            highpass_hz=hp,
            lowpass_hz=lp,
            extra_filters=None
        )

        if not ok:
            status_callback(f"❌ ffmpeg error on pass {tries}:\n{err_tail}", level="ERROR")

            break

        status_callback(
            f"📦 Output size: {format_bytes(size)} "
            f"(target {format_bytes(max(1, int(target_bytes)))})"
        )

        if size <= target_bytes:
            best_ok = (size, current_bps, True)

            if size >= int(target_bytes * 0.95):
                break

            low_bps = max(low_bps, current_bps)

            current_bps = min(high_bps, int((current_bps + high_bps) / 2))

            if current_bps >= high_bps or (high_bps - current_bps) < 1000:
                status_callback(
                    f"🎯 Reached {encoder} bitrate ceiling (~{high_bps//1000} kbps); "
                    f"best achievable ≈ {format_bytes(size)} for this track.",
                    level="WARNING"
                )
                break
        else:

            high_bps = min(high_bps, current_bps)
            current_bps = max(low_bps, int((low_bps + current_bps) / 2))

    if not best_ok:
        status_callback("🔁 Falling back to ABR binary search…")

        chosen_format = "opus" if encoder == "libopus" else ("aac" if encoder == "aac" else "mp3")
        audio_encoder = "libopus" if chosen_format == "opus" else ("aac" if chosen_format == "aac" else "libmp3lame")

        temp_output = os.path.join(save_path, f"_temp_audio_bs_.{ext}")
        if os.path.exists(temp_output):
            os.remove(temp_output)

        best_bitrate = binary_search_audio_bitrate(
            input_path, temp_output, audio_encoder,
            32_000, hi, target_bytes,
            status_callback, cancel_callback
        )  # :contentReference[oaicite:2]{index=2}

        if best_bitrate is None:

            best_bitrate = target_bps

        if os.path.exists(temp_output):
            os.remove(temp_output)
        ok, _, err_tail = _encode_audio_once(
            input_path, temp_output,
            encoder=encoder,
            bitrate_bps=best_bitrate,
            sr=out_sr, channels=out_ch,
            vbr_mode=("constrained" if encoder == "libopus" else "off"),
            loudnorm=False, highpass_hz=None, lowpass_hz=None
        )
        if not ok:
            status_callback(f"❌ ffmpeg error (final encode):\n{err_tail}", level="ERROR")
            return {}
        os.replace(temp_output, final_out)
    else:

        os.replace(tmp_out, final_out)

    took = time.time() - t0
    fin_size = os.path.getsize(final_out)
    status_callback(f"✅ Audio compressed to {format_bytes(fin_size)} in {took:.1f}s")

    stats = {
        "filename": os.path.basename(final_out),
        "original_size": os.path.getsize(input_path),
        "compressed_size": fin_size,
        "ratio": fin_size / max(1, os.path.getsize(input_path)),
        "time_taken": took,
        "output_path": final_out
    }

    _jsonl_log("encode_end", {"type": "audio", **stats})



    if webhook_url:
        _post_webhook_hardened(webhook_url, json_payload=stats, file_path=final_out)

    return stats



def compress_image(input_path: str, save_path: str, status_callback,
                   target_size_mb: int, webhook_url: str,
                   advanced_options: dict, cancel_callback) -> dict:
    status_callback(f"🚀 Compressing image: {input_path}")
    t_start = time.time()
    target_size_bytes = target_size_mb * 1024 * 1024
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    out_prefix = advanced_options.get("output_prefix", "")
    out_suffix = advanced_options.get("output_suffix", "")
    image_format = advanced_options.get("image_format", "jpg")
    if advanced_options.get("auto_jpeg"):
        image_format = "jpg"
    output_file = os.path.join(save_path, f"{out_prefix}{name}{out_suffix}.{image_format}")

    try:
        im = Image.open(input_path)
    except Exception as e:
        status_callback("❌ Could not open image: " + str(e), level="ERROR")
        return {}

    quality = 85
    attempts = 0
    success = False
    temp_output = None

    while attempts < ITERATIVE_MAX_ATTEMPTS:
        if cancel_callback():
            status_callback("⏹️ Image compression cancelled.", level="WARNING")
            return {}

        temp_output = output_file + "_tmp"
        fmt = (image_format or "jpg").lower()
        pil_fmt = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}.get(fmt, fmt.upper())
        im.convert("RGB").save(temp_output, pil_fmt, quality=quality, optimize=True)
        size = os.path.getsize(temp_output)
        status_callback(
            f"📦 Image size: {format_bytes(size)} at quality {quality} "
            f"(target {format_bytes(max(1, int(target_size_bytes)))})"
        )




        if size <= target_size_bytes:
            success = True
            break
        quality = max(10, quality - 10)
        attempts += 1

    if not success:
        status_callback("❌ Image compression failed.", level="ERROR")
        if temp_output and os.path.exists(temp_output):
            os.remove(temp_output)
        return {}

    if advanced_options.get("guetzli") and image_format.lower() == "jpg":
        guetzli_out = output_file + "_guetzli"
        try:
            res = subprocess.run(["guetzli", temp_output, guetzli_out], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=si, creationflags=NO_WIN)
            if res.returncode == 0:
                os.replace(guetzli_out, output_file)
                status_callback("Guetzli optimization applied.")
            else:
                status_callback("Guetzli failed: " + res.stderr.strip(), level="WARNING")
        except Exception as e:
            status_callback("Guetzli error: " + str(e), level="WARNING")
    elif advanced_options.get("pngopt") and image_format.lower() == "png":
        pngquant_out = output_file + "_pngquant.png"
        try:

            res1 = subprocess.run(
                ["pngquant", "--quality=65-80", "--speed", "1", temp_output, "--output", pngquant_out],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=si, creationflags=NO_WIN
            )

            if res1.returncode == 0:

                res2 = subprocess.run(
                    ["zopflipng", "--iterations=500", "--lossy_transparent", "--lossy_8bit", pngquant_out, output_file],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=si, creationflags=NO_WIN
                )

                if res2.returncode == 0:
                    status_callback("PNGQuant + Zopfli optimization applied.")
                else:
                    status_callback("Zopfli failed: " + res2.stderr.strip(), level="WARNING")
            else:
                status_callback("PNGQuant failed: " + res1.stderr.strip(), level="WARNING")
        except Exception as e:
            status_callback("PNGQuant/Zopfli error: " + str(e), level="WARNING")
    else:

        shutil.move(temp_output, output_file)


    t_end = time.time()
    final_size = os.path.getsize(output_file)
    status_callback(f"✅ Image compressed: {format_bytes(final_size)}")

    stats = {
        "filename": filename,
        "original_size": os.path.getsize(input_path),
        "compressed_size": final_size,
        "ratio": final_size / os.path.getsize(input_path),
        "time_taken": t_end - t_start,
        "output_path": output_file
    }

    _jsonl_log("encode_end", {"type": "image", **stats})


    if webhook_url:
        _post_webhook_hardened(webhook_url, file_path=output_file)

    return stats

def settings_window():
    win = Toplevel()
    win.title("Settings")
    win.geometry("300x200")
    Label(win, text="Settings go here").pack(pady=20)
    Button(win, text="Close", command=win.destroy).pack(pady=10)






def auto_compress(input_path: str, save_path: str, status_callback,
                  target_size_mb: int, webhook_url: str,
                  advanced_options: dict, cancel_callback) -> dict:
    

    try:

        _target_mb = int(round(float(target_size_mb) / (1024 * 1024))) if float(target_size_mb) >= (2 * 1024 * 1024) else int(target_size_mb)
        _target_mb = max(1, _target_mb)
    except Exception:
        _target_mb = 10  # safe default

    media_type = get_media_type(input_path)
    if media_type == "video":
        return compress_video(input_path, save_path, status_callback,
                              _target_mb, webhook_url,
                              advanced_options, cancel_callback)
    elif media_type == "audio":
        return compress_audio(input_path, save_path, status_callback,
                              _target_mb, webhook_url,
                              advanced_options, cancel_callback)
    elif media_type == "image":
        return compress_image(input_path, save_path, status_callback,
                              _target_mb, webhook_url,
                              advanced_options, cancel_callback)
    else:
        status_callback(f"❌ Unsupported file type: {input_path}", level="ERROR")
        return {}


class CompressorGUI:

    HB_URL = "https://github.com/HandBrake/HandBrake/releases/download/1.7.0/HandBrakeCLI-1.7.0-win64.zip"
    FF_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    def install_tool(self, name, url):
        
        tools_dir = os.path.join(SCRIPT_DIR, "tools")
        os.makedirs(tools_dir, exist_ok=True)
        dest_zip = os.path.join(tools_dir, f"{name}.zip")
        self.update_status(f"Downloading {name}...", level="INFO")
        try:
            r = requests.get(url)
            with open(dest_zip, "wb") as f:
                f.write(r.content)
            with zipfile.ZipFile(dest_zip, "r") as zip_ref:
                zip_ref.extractall(tools_dir)
            self.update_status(f"{name} installed.", level="INFO")
        except Exception as e:
            self.update_status(f"Failed to install {name}: {e}", level="ERROR")

    def check_dependencies(self):
        import shutil

        hb = DEFAULT_HANDBRAKE  if os.path.exists(DEFAULT_HANDBRAKE) else shutil.which("HandBrakeCLI") or shutil.which("HandBrakeCLI.exe")
        ff = DEFAULT_FFMPEG     if os.path.exists(DEFAULT_FFMPEG)    else shutil.which("ffmpeg")        or shutil.which("ffmpeg.exe")
        fp = DEFAULT_FFPROBE    if os.path.exists(DEFAULT_FFPROBE)   else shutil.which("ffprobe")       or shutil.which("ffprobe.exe")

        hb = hb or "HandBrakeCLI.exe"
        ff = ff or "ffmpeg.exe"
        fp = fp or "ffprobe.exe"

        self.handbrake_path = hb
        self.ffmpeg_path    = ff
        self.ffprobe_path   = fp

        

        if not shutil.which(HANDBRAKE_CLI) or not os.path.isfile(HANDBRAKE_CLI):
            self.install_tool("HandBrakeCLI", self.HB_URL)
        if not shutil.which(FFMPEG) or not os.path.isfile(FFMPEG):
            self.install_tool("ffmpeg", self.FF_URL)
            

    def setup_directories(self):
        import os
        for folder in ["user_settings", "heuristics"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    def browse_watch_folder(self):
        
        from tkinter import filedialog, messagebox
        folder = filedialog.askdirectory(parent=self.root, title="Select watch folder")
        if folder:
            self.watch_folder.set(folder)
            self.update_status(f"👀 Watch folder set to: {folder}")
        else:

            self.watch_var.set(False)
            messagebox.showinfo("Watch Folder", "No folder selected.")

    def open_save_folder(self):
        import os, sys, subprocess
        from tkinter import messagebox

        raw = self.save_path.get() if hasattr(self.save_path, "get") else str(self.save_path)
        path = os.path.abspath(os.path.expanduser(raw.strip() or "."))

        def _status(msg, level="INFO"):
            try:
                if hasattr(self, "update_status"):
                    self.update_status(msg, level=level)
                elif hasattr(self, "log_widget"):

                    self.log_widget.configure(state="normal")
                    self.log_widget.insert("end", f"[{level}] {msg}\n")
                    self.log_widget.see("end")
                    self.log_widget.configure(state="disabled")
                else:
                    print(f"[{level}] {msg}")
            except Exception:
                print(f"[{level}] {msg}")

        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            _status(f"Failed to ensure save folder exists: {e}", level="ERROR")
            try:
                messagebox.showerror("Open Save Folder", f"Could not create folder:\n{path}\n\n{e}")
            except Exception:
                pass
            return

        try:
            if sys.platform.startswith("win"):
                os.startfile(path)  # type: ignore
            elif sys.platform == "darwin":
                subprocess.run(["open", path], check=False)
            else:
                subprocess.run(["xdg-open", path], check=False)
            _status(f"Opened save folder: {path}")
        except Exception as e:
            _status(f"Failed to open save folder: {e}", level="ERROR")
            try:
                messagebox.showerror("Open Save Folder", f"Could not open folder:\n{path}\n\n{e}")
            except Exception:
                pass
    
    def _t(self, key: str, default: str | None = None) -> str:
        code = self.lang_var.get() if hasattr(self, "lang_var") else "en"

        return (LANG.get(code, {}).get(key)
                or LANG_BUILTIN["en"].get(key)
                or (default if default is not None else key))

    def _rebuild_ui_for_language(self):
        try:
            for w in list(self.root.winfo_children()):
                w.destroy()
        except Exception:
            pass

        self.setup_ui()
        self.setup_menu()

    def _on_language_change(self):
        _save_language_choice(self.lang_var.get())

        try:
            self.settings = getattr(self, "settings", {}) or {}
            self.settings["language"] = self.lang_var.get()
            self.save_settings()
        except Exception:
            pass
        self._rebuild_ui_for_language()

    def _get_target_bytes(self):
        

        try:
            raw = self.target_size_var.get() if hasattr(self, "target_size_var") else self.settings.get("target_size", 10)
        except Exception:
            raw = self.settings.get("target_size", 10)
        try:
            val = float(str(raw).strip())
        except Exception:
            val = 10.0

        try:
            unit = self.size_unit_var.get() if hasattr(self, "size_unit_var") else self.settings.get("size_unit", "MB")
        except Exception:
            unit = self.settings.get("size_unit", "MB")
        unit = (str(unit or "MB").upper())
        if unit not in {"B","KB","MB","GB","TB"}:
            unit = "MB"

        b = bytes_from_value_unit(val, unit)

        if val > 0 and b < 1 * 1024**2:
            b = 1 * 1024**2

        return int(b)



    
    def setup_ui(self):
        import os
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        from tkinter.scrolledtext import ScrolledText

        if not hasattr(self, "root") or self.root is None:
            self.root = tk.Tk()
        self.theme_var = tk.StringVar(value="Dark")   # default theme
        self.lang_var = tk.StringVar(value=_load_language_choice("en"))
        _load_lang_packs()
        self.root.configure(bg="#14161A")             # initial bg; gets overridden by apply_theme
        self.style = ttk.Style(self.root)

        saved_theme = (self.settings.get("theme") if hasattr(self, "settings") else None) or "Dark"
        self.theme_var = tk.StringVar(value=saved_theme)

        apply_theme(self.style, self.theme_var.get())
        try:
            retheme_runtime(self, self.style, self.theme_var.get())
        except Exception:
            pass
        try:
            self.root.configure(bg=APP_BG)
        except Exception:
            pass

        if not hasattr(self, "preset_var"):        self.preset_var = tk.StringVar(value=next(iter(PRESETS)))
        if not hasattr(self, "target_size_var"):   self.target_size_var = tk.IntVar(value=PRESETS[self.preset_var.get()])
        if not hasattr(self, "save_path"):         self.save_path = tk.StringVar(value=os.path.join(SCRIPT_DIR, "output"))
        if not hasattr(self, "size_unit_var"):
            self.size_unit_var = tk.StringVar(value=(self.settings.get("size_unit", "MB") if hasattr(self, "settings") and isinstance(self.settings, dict) else "MB"))
        if not hasattr(self, "profile_var"):       self.profile_var = tk.StringVar(value="")
        if not hasattr(self, "watch_var"):         self.watch_var = tk.BooleanVar(value=False)
        if not hasattr(self, "watch_folder"):      self.watch_folder = tk.StringVar(value=SCRIPT_DIR)
        if not hasattr(self, "webhook_url"):       self.webhook_url = ""
        if not hasattr(self, "webhook_var"):       self.webhook_var = tk.StringVar(value=self.webhook_url)
        if not hasattr(self, "file_list"): self.file_list = []

        def _adv_bool(name, key):
            if not hasattr(self, name):
                setattr(self, name, tk.BooleanVar(value=bool(ADVANCED_DEFAULTS.get(key, False))))
        def _adv_str(name, key):
            if not hasattr(self, name):
                setattr(self, name, tk.StringVar(value=str(ADVANCED_DEFAULTS.get(key, ""))))

        _adv_str ("adv_encoder",            "encoder")
        _adv_bool("adv_iterative",          "iterative")
        _adv_bool("adv_two_pass",           "two_pass")
        _adv_str ("adv_manual_crf",         "manual_crf")
        _adv_str ("adv_manual_bitrate",     "manual_bitrate")
        _adv_str ("adv_output_prefix",      "output_prefix")
        _adv_str ("adv_output_suffix",      "output_suffix")
        _adv_str ("adv_audio_format",       "audio_format")
        _adv_str ("adv_image_format",       "image_format")
        _adv_bool("adv_concurrent",         "concurrent")
        _adv_bool("adv_auto_output_folder", "auto_output_folder")
        _adv_bool("adv_guetzli",            "guetzli")
        _adv_bool("adv_pngopt",             "pngopt")
        _adv_bool("adv_auto_jpeg",          "auto_jpeg")
        if not hasattr(self, "adv_two_pass_fallback"): self.adv_two_pass_fallback = tk.BooleanVar(value=bool(ADVANCED_DEFAULTS.get("two_pass_fallback", True)))
        if not hasattr(self, "adv_auto_retry"):        self.adv_auto_retry        = tk.BooleanVar(value=bool(ADVANCED_DEFAULTS.get("auto_retry", True)))

        self.root.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.root, bg=APP_BG)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        self.title_label = ttk.Label(
            header, text="BitCrusher V9", style="Title.TLabel"
        )
        self.title_label.pack(side="left")

        self.root.grid_rowconfigure(1, weight=1)

        self.root.grid_rowconfigure(1, weight=1)
        content = tk.Frame(self.root, bg=APP_BG)
        content.grid(row=1, column=0, sticky="nsew")


        try:
            if hasattr(self, "animate_title"): self.animate_title()
        except Exception:
            pass
        self.root.bind("<FocusOut>", lambda e: getattr(self, "_pause_title", lambda: None)())
        self.root.bind("<FocusIn>",  lambda e: (getattr(self, "_pause_title", lambda: None)(),
                                                getattr(self, "animate_title",  lambda: None)()))

        ctrl = tk.Frame(content, bg=APP_BG)
        ctrl.pack(fill="x", padx=10, pady=(0,8))

        tk.Label(ctrl, text=self._t("lbl.preset","Preset:"), bg=APP_BG, fg=FG).pack(side="left")
        self.preset_combo = ttk.Combobox(
            ctrl,
            textvariable=self.preset_var,
            state="readonly",
            values=sorted(list(PRESETS.keys()))
        )
        self.preset_combo.pack(side="left", padx=(6,16))
        self.preset_combo.bind("<<ComboboxSelected>>",
            lambda _: getattr(self, "set_preset", lambda _=None: None)(self.preset_var.get())
        )

        tk.Label(ctrl, text=self._t("lbl.target_size","Target Size:"), bg=APP_BG, fg=FG).pack(side="left")

        self.size_unit_var = tk.StringVar(
            value=self.settings.get("size_unit","MB") if hasattr(self,"settings") and isinstance(self.settings,dict) else "MB"
        )

        size_frame = tk.Frame(ctrl, bg=APP_BG)
        size_frame.pack(side="left", padx=(6,16))

        ttk.Entry(size_frame, textvariable=self.target_size_var, width=7).pack(side="left")
        ttk.Combobox(
            size_frame,
            textvariable=self.size_unit_var,
            values=["KB","MB","GB","TB"],
            width=5,
            state="readonly"
        ).pack(side="left", padx=(6,0))


        
        tk.Entry(ctrl, textvariable=self.target_size_var, width=7).pack(side="left", padx=(6, 16))

        tk.Label(ctrl, text="Save to:", bg=APP_BG, fg=FG).pack(side="left")
        self.save_entry = tk.Entry(ctrl, textvariable=self.save_path, width=42)
        self.save_entry.pack(side="left", padx=6)
        ttk.Button(ctrl, text="Browse…", command=getattr(self, "select_save_folder", lambda: None)).pack(side="left", padx=(4, 0))

        main = tk.Frame(content, bg=APP_BG)   # was: tk.Frame(self.root, bg=APP_BG)
        main.pack(fill="both", expand=True, padx=10)

        left = tk.Frame(main, bg=CARD_BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        tk.Label(left, text=self._t("lbl.queue","Queue"), bg=CARD_BG, fg=FG, anchor="w").pack(fill="x", padx=10, pady=(10, 0))

        self.drop_frame = tk.Frame(left, bg=CARD_BG, bd=1, relief="solid", highlightthickness=0)
        self.drop_frame.pack(fill="both", expand=True, padx=10, pady=(6, 8))

        self.queue_box = tk.Listbox(
            self.drop_frame, selectmode="extended", activestyle="none",
            bg="#101215", fg=FG, highlightthickness=0, borderwidth=0
        )
        self.queue_box.pack(fill="both", expand=True, padx=6, pady=6)
        self.queue_box.bind("<<ListboxSelect>>", lambda e: update_preview(self))

        qbtns = tk.Frame(left, bg=CARD_BG); qbtns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(qbtns, text=self._t("btn.add_files","Add Files…"), command=getattr(self, "add_files", lambda: None)).pack(side="left")
        ttk.Button(qbtns, text=self._t("btn.remove_selected","Remove Selected"), command=getattr(self, "remove_selected", lambda: None)).pack(side="left", padx=6)
        ttk.Button(qbtns, text=self._t("btn.clear","Clear"), command=getattr(self, "clear_queue", lambda: None)).pack(side="left", padx=6)
        ttk.Button(qbtns, text="Move ↑", command=lambda: getattr(self, "move_selection", lambda *_: None)(-1)).pack(side="right")
        ttk.Button(qbtns, text=self._t("btn.move_down","Move ↓"), command=lambda: getattr(self, "move_selection", lambda *_: None)(+1)).pack(side="right", padx=6)

        try:
            if TkinterDnD and hasattr(self.root, "drop_target_register"):
                for w in (self.drop_frame, self.queue_box, self.root):
                    if hasattr(w, "drop_target_register"):
                        w.drop_target_register(DND_FILES)
                        w.dnd_bind("<<Drop>>", getattr(self, "drop_file_handler", lambda *_: None))
        except Exception:
            pass

        mid = tk.Frame(main, bg=CARD_BG)
        mid.pack(side="left", fill="both", expand=True, padx=6)
        tk.Label(mid, text=self._t("lbl.preview","Preview"), bg=CARD_BG, fg=FG, anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.preview_label = tk.Label(mid, bg="#101215", fg=FG, width=48, height=16, anchor="center")
        self.preview_label.pack(fill="both", expand=True, padx=10, pady=(6, 8))

        right = tk.Frame(main, bg=CARD_BG)
        right.pack(side="left", fill="y", padx=(6, 0))

        wb = tk.LabelFrame(right, text=self._t("panel.webhook","Webhook"), bg=CARD_BG, fg=FG, labelanchor="n")
        wb.pack(fill="x", padx=10, pady=(10, 6))
        tk.Label(wb, text=self._t("lbl.webhook_url","Discord/Webhook URL"), bg=CARD_BG, fg=FG_SUB).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Entry(wb, textvariable=self.webhook_var, width=34).pack(fill="x", padx=10, pady=(4, 8))

        wf = tk.LabelFrame(right, text=self._t("panel.watcher","Folder Watcher"), bg=CARD_BG, fg=FG, labelanchor="n")
        wf.pack(fill="x", padx=10, pady=6)
        self.watch_chk = tk.Checkbutton(
            wf, text=self._t("lbl.enable_watcher","Enable watcher"), variable=self.watch_var, onvalue=True, offvalue=False,
            bg=CARD_BG, fg=FG, activebackground=CARD_BG, activeforeground=FG, selectcolor=CARD_BG,
            command=getattr(self, "toggle_watch_folder", lambda: None)
        )
        self.watch_chk.pack(anchor="w", padx=10, pady=(6, 4))
        wrow = tk.Frame(wf, bg=CARD_BG); wrow.pack(fill="x", padx=10, pady=(0, 8))
        tk.Entry(wrow, textvariable=self.watch_folder, width=28).pack(side="left", fill="x", expand=True)
        ttk.Button(wrow, text=self._t("btn.browse","Browse…"), command=getattr(self, "browse_watch_folder", lambda: None)).pack(side="left", padx=6)

        pf = tk.LabelFrame(right, text=self._t("panel.profiles","Profiles"), bg=CARD_BG, fg=FG, labelanchor="n")
        pf.pack(fill="x", padx=10, pady=6)
        tk.Entry(pf, textvariable=self.profile_var).pack(fill="x", padx=10, pady=(6, 4))
        prow = tk.Frame(pf, bg=CARD_BG); prow.pack(fill="x", padx=10, pady=(0, 8))
        ttk.Button(prow, text=self._t("btn.save","Save"),  command=getattr(self, "save_profile",  lambda: None)).pack(side="left")
        ttk.Button(prow, text=self._t("btn.load","Load"),  command=getattr(self, "load_profile",  lambda: None)).pack(side="left", padx=6)

        adv_wrap = ttk.Frame(content, style="Card.TFrame")
        adv_wrap.pack(fill="x", padx=10, pady=(0, 8))

        ttk.Label(adv_wrap, text=self._t("panel.advanced","Advanced Options"), style="Sub.TLabel").pack(anchor="w", padx=10, pady=(6, 0))

        adv = ttk.Frame(adv_wrap, style="Card.TFrame")
        adv.pack(fill="x", padx=10, pady=(6, 8))

        adv_inner = ttk.Frame(adv, style="Card.TFrame")
        adv_inner.pack(fill="x")

        for i in range(4):
            adv_inner.columnconfigure(i, weight=0)
        adv_inner.columnconfigure(1, weight=1)
        adv_inner.columnconfigure(3, weight=1)

        ttk.Label(adv_inner, text=self._t("lbl.encoder","Encoder:"), style="Sub.TLabel").grid(row=0, column=0, padx=(0,8), pady=4, sticky="w")
        self.encoder_box = ttk.Combobox(
            adv_inner, textvariable=self.adv_encoder,
            values=["x264", "x265", "h264_nvenc", "hevc_nvenc", "av1"],
            width=14, state="readonly", style="Dark.TCombobox"
        )
        self.encoder_box.bind("<<ComboboxSelected>>", lambda e: self.save_settings())

        self.encoder_box.grid(row=0, column=1, padx=(0,16), pady=4, sticky="w")


        flags = ttk.Frame(adv_inner, style="Card.TFrame")
        flags.grid(row=0, column=2, columnspan=2, padx=0, pady=4, sticky="w")
        self.iterative_chk = ttk.Checkbutton(flags, text="Iterative", variable=self.iterative_var)
        self.iterative_chk.pack(side="left")
        self.two_pass_chk  = ttk.Checkbutton(flags, text="Two-pass", variable=self.two_pass_var)
        self.two_pass_chk.pack(side="left", padx=(10,0))

        ttk.Label(adv_inner, text=self._t("lbl.manual_crf","Manual CRF:"), style="Sub.TLabel").grid(row=1, column=0, padx=(0,8), pady=4, sticky="w")
        ttk.Entry(adv_inner, textvariable=self.manual_crf, width=8, style="Dark.TEntry").grid(row=1, column=1, padx=(0,16), pady=4, sticky="w")

        ttk.Label(adv_inner, text="Manual Bitrate (bps):", style="Sub.TLabel").grid(row=1, column=2, padx=(0,8), pady=4, sticky="w")
        ttk.Entry(adv_inner, textvariable=self.manual_bitrate, width=14, style="Dark.TEntry").grid(row=1, column=3, padx=0, pady=4, sticky="w")

        ttk.Label(adv_inner, text=self._t("lbl.prefix","Prefix:"), style="Sub.TLabel").grid(row=2, column=0, padx=(0,8), pady=4, sticky="w")
        ttk.Entry(adv_inner, textvariable=self.prefix_entry_var, width=12, style="Dark.TEntry").grid(row=2, column=1, padx=(0,16), pady=4, sticky="w")

        ttk.Label(adv_inner, text="Suffix:", style="Sub.TLabel").grid(row=2, column=2, padx=(0,8), pady=4, sticky="w")
        ttk.Entry(adv_inner, textvariable=self.suffix_entry_var, width=16, style="Dark.TEntry").grid(row=2, column=3, padx=0, pady=4, sticky="w")

        ttk.Label(adv_inner, text=self._t("lbl.audio","Audio:"), style="Sub.TLabel").grid(row=3, column=0, padx=(0,8), pady=4, sticky="w")
        self.audio_box = ttk.Combobox(
            adv_inner, textvariable=self.adv_audio_format,
            values=["aac","opus","mp3"], width=8, state="readonly", style="Dark.TCombobox"
        )
        self.audio_box.grid(row=3, column=1, padx=(0,16), pady=4, sticky="w")
        
        self.audio_box.bind("<<ComboboxSelected>>", lambda e: self.save_settings())

        ttk.Label(adv_inner, text="Image:", style="Sub.TLabel").grid(row=3, column=2, padx=(0,8), pady=4, sticky="w")
        self.image_box = ttk.Combobox(
            adv_inner, textvariable=self.adv_image_format,
            values=["jpg","png","webp"], width=8, state="readonly", style="Dark.TCombobox"
        )
        self.image_box.grid(row=3, column=3, padx=0, pady=4, sticky="w")
        
        self.image_box.bind("<<ComboboxSelected>>", lambda e: self.save_settings())

        flags2 = ttk.Frame(adv_inner, style="Card.TFrame")
        flags2.grid(row=4, column=0, columnspan=4, pady=(6,0), sticky="w")
        self.concurrent_chk   = ttk.Checkbutton(flags2, text="Concurrent",         variable=self.concurrent_var)
        self.auto_output_chk  = ttk.Checkbutton(flags2, text="Auto output folder", variable=self.auto_output_var)
        self.guetzli_chk      = ttk.Checkbutton(flags2, text="Guetzli (JPG)",      variable=self.guetzli_var)
        self.pngopt_chk       = ttk.Checkbutton(flags2, text="PNG opt",            variable=self.pngopt_var)
        self.auto_jpeg_chk    = ttk.Checkbutton(flags2, text="Auto JPEG",          variable=self.auto_jpeg_var)
        self.concurrent_chk.pack(side="left")
        self.auto_output_chk.pack(side="left", padx=(12,0))
        self.guetzli_chk.pack(side="left", padx=(12,0))
        self.pngopt_chk.pack(side="left", padx=(12,0))
        self.auto_jpeg_chk.pack(side="left", padx=(12,0))

        actions = tk.Frame(content, bg=APP_BG)
        actions.pack(fill="x", padx=10, pady=(0, 8))
        ttk.Button(actions, text=self._t("btn.start","Start Compression"), command=getattr(self, "start_compression", lambda: None)).pack(side="left")
        ttk.Button(actions, text=self._t("btn.stop","Stop"),              command=getattr(self, "stop_compression",  lambda: None)).pack(side="left", padx=6)
        ttk.Button(actions, text=self._t("btn.open_save",self._t("title.open_save_folder",self._t("title.open_save_folder","Open Save Folder"))),  command=getattr(self, "open_save_folder",  lambda: None)).pack(side="left", padx=6)
        ttk.Button(actions, text=self._t("btn.user_guide","User Guide"),        command=getattr(self, "show_user_guide",   lambda: None)).pack(side="right")

        logs = tk.Frame(content, bg=CARD_BG)
        logs.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        tk.Label(logs, text="Logs", bg=CARD_BG, fg=FG, anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.log_text = ScrolledText(logs, height=10, bg="#101215", fg=FG, insertbackground=FG, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(6, 8))

        self.log_widget = self.log_text
        self.log_widget = self.log_text
        bridge_gui_logger_color(self.log_widget)

        bridge_gui_logger(self.log_widget)

        if self.queue_box.size() == 0:
            self.preview_label.configure(text="No file selected", image="", compound="none")
        try:
            getattr(self, "set_preset", lambda *_: None)(self.preset_var.get())
        except Exception:
            pass

        try:
            self.webhook_url = self.webhook_var.get()
        except Exception:
            pass








    def _pause_title(self, *_):
        job = getattr(self, "_title_job", None)
        if job:
            self.root.after_cancel(job)
            self._title_job = None


    def download_from_youtube(self):
        
        from tkinter import simpledialog, messagebox

        url = simpledialog.askstring("YouTube Download", "Enter YouTube URL:")
        if not url:
            return

        choice = simpledialog.askstring(
            "Format",
            "Choose download format:\n• audio\n• video\n• audio+video"
        )
        if not choice:
            return
        choice = choice.strip().lower()
        if choice not in ("audio", "video", "audio+video"):
            messagebox.showerror("Invalid Choice", "Enter exactly: audio, video, or audio+video.")
            return

        temp_dir = tempfile.mkdtemp(prefix="yt_")
        if choice == "audio":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s")
            }
        elif choice == "video":
            ydl_opts = {
                "format": "bestvideo/best",
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s")
            }
        else:  # audio+video
            ydl_opts = {
                "format": "best",
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s")
            }

        self.update_status(f"⬇️ Downloading from YouTube: {url} ({choice})")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_path = ydl.prepare_filename(info)
        except Exception as e:
            self.log_error(f"YouTube download failed: {e}")
            messagebox.showerror("Download Error", str(e))
            return

        save_dir = self.save_path.get()
        try:
            tgt_size = int(self.target_size.get())
        except ValueError:
            from __main__ import MAX_SIZE_MB_DEFAULT
            tgt_size = MAX_SIZE_MB_DEFAULT

        adv_opts = self.gather_advanced_options()
        threading.Thread(
            target=lambda: self._compress_downloaded(downloaded_path, save_dir, tgt_size, adv_opts),
            daemon=True
        ).start()

    def _compress_downloaded(self, input_path, save_dir, target_size_mb, adv_opts):
        

        self.update_status(f"🚀 Compressing downloaded file: {input_path}")
        target_size_bytes = target_size_mb * 1024 * 1024
        actual_size = os.path.getsize(input_path)
        if actual_size <= target_size_bytes:
            self.update_status(f"⚡ Skipping compression — file is {format_bytes(actual_size)}, under target.")
            shutil.copy(input_path, os.path.join(save_dir, os.path.basename(input_path)))
            return
        stats = auto_compress(
            input_path,
            save_dir,
            self.update_status,    # callback writes to your on-screen log :contentReference[oaicite:2]{index=2}
            target_size_mb,
            "",                    # no webhook for YT downloads
            adv_opts,
            lambda: False          # never cancel
        )

        if not stats:
            return

        orig = stats.get("original_size", 0)
        comp = stats.get("compressed_size", 0)
        ratio = comp / orig if orig else 0
        took  = stats.get("time_taken", stats.get("duration", 0))

        def insert_row():
            self.stats_table.insert("", "end", values=(
                os.path.basename(input_path),
                format_bytes(orig),
                format_bytes(comp),
                f"{ratio:.2f}",
                f"{took:.1f}"
            ))
        self.root.after(0, insert_row)

    def start_youtube_download(self):
        
        url = self.yt_url_var.get().strip()
        fmt = self.yt_format_var.get().strip().lower()
        if not url or fmt not in ("audio", "video", "audio+video"):
            self.log_error("Invalid YouTube URL or format")
            return

        threading.Thread(
            target=self.download_from_youtube,
            args=(url, fmt),
            daemon=True
        ).start()

    def download_from_youtube(self, url, choice):
        
        temp_dir = tempfile.mkdtemp(prefix="yt_")
        ydl_opts = {"outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s")}
        if choice == "audio":
            ydl_opts["format"] = "bestaudio/best"
        elif choice == "video":
            ydl_opts["format"] = "bestvideo/best"
        else:  # audio+video
            ydl_opts["format"] = "best"

        self.update_status(f"⬇️ Downloading from YouTube: {url} ({choice})")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_path = ydl.prepare_filename(info)
        except Exception as e:
            self.log_error(f"YouTube download failed: {e}")
            return

        save_dir = self.save_path.get()
        try:
            tgt_size = int(self.target_size.get())
        except ValueError:
            from __main__ import MAX_SIZE_MB_DEFAULT
            tgt_size = MAX_SIZE_MB_DEFAULT

        adv_opts = self.gather_advanced_options()
        self._compress_downloaded(downloaded_path, save_dir, tgt_size, adv_opts)



    def drop_file_handler(self, raw_data):
        

        self.logger.debug(f"Raw DnD drop data: {raw_data}")

        paths = parse_dnd_files(raw_data if isinstance(raw_data, str) else "")

        for p in paths:
            if os.path.isfile(p):
                self.logger.info(f"Adding dropped file to queue: {p}")

                self.queue_files([p])
            else:
                self.logger.warning(f"Dropped item is not a file: {p}")






    def start_compression(self):
        
        if getattr(self, "compression_running", False):
            self.update_status("Compression already running.", level="WARNING")
            return

        try:
            target_bytes = int(self._get_target_bytes())
        except Exception:
            target_bytes = 10 * 1024 * 1024  # 10 MB fallback
        save_dir = getattr(self, "save_path_var", None)
        save_dir = save_dir.get() if hasattr(save_dir, "get") else getattr(self, "output_dir", "")

        try:
            snapshot = [self.queue_box.get(i) for i in range(self.queue_box.size())]
        except Exception:
            snapshot = list(getattr(self, "file_list", []) or [])

        norm = [_normalize_drop_path(p) for p in snapshot if isinstance(p, str)]
        files = [p for p in norm if os.path.isfile(p)]

        if not files:
            self.update_status("No valid files to process (queue empty or paths invalid).", level="ERROR")
            try:
                from tkinter import messagebox as mbox
                mbox.showerror("BitCrusher", "No valid files to process.\nAdd files to the queue first.")
            except Exception:
                pass
            return

        try:
            snapshot = [self.queue_box.get(i) for i in range(self.queue_box.size())]
        except Exception:
            snapshot = list(getattr(self, "file_list", []) or [])
        norm = [_normalize_drop_path(p) for p in snapshot if isinstance(p, str)]
        files = [p for p in norm if os.path.isfile(p)]
        if not files:
            self.update_status("No valid files to process (queue empty or paths invalid).", level="ERROR")
            try:
                from tkinter import messagebox as mbox
                mbox.showerror("BitCrusher", "No valid files to process.\nAdd files to the queue first.")
            except Exception:
                pass
            return

        save_dir = ""
        try:
            save_dir = (self.save_path.get() if hasattr(self, "save_path") else "").strip()
        except Exception:
            save_dir = ""
        if not save_dir:
            save_dir = os.path.dirname(files[0]) or os.getcwd()

        self._thread_target_bytes = int(target_bytes)
        self._thread_save_path = save_dir
        self._thread_file_list = files[:]  # immutable snapshot

        self.update_status(f"Starting encode @ target ~{human_bytes(self._thread_target_bytes)}", level="INFO")
        try:
            self.ensure_progress_bars()
            try:
                self.progress.stop()
            except Exception:
                pass
            self.progress["mode"] = "determinate"
            self.progress["maximum"] = max(1, len(files))
            self.progress["value"] = 0
        except Exception:
            pass

        self.compression_running = True
        th = threading.Thread(target=self.compress_all, name="compress_all", daemon=True)
        th.start()
        self.update_status(f"Worker started for {len(files)} file(s).", level="DEBUG")

        def _prep_after_start():
            try:
                self.ensure_progress_bars()

                try:
                    total = max(1, len(self._thread_file_list))
                    self.progress["maximum"] = total
                    self.progress["value"] = 0
                    try:
                        self.progress.stop()
                    except Exception:
                        pass
                except Exception:
                    pass

                try:
                    self.update_status(f"Starting compression for {len(self._thread_file_list)} file(s)…", level="INFO")
                except Exception:
                    pass
            except Exception:
                pass
        self.root.after(0, _prep_after_start)

        logging.info(f"[GUI] Launching compression thread. files={len(self._thread_file_list)} save_dir={self._thread_save_path}")


    def drop_file_handler(self, data):
        

        paths = parse_dnd_files(data if isinstance(data, str) else "")
        for p in paths:
            if os.path.isfile(p):

                self.queue_files([p])




    def __init__(self, root=None):
        import tkinter as tk
        from pathlib import Path
        import os, sys, platform, threading, logging
        from win10toast import ToastNotifier

        self.logger = setup_logging()
        if root is None:

            try:
                from tkinterdnd2 import TkinterDnD
                root = TkinterDnD.Tk() if TkinterDnD else tk.Tk()
            except Exception:
                root = tk.Tk()
        self.root = root

        try:
            import tkinter as tk
            if not hasattr(self, "theme_var"):
                self.theme_var = tk.StringVar(value="Dark")
        except Exception:
            pass

        self.iterative_var     = tk.BooleanVar(value=False)
        self.two_pass_var      = tk.BooleanVar(value=False)
        self.concurrent_var    = tk.BooleanVar(value=False)
        self.auto_output_var   = tk.BooleanVar(value=False)
        self.guetzli_var       = tk.BooleanVar(value=False)
        self.pngopt_var        = tk.BooleanVar(value=False)
        self.auto_jpeg_var     = tk.BooleanVar(value=False)

        self.webhook_var       = tk.StringVar(value="")
        self.watch_var         = tk.BooleanVar(value=False)
        self.watch_folder      = tk.StringVar(value="")
        self.profile_var       = tk.StringVar(value="")

        self.manual_crf        = tk.StringVar(value="")
        self.manual_bitrate    = tk.StringVar(value="")
        self.prefix_entry_var  = tk.StringVar(value="")
        self.suffix_entry_var  = tk.StringVar(value="_discord_ready")

        self.encoder_var       = tk.StringVar(value="x265")
        self.audio_fmt_var     = tk.StringVar(value="opus")
        self.image_fmt_var     = tk.StringVar(value="jpg")
        
        self.style = ttk.Style(self.root)   # don't apply yet; we’ll apply after loading settings

        self.settings_dir  = USER_SETTINGS_DIR  # e.g. .../tescompressor3/user_settings
        os.makedirs(self.settings_dir, exist_ok=True)
        self.settings_path = os.path.join(self.settings_dir, "settings.json")

        self.settings = {
            "output_dir": str(Path.home()),
            "watch_folder": "",
            "enable_watch": False,
            "preset": list(PRESETS.keys())[0],
            "target_size": MAX_SIZE_MB_DEFAULT,
            "webhook_url": ""
        }
        try:
            if os.path.isfile(self.settings_path):
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.saved_profiles = dict((self.settings or {}).get("profiles", {}))
                    chosen = (self.settings or {}).get("theme", "Dark")
                    self.theme_var = tk.StringVar(value=chosen)
                    apply_theme(self.style, chosen)

                    if not hasattr(self, "theme_var"):
                        self.theme_var = tk.StringVar(value="Dark")

                    self.queue_container  = getattr(self, "queue_container",  self.main_left if hasattr(self, "main_left") else self.root)
                    self.log_container    = getattr(self, "log_container",    self.log_text if hasattr(self, "log_text") else self.root)
                    self.preview_container= getattr(self, "preview_container",self.preview_label if hasattr(self, "preview_label") else self.root)

                    init_aesthetics(self)

                    self.root.configure(bg=APP_BG)
                    retheme_runtime(self, self.style, chosen)

                    self.THEMES = THEMES
                    self.apply_theme = apply_theme
                    self.retheme_runtime = retheme_runtime
                    self.fade_window = fade_window


        except Exception:
            pass

        if not hasattr(self, "webhook_var"):
            self.webhook_var  = tk.StringVar(value=getattr(self, "webhook_url", "") or "")
            self.webhook_url  = self.webhook_var  # keep old code working

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        if hasattr(self, "ensure_tray_icon"):
            self.ensure_tray_icon(start_if_needed=False)

        try:
            self.root.tk.eval('package require tkdnd')
        except Exception:
            pass

        self.root.withdraw()  # hide until setup is complete

        self.BASE_DIR = os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False)
            else os.path.abspath(__file__)
        )

        self.cancel_flag     = False
        self.file_list       = []
        self.stats_list      = []
        self.save_path       = tk.StringVar(value=str(Path.home()))
        self.target_size_var = tk.StringVar(value=str(MAX_SIZE_MB_DEFAULT))
        self.preset_var      = tk.StringVar(value=list(PRESETS.keys())[0])

        self.selected_preset = self.preset_var
        self.target_size     = self.target_size_var

        self.webhook_url     = tk.StringVar(value="")
        self.use_webhook     = tk.IntVar(value=0)

        self.adv_encoder     = tk.StringVar(value=ADVANCED_DEFAULTS["encoder"])
        self.adv_iterative   = tk.IntVar(value=1 if ADVANCED_DEFAULTS["iterative"] else 0)
        self.adv_two_pass    = tk.IntVar(value=1 if ADVANCED_DEFAULTS["two_pass"] else 0)
        self.adv_manual_crf  = tk.StringVar(value=ADVANCED_DEFAULTS["manual_crf"])
        self.adv_manual_bitrate = tk.StringVar(value=ADVANCED_DEFAULTS["manual_bitrate"])
        self.adv_output_prefix  = tk.StringVar(value=ADVANCED_DEFAULTS["output_prefix"])
        self.adv_output_suffix  = tk.StringVar(value=ADVANCED_DEFAULTS["output_suffix"])
        self.adv_audio_format   = tk.StringVar(value=ADVANCED_DEFAULTS["audio_format"])
        self.adv_image_format   = tk.StringVar(value=ADVANCED_DEFAULTS["image_format"])
        self.adv_concurrent     = tk.IntVar(value=1 if ADVANCED_DEFAULTS["concurrent"] else 0)
        self.adv_auto_output    = tk.IntVar(value=1 if ADVANCED_DEFAULTS["auto_output_folder"] else 0)
        self.adv_guetzli        = tk.IntVar(value=1 if ADVANCED_DEFAULTS["guetzli"] else 0)
        self.adv_pngopt         = tk.IntVar(value=1 if ADVANCED_DEFAULTS["pngopt"] else 0)
        self.adv_auto_jpeg      = tk.IntVar(value=1 if ADVANCED_DEFAULTS["auto_jpeg"] else 0)
        self.adv_grain_filter   = tk.IntVar(value=1 if ADVANCED_DEFAULTS.get("grain_filter", True) else 0)

        self.log_filter_var = tk.StringVar(value="INFO")
        self.profile_var    = tk.StringVar(value="")
        self.av_format_var  = tk.StringVar(value="audio+video")

        self.watch_folder   = tk.StringVar(value="")
        self.enable_watch   = tk.BooleanVar(value=False)

        self.save_path.set(self.settings.get("output_dir", self.save_path.get()))
        self.watch_folder.set(self.settings.get("watch_folder", self.watch_folder.get()))
        self.enable_watch.set(self.settings.get("enable_watch", False))

        self.enable_watch_compress = self.enable_watch

        self.notifier  = ToastNotifier()
        self.all_logs  = []
        self.stop_event = threading.Event()
        self.settings_path = os.path.join(USER_SETTINGS_DIR, "settings.json")

        self.setup_directories()
        self.setup_style()
        self.setup_ui()
        self.setup_drag_and_drop()

        minimized_startup = "--minimized" in sys.argv
        try:
            if minimized_startup and platform.system() == "Windows":
                self.root.withdraw()
            else:
                self.root.deiconify()
        except tk.TclError:
            logging.warning("Tried to show window after it was destroyed.")

        self.root.title("BitCrusher V9")
        self.root.resizable(True, True)
        self.root.geometry("1200x800")
        self.root.configure(bg="#2C2F33")

        self.log_info("Running Good!")
        self.log_warn("File migth have some issues")
        self.log_error("Compression failed")
        self.log_debug("ffmpeg args: ['-vcodec', 'libx264']")
        self.log_critical("Programm migth crash")
        self.log_exception("Exception caught during extraction.")
        self.default_crf = DEFAULT_CRF

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_file_handler)

        self.settings = self.load_settings()
        self.preset_var.set(self.settings.get("preset", list(PRESETS.keys())[0]))
        self.target_size_var.set(self.settings.get("target_size", str(MAX_SIZE_MB_DEFAULT)))
        if "size_unit" in data:
            try: self.size_unit_var.set(data["size_unit"])
            except Exception: pass

        import tkinter as tk  # ensure tk is in scope here

        self.webhook_var = tk.StringVar(value=self.settings.get("webhook_url", ""))
        self.webhook_url = self.webhook_var.get()

        def _sync_webhook_from_var(*_):
            try:
                self.webhook_url = self.webhook_var.get()
            except Exception:
                pass
        self.webhook_var.trace_add("write", lambda *_: _sync_webhook_from_var())

        self.use_webhook.set(self.settings.get("use_webhook", 0))
        adv = self.settings.get("advanced", {})
        self.adv_encoder.set(adv.get("encoder", "x264"))
        self.adv_iterative.set(1 if adv.get("iterative") else 0)
        self.adv_two_pass.set(1 if adv.get("two_pass") else 0)
        self.adv_manual_crf.set(adv.get("manual_crf", ""))
        self.adv_manual_bitrate.set(adv.get("manual_bitrate", ""))
        self.adv_output_prefix.set(adv.get("output_prefix", ""))
        self.adv_output_suffix.set(adv.get("output_suffix", "_discord_ready"))
        self.adv_audio_format.set(adv.get("audio_format", "aac"))
        self.adv_image_format.set(adv.get("image_format", "jpg"))
        self.adv_concurrent.set(1 if adv.get("concurrent") else 0)
        self.adv_auto_output.set(1 if adv.get("auto_output_folder") else 0)
        self.adv_guetzli.set(1 if adv.get("guetzli") else 0)
        self.adv_pngopt.set(1 if adv.get("pngopt") else 0)
        self.adv_auto_jpeg.set(1 if adv.get("auto_jpeg") else 0)
        self.save_path.set(self.settings.get("output_dir", ""))

        heur_path = os.path.join(HEURISTICS_DIR, "heuristics.json")
        self.heuristic = HeuristicLearner(heur_path)

        self.webhook = DiscordWebhookClient(self.settings.get("webhook_url", ""))

        self.watch_folders = self.settings.get("watch_folders", [])
        self.watcher = FolderWatcher(
            on_file_ready=lambda fp: self._enqueue_from_watcher(fp),
            status_cb=lambda m: self.update_status(m, level="INFO"),
            notify_cb=lambda title, msg: notify_info(title, msg),
            exts=(".mp4", ".mkv", ".mov", ".avi", ".webm",
                  ".mp3", ".flac", ".wav", ".m4a", ".aac",
                  ".jpg", ".jpeg", ".png", ".gif", ".webp"),
            min_bytes=1024,
            ignore_globs=("*.part", "*.tmp", "~$*", "*.crdownload", "*.download"),
            stable_secs=1.25
        )

        for _p in (self.watch_folders or []):
            try:
                self.watcher.add_path(_p)
            except Exception:
                pass

        if self.settings.get("watch_enabled", False):
            self.watcher.start()

        self.watch_folder.set(self.settings.get("watch_folder", ""))
        self.enable_watch.set(self.settings.get("enable_watch", False))

        self.setup_tray_icon()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        if self.enable_watch.get():
            self.start_folder_watcher()
        self.setup_menu()
        self.check_dependencies()

        self.tray_icon = None
        self._tray_icon_ready = False
        self._tray_thread = None






    def _notify(self, title, msg, duration=5, icon_path=None):
        threading.Thread(target=lambda: self.notifier.show_toast(title, msg,
                                      icon_path=icon_path, duration=duration),
                         daemon=True).start()

    def select_files(self):
        from tkinter import filedialog
        files = filedialog.askopenfilenames(
            title="Select media files",
            filetypes=[
                ("Video", "*.mp4 *.mov *.avi *.mkv"),
                ("Audio", "*.mp3 *.wav *.flac *.aac"),
                ("Image", "*.jpg *.png *.gif *.bmp")
            ]
        )
        if files:

            self.queue_files(files)


    def setup_drag_and_drop(self):

        widgets = [self.drop_frame, self.queue_box]  # add more if needed

        for w in widgets:
            try:

                ok = False
                try:
                    ver = self.root.tk.call('package', 'require', 'tkdnd')
                    ok = bool(ver)
                except Exception:
                    ok = False

                if ok:
                    from tkinterdnd2 import DND_FILES
                    w.drop_target_register(DND_FILES)
                    w.dnd_bind('<<Drop>>', lambda e: self.drop_file_handler(e.data))
                else:

                    pass
            except Exception as e:

                self.logger.warning(f"Drag-and-drop disabled on this widget: {e}")




    def setup_tray_icon(self):

        icon_path = resource_path("icon.png")
        image = Image.open(resource_path("icon.png"))
        menu = pystray.Menu(
            pystray.MenuItem("Show BitCrusher", self.on_show),
            pystray.MenuItem("Quit",         self.on_quit)
        )
        self.tray = pystray.Icon("BitCrusher", image, "BitCrusher V10", menu)

        threading.Thread(target=self.tray.run, daemon=True).start()

    def on_exit(self):
        
        try:
            self.save_settings()
        except Exception:
            pass
        try:
            self.stop_folder_watcher()
        except Exception:
            pass
        try:
            self.root.quit()   # let mainloop() return
        except Exception:
            pass
        return 0

    def on_quit(self, icon=None, item=None):
        
        try:
            self.save_settings()
        except Exception:
            pass
        try:
            self.root.after(0, self._shutdown_and_exit)
        except Exception:
            self._shutdown_and_exit()

    def on_close(self):
        
        from tkinter import messagebox
        try:
            resp = messagebox.askyesnocancel(
                "Close or Minimize?",
                "Do you want to exit the app?\n\nYes = Exit\nNo = Minimize to tray\nCancel = Keep running"
            )
        except Exception:
            resp = True
        if resp is True:
            self._shutdown_and_exit()
        elif resp is False:
            try:
                self.ensure_tray_icon(start_if_needed=True)
                self.root.iconify()
            except Exception:
                pass
        else:
            return

    def ensure_tray_icon(self, start_if_needed=False):
        
        if getattr(self, "_tray_icon_ready", False):
            return
        try:
            import pystray
            from PIL import Image, ImageDraw
        except Exception:
            self._tray_icon_ready = False
            return

        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        drw = ImageDraw.Draw(img)
        drw.ellipse((4, 4, 28, 28), fill=(0, 122, 204, 255))

        def _restore(_icon=None, _item=None):
            self.root.after(0, self.restore_from_tray)

        def _exit(_icon=None, _item=None):
            self.root.after(0, self._shutdown_and_exit)

        menu = pystray.Menu(
            pystray.MenuItem("Restore", _restore, default=True),
            pystray.MenuItem("Exit", _exit)
        )
        self.tray_icon = pystray.Icon("compressor_gui", img, "Compressor", menu)

        if start_if_needed and not getattr(self, "_tray_thread", None):
            import threading
            self._tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            self._tray_thread.start()
        self._tray_icon_ready = True

    def restore_from_tray(self):
        
        try:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        except Exception:
            pass
        try:
            if getattr(self, "tray_icon", None):
                self.tray_icon.stop()
        except Exception:
            pass
        finally:
            self._tray_icon_ready = False
            self._tray_thread = None

    def _shutdown_and_exit(self):
        
        if getattr(self, "_shutting_down", False):
            return
        self._shutting_down = True

        try:
            self.save_settings()
        except Exception:
            pass
        try:
            self.stop_folder_watcher()
        except Exception:
            pass
        try:
            if getattr(self, "tray_icon", None):

                try:
                    self.tray_icon.stop()
                except Exception:
                    pass
        except Exception:
            pass

        try:
            self.root.quit()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

        try:
            import os
            os._exit(0)
        except Exception:
            pass







    def on_show(self, icon, item):
        
        try:
            self.root.deiconify()
        except (tk.TclError, RuntimeError):
            logging.warning("Tried to show window from tray, but it was already destroyed.")
        return 0

    def on_quit(self, icon=None, item=None):
        try:
            self.save_settings()
        except Exception:
            pass

        try:
            self.root.after(0, self._shutdown_and_exit)
        except Exception:
            self._shutdown_and_exit()


    def log_info(self, msg):
        if hasattr(self, "logger"):
            self.logger.info(msg)

    def log_warn(self, msg):
        if hasattr(self, "logger"):
            self.logger.warning(msg)

    def log_error(self, msg):
        if hasattr(self, "logger"):
            self.logger.error(msg)

    def log_debug(self, msg):
        if hasattr(self, "logger"):
            self.logger.debug(msg)

    def log_critical(self, msg):
        if hasattr(self, "logger"):
            self.logger.critical(msg)

    def log_exception(self, msg):
        if hasattr(self, "logger"):
            self.logger.exception(msg)

    def select_output_dir(self):
        

        directory = filedialog.askdirectory(
            parent=self.root,
            title="Select Output Folder"
        )
        if directory:

            self.save_path.set(directory)

            self.log_info(f"Save folder set to: {directory}")

    def open_advanced(self):
        
        self.open_advanced_options()


        
    def queue_file(self, filepath):

        self.queue_files([filepath])


    def _enqueue_from_watcher(self, filepath: str):
        try:
            self.queue_add(filepath)
            self.log(f"Queued via Watcher: {filepath}")
            try:
                notify_info("BitCrusher", f"Queued via Watcher:\n{os.path.basename(filepath)}", duration=4)
            except Exception:
                pass
        except Exception:
            self.log("Watcher enqueue failed", level="ERROR")



    def queue_files(self, filepaths):
        
        for filepath in filepaths:
            if (
                os.path.isfile(filepath)
                and get_media_type(filepath) != "unknown"
                and filepath not in self.file_list
            ):
                _norm = _normalize_drop_path(filepath)
                try:
                    if not hasattr(self, "file_list"):
                        self.file_list = []
                    if _norm not in self.file_list:
                        self.file_list.append(_norm)
                except Exception:
                    pass
                self.queue_box.insert("end", _norm)





    def make_responsive(self):
        

        for r in range(6):
            self.root.grid_rowconfigure(r, weight=0)

        self.root.grid_rowconfigure(1, weight=3)  # drop+queue+preview
        self.root.grid_rowconfigure(4, weight=2)  # stats table
        self.root.grid_rowconfigure(5, weight=1)  # log pane

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)


    def clear_queue(self):
        self.file_queue.clear()
        self.queue_listbox.delete(0, tk.END)

    def setup_menu(self):
        import tkinter as tk

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=self._t("menu.clear_queue","Clear Queue"), command=self.clear_queue)
        file_menu.add_command(label=self._t("menu.exit","Exit"), command=self.on_exit)
        menubar.add_cascade(label=self._t("menu.file","File"), menu=file_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label=self._t("menu.configure_paths","Configure Paths"), command=self.open_settings_dialog)
        settings_menu.add_command(label=self._t("menu.save_profile","Save Profile"), command=self.save_profile)
        settings_menu.add_command(label=self._t("menu.load_profile","Load Profile"), command=self.load_profile)
        menubar.add_cascade(label=self._t("menu.settings","Settings"), menu=settings_menu)

        themes_menu = tk.Menu(menubar, tearoff=0)
        for name in list(THEMES.keys()):
            themes_menu.add_radiobutton(
                label=name,
                variable=self.theme_var,
                value=name,
                command=lambda n=name: self._on_theme_select(n)
            )
        themes_menu.add_separator()
        themes_menu.add_command(label=self._t("menu.theme_lab","Theme Lab…"), command=lambda: open_theme_lab(self))
        themes_menu.add_command(label=self._t("menu.save_theme","Save Current Theme…"), command=lambda: save_current_theme_as(self))
        themes_menu.add_command(label=self._t("menu.load_theme","Load Theme JSON…"), command=lambda: load_custom_theme(self))
        menubar.add_cascade(label=self._t("menu.themes","Themes"), menu=themes_menu)

        guide_menu = tk.Menu(menubar, tearoff=0)
        guide_menu.add_command(label=self._t("menu.user_guide","User Guide"), command=self.show_user_guide)
        menubar.add_cascade(label=self._t("menu.guide","Guide"), menu=guide_menu)

        viewm = tk.Menu(menubar, tearoff=0)
        viewm.add_command(label=self._t("menu.dashboard","Dashboard"), command=self.show_dashboard)
        menubar.add_cascade(label=self._t("menu.view","View"), menu=viewm)

        lang_menu = tk.Menu(menubar, tearoff=0)
        for code, native in LANG_CODES:
            lang_menu.add_radiobutton(
                label=native,
                variable=self.lang_var,
                value=code,
                command=self._on_language_change
            )
        lang_menu.add_separator()
        lang_menu.add_command(label=self._t("menu.open_i18n_folder","Open i18n Folder…"),
                              command=lambda: _open_folder(_i18n_dir()))
        lang_menu.add_command(label=self._t("menu.export_lang_templates","Export Language Templates…"),
                              command=lambda: (_export_lang_templates([c for c,_ in LANG_CODES if c!="en"]),
                                               _open_folder(_i18n_dir())))
        menubar.add_cascade(label=self._t("menu_language","Language"), menu=lang_menu)

        self.root.config(menu=menubar)
        init_aesthetics(self)

        try:
            items = [menubar.entrycget(i, "label") for i in range(menubar.index("end")+1)]
            LOG.info("Menubar entries: %s", items)
        except Exception:
            pass

    def show_dashboard(self):
        
        import tkinter as tk
        from tkinter import ttk

        if getattr(self, "_dash_win", None) and tk.Toplevel.winfo_exists(self._dash_win):
            try:
                self._dash_win.lift()
                self._dash_win.focus_force()
            except Exception:
                pass
            return

        win = tk.Toplevel(self.root)
        self._dash_win = win
        win.title("BitCrusher — Dashboard")
        win.geometry("520x360")
        win.resizable(False, False)

        container = ttk.Frame(win, padding=12)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Runtime Metrics", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        rows = [
            ("Queue (pending)", "queue_pending"),
            ("Processing", "processing"),
            ("Processed (this run)", "processed"),
            ("Average Size Ratio", "avg_ratio"),
            ("Average Time / File", "avg_time"),
            ("Watcher", "watcher"),
            ("Watched Folders", "watch_dirs"),
            ("Webhook", "webhook"),
        ]
        self._dash_vars = {}
        r = 1
        for label, key in rows:
            ttk.Label(container, text=label + ":").grid(row=r, column=0, sticky="w", padx=(0, 10), pady=4)
            var = tk.StringVar(value="—")
            self._dash_vars[key] = var
            ttk.Label(container, textvariable=var).grid(row=r, column=1, sticky="w", pady=4)
            r += 1

        ttk.Separator(container).grid(row=r, column=0, columnspan=2, sticky="ew", pady=(10, 8))
        r += 1
        ttk.Button(container, text="Close", command=win.destroy).grid(row=r, column=1, sticky="e")

        def _queue_len():
            for attr in ("queue_files", "file_queue", "files_to_process", "pending_files", "queued_files"):
                q = getattr(self, attr, None)
                if isinstance(q, (list, tuple, set)):
                    return len(q)
                if hasattr(q, "__len__"):
                    try:
                        return len(q)
                    except Exception:
                        pass
            return 0

        def _is_processing():
            for attr in ("_is_processing", "is_processing", "processing"):
                v = getattr(self, attr, None)
                if isinstance(v, bool):
                    return v
            for attr in ("_worker_running", "worker_running"):
                v = getattr(self, attr, None)
                if isinstance(v, bool):
                    return v
            return False

        def _processed_count():
            lst = getattr(self, "stats_list", None)
            return len(lst) if isinstance(lst, list) else 0

        def _avg_ratio_and_time():
            lst = getattr(self, "stats_list", None)
            if not isinstance(lst, list) or not lst:
                return ("—", "—")
            ratios, times = [], []
            for rec in lst:
                try:
                    if "ratio" in rec:
                        ratios.append(float(rec["ratio"]))
                    elif "original_size" in rec and "compressed_size" in rec:
                        o = float(rec["original_size"]) or 1.0
                        c = float(rec["compressed_size"])
                        ratios.append(c / o)
                    if "time_taken" in rec:
                        times.append(float(rec["time_taken"]))
                except Exception:
                    pass
            avg_r = (sum(ratios) / len(ratios)) if ratios else None
            avg_t = (sum(times) / len(times)) if times else None
            r_txt = f"{avg_r*100:.1f}%" if isinstance(avg_r, float) else "—"
            t_txt = f"{avg_t:.2f}s" if isinstance(avg_t, float) else "—"
            return (r_txt, t_txt)

        def _watcher_status():
            enabled = bool(self.settings.get("watch_enabled", False))
            active = False
            try:
                w = getattr(self, "watcher", None)
                active = bool(getattr(w, "_running", False))
            except Exception:
                pass
            return "On (active)" if enabled and active else ("On (idle)" if enabled else "Off")

        def _watch_dirs():
            try:
                dirs = list(self.settings.get("watch_folders", []) or [])
            except Exception:
                dirs = []
            return str(len(dirs)) if dirs else "0"

        def _webhook_status():
            url = ""
            try:
                url = self.settings.get("webhook_url", "") or getattr(self, "webhook_url_var", None).get()
            except Exception:
                pass
            if url:
                masked = url[:40] + "…" if len(url) > 41 else url
                return f"Configured ({masked})"
            return "Not set"

        def _refresh():
            try:
                self._dash_vars["queue_pending"].set(str(_queue_len()))
                self._dash_vars["processing"].set("Yes" if _is_processing() else "No")
                self._dash_vars["processed"].set(str(_processed_count()))
                r_txt, t_txt = _avg_ratio_and_time()
                self._dash_vars["avg_ratio"].set(r_txt)
                self._dash_vars["avg_time"].set(t_txt)
                self._dash_vars["watcher"].set(_watcher_status())
                self._dash_vars["watch_dirs"].set(_watch_dirs())
                self._dash_vars["webhook"].set(_webhook_status())
            except Exception:
                pass
            try:
                win.after(1000, _refresh)
            except Exception:
                pass

        _refresh()



    def show_dashboard(self):
        
        import tkinter as tk
        from tkinter import ttk

        if getattr(self, "_dash_win", None) and tk.Toplevel.winfo_exists(self._dash_win):
            try:
                self._dash_win.lift()
                self._dash_win.focus_force()
            except Exception:
                pass
            return

        win = tk.Toplevel(self.root)
        self._dash_win = win
        win.title("BitCrusher — Dashboard")
        win.geometry("520x360")
        win.resizable(False, False)

        container = ttk.Frame(win, padding=12)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Runtime Metrics", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        rows = [
            ("Queue (pending)", "queue_pending"),
            ("Processing", "processing"),
            ("Processed (this run)", "processed"),
            ("Average Size Ratio", "avg_ratio"),
            ("Average Time / File", "avg_time"),
            ("Watcher", "watcher"),
            ("Watched Folders", "watch_dirs"),
            ("Webhook", "webhook"),
        ]
        self._dash_vars = {}
        r = 1
        for label, key in rows:
            ttk.Label(container, text=label + ":").grid(row=r, column=0, sticky="w", padx=(0, 10), pady=4)
            var = tk.StringVar(value="—")
            self._dash_vars[key] = var
            ttk.Label(container, textvariable=var).grid(row=r, column=1, sticky="w", pady=4)
            r += 1

        ttk.Separator(container).grid(row=r, column=0, columnspan=2, sticky="ew", pady=(10, 8))
        r += 1
        ttk.Button(container, text="Close", command=win.destroy).grid(row=r, column=1, sticky="e")

        def _queue_len():

            for attr in ("queue_files", "file_queue", "files_to_process", "pending_files", "queued_files"):
                q = getattr(self, attr, None)
                if isinstance(q, (list, tuple, set)):
                    return len(q)

                if hasattr(q, "__len__"):
                    try:
                        return len(q)
                    except Exception:
                        pass
            return 0

        def _is_processing():
            for attr in ("_is_processing", "is_processing", "processing"):
                v = getattr(self, attr, None)
                if isinstance(v, bool):
                    return v

            for attr in ("_worker_running", "worker_running"):
                v = getattr(self, attr, None)
                if isinstance(v, bool):
                    return v
            return False

        def _processed_count():
            lst = getattr(self, "stats_list", None)
            return len(lst) if isinstance(lst, list) else 0

        def _avg_ratio_and_time():
            lst = getattr(self, "stats_list", None)
            if not isinstance(lst, list) or not lst:
                return ("—", "—")
            ratios, times = [], []
            for rec in lst:
                try:
                    if "ratio" in rec:
                        ratios.append(float(rec["ratio"]))
                    elif "original_size" in rec and "compressed_size" in rec:
                        o = float(rec["original_size"]) or 1.0
                        c = float(rec["compressed_size"])
                        ratios.append(c / o)
                    if "time_taken" in rec:
                        times.append(float(rec["time_taken"]))
                except Exception:
                    pass
            avg_r = (sum(ratios) / len(ratios)) if ratios else None
            avg_t = (sum(times) / len(times)) if times else None
            r_txt = f"{avg_r*100:.1f}%" if isinstance(avg_r, float) else "—"
            t_txt = f"{avg_t:.2f}s" if isinstance(avg_t, float) else "—"
            return (r_txt, t_txt)

        def _watcher_status():
            enabled = bool(self.settings.get("watch_enabled", False))
            active = False
            try:
                w = getattr(self, "watcher", None)
                active = bool(getattr(w, "_running", False))
            except Exception:
                pass
            return "On (active)" if enabled and active else ("On (idle)" if enabled else "Off")

        def _watch_dirs():
            dirs = []
            try:
                dirs = list(self.settings.get("watch_folders", []) or [])
            except Exception:
                pass
            return str(len(dirs)) if dirs else "0"

        def _webhook_status():
            url = ""
            try:
                url = self.settings.get("webhook_url", "") or getattr(self, "webhook_url_var", None).get()
            except Exception:
                pass
            if url:
                masked = url[:40] + "…" if len(url) > 41 else url
                return f"Configured ({masked})"
            return "Not set"

        def _refresh():
            try:
                self._dash_vars["queue_pending"].set(str(_queue_len()))
                self._dash_vars["processing"].set("Yes" if _is_processing() else "No")
                self._dash_vars["processed"].set(str(_processed_count()))
                r_txt, t_txt = _avg_ratio_and_time()
                self._dash_vars["avg_ratio"].set(r_txt)
                self._dash_vars["avg_time"].set(t_txt)
                self._dash_vars["watcher"].set(_watcher_status())
                self._dash_vars["watch_dirs"].set(_watch_dirs())
                self._dash_vars["webhook"].set(_webhook_status())
            except Exception:
                pass

            try:
                win.after(1000, _refresh)
            except Exception:
                pass

        _refresh()




    def show_user_guide(self):
        
        try:

            base = os.path.dirname(os.path.abspath(__file__))
            candidates = [
                os.path.join(base, "docs", "USER_GUIDE.html"),
                os.path.join(base, "docs", "UserGuide.html"),
                os.path.join(base, "docs", "user_guide.html"),
                os.path.join(base, "USER_GUIDE.html"),
                os.path.join(base, "UserGuide.html"),
                os.path.join(base, "user_guide.html"),
                os.path.join(base, "docs", "USER_GUIDE.md"),
                os.path.join(base, "README.md"),
            ]

            for p in candidates:
                if os.path.isfile(p):
                    try:

                        if os.name == "nt" and p.lower().endswith((".html", ".htm", ".md")):
                            os.startfile(p)  # type: ignore[attr-defined]
                        else:
                            webbrowser.open_new_tab("file://" + os.path.abspath(p).replace("\\", "/"))
                        return
                    except Exception:
                        pass

            from tkinter import messagebox as mbox
            mbox.showinfo(
                "BitCrusher — Quick Guide",
                (
                    "1) Add files with “Add Files…”, or drag & drop into the queue.\n"
                    "2) Choose a target size (MB) or a preset.\n"
                    "3) (Optional) Open Advanced Options to tweak encoder/CRF/audio.\n"
                    "4) Click “Start Compression”.\n\n"
                    "Tips:\n"
                    "• Folder Watcher will auto-queue new files when enabled (Settings).\n"
                    "• Webhook URL (Settings → Webhook) posts start/success/failure to Discord.\n"
                    "• Use Profiles (Settings → Save/Load Profile) to store your favorite setup."
                )
            )
        except Exception as e:
            try:
                from tkinter import messagebox as mbox
                mbox.showerror("User Guide", f"Could not open guide:\n{e}")
            except Exception:
                pass




    def rebuild_themes_menu(self):
        
        try:
            menubar = self.root.nametowidget(self.root['menu'])

            self.setup_menu()  # your setup_menu already constructs the full menubar
        except Exception:
            pass



    def _on_theme_select(self, name: str):
        

        self.theme_var.set(name)

        try:
            animated_retheme(self, name)
        except Exception:
            try:
                apply_theme(self.style, name)
                retheme_runtime(self, self.style, name)
            except Exception:
                pass

        self.settings = getattr(self, "settings", {}) or {}
        self.settings["theme"] = name
        try:
            self.save_settings()
        except Exception:
            pass

        try:
            _save_theme_choice(name)
        except Exception:
            pass

        from pathlib import Path

    def load_settings(self) -> dict:
        
        from pathlib import Path

        defaults = {
            "theme": "Dark",
            "output_dir": str(Path.home()),
            "watch_folder": "",
            "enable_watch": False,
            "preset": next(iter(PRESETS.keys())),
            "target_size": MAX_SIZE_MB_DEFAULT,
            "webhook_url": "",
            "use_webhook": 0,
            "advanced": dict(ADVANCED_DEFAULTS),
        }
        data = dict(defaults)

        try:
            if os.path.isfile(self.settings_path):
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    disk = json.load(f) or {}

                try:
                    if "size_unit" in settings:
                        if not hasattr(self, "size_unit_var"):
                            import tkinter as tk
                            self.size_unit_var = tk.StringVar(value="MB")
                        self.size_unit_var.set(str(data["size_unit"] or "MB"))
                        self.size_unit_var = size_unit_var
                except Exception:
                    pass

                if isinstance(disk, dict):
                    for k in ("theme", "output_dir", "watch_folder", "enable_watch",
                              "preset", "target_size", "webhook_url", "use_webhook"):
                        if k in disk:
                            data[k] = disk[k]
                    adv = dict(ADVANCED_DEFAULTS)
                    adv.update(disk.get("advanced", {}) or {})
                    data["advanced"] = adv
        except Exception as e:
            try: LOG.error(f"Failed to load settings: {e}")
            except Exception: pass

        try:
            if not hasattr(self, "theme_var"):
                self.theme_var = tk.StringVar(value=data["theme"])
            else:
                self.theme_var.set(data["theme"])
            apply_theme(self.style, data["theme"])
            self.root.configure(bg=APP_BG)
            try:
                from ui_aesthetics import retheme_runtime
                retheme_runtime(self, self.style, data["theme"])
            except Exception:
                pass
        except Exception:
            pass

        try: self.save_path.set(data["output_dir"])
        except Exception: pass
        try: self.watch_folder.set(data["watch_folder"])
        except Exception: pass
        try: self.enable_watch.set(1 if data["enable_watch"] else 0)
        except Exception: pass

        try: self.target_size_var.set(str(data["target_size"]))
        except Exception: pass

        preset = data.get("preset", next(iter(PRESETS.keys())))
        preset_mb = PRESETS.get(preset)
        if isinstance(preset_mb, int) and int(data["target_size"]) != int(preset_mb):
            preset = next((k for k in PRESETS if str(k).lower().startswith("custom")), "Custom (use size below)")
        try: self.preset_var.set(preset)
        except Exception: pass

        try:
            if hasattr(self, "webhook_var"):
                self.webhook_var.set(data.get("webhook_url", ""))
            else:
                self.webhook_var = tk.StringVar(value=data.get("webhook_url", ""))
        except Exception: pass
        try: self.use_webhook.set(int(data.get("use_webhook", 0)))
        except Exception: pass

        adv = data.get("advanced", {})
        try: self.adv_iterative.set(1 if adv.get("iterative") else 0)
        except Exception: pass
        try: self.adv_two_pass.set(1 if adv.get("two_pass") else 0)
        except Exception: pass
        try: self.adv_two_pass_fallback.set(1 if adv.get("two_pass_fallback", True) else 0)
        except Exception: pass
        try: self.adv_auto_retry.set(1 if adv.get("auto_retry", True) else 0)
        except Exception: pass
        try: self.adv_grain_filter.set(1 if adv.get("grain_filter", True) else 0)
        except Exception: pass
        try: self.adv_concurrent.set(1 if adv.get("concurrent") else 0)
        except Exception: pass
        try: self.adv_auto_output.set(1 if adv.get("auto_output_folder") else 0)
        except Exception: pass
        try: self.adv_guetzli.set(1 if adv.get("guetzli") else 0)
        except Exception: pass
        try: self.adv_pngopt.set(1 if adv.get("pngopt") else 0)
        except Exception: pass
        try: self.adv_auto_jpeg.set(1 if adv.get("auto_jpeg") else 0)
        except Exception: pass

        try: self.adv_encoder.set(adv.get("encoder", "x264"))
        except Exception: pass
        try: self.adv_manual_crf.set(adv.get("manual_crf", ""))
        except Exception: pass
        try: self.adv_manual_bitrate.set(adv.get("manual_bitrate", ""))
        except Exception: pass
        try: self.adv_output_prefix.set(adv.get("output_prefix", ""))
        except Exception: pass
        try: self.adv_output_suffix.set(adv.get("output_suffix", "_discord_ready"))
        except Exception: pass
        try: self.adv_audio_format.set(adv.get("audio_format", "aac"))
        except Exception: pass
        try: self.adv_image_format.set(adv.get("image_format", "jpg"))
        except Exception: pass

        return data


    def save_settings(self) -> None:
        
        try:

            if not hasattr(self, "size_unit_var"):
                try:
                    import tkinter as tk
                    self.size_unit_var = tk.StringVar(value="MB")
                except Exception:
                    class _UnitDummy:
                        def get(self): return "MB"
                    self.size_unit_var = _UnitDummy()

            out_dir      = self.save_path.get() if hasattr(self.save_path, "get") else str(self.save_path)
            watch_dir    = self.watch_folder.get() if hasattr(self.watch_folder, "get") else str(self.watch_folder)
            enable_watch = bool(self.enable_watch.get()) if hasattr(self.enable_watch, "get") else bool(self.enable_watch)
            preset       = self.preset_var.get() if hasattr(self.preset_var, "get") else str(self.preset_var)

            try:

                target_size = max(1, int(round(self._get_target_bytes() / (1024 * 1024))))
            except Exception:
                target_size = MAX_SIZE_MB_DEFAULT

            webhook      = (self.webhook_var.get() if hasattr(self, "webhook_var") and hasattr(self.webhook_var, "get")
                            else str(getattr(self, "webhook_url", "")))
            theme        = str(self.theme_var.get()) if hasattr(self, "theme_var") else "Dark"
            use_webhook  = int(self.use_webhook.get()) if hasattr(self, "use_webhook") and hasattr(self.use_webhook, "get") else 0

            adv = {
                "auto_retry":          bool(self.adv_auto_retry.get())        if hasattr(self, "adv_auto_retry")        else ADVANCED_DEFAULTS.get("auto_retry", True),
                "two_pass_fallback":   bool(self.adv_two_pass_fallback.get()) if hasattr(self, "adv_two_pass_fallback") else ADVANCED_DEFAULTS.get("two_pass_fallback", True),
                "grain_filter":        bool(self.adv_grain_filter.get())      if hasattr(self, "adv_grain_filter")      else ADVANCED_DEFAULTS.get("grain_filter", True),
                "encoder":             str(self.adv_encoder.get())            if hasattr(self, "adv_encoder")            else ADVANCED_DEFAULTS.get("encoder", "x264"),
                "iterative":           bool(self.adv_iterative.get())         if hasattr(self, "adv_iterative")         else ADVANCED_DEFAULTS.get("iterative", False),
                "two_pass":            bool(self.adv_two_pass.get())          if hasattr(self, "adv_two_pass")          else ADVANCED_DEFAULTS.get("two_pass", False),
                "manual_crf":          str(self.adv_manual_crf.get())         if hasattr(self, "adv_manual_crf")        else "",
                "manual_bitrate":      str(self.adv_manual_bitrate.get())     if hasattr(self, "adv_manual_bitrate")    else "",
                "output_prefix":       str(self.adv_output_prefix.get())      if hasattr(self, "adv_output_prefix")     else "",
                "output_suffix":       str(self.adv_output_suffix.get())      if hasattr(self, "adv_output_suffix")     else "_discord_ready",
                "audio_format":        str(self.adv_audio_format.get())       if hasattr(self, "adv_audio_format")      else "aac",
                "image_format":        str(self.adv_image_format.get())       if hasattr(self, "adv_image_format")      else "jpg",
                "concurrent":          bool(self.adv_concurrent.get())        if hasattr(self, "adv_concurrent")        else False,
                "auto_output_folder":  bool(self.adv_auto_output.get())       if hasattr(self, "adv_auto_output")       else False,
                "guetzli":             bool(self.adv_guetzli.get())           if hasattr(self, "adv_guetzli")           else False,
                "pngopt":              bool(self.adv_pngopt.get())            if hasattr(self, "adv_pngopt")            else False,
                "auto_jpeg":           bool(self.adv_auto_jpeg.get())         if hasattr(self, "adv_auto_jpeg")         else False,
            }

            payload = {
                "theme":        theme,
                "ui_theme":     theme,
                "output_dir":   out_dir,
                "watch_folder": watch_dir,
                "enable_watch": enable_watch,
                "preset":       preset,
                "target_size":  target_size,
                "webhook_url":  webhook,
                "use_webhook":  use_webhook,
                "advanced":     dict(adv),
                "profiles":     dict(getattr(self, "saved_profiles", {})),
                "language":     self.lang_var.get(),
                "size_unit":    (self.size_unit_var.get() if hasattr(self, "size_unit_var") else "MB"),
            }


            

            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            tmp = self.settings_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            os.replace(tmp, self.settings_path)

            self.settings = payload
            try: LOG.info("Settings saved → %s", self.settings_path)
            except Exception: pass
        except Exception as e:
            try: LOG.error(f"Failed to save settings: {e}")
            except Exception: pass

    def gather_advanced_options(self) -> dict:
        
        opts = {}

        try:
            val = (self.encoder_var.get() if hasattr(self, "encoder_var") else "").strip()
            if not val:
                val = self.settings.get("encoder", "") or self.settings.get("advanced", {}).get("encoder", "")
            opts["encoder"] = val or "x264"
        except Exception:
            opts["encoder"] = self.settings.get("encoder", "x264")

        try:
            crf_raw = (self.crf_var.get() if hasattr(self, "crf_var") else self.settings.get("manual_crf", ""))
            crf_raw = str(crf_raw).strip()
            if crf_raw:
                opts["manual_crf"] = str(int(crf_raw))
        except Exception:

            pass

        try:
            opts["two_pass"] = bool(self.two_pass_var.get()) if hasattr(self, "two_pass_var") else bool(self.settings.get("two_pass", False))
        except Exception:
            pass

        try:
            ov = None
            if hasattr(self, "overshoot_var"):
                ov = float(self.overshoot_var.get())
            elif "overshoot_ratio" in self.settings:
                ov = float(self.settings["overshoot_ratio"])
            if ov is not None:
                opts["overshoot_ratio"] = max(0.90, min(1.15, ov))
        except Exception:
            pass

        try:
            if hasattr(self, "adv_hwaccel"):
                opts["hwaccel"] = self.adv_hwaccel.get()
            else:
                opts["hwaccel"] = self.settings.get("hwaccel", "CPU")
        except Exception:
            opts["hwaccel"] = "CPU"

        return opts

    def _profiles_file(self) -> str:
        
        try:
            base = os.path.join(os.getcwd(), "user_settings")
            os.makedirs(base, exist_ok=True)
            return os.path.join(base, "profiles.json")
        except Exception:
            return "profiles.json"

    def _read_profiles(self) -> dict:
        pf = self._profiles_file()
        try:
            if os.path.isfile(pf):
                with open(pf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, dict) else {}
        except Exception:
            pass
        return {}

    def _write_profiles(self, data: dict) -> None:
        pf = self._profiles_file()
        try:
            with open(pf, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            try:
                self._notify("Save Profile Error", str(e))
            except Exception:
                pass

    def save_profile(self):
        
        try:
            name = sd.askstring("Save Profile", "Enter profile name:")
            if not name:
                return
            name = name.strip()
            if not name:
                return

            snap = dict(self.settings)

            profiles = self._read_profiles()
            profiles[name] = snap
            self._write_profiles(profiles)

            try:
                self._notify("Profile Saved", f"Saved profile: {name}")
            except Exception:
                pass
        except Exception as e:
            self.log(f"Profile save failed: {e}", level="ERROR")

    def load_profile(self):
        
        try:
            profiles = self._read_profiles()
            if not profiles:
                self._notify("Load Profile", "No profiles saved yet.")
                return

            names = sorted(profiles.keys(), key=str.lower)
            prompt = "Available profiles:\n- " + "\n- ".join(names) + "\n\nType a name to load:"
            name = sd.askstring("Load Profile", prompt)
            if not name:
                return
            name = name.strip()
            if name not in profiles:
                self._notify("Load Profile", f"Profile not found: {name}")
                return

            new_settings = profiles[name]
            if not isinstance(new_settings, dict):
                self._notify("Load Profile", f"Invalid profile data: {name}")
                return

            self.settings.update(new_settings)

            self.save_settings()

            try:

                self.webhook.set_url(self.settings.get("webhook_url","") or getattr(self, "webhook_url_var", tk.StringVar(value="")).get())
            except Exception:
                pass

            try:
                self.stop_folder_watcher()
            except Exception:
                pass
            try:

                if hasattr(self, "watch_folders"):
                    self.watch_folders = self.settings.get("watch_folders", [])
                else:
                    self.watch_folders = self.settings.setdefault("watch_folders", [])

                for _p in (self.watch_folders or []):
                    try:
                        self.watcher.add_path(_p)
                    except Exception:
                        pass
                if self.settings.get("watch_enabled", False):
                    self.start_folder_watcher()
            except Exception:
                pass

            try:
                if hasattr(self, "watch_folder"):
                    self.watch_folder.set(self.settings.get("watch_folder", ""))
                if hasattr(self, "enable_watch"):
                    self.enable_watch.set(self.settings.get("enable_watch", False))
                if hasattr(self, "save_path"):
                    self.save_path.set(self.settings.get("output_dir", self.save_path.get()))
                if hasattr(self, "theme_var"):
                    self.theme_var.set(self.settings.get("theme", self.theme_var.get()))
            except Exception:
                pass

            try:
                self._notify("Profile Loaded", f"Loaded profile: {name}")
            except Exception:
                pass
        except Exception as e:
            self.log(f"Profile load failed: {e}", level='ERROR')





    def open_settings_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("450x300")
        win.transient(self.root)
        win.grab_set()
        pad = {"padx": 10, "pady": 5}

        tk.Label(win, text="Default Save Folder:").grid(row=0, column=0, sticky="e", **pad)
        save_entry = tk.Entry(win, width=40)
        save_entry.insert(0, self.settings.get("output_dir", ""))
        save_entry.grid(row=0, column=1, **pad)
        def browse_save():
            d = filedialog.askdirectory(parent=win)
            if d:
                save_entry.delete(0, tk.END)
                save_entry.insert(0, d)
        ttk.Button(win, text="Browse…", command=browse_save).grid(row=0, column=2, **pad)

        auto_del_var = tk.BooleanVar(value=self.settings.get("auto_delete", False))
        ttk.Checkbutton(win, text="Auto-delete originals", variable=auto_del_var)\
            .grid(row=1, column=1, sticky="w", **pad)

        tk.Label(win, text="Watch Folder:").grid(row=2, column=0, sticky="e", **pad)
        watch_entry = tk.Entry(win, width=40)
        watch_entry.insert(0, self.settings.get("watch_folder", ""))
        watch_entry.grid(row=2, column=1, **pad)
        def browse_watch():
            d = filedialog.askdirectory(parent=win)
            if d:
                watch_entry.delete(0, tk.END)
                watch_entry.insert(0, d)
        ttk.Button(win, text="Browse…", command=browse_watch).grid(row=2, column=2, **pad)

        watch_on_var = tk.BooleanVar(value=self.settings.get("enable_watch", False))
        ttk.Checkbutton(win, text="Enable Watch-Folder", variable=watch_on_var)\
            .grid(row=3, column=1, sticky="w", **pad)

    def on_save():
        self.settings["output_dir"]   = save_entry.get()
        self.settings["auto_delete"]  = auto_del_var.get()
        self.settings["watch_folder"] = watch_entry.get()
        self.settings["enable_watch"] = watch_on_var.get()
        self.settings["theme"]        = self.theme_var.get()

        self.save_path.set(self.settings["output_dir"])
        self.watch_folder.set(self.settings["watch_folder"])
        self.enable_watch.set(self.settings.get("enable_watch", False))

        self.save_settings()

        try:
            self.webhook.set_url(self.settings.get("webhook_url", "")
                                 or self.webhook_url_var.get())
        except Exception:
            pass

        if self.settings["enable_watch"]:
            self.stop_folder_watcher()
            self.start_folder_watcher()
        else:
            self.stop_folder_watcher()

        win.destroy()

        btns = tk.Frame(win)
        btns.grid(row=4, column=0, columnspan=3, pady=20)
        tk.Button(btns, text="Save", command=on_save).pack(side="left", padx=10)
        ttk.Button(btns, text=_("title.cancel"), command=win.destroy).pack(side="right", padx=10)

        win.wait_window()




    def compress_file_task(self, filepath, output_folder, target_size, webhook, adv_options):
        import os, time, logging
        from pathlib import Path

        t0 = time.time()
        logging.info(f"➡️ Compressing: {filepath}")

        try:
            wh = webhook if webhook else getattr(self, "webhook", None)
            if wh:
                wh.send_text(f"🚀 Compressing: {os.path.basename(filepath)}")
        except Exception:
            pass

        try:

            target_bytes = int(target_size) if isinstance(target_size, (int, float)) and int(target_size) > 0 else self._get_target_bytes()

            try:
                t_mb = max(0, int(target_bytes // (1024 * 1024)))
            except Exception:
                t_mb = 0
            if isinstance(adv_options, dict) and t_mb > 0:

                adv_options["two_pass"] = True

                try:
                    ov = float(adv_options.get("overshoot_ratio", 1.00))
                except Exception:
                    ov = 1.00
                adv_options["overshoot_ratio"] = max(0.90, min(1.15, ov))
        except Exception:
            target_bytes = self._get_target_bytes()

        try:
            src_bytes = os.path.getsize(filepath)
            target_bytes = int(max(1, target_bytes))
            ratio = (target_bytes / float(src_bytes)) if src_bytes else 1.0

            ext = os.path.splitext(filepath)[1].lower()
            is_audio = ext in {".flac", ".wav", ".mp3", ".m4a", ".aac", ".opus", ".ogg", ".wma", ".alac", ".aiff", ".aif"}

            if ratio < 0.06:

                try:
                    self.update_status(
                        f"[WARN] Target {human_bytes(target_bytes)} is very small "
                        f"({ratio*100:.1f}% of source {human_bytes(src_bytes)}); quality may suffer."
                    , level="WARN")
                except Exception:
                    pass

                if not is_audio:
                    from tkinter import messagebox as mbox
                    mbox.showwarning(
                        self.tr("unreal.title"),
                        f"{self.tr('unreal.header')}\n\n"
                        f"{self.tr('unreal.original')}: {human_bytes(src_bytes)}\n"
                        f"{self.tr('unreal.target')}: {human_bytes(target_bytes)}\n\n"
                        f"{self.tr('unreal.why')}\n"
                        f"{self.tr('unreal.why.v')}\n"
                        f"{self.tr('unreal.why.a')}\n"
                        f"{self.tr('unreal.why.m')}\n\n"
                        f"{self.tr('unreal.better')}\n"
                        f"{self.tr('unreal.opt.aim')}\n"
                        f"{self.tr('unreal.opt.scale')}\n"
                        f"{self.tr('unreal.opt.codec')}"
                    )

                    target_bytes = max(1, int(src_bytes * 0.06))
                    ratio = target_bytes / float(src_bytes)
        except Exception:
            pass


        self._notify("Compression Started", f"Processing {os.path.basename(filepath)}")
        try:
            self.update_status(f"Starting encode @ target ~{human_bytes(target_bytes)} ({ratio*100:.1f}% of source)")
        except Exception:
            pass

        try:
            dur, w, h, br, fr = get_video_metadata(filepath)
        except Exception:
            dur = w = h = br = fr = 0
        features = {
            "duration": dur,
            "width": w,
            "height": h,
            "bitrate": br,
            "frame_rate": fr
        }

        try:
            t_mb = max(1, int(target_bytes // (1024 * 1024)))
        except Exception:
            t_mb = 1
        try:
            used_crf = self.heuristic.predict([t_mb] + list(features.values()))
        except Exception:
            used_crf = self.default_crf
            self.log_warn("Heuristic model not trained; using default CRF.")

        adv_options = adv_options.copy()
        adv_options["manual_crf"] = str(used_crf)

        try:
            adv_options["hwaccel"] = (self.adv_hwaccel.get() if hasattr(self, "adv_hwaccel") else adv_options.get("hwaccel", "CPU"))
        except Exception:
            adv_options["hwaccel"] = adv_options.get("hwaccel", "CPU")

        adv_options["encoder"] = (adv_options.get("encoder") or "x264")

        stats = {}
        try:

            self._current_target_bytes = int(target_bytes)

            stats = auto_compress(
                filepath,
                output_folder,
                self.update_status,
                target_bytes,
                wh,
                adv_options,
                (lambda: bool(self.compression_cancelled))
            )

            if stats and stats.get("compressed_size") is not None:

                rec = {
                    "filename":        os.path.basename(filepath),
                    "original_size":   stats["original_size"],
                    "compressed_size": stats["compressed_size"],
                    "ratio":           stats["compressed_size"] / stats["original_size"],
                    "time_taken":      time.time() - t0
                }
                self.stats_list.append(rec)

                size_str = format_bytes(stats["compressed_size"])
                self._notify(
                    "Compression Completed",
                    f"{rec['filename']} → {size_str} (CRF {used_crf})"
                )

                try:
                    wh = webhook if webhook else getattr(self, "webhook", None)
                    if wh:
                        out_file = stats.get("output_path") or stats.get("out_path") or stats.get("output")
                        msg = f"✅ Done: {os.path.basename(filepath)}" + (
                              f" → {os.path.basename(out_file)}" if out_file else f" → {size_str}"
                        )
                        wh.send_text(msg)
                        if out_file and os.path.isfile(out_file):
                            wh.send_file(out_file, description=msg)

                            try:
                                self.update_status(f"✅ Finished {os.path.basename(filepath)}", level="INFO")
                            except Exception:
                                pass
                except Exception:
                    pass
            else:
                self._notify(
                    "Compression Failed",
                    f"{os.path.basename(filepath)} (no output)"
                )

                try:
                    wh = webhook if webhook else getattr(self, "webhook", None)
                    if wh:
                        wh.send_text(f"❌ Failed: {os.path.basename(filepath)} — no output file.")
                except Exception:
                    pass

            self.heuristic.update(target_size, features, used_crf)

        except Exception as e:

            try:
                wh = webhook if webhook else getattr(self, "webhook", None)
                if wh:
                    wh.send_text(f"❌ Failed: {os.path.basename(filepath)} — check logs.")
            except Exception:
                pass

            logging.error(f"❌ Compression error for {filepath}: {e}")
            self._notify(
                "Compression Failed",
                f"{os.path.basename(filepath)}: {e}"
            )

            self.heuristic.update(target_size, features, used_crf)





    def compress_file(self, input_path, output_path):
        try:
            handbrake_path = self.get_handbrake_path()
            command = [
                handbrake_path,
                '-i', input_path,
                '-o', output_path,
                '-e', 'x264',
                '-q', '22',
                '--optimize',
                '--preset', 'Very Fast 1080p30'
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr)
        except Exception as e:
            raise RuntimeError(f"Compression failed for {input_path}: {e}")

    def process_queue(self):
        if not self.files:
            messagebox.showwarning("Warning", "No files in queue.")
            return

        def compress_files():
            for file in self.files:
                if self.stop_event.is_set():
                    self.log("Compression canceled by user.")
                    break
                try:
                    ext = os.path.splitext(file)[1]
                    output_file = self.get_output_filename(file, ext)
                    self.log(f"Compressing: {file}")
                    notify_info(
                        title="BitCrusher",
                        msg=f"Started compressing:\n{os.path.basename(file)}",
                        duration=3
                    )

                    self.compress_file(file, output_file)
                    self.log(f"✔ Done: {output_file}")
                    notify_info(
                        title="BitCrusher",
                        msg=f"Finished compressing:\n{os.path.basename(file)}",
                        duration=3
                    )

                except Exception as e:
                    self.log(f"❌ Error: {e}")
                    notify_error(
                        title="BitCrusher - Error",
                        msg="Compression failed! Check logs.",
                        duration=5
                    )
            self.stop_event.clear()

        self.stop_event.clear()
        self.processing_thread = threading.Thread(target=compress_files)
        self.processing_thread.start()

    def get_output_filename(self, input_file, ext=None):
        base = os.path.splitext(input_file)[0]
        ext = ext if ext else os.path.splitext(input_file)[1]
        return f"{base}_compressed{ext}"


    def setup_style(self):
        
        from tkinter import ttk

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            background="#7289DA",
            foreground="white",
            relief="flat",
            padding=6,
            font=("Segoe UI", 10)
        )
        style.map(
            "TButton",
            background=[("active", "#99AAB5")],
            foreground=[("active", "white")]
        )

        style.configure(
            "TLabel",
            background="#2C2F33",
            foreground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TEntry",
            fieldbackground="#99AAB5",
            foreground="black",
            padding=3
        )
        style.configure(
            "TCombobox",
            fieldbackground="#99AAB5",
            foreground="black",
            padding=3
        )

        style.configure("TSeparator",            background="#2C2F33")
        style.configure("Horizontal.TSeparator", background="#2C2F33")
        style.configure("Vertical.TSeparator",   background="#2C2F33")

        style.configure(
            "Treeview",
            background="#2C2F33",
            fieldbackground="#2C2F33",
            foreground="white",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#23272A",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )








    def animate_title(self):
        text = "BitCrusher V9"
        i   = getattr(self, "_title_i", 0)
        d   = getattr(self, "_title_dir", 1)

        self.title_label.configure(text=text[:i])

        if d > 0 and i < len(text):
            i += 1; delay = 80
        elif d < 0 and i > 0:
            i -= 1; delay = 80
        else:
            d *= -1; delay = 1000  # longer end pause

        self._title_i, self._title_dir = i, d

        if self.root.focus_displayof() is not None:
            self._title_job = self.root.after(delay, self.animate_title)





    def check_dependencies(self):
        
        tools = {
            "HandBrakeCLI": HANDBRAKE_CLI,
            "ffprobe":      FFPROBE,
            "ffmpeg":       FFMPEG
        }
        missing = [name for name, exe in tools.items() if not shutil.which(exe)]
        if not missing:
            return
        msg = "Missing tools detected:\n" + "\n".join(missing) + "\n\nInstall now?"
        if messagebox.askyesno("Dependencies Missing", msg):
            for name in missing:
                self.install_tool(name)
            messagebox.showinfo("Install Complete",
                                "Tools installed. Please restart the app.")
            self.root.quit()


    def cancel_queue(self):
        if hasattr(self, 'processing_thread') and self.processing_thread.is_alive():
            self.stop_event.set()
            self.log("Cancel requested.")
            messagebox.showinfo("Cancel", "Queue cancel requested.")
        else:
            messagebox.showinfo("Cancel", "No active compression to cancel.")



    def install_tool(self, name: str):
        
        import hashlib
        from zipfile import ZipFile, is_zipfile

        tool_urls = {
            "HandBrakeCLI": {
                "url": "https://github.com/HandBrake/HandBrake/releases/download/1.7.3/HandBrakeCLI-1.7.3-win-x86_64.zip",
                "exe": "HandBrakeCLI.exe"
            },
            "ffmpeg": {
                "url": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
                "exe": "ffmpeg.exe"
            },
            "ffprobe": {
                "url": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
                "exe": "ffprobe.exe"
            }
        }

        info = tool_urls.get(name)
        if not info:
            self.update_status(f"❌ Unknown tool '{name}'", level="ERROR")
            return

        tools_dir = Path(SCRIPT_DIR) / "tools"
        tools_dir.mkdir(exist_ok=True)

        exe_path = tools_dir / info["exe"]
        zip_path = tools_dir / f"{name}.zip"
        url = info["url"]

        if exe_path.exists():
            self.update_status(f"✅ {name} already installed at: {exe_path}")
            return

        self.update_status(f"⬇️ Downloading {name}…")

        for attempt in range(3):
            try:
                r = requests.get(url, stream=True, timeout=30)
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(1024 * 1024):
                        f.write(chunk)
                break
            except Exception as e:
                if attempt == 2:
                    self.update_status(f"❌ Failed to download {name}: {e}", level="ERROR")
                    return
                time.sleep(2)

        if not is_zipfile(zip_path):
            self.update_status(f"❌ Corrupted or invalid ZIP: {zip_path}", level="ERROR")
            zip_path.unlink(missing_ok=True)
            return

        self.update_status(f"📦 Extracting {name}…")
        try:
            with ZipFile(zip_path, "r") as zip_ref:
                members = [m for m in zip_ref.namelist() if m.endswith(info["exe"])]
                if not members:
                    self.update_status(f"❌ {info['exe']} not found in ZIP", level="ERROR")
                    return
                for member in members:
                    zip_ref.extract(member, tools_dir)

                    extracted = tools_dir / member
                    flattened = tools_dir / info["exe"]
                    extracted.rename(flattened)
            zip_path.unlink(missing_ok=True)
            self.update_status(f"✅ {name} installed to {exe_path}")
        except Exception as e:
            self.update_status(f"❌ Extraction failed: {e}", level="ERROR")
            zip_path.unlink(missing_ok=True)




    def setup_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.add_files())
        self.root.bind("<Control-s>", lambda e: self.start_compression())
        self.root.bind("<Control-p>", lambda e: self.toggle_pause())
        self.root.bind("<Escape>",    lambda e: self.cancel_compression())

    def toggle_pause(self):
        
        self.paused = not getattr(self, "paused", False)
        self.update_status("⏸️ Paused" if self.paused else "▶️ Resumed")

    def select_watch_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.watch_folder.set(folder)
            self.update_status(f"Watch folder set to: {folder}")
            if self.enable_watch.get():
                self.stop_folder_watcher()
                self.start_folder_watcher()


    def set_preset(self, value):
        
        v = str(value or "")
        if v.lower().startswith("custom"):
            return
        mb = PRESETS.get(v)
        if isinstance(mb, int):
            self.target_size_var.set(str(mb))






    def toggle_watch(self):
        if self.enable_watch.get():
            if not self.watch_folder.get():
                messagebox.showwarning("Watch Folder","Please select a folder first.")
                self.enable_watch.set(False)
            else:
                self.start_folder_watcher()
        else:
            self.stop_folder_watcher()


    def handle_drop(self, event):
        raw_data = event.data
        self.update_status(f"Drag-and-Drop raw data: {raw_data}", level="DEBUG")
        notification.notify(
            title="BitCrusher",
            message="File dropped into BitCrusher!",
            timeout=2
        )

        for f in parse_dnd_files(raw_data):
            if os.path.exists(f) and f not in self.file_list:
                _norm = _normalize_drop_path(filepath)
                try:
                    if not hasattr(self, "file_list"):
                        self.file_list = []
                    if _norm not in self.file_list:
                        self.file_list.append(_norm)
                except Exception:
                    pass
                self.queue_box.insert("end", _norm)


    def notify(title, message):
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=5  # seconds
            )
        except Exception as e:
            print(f"[NOTIFY ERROR] {e}")

    def drop_file_handler(self, event):
        
        raw = getattr(event, "data", event)
        self.logger.debug(f"Raw DnD data: {raw!r}")

        try:
            paths = self.root.tk.splitlist(raw)
        except tk.TclError:
            paths = [raw]

        for p in paths:
            path = p.strip("{}")
            if path.lower().startswith("file:///"):
                path = path[8:]
            elif path.lower().startswith("file://"):
                path = path[7:]
            path = os.path.normpath(path)

            if os.path.isfile(path):
                if path not in getattr(self, "file_list", []):

                    _norm = _normalize_drop_path(path)
                    try:
                        if not hasattr(self, "file_list"):
                            self.file_list = []
                        if _norm not in self.file_list:
                            self.file_list.append(_norm)
                    except Exception:
                        pass
                    self.queue_box.insert("end", _norm)

                    self.logger.info(f"Queued via DnD: {path}")
                else:
                    self.logger.info(f"Already queued: {path}")
            else:
                self.logger.warning(f"Ignored drop: not a file: {path}")

        return "break"






    def add_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("Media files", 
            "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.m4v *.3gp *.3g2 *.mpeg *.mpg "
            "*.mp3 *.wav *.aac *.ogg *.flac *.wma *.m4a *.opus "
            "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.raw")])
        for path in paths:
            if path not in self.file_list:
                self.file_list.append(path)
                self.queue_box.insert("end", path)
                notification.notify(
                    title="BitCrusher - File Added",
                    message=f"{os.path.basename(path)} added to queue.",
                    timeout=3
                )


    def remove_selected(self):
        indices = list(self.queue_box.curselection())
        for i in reversed(indices):
            self.queue_box.delete(i)
            del self.file_list[i]

    def move_up(self):
        selections = self.queue_box.curselection()
        for i in selections:
            if i > 0:
                self.file_list[i], self.file_list[i-1] = self.file_list[i-1], self.file_list[i]
        self.refresh_queue_box()

    def move_down(self):
        selections = list(self.queue_box.curselection())
        for i in reversed(selections):
            if i < len(self.file_list) - 1:
                self.file_list[i], self.file_list[i+1] = self.file_list[i+1], self.file_list[i]
        self.refresh_queue_box()

    def clear_queue(self):
        self.file_list.clear()
        self.queue_box.delete(0, "end")

    def refresh_queue_box(self):
        self.queue_box.delete(0, "end")
        for f in self.file_list:
            _norm = _normalize_drop_path(f)
            self.queue_box.insert("end", _norm)
            try:
                if not hasattr(self, "file_list"):
                    self.file_list = []
                if _norm not in self.file_list:
                    self.file_list.append(_norm)
            except Exception:
                pass


    def update_preview(self, event):
        selection = self.queue_box.curselection()
        if not selection:
            self.preview_label.config(image="", text="No file selected")
            return
        filepath = self.file_list[selection[0]]
        media_type = get_media_type(filepath)
        if media_type == "image":
            try:
                im = Image.open(filepath)
                im.thumbnail((300,300))
                photo = ImageTk.PhotoImage(im)
                self.preview_label.image = photo
                self.preview_label.config(image=photo, text="")
            except Exception as e:
                self.preview_label.config(text="Image preview error: " + str(e))
        elif media_type == "video":
            try:
                duration, width, height, bitrate, fps = get_video_metadata(filepath)
                info = (f"Video File\nDuration: {duration:.2f}s\n"
                        f"Resolution: {width}x{height}\nBitrate: {bitrate}bps\nFPS: {fps}")
                self.preview_label.config(image="", text=info, font=("Segoe UI", 10))
            except Exception as e:
                self.preview_label.config(text="Video preview error: " + str(e))
        elif media_type == "audio":
            self.preview_label.config(image="", text="Audio File\nNo preview available.",
                                      font=("Segoe UI", 10))
        else:
            self.preview_label.config(image="", text="Unsupported file type.",
                                      font=("Segoe UI", 10))

    def _thumb_from_video(path, out_png):
        try:
            subprocess.run([FFMPEG, '-y', '-ss', '00:00:01', '-i', path, '-frames:v', '1', out_png],
                           startupinfo=si, creationflags=NO_WIN,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return os.path.exists(out_png)
        except Exception:
            return False


    def update_preview(self, *_):
        sel = self.queue_box.curselection()
        if not sel:
            self.preview_label.configure(text="No file selected", image="", compound="none")
            return
        fpath = self.queue_box.get(sel[0])
        ext = os.path.splitext(fpath)[1].lower()
        tmp_png = os.path.join(tempfile.gettempdir(), 'bc_thumb.png')
        img_obj = None
        if ext in {'.mp4','.mkv','.mov','.webm','.avi','.m4v'} and _thumb_from_video(fpath, tmp_png):
            img_obj = ImageTk.PhotoImage(Image.open(tmp_png).resize((512, 288)))
        elif ext in {'.jpg','.jpeg','.png','.gif','.bmp','.tiff'}:
            img_obj = ImageTk.PhotoImage(Image.open(fpath).resize((512, 288)))
        if img_obj:
            self.preview_label.configure(image=img_obj, text=os.path.basename(fpath), compound='bottom')
            self.preview_label.image = img_obj
        else:
            self.preview_label.configure(text=os.path.basename(fpath), image="", compound='none')

    def update_status(self, msg, level="INFO"):
        

        log_message(self.log_widget, msg, level)

        self.all_logs.append((level, msg))




    def apply_log_filter(self, filter_val):
        self.log_widget.config(state="normal")
        self.log_widget.delete(1.0, "end")
        for lev, msg in self.all_logs:
            if filter_val == "ALL" or lev == filter_val:
                timestamp = time.strftime("%H:%M:%S")
                self.log_widget.insert("end", f"[{timestamp}] [{lev}] {msg}\n")
        self.log_widget.config(state="disabled")

    def open_advanced_options(self):
        adv_win = tk.Toplevel(self.root)
        adv_win.title("Advanced Options")
        adv_win.geometry("450x600")
        adv_win.transient(self.root)
        adv_win.grab_set()
        adv_win.lift()
        adv_win.focus_force()
        adv_font = ("Segoe UI", 10)
        pad = {"pady": 4, "padx": 4}

        tk.Label(adv_win, text="Encoder:", font=adv_font) \
          .grid(row=0, column=0, sticky="e", **pad)
        tk.OptionMenu(adv_win, self.adv_encoder, "x264", "x265", "AV1") \
          .grid(row=0, column=1, **pad)

        tk.Label(adv_win, text="Iterative Compression:", font=adv_font) \
          .grid(row=1, column=0, sticky="e", **pad)
        tk.Checkbutton(adv_win, variable=self.adv_iterative, bg="white") \
          .grid(row=1, column=1, **pad)

        tk.Label(adv_win, text="Two-Pass Encoding:", font=adv_font) \
          .grid(row=2, column=0, sticky="e", **pad)
        tk.Checkbutton(adv_win, variable=self.adv_two_pass, bg="white") \
          .grid(row=2, column=1, **pad)

        tk.Label(adv_win, text="Manual CRF:", font=adv_font) \
          .grid(row=3, column=0, sticky="e", **pad)
        tk.Entry(adv_win, textvariable=self.adv_manual_crf, width=10) \
          .grid(row=3, column=1, **pad)

        tk.Label(adv_win, text="Manual Bitrate (bps):", font=adv_font) \
          .grid(row=4, column=0, sticky="e", **pad)
        tk.Entry(adv_win, textvariable=self.adv_manual_bitrate, width=15) \
          .grid(row=4, column=1, **pad)

        tk.Label(adv_win, text="Output Prefix:", font=adv_font) \
          .grid(row=5, column=0, sticky="e", **pad)
        tk.Entry(adv_win, textvariable=self.adv_output_prefix, width=15) \
          .grid(row=5, column=1, **pad)

        tk.Label(adv_win, text="Output Suffix:", font=adv_font) \
          .grid(row=6, column=0, sticky="e", **pad)
        tk.Entry(adv_win, textvariable=self.adv_output_suffix, width=15) \
          .grid(row=6, column=1, **pad)

        tk.Label(adv_win, text="Audio Format (aac/mp3/opus):", font=adv_font) \
          .grid(row=7, column=0, sticky="e", **pad)
        tk.OptionMenu(adv_win, self.adv_audio_format, "aac", "mp3", "opus") \
          .grid(row=7, column=1, **pad)

        tk.Label(adv_win, text="Image Format (jpg/png):", font=adv_font) \
          .grid(row=8, column=0, sticky="e", **pad)
        tk.OptionMenu(adv_win, self.adv_image_format, "jpg", "png") \
          .grid(row=8, column=1, **pad)

        tk.Checkbutton(adv_win, text="Use Guetzli for JPEG", variable=self.adv_guetzli, bg="white") \
          .grid(row=9, column=0, columnspan=2, sticky="w", **pad)

        tk.Checkbutton(adv_win, text="PNGQuant + Zopfli Mode", variable=self.adv_pngopt, bg="white") \
          .grid(row=10, column=0, columnspan=2, sticky="w", **pad)

        tk.Checkbutton(adv_win, text="Auto Convert All Images to JPEG", variable=self.adv_auto_jpeg, bg="white") \
          .grid(row=11, column=0, columnspan=2, sticky="w", **pad)

        tk.Label(adv_win, text="HW Acceleration:", font=adv_font) \
          .grid(row=12, column=0, sticky="e", **pad)
        self.adv_hwaccel = tk.StringVar(value="CPU")
        tk.OptionMenu(adv_win, self.adv_hwaccel, "CPU", "NVENC") \
          .grid(row=12, column=1, **pad)

        tk.Label(adv_win, text="Concurrent Compression:", font=adv_font) \
          .grid(row=13, column=0, sticky="e", **pad)
        tk.Checkbutton(adv_win, variable=self.adv_concurrent, bg="white") \
          .grid(row=13, column=1, **pad)

        tk.Label(adv_win, text="Auto Create Output Folder:", font=adv_font) \
          .grid(row=14, column=0, sticky="e", **pad)
        tk.Checkbutton(adv_win, variable=self.adv_auto_output, bg="white") \
          .grid(row=14, column=1, **pad)

        ttk.Button(adv_win, text="OK", command=adv_win.destroy) \
          .grid(row=15, column=0, columnspan=2, pady=10)

        adv_win.wait_window()


    def cancel_compression(self):
        self.cancel_flag = True
        self.update_status("⏹️ Cancel requested.")

    def compression_cancelled(self):
        return self.cancel_flag

    def compress_all(self):
        

        self.cancel_flag = False
        self.compression_cancelled = False
        def is_cancelled(self):

            return bool(getattr(self, "compression_cancelled", False))
        self.paused = False

        files = list(getattr(self, "_thread_file_list", []) or [])
        files = [_normalize_drop_path(p) for p in files if isinstance(p, str)]
        files = [p for p in files if os.path.isfile(p)]
        total = len(files)

        if total == 0:
            self.root.after(0, lambda: self.update_status("No files in queue to compress.", level="ERROR"))
            self.compression_running = False
            return

        def _prep():
            try:
                self.ensure_progress_bars()
                try:
                    self.progress.stop()
                except Exception:
                    pass
                self.progress["mode"] = "determinate"
                self.progress["maximum"] = max(1, total)
                self.progress["value"] = 0
            except Exception:
                pass
        self.root.after(0, _prep)

        processed = 0
        errors = 0
        t_start = time.time()

        for idx, path in enumerate(files, start=1):
            if self.cancel_flag or self.compression_cancelled:
                break

            out_dir = getattr(self, "_thread_save_path", "") or os.path.dirname(path) or os.getcwd()
            tgt = int(getattr(self, "_thread_target_bytes", self._get_target_bytes()))
            self._current_target_bytes = int(tgt)  # canonical target for logs

            try:
                self.update_status(f"▶ Processing {os.path.basename(path)} ({idx}/{total})", level="INFO")
                self.compress_file_task(
                    filepath=path,
                    output_folder=out_dir,
                    target_size=tgt,
                    webhook=(self.webhook_url.get() if hasattr(self, "webhook_url") and self.use_webhook.get() else ""),
                    adv_options=getattr(self, "_thread_adv_options", getattr(self, "advanced_options", {})),
                )
                processed += 1
            except Exception as e:
                errors += 1
                try:
                    self.update_status(f"❌ Compression error for {filepath}: {e}", level="ERROR")
                except Exception:
                    pass

            try:
                self.root.after(0, self._bump_progress, idx)
            except Exception:
                pass

        dt = time.time() - t_start

        def _bump_progress(self, v):
            try:

                self.ensure_progress_bars()
                if hasattr(self, "progress") and self.progress:
                    self.progress.configure(value=v)
            except Exception:
                pass

        def _finish():
            try:
                self.progress.stop()
                self.progress["mode"] = "indeterminate"
            except Exception:
                pass
            if processed > 0:
                try:
                    self.update_status(
                        f"✅ All files processed. {processed}/{total} ok, {errors} errors in {dt:.1f}s.",
                        level="INFO"
                    )
                except Exception:
                    pass
                try:
                    self.display_statistics()
                except Exception:
                    pass
            else:
                try:
                    self.update_status("No files were processed.", level="ERROR")
                except Exception:
                    pass

        self.root.after(0, _finish)
        self.compression_running = False


    def _bump_progress(self, v):
        try:

            self.ensure_progress_bars()
            if hasattr(self, "progress") and self.progress:
                self.progress.configure(value=v)
        except Exception:
            pass


def start_folder_watcher(self):
    
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except Exception as e:
        self.update_status(f"Folder watcher unavailable: {e}", level="ERROR")
        return

    watch_dir = ""
    try:
        watch_dir = (self.watch_folder_var.get() if hasattr(self, "watch_folder_var") else "").strip()
    except Exception:
        watch_dir = ""
    if not watch_dir or not os.path.isdir(watch_dir):
        self.update_status("Watcher not started: invalid watch folder.", level="ERROR")
        return

    class _Handler(FileSystemEventHandler):
        def on_created(hself, event):
            try:
                if getattr(event, "is_directory", False):
                    return
                path = _normalize_drop_path(getattr(event, "src_path", ""))
                if os.path.isfile(path) and get_media_type(path) != "unknown":

                    try:
                        if not hasattr(self, "file_list"):
                            self.file_list = []
                        if path not in self.file_list:
                            self.file_list.append(path)
                    except Exception:
                        pass
                    try:
                        self.queue_box.insert("end", path)
                    except Exception:
                        pass
                    self.update_status(f"📥 Detected new file: {path}", level="INFO")
            except Exception:
                pass

    try:
        self._observer = Observer()
        self._observer.schedule(_Handler(), watch_dir, recursive=False)
        self._observer.start()
        self.update_status(f"Watcher started on {watch_dir}", level="INFO")
    except Exception as e:
        self.update_status(f"Failed to start watcher: {e}", level="ERROR")

from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileMovedEvent
from watchdog.observers import Observer
import queue as _queue

class FolderWatcher(FileSystemEventHandler):
    
    def __init__(self,
                 on_file_ready,
                 status_cb=None,
                 notify_cb=None,
                 exts=(".mp4",".mkv",".mov",".avi",".webm",".mp3",".flac",".wav",".m4a",".aac",".jpg",".jpeg",".png",".gif",".webp"),
                 min_bytes=1,
                 ignore_globs=("*.part","*.tmp","~$*","*.crdownload","*.download"),
                 stable_secs=1.25):
        super().__init__()
        self.on_file_ready = on_file_ready
        self.status_cb = status_cb
        self.notify_cb = notify_cb
        self.exts = tuple(e.lower() for e in exts or ())
        self.min_bytes = int(min_bytes or 1)
        self.ignore_globs = tuple(ignore_globs or ())
        self.stable_secs = float(stable_secs or 1.25)
        self._observer = Observer()
        self._paths = set()
        self._work = _queue.Queue()
        self._seen = {}  # path -> last_size
        self._running = False
        self._worker = threading.Thread(target=self._drain, daemon=True)

    def add_path(self, folder):
        try:
            folder = os.path.abspath(folder)
        except Exception:
            return
        if not os.path.isdir(folder): return
        if folder in self._paths: return
        self._paths.add(folder)
        self._observer.schedule(self, folder, recursive=False)
        if self.notify_cb:
            self.notify_cb("Folder Watcher", f"Watching: {folder}")

    def remove_path(self, folder):

        folder = os.path.abspath(folder)
        if folder not in self._paths: return
        self._paths.remove(folder)
        if self._running:
            self.stop(); self.start()

    def start(self):
        if self._running: return
        self._running = True
        try:
            self._observer.start()
        except Exception:
            pass
        if not self._worker.is_alive():
            self._worker = threading.Thread(target=self._drain, daemon=True)
            self._worker.start()
        if self.status_cb: self.status_cb("Folder watcher started.")

    def stop(self):
        if not self._running: return
        self._running = False
        try:
            self._observer.stop()
            self._observer.join(timeout=2)
        except Exception:
            pass
        if self.status_cb: self.status_cb("Folder watcher stopped.")

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent) and not event.is_directory:
            self._enqueue(event.src_path)

    def on_moved(self, event):
        if isinstance(event, FileMovedEvent) and not event.is_directory:
            self._enqueue(event.dest_path)

    def _enqueue(self, path):
        try:
            p = os.path.abspath(path)
            name = os.path.basename(p)

            for pat in self.ignore_globs:
                if fnmatch(name.lower(), pat.lower()):
                    return

            if self.exts and not any(p.lower().endswith(e) for e in self.exts):
                return
            self._work.put(p, block=False)
            if self.status_cb: self.status_cb(f"Detected new file: {p}")
            if self.notify_cb: self.notify_cb("New file detected", p)
        except Exception:
            pass

    def _is_stable(self, p):
        try:
            st = os.stat(p)
            if st.st_size < self.min_bytes: return False
            last = self._seen.get(p)
            self._seen[p] = st.st_size
            return (last is not None and last == st.st_size)
        except Exception:
            return False

    def _drain(self):
        while True:
            try:
                p = self._work.get(timeout=0.5)
            except Exception:
                if not self._running: return
                continue

            t0 = time.time()
            stable = False
            while time.time() - t0 < max(3.0, self.stable_secs * 3):
                time.sleep(self.stable_secs)
                if self._is_stable(p):
                    stable = True
                    break
            if stable and os.path.isfile(p):
                try:
                    self.on_file_ready(p)
                except Exception:
                    LOG.exception("FolderWatcher callback failed for %s", p)


        class WatchHandler(FileSystemEventHandler):
            def on_created(handler_self, event):
                if event.is_directory:
                    return
                path = event.src_path
                self.update_status(f"📂 Detected new file: {path}")
                if os.path.isfile(path) and get_media_type(path) != "unknown":

                    _norm = _normalize_drop_path(path)
                    try:
                        if not hasattr(self, "file_list"):
                            self.file_list = []
                        if _norm not in self.file_list:
                            self.file_list.append(_norm)
                    except Exception:
                        pass
                    self.queue_box.insert("end", _norm)


        self.update_status(f"👀 Watching: {self.watch_folder.get()}")
        self._watch_observer = Observer()
        self._watch_handler  = WatchHandler()
        self._watch_observer.schedule(
            self._watch_handler,
            self.watch_folder.get(),
            recursive=False
        )
        self._watch_observer.start()

    def stop_folder_watcher(self):
        
        if hasattr(self, "_watch_observer"):
            self.update_status("🛑 Stopping watch folder.")
            self._watch_observer.stop()
            self._watch_observer.join()
            del self._watch_observer, self._watch_handler

    def toggle_watch_folder(self):
        
        from tkinter import messagebox
        if self.watch_var.get():
            if not os.path.isdir(self.watch_folder.get()):
                messagebox.showerror("Error", "Invalid watch folder.")
                self.watch_var.set(False)
                return
            self.start_folder_watcher()
        else:
            self.stop_folder_watcher()



    def display_statistics(self):
        
        for row in self.stats_table.get_children():
            self.stats_table.delete(row)

        for s in self.stats_list:
            orig = format_bytes(s["original_size"])
            comp = format_bytes(s["compressed_size"])
            ratio = f"{s['ratio']:.2f}"
            took  = f"{s['time_taken']:.1f}"
            self.stats_table.insert("", "end", values=(s["filename"], orig, comp, ratio, took))




    def select_save_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)
            self.update_status(f"Save folder set: {folder}")


    def show_user_guide(self):
        guide_text = (
            "BitCrusher V9 - User Guide\n\n"
            "1. Adding Files:\n"
            "   - Drag and drop or use 'Add Files'.\n\n"
            "2. Queue:\n"
            "   - Remove, reorder, or clear with the buttons.\n\n"
            "3. Preview:\n"
            "   - Images show a thumbnail; videos show metadata; audio has no preview.\n\n"
            "4. Compression Settings:\n"
            "   - Choose a preset or adjust in 'Advanced Options'.\n\n"
            "5. Profiles:\n"
            "   - Save/load advanced settings via Settings → Save/Load Profile.\n\n"
            "6. Start:\n"
            "   - Pick a valid save folder, click 'Start Compression'.\n\n"
            "7. Logs & Stats:\n"
            "   - Filter logs; view compression stats below.\n\n"
            "Enjoy using BitCrusher V9!"
        )
        messagebox.showinfo("User Guide", guide_text)


    def save_profile(self):
        name = simpledialog.askstring("Save Profile", "Profile name:")
        if not name:
            return

        opts = self._collect_current_options()

        if not hasattr(self, "saved_profiles") or self.saved_profiles is None:
            self.saved_profiles = {}
        self.saved_profiles[name] = opts

        try:
            self.save_settings()
        except Exception:
            pass

        try:
            if hasattr(self, "profile_combo"):
                self.profile_combo["values"] = sorted(self.saved_profiles.keys())
        except Exception:
            pass

        try:
            self.snackbar(self.root, f"Saved profile '{name}'", 1400, "info")
        except Exception:
            pass

    def _collect_current_options(self) -> dict:
        
        opts = {}

        try:
            from testcompressor3 import ADVANCED_DEFAULTS as _ADV
        except Exception:
            _ADV = {
                "auto_retry": True, "overshoot_ratio": 1.00, "two_pass_fallback": True,
                "grain_filter": True, "auto_retry_done": False, "two_pass_forced": False,
                "encoder": "x264", "iterative": False, "two_pass": False, "manual_crf": "",
                "manual_bitrate": "", "output_prefix": "", "output_suffix": "_discord_ready",
                "audio_format": "aac", "image_format": "jpg", "concurrent": False,
                "auto_output_folder": False, "guetzli": False, "pngopt": False, "auto_jpeg": False,
            }
        opts.update(_ADV)

        try:
            opts.update((self.settings or {}).get("advanced", {}) or {})
        except Exception:
            pass

        def _g(name, default=None):
            v = getattr(self, name, None)
            try:
                return v.get() if hasattr(v, "get") else (v if v is not None else default)
            except Exception:
                return default

        mapping = {
            "encoder": "adv_encoder",
            "audio_format": "adv_audio_format",
            "manual_crf": "adv_manual_crf",
            "manual_bitrate": "adv_manual_bitrate",
            "iterative": "adv_iterative",
            "two_pass": "adv_two_pass",
            "two_pass_fallback": "adv_two_pass_fallback",
            "grain_filter": "adv_grain_filter",
            "auto_retry": "adv_auto_retry",
            "overshoot_ratio": "adv_overshoot_ratio",
            "output_prefix": "adv_output_prefix",
            "output_suffix": "adv_output_suffix",
            "image_format": "adv_image_format",
            "concurrent": "adv_concurrent",
            "auto_output_folder": "adv_auto_output_folder",
            "guetzli": "adv_guetzli",
            "pngopt": "adv_pngopt",
            "auto_jpeg": "adv_auto_jpeg",
        }
        for k, attr in mapping.items():
            val = _g(attr, opts.get(k))
            if val is not None:
                opts[k] = val

        try:
            t_val = self.target_size_var.get() if hasattr(self.target_size_var, "get") else self.target_size_var
            t_mb = int(float(t_val)) if str(t_val).strip() else 0
        except Exception:
            t_mb = 0
        if t_mb > 0:
            opts["two_pass"] = True

            opts["overshoot_ratio"] = 1.00


        return opts

    def _apply_profile_options(self, opts: dict) -> None:
        
        if not isinstance(opts, dict):
            return

        def _s(name, value):
            var = getattr(self, name, None)
            try:
                if hasattr(var, "set"):
                    var.set(value)
            except Exception:
                pass

        mapping = {
            "encoder": "adv_encoder",
            "audio_format": "adv_audio_format",
            "manual_crf": "adv_manual_crf",
            "manual_bitrate": "adv_manual_bitrate",
            "iterative": "adv_iterative",
            "two_pass": "adv_two_pass",
            "two_pass_fallback": "adv_two_pass_fallback",
            "grain_filter": "adv_grain_filter",
            "auto_retry": "adv_auto_retry",
            "overshoot_ratio": "adv_overshoot_ratio",
            "output_prefix": "adv_output_prefix",
            "output_suffix": "adv_output_suffix",
            "image_format": "adv_image_format",
            "concurrent": "adv_concurrent",
            "auto_output_folder": "adv_auto_output_folder",
            "guetzli": "adv_guetzli",
            "pngopt": "adv_pngopt",
            "auto_jpeg": "adv_auto_jpeg",
        }
        for k, attr in mapping.items():
            if k in opts:
                _s(attr, opts[k])

        try:
            self.settings = getattr(self, "settings", {}) or {}
            adv = dict(self.settings.get("advanced", {}))
            adv.update(opts)
            self.settings["advanced"] = adv
            self.save_settings()
        except Exception:
            pass



    def load_profile(self):
        name = self.profile_var.get().strip()
        if name in self.saved_profiles:
            prof = self.saved_profiles[name]
            if "preset_name" in prof:
                self.selected_preset.set(prof["preset_name"])

            self.adv_encoder.set(prof["encoder"])
            self.adv_iterative.set(1 if prof["iterative"] else 0)
            self.adv_two_pass.set(1 if prof["two_pass"] else 0)
            self.adv_manual_crf.set(prof["manual_crf"])
            self.adv_manual_bitrate.set(prof["manual_bitrate"])
            self.adv_output_prefix.set(prof["output_prefix"])
            self.adv_output_suffix.set(prof["output_suffix"])
            self.adv_audio_format.set(prof["audio_format"])
            self.adv_image_format.set(prof["image_format"])
            self.adv_concurrent.set(1 if prof["concurrent"] else 0)
            self.adv_auto_output.set(1 if prof["auto_output_folder"] else 0)
            self.adv_guetzli.set(1 if prof["guetzli"] else 0)
            self.adv_pngopt.set(1 if prof["pngopt"] else 0)
            self.adv_auto_jpeg.set(1 if prof["auto_jpeg"] else 0)
            self.update_status(f"Profile '{name}' loaded.")
        else:
            messagebox.showerror("Error", "Profile not found.")

    def setup_tray(self):
        def on_show(icon, item):
            self.root.deiconify()

        def on_quit(icon, item):
            self.tray_icon.stop()
            self.root.quit()

        try:
            image = Image.open("icon.png")  # You can change this to your actual tray icon
        except Exception:
            image = Image.new('RGB', (16, 16), color='black')

        menu = pystray.Menu(
            pystray.MenuItem("Open BitCrusher", on_show),
            pystray.MenuItem("Exit", on_quit)
        )
        self.tray_icon = pystray.Icon("bitcrusher", image, "BitCrusher v10", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()


    def gather_advanced_options(self) -> dict:
        return {
            "encoder": self.adv_encoder.get(),
            "iterative": bool(self.adv_iterative.get()),
            "two_pass": bool(self.adv_two_pass.get()),
            "manual_crf": self.adv_manual_crf.get().strip(),
            "manual_bitrate": self.adv_manual_bitrate.get().strip(),
            "output_prefix": self.adv_output_prefix.get().strip(),
            "output_suffix": self.adv_output_suffix.get().strip(),
            "audio_format": self.adv_audio_format.get().strip(),
            "image_format": self.adv_image_format.get().strip(),
            "concurrent": bool(self.adv_concurrent.get()),
            "auto_output_folder": bool(self.adv_auto_output.get()),
            "guetzli": bool(self.adv_guetzli.get()),
            "pngopt": bool(self.adv_pngopt.get()),
            "auto_jpeg": bool(self.adv_auto_jpeg.get())
        }

    def export_presets(self):
        
        fp = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not fp:
            return
        data = {"presets": PRESETS, "profiles": getattr(self, "saved_profiles", {})}
        try:
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.update_status(f"Presets exported to {fp}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export presets: {e}")

    def import_presets(self):
        
        fp = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not fp:
            return
        try:
            data = json.load(open(fp, "r", encoding="utf-8"))
            PRESETS.clear()
            PRESETS.update(data.get("presets", {}))
            if hasattr(self, "saved_profiles"):
                self.saved_profiles.clear()
                self.saved_profiles.update(data.get("profiles", {}))
            self.update_status("Presets imported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import presets: {e}")

    def toggle_theme(self):
        
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()
        self.save_settings()

    def show_dashboard(self):
        
        dash = tk.Toplevel(self.root)
        dash.title("Dashboard")
        dash.geometry("400x250")
        from tkinter import Label

        total = len(self.stats_list)
        if total == 0:
            Label(dash, text="No compression data yet.").pack(pady=20)
            return

        tot_orig = sum(s["original_size"] for s in self.stats_list)
        tot_comp = sum(s["compressed_size"] for s in self.stats_list)
        avg_rat  = sum(s["ratio"] for s in self.stats_list) / total
        avg_time = sum(s["time_taken"] for s in self.stats_list) / total

        info = (
            f"Files compressed: {total}\n"
            f"Total orig size: {format_bytes(tot_orig)}\n"
            f"Total comp size: {format_bytes(tot_comp)}\n"
            f"Avg ratio: {avg_rat:.2f}\n"
            f"Avg time: {avg_time:.1f}s"
        )
        Label(dash, text=info, justify="left", font=("Segoe UI", 10))\
            .pack(padx=10, pady=10)




class DropZone(TkinterDnD.Tk):
    def __init__(self, file_callback):
        super().__init__()
        self.file_callback = file_callback
        self.withdraw()
        self.overrideredirect(True)
        self.geometry("1x1+10+10")
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)
        self.after(1000, self.hide_near_tray)

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        for f in files:
            if os.path.isfile(f):
                self.file_callback(f)

    def hide_near_tray(self):
        if platform.system() == "Windows":
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f"100x100+{screen_width - 120}+{screen_height - 140}")
        self.deiconify()




    def export_presets(self):
        
        fp = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not fp:
            return
        data = {"presets": PRESETS, "profiles": getattr(self, "saved_profiles", {})}
        try:
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.update_status(f"Presets exported to {fp}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export presets: {e}")

    def import_presets(self):
        
        fp = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not fp:
            return
        try:
            data = json.load(open(fp, "r", encoding="utf-8"))
            PRESETS.clear()
            PRESETS.update(data.get("presets", {}))
            if hasattr(self, "saved_profiles"):
                self.saved_profiles.clear()
                self.saved_profiles.update(data.get("profiles", {}))
            self.update_status("Presets imported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import presets: {e}")

    def toggle_theme(self):
        
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()
        self.save_settings()

    import colorsys
    APP_BG = "#0f1216"
    CARD_BG = "#161a20"
    FG      = "#E8EAED"
    FG_SUB  = "#A8B0BA"
    ACCENT  = "#7C5CFF"   # purple
    ACCENT_2= "#3DDC97"   # mint
    ERROR   = "#FF6B6B"
    WARN    = "#FFB020"

    def _hsl_shift(hex_color: str, h_delta=0.0, s_mul=1.0, l_mul=1.0) -> str:
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

    def apply_theme(style: ttk.Style):
        style.theme_use("clam")

        style.configure(".", background=APP_BG, foreground=FG)
        style.configure("TFrame", background=APP_BG)
        style.configure("Card.TFrame", background=CARD_BG)
        style.configure("TLabel", background=APP_BG, foreground=FG)
        style.configure("Sub.TLabel", background=APP_BG, foreground=FG_SUB)

        btn_bg  = _hsl_shift(ACCENT, l_mul=0.88)
        btn_bg2 = ACCENT
        style.configure("TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12,8), background=btn_bg, foreground="#ffffff",
            borderwidth=0, focusthickness=0)
        style.map("TButton",
            background=[("active", btn_bg2), ("disabled", "#2B2F36")],
            foreground=[("disabled", "#7a8088")])

        style.configure("Ghost.TButton",
            font=("Segoe UI", 10), padding=(10,6),
            background=CARD_BG, foreground=FG,
            bordercolor="#2A2E34", relief="flat")
        style.map("Ghost.TButton",
            background=[("active", _hsl_shift(CARD_BG, l_mul=1.06))])

        style.configure("TEntry", fieldbackground=_hsl_shift(CARD_BG, l_mul=1.06),
                        bordercolor="#2A2E34", relief="flat", padding=6)
        style.configure("TCombobox", fieldbackground=_hsl_shift(CARD_BG, l_mul=1.06),
                        foreground=FG, background=CARD_BG)
        style.map("TCombobox",
            fieldbackground=[("readonly", _hsl_shift(CARD_BG, l_mul=1.02))])

        style.configure("Accent.Horizontal.TProgressbar",
            troughcolor=CARD_BG, background=ACCENT, bordercolor=CARD_BG,
            lightcolor=ACCENT, darkcolor=_hsl_shift(ACCENT, l_mul=0.8))

        style.configure("Card.TLabelframe",
                        background=CARD_BG,
                        borderwidth=0,   # removes that white line
                        relief="flat")   # ensure no groove outline
        style.configure("Card.TLabelframe.Label",
                        background=CARD_BG,
                        foreground=FG_SUB,
                        padding=(6,0))

        style.configure("TCheckbutton", background=APP_BG, foreground=FG)
        style.map("TCheckbutton", foreground=[("disabled", FG_SUB)])

        entry_bg    = _hsl_shift(CARD_BG, l_mul=1.06)
        entry_bg_ro = _hsl_shift(CARD_BG, l_mul=1.02)
        entry_fg_dis = "#7a8088"

        style.configure("Dark.TEntry",
            fieldbackground=entry_bg,
            foreground=FG,
            padding=6,
            bordercolor="#2A2E34",
            relief="flat")
        style.map("Dark.TEntry",
            fieldbackground=[("focus", entry_bg), ("!focus", entry_bg), ("disabled", _hsl_shift(CARD_BG, l_mul=1.0))],
            foreground=[("disabled", entry_fg_dis)])

        style.configure("Dark.TCombobox",
            fieldbackground=entry_bg,
            background=CARD_BG,
            foreground=FG,
            padding=4,
            bordercolor="#2A2E34",
            relief="flat")
        style.map("Dark.TCombobox",
            fieldbackground=[("readonly", entry_bg_ro), ("!readonly", entry_bg)],
            foreground=[("disabled", entry_fg_dis)])

        style.configure("Card.TLabelframe",
                        background=CARD_BG,
                        borderwidth=0,
                        relief="flat")
        style.configure("Card.TLabelframe.Label",
                        background=CARD_BG,
                        foreground=FG_SUB,
                        padding=(6, 0))

        style.layout("Card.TLabelframe", [
            ('Labelframe.padding', {'sticky': 'nswe', 'children': [
                ('Labelframe.label',  {'side': 'top', 'sticky': ''}),
                ('Labelframe.client', {'sticky': 'nswe'})
            ]})
        ])

        style.configure("Dark.TSeparator", background=_hsl_shift(CARD_BG, l_mul=1.02))






    def show_dashboard(self):
        
        win = Toplevel(self.root)
        win.title("Dashboard")
        total = len(self.stats_list)
        ratios = []
        for s in self.stats_list:
            orig = s.get("orig_size", 1)
            comp = s.get("compressed_size", 0)
            ratios.append(comp / orig if orig else 0)
        avg_ratio = sum(ratios) / total if total else 0
        Label(win, text=f"Files processed: {total}").pack(padx=10, pady=5)
        Label(win, text=f"Avg compression ratio: {avg_ratio:.2f}").pack(padx=10, pady=5)
        columns = ("File","Ratio")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        for s in self.stats_list[-5:]:
            f = os.path.basename(s.get("filepath",""))
            orig = s.get("orig_size",1)
            comp = s.get("compressed_size",0)
            ratio = comp/orig if orig else 0
            tree.insert("", "end", values=(f, f"{ratio:.2f}"))
        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def main():

        setup_logging()

        if TkinterDnD:
            root = TkinterDnD.Tk()
        else:
            root = tk.Tk()

        app = CompressorGUI(root)
        root.mainloop()

import http.server, socketserver, json as _json

class _AgentState:
    paused = False
    cpu_cap = 85  # percent
    queue = []
    lock = _th.Lock()

def _agent_should_pause():
    try:
        return _AgentState.paused or psutil.cpu_percent(interval=1) > _AgentState.cpu_cap
    except Exception:
        return _AgentState.paused

class _SimpleHandler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = _json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/state"):
            with _AgentState.lock:
                self._send(200, {"paused": _AgentState.paused, "cpu_cap": _AgentState.cpu_cap, "queued": len(_AgentState.queue)})
        else:
            self._send(404, {"error":"not found"})

    def do_POST(self):
        if self.path.startswith("/pause"):
            _AgentState.paused = True
            self._send(200, {"ok": True, "paused": True})
        elif self.path.startswith("/resume"):
            _AgentState.paused = False
            self._send(200, {"ok": True, "paused": False})
        elif self.path.startswith("/cap/"):
            try:
                cap = int(self.path.split("/cap/")[1])
                _AgentState.cpu_cap = max(10, min(99, cap))
                self._send(200, {"ok":True, "cpu_cap":_AgentState.cpu_cap})
            except Exception:
                self._send(400, {"ok":False})
        else:
            self._send(404, {"error":"not found"})

def _agent_worker(out_dir, target_mb, adv_opts, webhook):
    while True:
        with _AgentState.lock:
            path = _AgentState.queue.pop(0) if _AgentState.queue else None
        if not path:
            time.sleep(0.5); continue

        while _agent_should_pause():
            time.sleep(2)
        try:
            media = get_media_type(path)
            if media == "video":
                auto_compress(path, out_dir, lambda m, level="INFO": None, target_mb, webhook, adv_opts, lambda: False)
            elif media in ("audio","image"):
                auto_compress(path, out_dir, lambda m, level="INFO": None, target_mb, webhook, adv_opts, lambda: False)

        except Exception as e:

            pass

class _AgentWatchHandler(FileSystemEventHandler):
    def __init__(self, out_dir, target_mb, adv_opts, webhook):
        self.out_dir = out_dir
        self.target_mb = target_mb
        self.adv_opts = adv_opts
        self.webhook = webhook
    def on_created(self, event):
        if not event.is_directory and os.path.isfile(event.src_path):
            with _AgentState.lock:
                _AgentState.queue.append(event.src_path)

def run_agent(watch_dir, out_dir, target_mb=10, webhook=""):

    adv_opts = {
        "encoder": "x264", "two_pass": False, "iterative": False,
        "manual_crf":"", "manual_bitrate":"", "output_prefix":"", "output_suffix":"_discord_ready",
        "audio_format":"aac", "image_format":"jpg", "concurrent": False,
        "auto_output_folder": False, "guetzli": False, "pngopt": False, "auto_jpeg": False
    }

    os.makedirs(out_dir, exist_ok=True)

    _th.Thread(target=_agent_worker, args=(out_dir, target_mb, adv_opts, webhook), daemon=True).start()

    obs = Observer()
    obs.schedule(_AgentWatchHandler(out_dir, target_mb, adv_opts, webhook), watch_dir, recursive=False)
    obs.start()

    with socketserver.TCPServer(("127.0.0.1", 8765), _SimpleHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            obs.stop(); obs.join()


def _cli_status(msg, level="INFO"):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def _cli_cancel():

    return False

def _ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p

def _infer_save_dir(out_arg, first_input):
    if out_arg:
        return _ensure_dir(os.path.abspath(os.path.expanduser(out_arg)))

    base = os.path.dirname(os.path.abspath(first_input)) or "."
    return base

def _build_adv_from_args(args) -> dict:
    adv = dict(ADVANCED_DEFAULTS)  # start from your defaults
    if args.encoder:
        adv["encoder"] = args.encoder
    if args.hwaccel:
        adv["hwaccel"] = args.hwaccel
    if args.two_pass:
        adv["two_pass"] = True
    if args.force_two_pass:
        adv["two_pass_forced"] = True
    if args.crf is not None:
        adv["manual_crf"] = str(args.crf)
    if args.bitrate is not None:
        adv["manual_bitrate"] = str(int(args.bitrate))
    if args.audio_format:
        adv["audio_format"] = args.audio_format
    if args.image_format:
        adv["image_format"] = args.image_format
    if args.prefix is not None:
        adv["output_prefix"] = args.prefix
    if args.suffix is not None:
        adv["output_suffix"] = args.suffix

    return adv

def _expand_inputs(inputs: list[str]) -> list[str]:
    expanded = []
    for item in inputs:
        item = os.path.expanduser(item)

        if any(ch in item for ch in "*?[]"):
            expanded.extend(glob(item, recursive=True))
        elif os.path.isdir(item):

            for root, _, files in os.walk(item):
                for f in files:
                    p = os.path.join(root, f)
                    if get_media_type(p) in {"video", "audio", "image"}:
                        expanded.append(p)
        else:
            expanded.append(item)

    seen = set()
    result = []
    for p in expanded:
        ap = os.path.abspath(p)
        if ap not in seen and os.path.exists(ap):
            seen.add(ap)
            result.append(ap)
    return result

def _print_summary(stats_list):
    if not stats_list:
        return
    print("\n=== Summary ===")
    for s in stats_list:
        try:
            in_sz = s.get("original_size")
            out_sz = s.get("compressed_size")
            ratio = (out_sz / in_sz) if in_sz else 0
            print(f"- {s.get('filename') or ''}  "
                  f"{format_bytes(in_sz)} → {format_bytes(out_sz)}  "
                  f"({ratio*100:.1f}% of original)")
        except Exception:
            pass

def build_arg_parser():
    p = argparse.ArgumentParser(
        prog="BitCrusher",
        description="Fast media compression (video/audio/image) — GUI by default, CLI with args.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("inputs", nargs="*", help="Files/folders/globs to compress (if empty, GUI launches)")
    p.add_argument("-o", "--output", help="Output directory (default: alongside first input)")
    p.add_argument("-t", "--target-size", type=float, default=10.0,
                   help="Target size in MB (applies to each item)")
    p.add_argument("--encoder", choices=["x264","x265","h264_nvenc","hevc_nvenc","h264_qsv","hevc_qsv","h264_amf","hevc_amf","av1"],
                   help="Video encoder to use")
    p.add_argument("--hwaccel", choices=["CPU","NVENC","QSV","AMF"], default="CPU",
                   help="Hardware acceleration hint (for GPU pipelines)")
    p.add_argument("--two-pass", action="store_true", help="Allow two-pass when beneficial")
    p.add_argument("--force-two-pass", action="store_true", help="Force two-pass regardless of heuristics")
    p.add_argument("--crf", type=int, help="Manual CRF (overrides prediction for video)")
    p.add_argument("--bitrate", type=int, help="Manual video bitrate in bps (forces ABR; may trigger 2-pass)")
    p.add_argument("--audio-format", choices=["opus","aac","mp3"], help="Preferred audio codec")
    p.add_argument("--image-format", choices=["jpg","png","webp"], help="Preferred image output format")
    p.add_argument("--prefix", default="", help="Output filename prefix")
    p.add_argument("--suffix", default="_discord_ready", help="Output filename suffix")
    p.add_argument("--webhook", help="Webhook URL to POST results")
    p.add_argument("-q", "--quiet", action="store_true", help="Less verbose CLI logging")
    p.add_argument("--version", action="store_true", help="Print version info and exit")
    return p

def cli_main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.version:
        print("BitCrusher CLI — powered by HandBrakeCLI/ffmpeg")
        return 0

    if not args.inputs:

        return None

    files = _expand_inputs(args.inputs)
    if not files:
        print("No matching files found.")
        return 1

    out_dir = _infer_save_dir(args.output, files[0])
    adv = _build_adv_from_args(args)
    target_mb = max(1, int(round(args.target_size)))
    stats_all = []

    if args.quiet:
        def _status_quiet(msg, level="INFO"):
            if level in ("ERROR","CRITICAL","WARNING"):
                _cli_status(msg, level)
        status_cb = _status_quiet
    else:
        status_cb = _cli_status

    for src in files:
        media = get_media_type(src)
        try:
            s = auto_compress(
                input_path=src,
                save_path=out_dir,
                status_callback=status_cb,
                target_size_mb=target_mb,
                webhook_url=(args.webhook or ""),
                advanced_options=adv,
                cancel_callback=_cli_cancel
            )

            if s is None:
                s = {}
            s.setdefault("filename", os.path.basename(src))
            s.setdefault("original_size", os.path.getsize(src))
            s.setdefault("compressed_size", os.path.getsize(
                os.path.join(out_dir, f"{adv.get('output_prefix','')}{Path(src).stem}{adv.get('output_suffix','_discord_ready')}.{ 'mp4' if media=='video' else ('opus' if adv.get('audio_format','opus')=='opus' else adv.get('audio_format','aac')) if media=='audio' else adv.get('image_format','jpg')}"))
                if os.path.exists(os.path.join(out_dir, f"{adv.get('output_prefix','')}{Path(src).stem}{adv.get('output_suffix','_discord_ready')}.{ 'mp4' if media=='video' else ('opus' if adv.get('audio_format','opus')=='opus' else adv.get('audio_format','aac')) if media=='audio' else adv.get('image_format','jpg')}")) else s.get("compressed_size", 0)
            )
            stats_all.append(s)
        except Exception as e:
            status_cb(f"❌ Failed: {src} — {e}", level="ERROR")

    _print_summary(stats_all)
    return 0

print("[DEBUG] about to enter main block")

if __name__ == "__main__":
    try:

        app = CompressorGUI()
        try:
            _BOOT_PHASE = False  # GUI constructed; suppress blocking crash popups from now on
        except Exception:
            pass

        if hasattr(app, "setup_ui"):
            app.setup_ui()
        if hasattr(app, "check_dependencies"):
            app.check_dependencies()

        app.root.mainloop()

    except Exception as e:
        import traceback
        print("[FATAL] Uncaught exception while launching GUI:", e)
        traceback.print_exc()








