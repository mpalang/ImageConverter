# -*- coding: utf-8 -*-
"""
Created on Sat May 30 14:27:42 2026

@author: moritz
"""

from pathlib import Path
from PIL import Image
import pillow_heif
import os
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QProgressBar,
    QStyle,
    QMessageBox,
)
# from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys

if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent))
from cpp import png_reader
from utils.file_operations import get_files, copy_file, delete_file


class MainWindow(QWidget):
    def __init__(self, default_input_path):
        
        #Initialize
        super().__init__()
        
        self.setWindowTitle("Image Converter")
        self.resize(300, 300)
        layout = QVBoxLayout()
        
        #Options:
        layout.addWidget(QLabel("Options:"))
        layout_folder = QHBoxLayout()
        self.entry_inputpath = QLineEdit()
        self.entry_inputpath.setText(default_input_path)
        layout_folder.addWidget(self.entry_inputpath)
        button_folder = QPushButton()
        button_folder.clicked.connect(self.filepath_dialog)
        button_folder.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        layout_folder.addWidget(button_folder)
        layout.addLayout(layout_folder)
       
        self.cb_subfolders = QCheckBox("include subfolders")
        self.cb_subfolders.setChecked(True)
        layout.addWidget(self.cb_subfolders)
        self.cb_deloriginal = QCheckBox("delete original")
        self.cb_deloriginal.setChecked(False)
        layout.addWidget(self.cb_deloriginal)
        self.cb_extrafolder = QCheckBox("create extra folder")
        self.cb_extrafolder.setChecked(False)
        layout.addWidget(self.cb_extrafolder)
        
        layout_format = QHBoxLayout()
        self.format_in = QComboBox()
        self.format_in.addItems(["HEIC", "HEIF","PNG","ICO","JPG"])
        layout_format.addWidget(self.format_in)
        self.format_out = QComboBox()
        self.format_out.addItems(["HEIC","PNG","ICO","JPG", "PNG"])
        layout_format.addWidget(self.format_out)
        layout.addLayout(layout_format)
        
        # Progress
        layout.addWidget(QLabel("Progress:"))
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # Set min/max steps
        self.progress_bar.setValue(0)       # Initial value
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel('Ready \n\n')
        self.status_label.setFixedWidth(180)
        self.status_label.setFixedHeight(60)
        self.status_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.status_label)
        
        # Execute  
        layout_execute = QHBoxLayout()
        button_go = QPushButton("Go")
        button_go.clicked.connect(self.copy_files)
        layout_execute.addWidget(button_go)
        button_exit = QPushButton("Exit")
        button_exit.clicked.connect(self.exit_app)
        layout_execute.addWidget(button_exit)
        layout.addLayout(layout_execute)
        
        self.setLayout(layout)

    # =============================================================================
    # =============================================================================
    # Functions
    # =============================================================================

    def filepath_dialog(self):
        # Opens dialog and returns selected directory path
        self.input_path = QFileDialog.getExistingDirectory(self, "Select Directory", self.entry_inputpath.text())
        if self.input_path:
            self.entry_inputpath.setText(self.input_path)

    def copy_files(self):
      try: 
        self.input_path = self.entry_inputpath.text()
        self.format_in = self.format_in.currentText().lower()
        self.format_out = self.format_out.currentText().lower()
        self.include_subfolders = self.cb_subfolders.isChecked()
        
        #Get files:
        files = get_files(self.input_path,self.format_in,subfolders=self.include_subfolders)
           
        if len(files)>0:
            for n,file in enumerate(files):
                # create a new filename for the PNG file
                new_file = self.make_filename(file)
                
                #Output:
                self.status_label.setText(
                        f'''saving file ({n+1}/{len(files)}): {Path(new_file).name}
                        To: {Path(new_file).parent}
                        Format: {self.format_out}'''                              )
                QApplication.processEvents()
                
                copy_file(file,new_file,self.format_in,self.format_out)
                
                if self.cb_deloriginal.isChecked():
                    try:
                        delete_file(file,new_file)
                    except Exception as e:
                        QMessageBox.critical(self,'Error',f'Could not delete file:\n {e}')
                
            self.progress_bar.setValue(int((n + 1) / len(files) * 100))
            QApplication.processEvents()
            
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No HEIC files")
            self.status_label.setText('No HEIC files found.')
            QApplication.processEvents() 
            
        #Output:
        self.status_label.setText('Done :). Ready to go again.')
        self.progress_bar.setValue(0)
        QApplication.processEvents() 
        
      except Exception as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An error occurred")
        msg.setInformativeText(str(e))
        msg.setDetailedText(str(e)) # Optional: shows full traceback if formatted
        msg.setWindowTitle("Error")
        msg.exec_()
    
    def make_filename(self,file):
        if self.cb_extrafolder.isChecked():
            output_folder = f'{self.format_in.upper()}_to_{self.format_out.upper()}'
            os.makedirs(Path(self.input_path,output_folder), exist_ok=True)
            new_file = Path(self.input_path,output_folder,file.stem+'.'+self.format_out)
        else:
            new_file = Path(file).with_suffix('.'+self.format_out.lower())
            
        return new_file
    
    def exit_app(self):
        self.close()
  
  
# =============================================================================
# =============================================================================
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if type(sys.argv) == str:
        default_input_path = sys.argv
    else:
        default_input_path = r'C:\Users'
    
    window = MainWindow(default_input_path)
    window.show()

    sys.exit(app.exec())

