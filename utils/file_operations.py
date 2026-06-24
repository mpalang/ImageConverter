# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:41:37 2026

@author: morit
"""
from pathlib import Path
import os
from PIL import Image
import pillow_heif

def get_files(input_path,file_extension,subfolders=True):
    file_extension = file_extension.lower()
    if subfolders:
        files = list(Path(input_path).rglob(f'*.{file_extension}', case_sensitive=False))
    else:
        files = list(Path(input_path).glob(f'*.{file_extension}', case_sensitive=False))
        
    return files

                    
def copy_file(file_in,file_out,format_in,format_out):
    if format_in=='heic':
        img = read_heic(file_in)
        
        
    if format_out=='png':
        img.save(file_out, format=format_out)
    elif format_out=='jpg':
        img.save(file_out, quality=95)


def read_heic(file):
    pillow_heif.register_heif_opener()
    img = Image.open(file)
    return img
    
def delete_file(old_file,new_file):
    #delete original
    if os.path.getsize(new_file)>0:
        os.unlink(old_file)
    else:
        print("Maybe something wrong with the copying...")