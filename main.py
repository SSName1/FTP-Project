from ftp_connect import ftp_fetch, ftp_push

if __name__ == '__main__':
    # fetch and print files from the FTP server
    print(ftp_fetch())

    # send files to the server
    ftp_push()  # will take file paths as arguments
