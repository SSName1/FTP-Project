#!/usr/bin/env python
# ftpserver-cli.py
import sys
sys.path.append("/path/to/pyftpdlib-svn") # enter your proper path here
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def processCmdLineOptions():
  global optparser
  optparser = argparse.ArgumentParser(description="ftpserver-cli",
              formatter_class=argparse.RawDescriptionHelpFormatter)
  optparser.add_argument('-u', '--username', action='store', type=str,
      default="user", help="username")
  optparser.add_argument('-p', '--password', action='store', type=str,
      default="12345", help="password")
  optparser.add_argument('-t', '--port', action='store', type=int,
      default="21", help="port")

  # PATH IS HARDCODED HERE, IF RUNNING LOCAL FTP SERVER CHANGE PATH BELOW IN CMDPARSER
  optparser.add_argument('-d', '--directory', action='store', type=str,
      default="/home/parallels/PycharmProjects/FTP-Project/csvSamples/Samples - Valid/", help="port")
  optargs = optparser.parse_args(sys.argv[1:]) #(sys.argv)
  return optargs


if __name__=="__main__":
    optargs = processCmdLineOptions()

    print("Using: user: %s pass: %s port: %d dir: %s" % (optargs.username, optargs.password, optargs.port, optargs.directory))

    authorizer = DummyAuthorizer()
    authorizer.add_user(optargs.username, optargs.password, optargs.directory, perm="elradfmw")
    #authorizer.add_anonymous("/home/nobody")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", optargs.port), handler)
    server.serve_forever()
