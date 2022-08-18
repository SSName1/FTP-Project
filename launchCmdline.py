import CSVparsing as parser
import ftp_connect as FTP
from pathlib import Path
import os
import shutil

#Code was collaborated and written together by Harry S, Sunil S
class runCmdline():

    def __init__(self):
        self.outputList=[] #show list for possible files for a specific date
        self.choiceCond=True

    def decisionTree(self):
        #main menu for command line application
        while self.choiceCond:
            print("---------\nMain Menu\n---------\n")
            print("Option 1: Select Date to view files (1)")
            print("Option 2: Open Specific File (2)")
            print("Option 3: Quit (3)\n")
            self.uChoice=str(input(">: "))
            #keeps tracks of user input and provides service based on input
            if self.uChoice=="1":
                self.dateChoice=str(input("Enter Date to view files in (YYYYMMDD) Format\n>: "))
                self.dateFileView(self.dateChoice) #function call
                self.uChoice=False #to exit the WHILE loop
                exit(0) #end program execution
            elif self.uChoice=="2":
                self.uChoice=str(input("Please Enter Specific Filename to View (MED_DATA_YYYYMMDDHHMMSS.csv) >: "))
                self.specificFile(self.uChoice) #function call
                self.uChoice = False
                exit(0)
            elif self.uChoice=="3":
                exit(0)
            else:
                print("Enter Valid Data\n") #erroneous input


    def dateFileView(self,date):
        try:
            testCast=int(date) #tests if input is a date
        except:
            print("Wrong Data Format") #otherwise it is rejected
            exit(0)
        try:
            self.itemList = FTP.ftp_fetch()  # validation to check if there is a connection to FTP
        except:
            print("Couldn't connect to FTP Server, is config up to date? or is server running?")
            exit(0)
        for items in self.itemList:
            if parser.validateFilename(items):
                if date in str(items):
                    os.makedirs("tempFTPDownload/", exist_ok=True)
                    FTP.ftp_pull(items, "tempFTPDownload/" + str(items))
                    if parser.masterValidate("tempFTPDownload/",items):  # Validates all files before adding them to Show List
                        os.makedirs("FTPDownload/" + str(date[:4]) + "/" + str(date[4:6]) + "/" + str(date[6:8]), exist_ok=True)
                        self.outputList.append(items)

        if len(self.outputList) != 0:
            for files in self.outputList:
                os.rename("tempFTPDownload/" + files,"FTPDownload/"+files[9:13]+"/"+files[13:15]+"/"+files[15:17]+"/"+files)
            shutil.rmtree("tempFTPDownload")

        print("The Files for that current day are:")
        for file in self.outputList:
            print(file)

        self.uChoice=str(input("Enter File to View >: "))
        if self.uChoice not in self.itemList: #if filename not found in displayed list
            print("Wrong Filename")
            exit(0)
        else:
            parser.outputNiceCsv(self.uChoice,"FTPDownload/"+self.uChoice[9:13]+"/"+self.uChoice[13:15]+"/"+self.uChoice[15:17]+"/") #object method call to print csv in console

    def specificFile(self,filename):
        try:
            self.itemList = FTP.ftp_fetch()  # validation to check if there is a connection to FTP
        except:
            print("Couldn't connect to FTP Server, is config up to date? or is server running?")
            exit(0)
        if filename in self.itemList:
            FTP.ftp_pull(filename, "tempFTPDownload/" + str(filename))
            if parser.masterValidate("tempFTPDownload/", filename):  # Validates all files before adding them to Show List
                parser.outputNiceCsv(self.uChoice, "tempFTPDownload/")
            else:
                print("Invalid Datafile on FTP Server") #if file cannot be found in file downloaded from FTP server
                exit(0)
        else:
            print("Wrong Filename")
            exit(0)

if __name__=="__main__":
    cmdRunObj=runCmdline()
    cmdRunObj.decisionTree()
