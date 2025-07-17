from pynput import mouse
from PIL import Image
import pyscreenshot as ImageGrab
import easyocr, pyperclip, threading
import numpy as np
# 初始化 EasyOCR 识别器（中文+英文，GPU=False 兼容所有电脑）
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

start_x = start_y = None

def on_click(x, y, button, pressed):
    global start_x, start_y
    if button != mouse.Button.left:
        return
    if pressed:                      # 按下左键，记录起点
        start_x, start_y = x, y
    else:                            # 松开左键，截图并 OCR
        end_x, end_y = x, y
        if start_x is None:
            return
        left, top    = min(start_x, end_x), min(start_y, end_y)
        right, bottom = max(start_x, end_x), max(start_y, end_y)
        if abs(right-left) < 10 or abs(bottom-top) < 10:
            return
        img = ImageGrab.grab(bbox=(left, top, right, bottom))
        img_np = np.asarray(img)
	# EasyOCR 返回 [(bbox, text, confidence), ...]
        results = reader.readtext(img_np, detail=0)   # detail=0 只返回文字列表
        text = '\n'.join(results).strip()
        if text:
            pyperclip.copy(text)
            print('已复制到剪贴板：\n', text)
        else:
            print('未识别到文字')
        return False   # 结束监听

print('按住左键拖一个框，松开后自动 OCR → 剪贴板。按 Ctrl+C 退出。')
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
