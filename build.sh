pyinstaller ocr_tray.py \
  --name OCR \
  --collect-all rumps \
  --collect-all easyocr \
  --collect-all torch \
  --collect-all torchvision \
  --hidden-import PIL._imaging \
  --clean
