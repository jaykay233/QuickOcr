#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocr_tray.py – macOS 菜单栏托盘 OCR
python3 ocr_tray.py          # 直接运行
"""
import os
import sys
import threading
import numpy as np
from PIL import Image
import pyscreenshot as ImageGrab
import easyocr
import rumps
from pynput import mouse
import time
import warnings
warnings.filterwarnings('ignore')

APP_NAME = "QuickOCR"

# macOS Retina 屏幕缩放因子（可动态获取，这里简化为 2）
SCALE = 1


class OcrTrayApp(rumps.App):
    def __init__(self):
        # 兼容 PyInstaller 打包后的资源路径
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        icon_path = os.path.join(base_dir, 'icon.png')

        super().__init__(APP_NAME, icon=icon_path, quit_button=None)

        # 初始化 EasyOCR（CPU）
        self.reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

        # 状态
        self.listening = False
        self.mouse_listener = None
        self.drag_start = None
        self.drag_end = None

        # 菜单
        self.listen_item = rumps.MenuItem("Start Listening", callback=self.toggle_listen)
        self.menu = [
            rumps.MenuItem("Quick OCR", callback=self.quick_ocr),
            None,
            self.listen_item,
            rumps.MenuItem("Quit", callback=lambda _: rumps.quit_application())
        ]

        # 默认不监听
        self.stop_listening()

    # ---------------- 菜单 ----------------
    def toggle_listen(self, _):
        if self.listening:
            self.stop_listening()
        else:
            self.start_listening()

    def start_listening(self):
        if self.mouse_listener is not None:
            return
        self.listening = True
        self.title = "🔍"
        self.listen_item.title = "Stop Listening"

        # 创建并启动鼠标监听器
        self.mouse_listener = mouse.Listener(on_click=self._on_mouse_event)
        self.mouse_listener.start()

    def stop_listening(self):
        if self.mouse_listener is None:
            return
        self.listening = False
        self.title = "⏸️"
        self.listen_item.title = "Start Listening"

        self.mouse_listener.stop()
        self.mouse_listener = None

    @rumps.clicked("Quick OCR")
    def quick_ocr(self, _):
        threading.Thread(target=self.run_ocr_once, daemon=True).start()

    # ---------------- 鼠标事件 ----------------

    def _on_mouse_event(self, x, y, button, pressed):
        if button != mouse.Button.left:
            return

        x *= SCALE
        y *= SCALE

        if pressed:
            self.drag_start = (x, y)
        else:
            # 抖动过滤
            if abs(x - self.drag_start[0]) < 8 and abs(y - self.drag_start[1]) < 8:
                return
            self.drag_end = (x, y)

            left, top = min(self.drag_start[0], x), min(self.drag_start[1], y)
            right, bottom = max(self.drag_start[0], x), max(self.drag_start[1], y)
            if right - left < 10 or bottom - top < 10:
                return

            threading.Thread(target=self.run_ocr_once, daemon=True).start()
    
    # ---------------- OCR 核心 ----------------
    def run_ocr_once(self):
        try:
            if self.drag_start is None or self.drag_end is None:
                return

            x1, y1 = self.drag_start
            x2, y2 = self.drag_end
            left, top = min(x1, x2), min(y1, y2)
            right, bottom = max(x1, x2), max(y1, y2)
            print(x1, x2, y1, y2)
            if right - left < 10 or bottom - top < 10:
                return
            print("ok")
            # 截图并保存调试图
            img = ImageGrab.grab(bbox=(left, top, right, bottom))
            img.save("/Users/mason/Downloads/debug_ocr.png")  # 调试用

            # 放大 + 灰度 + OCR
            img = img.convert("L").resize((img.width * 2, img.height * 2), Image.LANCZOS)
            results = self.reader.readtext(np.array(img), detail=0, low_text=0.3)
            text = "\n".join(results).strip()

            if text:
                import subprocess
                subprocess.run(["pbcopy"], input=text.encode())
                rumps.notification(title=APP_NAME, subtitle="已复制", message=text[:60])
            else:
                rumps.notification(title=APP_NAME, subtitle="提示", message="未识别到文字")
        except Exception as e:
            rumps.notification(title=APP_NAME, subtitle="出错", message=str(e))


if __name__ == "__main__":
    OcrTrayApp().run()
