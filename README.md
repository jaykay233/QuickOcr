# QuickOCR  
**A tiny macOS menu-bar utility for drag-to-copy OCR**

---

## ✨ What it does

- Left-drag anywhere → **instantly extract text**  
- One-click icon → **copy to clipboard**  
- CPU-only build → **no GPU, no hassle**  
- Zero-config menu-bar app → **always ready**

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourname/quickocr.git
cd quickocr
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 ocr_tray.py
```

Drag on the screen → text lands in your clipboard!

---

## 🛠️ Build Your Own `.app`

```bash
pip install pyinstaller
pyinstaller ocr_tray.py \
  --name QuickOCR \
  --onefile \
  --windowed \
  --icon icon.icns \
  --collect-all rumps \
  --collect-all easyocr \
  --collect-all torch \
  --collect-all torchvision \
  --clean
```

Drop `dist/QuickOCR.app` into `/Applications`.

---

## 📂 Project Layout

```
quickocr/
├── ocr_tray.py          # main script
├── requirements.txt     # dependencies
├── icon.icns            # app icon
├── LICENSE              # MIT
└── README.md            # you are here
```

---

## 📄 Requirements

- Python ≥ 3.11  
- macOS ≥ 12 (for rumps & accessibility permissions)

### Install via pip
```txt
rumps
easyocr
pillow
pyscreenshot
pynput
numpy
```

---

## ⚙️ Customize

| Variable | Purpose |
|----------|---------|
| `SCALE = 2` | Retina scaling |
| `JITTER_THRESHOLD = 8` | ignore micro-drags |
| `SAVE_DIR` | debug screenshots path |

---

## 🔐 Permissions

On first run grant:

- **System Settings → Privacy & Security → Accessibility**  
- **System Settings → Privacy & Security → Input Monitoring**

Select `QuickOCR.app` in both lists.

---

## 📄 License

MIT © 2024 [jaykay233](https://github.com/jaykay233)

---

⭐ **Star if it saves your day!**
