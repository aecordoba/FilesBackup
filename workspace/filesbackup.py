#!/usr/bin/python3
# filesbackup.py
"""Application for check the files status and guard them from a server."""
import shutil
import os
import tkinter as tk
from datetime import datetime, timedelta
from ftplib import FTP
from pathlib import Path
from tkinter import ttk
from pytz import timezone

import config
from file import File

DAYS_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def main():
    ftp = FTP(config.server['ip'])
    ftp.login(user=config.server['username'], passwd=config.server['password'])

    now = datetime.now(timezone('America/Argentina/Buenos_Aires'))
    print(f'{now}: Backup in progress...')
    files = []

    for filename in config.filenames:
        file = File(filename, ftp.size(filename), datetime.strptime(ftp.sendcmd('MDTM ' + filename)[4:], "%Y%m%d%H%M%S"))
        files.append(file)

    for file in files:
        if (file.modification_time + timedelta(days=1)) < now:
            print(f'{file.filename} file not modified in last 24 hours. Last modification: {file.modiffication_time}.')
            popup_message("WARNING!", f'{file.filename} file not modified in last 24 hours.\nLast modification: {file.modification_time}.')
        else:
            localfile = open(file.filename, 'wb')
            ftp.retrbinary('RETR ' + file.filename, localfile.write, 1024)
            localfile.close()
            if file.size == os.path.getsize(file.filename):
                shutil.move(file.filename, f'/backup/sgi_backup/{DAYS_OF_WEEK[file.modification_time.weekday()]}/{file.filename}')
                print(f'Successfully downloaded {file.filename} ({file.size} bytes).')
            else:
                popup_message("WARNING!", f'{file.filename} file couldn\'t be downloaded.\nOriginal file size: {file.size}.\nDownloaded file size: {os.path.getsize(file.filename)}')

    ftp.quit()


def popup_message(title, message):
    popup = tk.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=message, font=("Helvetica", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Ok", command = popup.destroy)
    B1.pack()
    popup.mainloop()


# call main().
if __name__ == '__main__':
    main()
