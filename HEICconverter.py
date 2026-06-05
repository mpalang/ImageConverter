# -*- coding: utf-8 -*-
"""
Created on Sat May 30 14:27:42 2026

@author: moritz
"""

from pathlib import Path
from PIL import Image
import pillow_heif
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import sys


class front_end:
    def __init__(self):
        
        self.root = tk.Tk()
        
        # Setting some window properties
        self.root.title("HEIC converter")
        # self.root.configure(background="")
        self.root.resizable(False, False)
        self.root.geometry("300x280+50+50")
        
        frame_settings = tk.Frame(self.root)
        frame_settings.pack()
        #settings:   
        self.input_path = tk.StringVar(self.root,r"P:\My Pictures\Favoriten\2024\Test")
        self.include_subfolders = tk.BooleanVar(value=True)
        self.file_format = tk.StringVar(self.root,'JPG')
        self.delete_original = tk.BooleanVar(value=False)
        self.extra_output_folder = tk.BooleanVar(value=False)
        
        entry_filepath = tk.Entry(frame_settings,text = self.input_path,width=40)
        entry_filepath.grid(row=1,column=1)
        button_filepath = tk.Button(frame_settings,text='find',command=self.filepath_dialog) 
        button_filepath.grid(row=1,column=2)
       
        checkbox_subfolder = tk.Checkbutton(frame_settings, text="convert subfolders", variable=self.include_subfolders)
        checkbox_subfolder.grid(row=2,column=1,sticky='w'   )
        checkbox_delete_original = tk.Checkbutton(frame_settings, text="delete original", variable=self.delete_original)
        checkbox_delete_original.grid(row=3,column=1,sticky='w')
        checkbox_extra_folder = tk.Checkbutton(frame_settings, text="create extra folder", variable=self.extra_output_folder)
        checkbox_extra_folder.grid(row=4,column=1,sticky='w')
        
        dropdown_format = tk.OptionMenu(frame_settings, self.file_format, *['JPG','PNG'])
        dropdown_format.grid(row=5,column=1,sticky='w')
        
        
        # =============================================================================
        # Progress bar
        # =============================================================================
        
        frame_progress = tk.Frame(self.root)
        frame_progress.pack(pady=10)
        
        self.progress = ttk.Progressbar(
                            frame_progress,
                            orient="horizontal",
                            length=400,
                            mode="determinate",
                            maximum=100
                        )
        self.progress.grid(row=1,column=1,sticky='w')
         
        self.status_label1 = tk.Label(frame_progress, text="Ready")
        self.status_label1.grid(row=2,column=1,sticky='w')
        self.status_label2 = tk.Label(frame_progress, text="")
        self.status_label2.grid(row=3,column=1,sticky='w')
        
        # =============================================================================
        # =============================================================================
                
        frame_execute = tk.Frame(self.root)
        frame_execute.pack()
        
        button_go = tk.Button(frame_execute,text = 'Go',command= self.copy_files) 
        button_go.grid(row=10,column=1)
        button_exit = tk.Button(frame_execute,text = 'Exit',command=self.exit_app) 
        button_exit.grid(row=10,column=2)
        # button_test = tk.Button(frame_execute,text = 'Test',command=self.test) 
        # button_test.grid(row=10,column=3)
        
        self.root.mainloop()

        
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # =============================================================================
    # Functions
    # =============================================================================
    def test(self):
        pass
        
    def filepath_dialog(self):
        input_path = filedialog.askdirectory(title="Select a sFile",initialdir=self.input_path.get())
        self.input_path.set(input_path)

    def copy_files(self):
        
        input_path = self.input_path.get()
        file_format = self.file_format.get()
        
        #Get files:
        if self.include_subfolders.get():
            HEIC_files = list(Path(input_path).rglob('*.HEIC'))
        else:
            HEIC_files = list(Path(input_path).glob('*.HEIC'))
        
        for n,file in enumerate(HEIC_files):
            # create a new filename for the PNG file
            if self.extra_output_folder.get():
                output_folder = 'HEICto'+file_format.upper()
                os.makedirs(Path(input_path,output_folder), exist_ok=True)
                new_file = Path(input_path,output_folder,file.stem+'.'+file_format.lower())
            else:
                new_file = Path(file).with_suffix('.'+file_format.lower())
            
            #Output:
            self.status_label1.config(
                        text=f'saving file ({n+1}/{len(HEIC_files)}): {Path(new_file).name}'
                    )
            self.status_label2.config(
                        text=f'To: {Path(new_file).parent}'
                    )

            self.progress["value"] = 100*(n+1)/len(HEIC_files)
            self.root.update_idletasks()
            
            #Copy HEIC file to new format
            pillow_heif.register_heif_opener()
            img = Image.open(file)
            if file_format == 'JPG':
                img.save(new_file, quality=95)
            else:
                img.save(new_file, format=file_format)
            
            #delete original
            if self.delete_original.get():
                if os.path.getsize(file)<os.path.getsize(new_file):
                    os.unlink(file)
                else:
                    print('Error') 
        
        #Output:
        self.status_label1.config(
                    text='Done! Ready for the next one :)')
        self.status_label2.config(
                    text='')

        self.progress["value"] = 0
        self.root.update_idletasks()
        
    def exit_app(self):
        self.root.destroy()
  
  

if __name__ == '__main__':
    front_end()
