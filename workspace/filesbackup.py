#!/usr/bin/python3
# filesbackup.py
"""Application for check the files status and guard them from a server."""
from ftplib import FTP
from datetime import datetime
from datetime import timedelta
from file import File
import config


def main():
    ftp = FTP(config.server['ip'])
    ftp.login(user=config.server['username'], passwd=config.server['password'])

#    now = datetime.now()
    now = datetime(2020, 1, 18)
    print(now)
    files = []

    for filename in config.filenames:
        file = File(filename, ftp.size(filename), datetime.strptime(ftp.sendcmd('MDTM ' + filename)[4:], "%Y%m%d%H%M%S"))
        files.append(file)

    for file in files:
        if (file.modiffication_time + timedelta(days=1)) < now:
            print(f'{file.filename} file not modiffied in last 24 hours. Last modiffication: {file.modiffication_time}.')





    ftp.quit()


# call main().
if __name__ == '__main__':
    main()
