#!/usr/bin/python3
# filesbackup.py
"""Application for check the files status and guard them from a server."""

import ftplib
import os
import shutil
from datetime import datetime, timedelta
from ftplib import FTP
from pathlib import Path

from pytz import timezone

import config
from file import File

DAYS_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def main():
    try:
        ftp = FTP(config.server['ip'])
        ftp.login(user=config.server['username'],
                  passwd=config.server['password'])

        now = datetime.now(timezone('America/Argentina/Buenos_Aires'))
        print(f'{now}: Backup in progress...')
        files = []

        for filename in config.filenames:
            file = File(filename, ftp.size(filename), datetime.strptime(
                ftp.sendcmd('MDTM ' + filename)[4:], "%Y%m%d%H%M%S"))
            files.append(file)

        for file in files:
            if (file.modification_time + timedelta(days=1)) < now:
                print(
                    f'{file.filename} file not modified in last 24 hours. Last modification: {file.modification_time}.')
            else:
                localfile = open(file.filename, 'wb')
                ftp.retrbinary('RETR ' + file.filename, localfile.write, 1024)
                localfile.close()
                if file.size == os.path.getsize(file.filename):
                    print(
                        f'Successfully downloaded {file.filename} ({file.size} bytes).')

                    destination = config.base_directory
                    if file.modification_time.day == 1:
                        destination += "1st/"
                    elif file.modification_time.day == 15:
                        destination += "15th/"
                    else:
                        destination += DAYS_OF_WEEK[file.modification_time.weekday()] + \
                            "/"

                    shutil.move(file.filename, f'{destination}{file.filename}')
                    print(f'{file.filename} successfully moved to {destination}.')
                else:
                    print(f'{file.filename} file couldn\'t be downloaded.\n\tOriginal file size: {file.size}.\n\tDownloaded file size: {os.path.getsize(file.filename)}')

        ftp.quit()

    except ftplib.all_errors as e:
        print("FTP error:", e)


# call main().
if __name__ == '__main__':
    main()
