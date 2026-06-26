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
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys
import traceback

if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import add_logger
logger = add_logger(__name__)


class MainWindow(QWidget):
    def __init__(self):

        #Initialize
        super().__init__()
        icon_path = Path(Path(__file__).parent.parent,'icon.ico')
        self.setWindowIcon(QIcon(str(icon_path)))
        self.build_gui()

    # =============================================================================
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Functions
    # =============================================================================
    
    def build_gui(self):
        self.setWindowTitle("Image Converter")
        self.resize(300, 300)
        layout = QVBoxLayout()
        
        
        #Options:
        layout.addWidget(QLabel("Options:"))
        layout_folder = QHBoxLayout()
        self.entry_inputpath = QLineEdit()
        #self.entry_inputpath.setText(self.path)
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
        self.format_in_input = QComboBox()
        self.format_in_input.addItems(["HEIC","JPEG","PNG","ICO"])
        layout_format.addWidget(self.format_in_input)
        self.format_out_input = QComboBox()
        self.format_out_input.addItems(["JPEG","PNG","ICO"])
        layout_format.addWidget(self.format_out_input)
        layout.addLayout(layout_format)
        
        # Progress
        layout.addWidget(QLabel("Progress:"))
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # Set min/max steps
        self.progress_bar.setValue(0)       # Initial value
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel('Ready \n\n')
        self.status_label.setFixedWidth(180)
        self.status_label.setFixedHeight(90)
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
        self.format_in = self.format_in_input.currentText().lower()
        self.format_out = self.format_out_input.currentText().lower()
        
        
        #Get files:
        files = self.get_files()
           
        if len(files)>0:
            for n,file in enumerate(files):
                # create a new filename for the PNG file
                new_file = self.make_filename(file)
                
                #Output:
                self.status_label.setText(
                        f'''saving file ({n+1}/{len(files)}):
{Path(new_file).name}
To: {Path(new_file).parent}
Format: {self.format_out}
                        ''')
                                   
                pillow_heif.register_heif_opener()
                img = Image.open(file)
                if self.format_out == 'jpeg':
                    if len(img.split()) == 4:
                        img_old = img
                        img = Image.new("RGB", img_old.size, (255, 255, 255))
                        img.paste(img_old, mask=img_old.split()[3])
                    else:
                        if img.mode != 'RGB':
                            img = img.convert('rgb')

                img.save(new_file, format=self.format_out.upper())
                img.close()
                
                if Path(new_file).exists():
                     logger.info(f'Copied file {Path(file)} to {Path(new_file)}')
                
                if self.cb_deloriginal.isChecked():
                    try:
                        self.delete_file(file)
                        logger.info(f'Deleted {Path(file)}.')
                    except Exception as e:
                        QMessageBox.critical(self,'Error',f'Could not delete file:\n {e}')
                        logger.exception('Error deleting file')
                
                self.progress_bar.setValue(int((n + 1) / len(files) * 100))
                QApplication.processEvents()
                
               
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"No {self.format_in}-files")
            self.status_label.setText(f'No {self.format_in}-files found.')
            QApplication.processEvents() 
            
        #Output:
        self.status_label.setText('Done :). Ready to go again.')
        self.progress_bar.setValue(0)
        QApplication.processEvents() 
        
      except Exception as e:
        logger.exception('Copying failed.')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An error occurred")
        msg.setInformativeText(str(e))
        msg.setDetailedText(traceback.format_exc()) # Optional: shows full traceback if formatted
        msg.setWindowTitle("Error")
        msg.exec_()

    def get_files(self):
        if self.cb_subfolders.isChecked():
            files = list(Path(self.input_path).rglob(f'*.{self.format_in}', case_sensitive=False))
        else:
            files = list(Path(self.input_path).glob(f'*.{self.format_in}', case_sensitive=False))
        return files
    
    def make_filename(self,file):
        if self.cb_extrafolder.isChecked():
            output_folder = f'{self.format_in.upper()}_to_{self.format_out.upper()}'
            os.makedirs(Path(self.input_path,output_folder), exist_ok=True)
            new_file = Path(self.input_path,output_folder,file.stem+'.'+self.format_out)
        else:
            new_file = Path(file).with_suffix('.'+self.format_out.lower())
            
        return new_file
    
    def delete_file(self,file):
        if Path(file).exists():
            if Path(file).stat().st_size:
                Path(file).unlink()
            
                 
    def exit_app(self):
        self.close()
  
  
# =============================================================================
# =============================================================================
        
if __name__ == "__main__":
        # app = QApplication(sys.argv)
        
        # if type(sys.argv) == str:
        #     default_input_path = sys.argv
        # else:
        #     default_input_path = r'C:\Users'
        
        # window = MainWindow(default_input_path)
        # window.show()

        # sys.exit(app.exec())

    # Spyder workaround:
        app = QApplication.instance()

        if app is None:
            app = QApplication(sys.argv)

        if type(sys.argv) == str:
            default_input_path = sys.argv
        else:
            default_input_path = r'C:\Users\morit\OneDrive\Bilder\Test'
        
        window = MainWindow(default_input_path)
        window.show()

        if not QApplication.instance().startingUp():
            sys.exit(app.exec())
        else:
            app.exec()

