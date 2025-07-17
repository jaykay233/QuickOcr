from setuptools import setup

APP = ['ocr_tray.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['rumps', 'easyocr', 'PIL', 'pynput', 'numpy'],
    'excludes': [
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'matplotlib',
        'scipy', 'test', 'unittest', 'setuptools', 'pkg_resources','cv2', 'torch', 'sklearn', 'IPython', 'tornado', 'zmq', 'test'
    ],
    'iconfile': 'icon.icns',
    'plist': {'LSUIElement': True},
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
