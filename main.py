import argparse
from launchGui import launch_gui
from launchCmdline import runCmdline

parser = argparse.ArgumentParser(description="A Medical Data Viewing Program")
parser.add_argument("--gui", help="Show the GUI", action="store_true")
parser.add_argument("--cli", help="Show the CMDLINE Version", action="store_true")
args = parser.parse_args()

if __name__=="__main__":
    if (args.gui):
        launch_gui()
    else:
        cmdObj=runCmdline()
        cmdObj.decisionTree()