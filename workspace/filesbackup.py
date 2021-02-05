#!/usr/bin/python3
# filesbackup.py
"""Application for check the files status and guard them from a server."""
from ftplib import FTP
from datetime import datetime
import config


def main():
    ftp = FTP(config.server['ip'])
    ftp.login(user=config.server['username'], passwd=config.server['password'])

    for filename in config.filenames:
        size = ftp.size(filename)
        modification_time = ftp.sendcmd('MDTM ' + filename)
        modification_time = datetime.strptime(modification_time[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
        print(f'{filename}:\t{size}\t{modification_time}')


    ftp.quit()


# call main().
if __name__ == '__main__':
    main()
