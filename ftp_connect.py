# todo: handle refusal

def ftp_connect():
    # import modules
    from ftplib import FTP
    import json

    # open and parse the config file
    c = open("config.json")
    config = json.load(c)

    # make the FTP connection and log in
    ftp = FTP(config['FTP_HOST'])  # connect to host, default port
    ftp.login(config['FTP_USER'], config['FTP_PASS'])

    return ftp


def ftp_fetch():
    # set the ftp variable to the return of the connect function, to restore capability to the ftp commands
    ftp = ftp_connect()

    # fetch the data and append it to a variable
    data = ftp.nlst()

    # ftp.quit()

    # the return data is an array, python seems to handle it seamlessly
    return data


def ftp_pull(remoteFile, localFolder, return_bool = False):
    # set the ftp variable to the return of the connect function, to restore capability to the ftp commands
    ftp = ftp_connect()

    # open the local file for writing in binary mode
    lf = open(localFolder, 'wb')
    
    # fetch the data from the ftp server and write it to the local file
    ftp.retrbinary('RETR ' + remoteFile, lf.write)

    # close the connection to the FTP server and the local file
    ftp.quit()
    lf.close()

    # optional return if successful
    if return_bool:
        return True

def ftp_push(*args):
    ftp = ftp_connect()

    # somehow upload files from the argument here

    # close the ftp connection
    ftp.quit()

