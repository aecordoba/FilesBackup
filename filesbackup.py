#!/usr/bin/python3
# filesbackup.py
"""Application for check the files status and guard them from a server."""

import os
import shutil
from datetime import datetime, timedelta
from ftplib import FTP, all_errors
from pytz import timezone
import config
from file import File

DAYS_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def main():
    now = datetime.now(timezone('America/Argentina/Buenos_Aires'))
    try:
        ftp = FTP(config.server['ip'])
        ftp.login(user=config.server['username'],
            passwd=config.server['password'])

        print(now, ": Backup in progress...", sep='')
        files = []

        for filename in config.filenames:
            file = File(filename, ftp.size(filename), datetime.strptime(
                ftp.sendcmd('MDTM ' + filename)[4:], "%Y%m%d%H%M%S"))
            files.append(file)

        for file in files:
            if (file.modification_time + timedelta(days=1)) < now:
                print(file.filename, "file not modified in last 24 hours. Last modification:", file.modification_time, ".")
            else:
                print(file.filename, " (size: ", file.size, " last modification: ", file.modification_time, ") was found.", sep='')
                localfile = open(file.filename, 'wb')
                ftp.retrbinary('RETR ' + file.filename, localfile.write, 1024)
                localfile.close()
                if file.size == os.path.getsize(file.filename):
                    print("Successfully downloaded ", file.filename, " (", file.size, " bytes).", sep='')

                    destination = config.base_directory
                    if file.modification_time.day == 1 or file.modification_time.day == 15:
                        destination += "yearly/" + file.modification_time.strftime("%B")[0:3].lower() + file.modification_time.strftime("%d") + "/"
                    else:
                        destination += DAYS_OF_WEEK[file.modification_time.weekday()] + \
                                       "/"

                    shutil.move(file.filename, destination + file.filename)
                    print(file.filename, " successfully moved to ", destination, ".", sep='')
                else:
                    print(file.filename, "file could not be downloaded. Original file size:", file.size, "Downloaded file size:", os.path.getsize(file.filename))

        ftp.quit()

    except all_errors as e:
        print(now, ": FTP error: ", e, sep='')


# call main().
if __name__ == '__main__':
    main()
