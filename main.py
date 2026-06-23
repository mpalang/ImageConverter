# -*- coding: utf-8 -*-
"""
Created on Sat May 30 14:27:42 2026

@author: moritz
"""
from PySide6.QtWidgets import QApplication
import sys
from pathlib import Path

if str(Path(__file__)) not in sys.path:
    sys.path.append(str(Path(__file__)))
from gui.MainWindow import MainWindow
from cpp import read_png


def main():
    app = QApplication(sys.argv)
    
    if type(sys.argv) == str:
        default_input_path = sys.argv
    else:
        default_input_path = r'C:\Users'
    
    window = MainWindow(default_input_path)
    window.show()

    sys.exit(app.exec())
        
if __name__ == "__main__":
    main()
