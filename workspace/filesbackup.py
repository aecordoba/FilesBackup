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

    now = datetime.now()

    for filename in config.filenames:
#        size = ftp.size(filename)
#        modification_time = ftp.sendcmd('MDTM ' + filename)
#        modification_time = datetime.strptime(modification_time[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
#        print(f'{filename}:\t{size}\t{modification_time}')
#        remote_modification = ftp.voidcmd("MDTM " + filename)
#        modification_time = datetime.strptime(remote_modification[4:], "%Y%m%d%H%M%S")
#        print(f'Remote file: {modification_time} /Diff: {now - modification_time}')

    
        file = File(filename, ftp.size(filename), datetime.strptime(ftp.sendcmd('MDTM ' + filename)[4:], "%Y%m%d%H%M%S"))
        print(file)





    ftp.quit()


# call main().
if __name__ == '__main__':
    main()
