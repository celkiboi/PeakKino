import os
from .models import *

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
        os.rmdir(folder_path)

def srt_to_vtt(srt_content):
    lines = srt_content.splitlines()
    vtt_content = "WEBVTT\n\n"
    
    for line in lines:
        if '-->' in line:
            line = line.replace(',', '.')
        vtt_content += line + '\n'

    return vtt_content