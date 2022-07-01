

import os
import fileopt

if __name__ == "__main__":
    ftpip = '192.168.200.228'
    ftpcwd = '/export/yangwang'
    ftpusr = 'yangwang'
    ftppass = 'hello,wy'
    update_filename = "p301d"
    remoteip = '192.168.10.101'
    upload_filename = update_filename

    boardusr = 'root'
    boardpass = 'artosyn'

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        update_filename, update_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, boardusr, boardpass)

    os.system("pause")
