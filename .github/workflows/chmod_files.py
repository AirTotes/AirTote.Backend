from ftplib import FTP_TLS
from sys import argv

def chmod_recursive(ftp: FTP_TLS, path: str):
  items = ftp.mlsd(path)
  for fname,opt in items:
    path_to_file = path + '/' + fname

    if opt['type'] == 'dir':
      chmod_recursive(ftp, path_to_file)
    elif opt['type'] == 'file':
      if fname.endswith('.sh'):
        if opt['unix.mode'] != '0700':
          ftp.sendcmd('SITE CHMOD 700 ' + path_to_file)
      elif opt['unix.mode'] != '0604':
        ftp.sendcmd('SITE CHMOD 604 ' + path_to_file)

with FTP_TLS(
    host=argv[2],
    user=argv[3],
    passwd=argv[4]
) as ftp:
  ftp.prot_p()
  chmod_recursive(ftp, argv[5])
