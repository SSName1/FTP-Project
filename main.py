from ftp_connect import ftp_fetch, ftp_push
from tkinter import *
import argparse
from calendarTest import launch_gui

parser = argparse.ArgumentParser(description="A simple hello world program")
parser.add_argument("--gui", help="Show the GUI", action="store_true")
args = parser.parse_args()

if (args.gui):
    launch_gui()
else:
    print("Hello, world!")