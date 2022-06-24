from ftplib import FTP_TLS
from sys import argv

def chmod_recursive(ftp: FTP_TLS, path: str):
  items = ftp.mlsd(path)
  for fname,opt in items:
    path_to_file = path + '/' + fname
    print(path_to_file)

    if opt['type'] == 'dir':
      chmod_recursive(ftp, path_to_file)
    elif opt['type'] == 'file':
      if fname.endswith('.sh'):
        if opt['unix.mode'] != '0700':
          ftp.sendcmd('SITE CHMOD 700 ' + path_to_file)
          print('==> Permission has changed to 700')
      elif opt['unix.mode'] != '0604':
        ftp.sendcmd('SITE CHMOD 604 ' + path_to_file)
        print('==> Permission has changed to 604')

with FTP_TLS(
    host=argv[1],
    user=argv[2],
    passwd=argv[3]
) as ftp:
  ftp.prot_p()
  chmod_recursive(ftp, argv[4])
