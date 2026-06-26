# -*- coding: utf-8 -*-
"""
Created on Sat May 30 14:27:42 2026

@author: moritzpalang
"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
import sys
from pathlib import Path

if str(Path(__file__)) not in sys.path:
    sys.path.append(str(Path(__file__)))
from gui.MainWindow import MainWindow
from utils.logger import setup_logger, add_logger
setup_logger()
logger = add_logger(__name__)

if __name__=='__main__':
    QCoreApplication.setOrganizationName("SmoereApps")
    QCoreApplication.setApplicationName("FancyFit")
    
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)
                
    window = MainWindow()
    window.show()

    
    if not QApplication.instance().startingUp():
        sys.exit(app.exec())
    else:
       app.exec()
    app = QApplication(sys.argv)
    


