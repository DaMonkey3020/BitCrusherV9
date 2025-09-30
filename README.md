# BitCrusherV9

My attempt at building a file compressor.
I hope everyone can all enjoy this as much as I enjoyed making it and using it.

---

## What this release is

This is the **initial full portable release** of BitCrusher.
Everything is bundled up so you can literally **drop and run**—no messing with Python installs or digging around for dependencies.

Stuff is still a little wobbly in corner cases, but the **GUI and main compression engine are as solid as rocks**.
In case you notice bugs, make an Issue here or ping me. Logs are automatically generated so you can simply send me the file and I can easily locate it.

---

## Installation & First Run

If I didn't mess things up (fingers crossed), you just:

1. **Download and unzip** the release `.zip`.
2. **Double-click** `Run_Bitcrusher_s.cmd`.

That's it.
No `pip install`, no subtle setup wizard, no dependency chase manually.

Some heads-up:

* Only works on **Windows 10 and 11**.
* First run will **always** be slow—Python is warming up caches and loading the site-packages.
* The better your PC, the more smoothly and fastly it runs.
  Don't grump if your machine is crap—upgrade when you can.
* Automatically saves logs in the `logs` directory.

---

## Feature Deep Dive

BitCrusher is more than just another "zip it smaller" tool.
Here's what happens behind the scenes:

### Core Compression
- **Smart target size**: Give it a size (e.g. `8 MB`) and it dynamically resizes the correct CRF / bitrate through `ffmpeg` and `HandBrakeCLI`.
- **Multi-format**: Compresses video, audio, and photos without extra tools.
- **Predictive heuristics**: Combined `smart_rate.py` model to choose optimal CRF even on first encode.

### Modern GUI
- Done with **Tkinter + TkinterDnD2** for actual drag-and-drop.
- Pile up multiple files; observe progress in real time.
- Dark/clean theme optimized in `ui_aesthetics.py`.

### Internationalization
- **Deep Translator** integration.
- Real-time UI translation—so you can change languages on the fly.

### Utility Stack
- **Portable Python runtime** included.
- **Full dependency package** in `site/Lib/site-packages`.
- Fully offline when executed after download.

### Developer-Friendly
- Automatic logging to `logs/`.
- Plain JSON files for all configuration.
- Code authored for Python 3.13 and readily updatable with packaging.

---



