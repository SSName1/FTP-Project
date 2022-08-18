import CSVparsing as parser
import ftp_connect as FTP

class runCmdline():

    def __init__(self):
        self.outputList=[]
        self.choiceCond=True

    def decisionTree(self):
        while self.choiceCond:
            print("---------\nMain Menu\n---------\n")
            print("Option 1: Select Date to view files (1)")
            print("Option 2: Open Specific File (2)")
            print("Option 3: Quit (3)\n")
            self.uChoice=str(input(">: "))
            if self.uChoice=="1":
                self.dateChoice=str(input("Enter Date to view files in (YYYYMMDD) Format\n>: "))
                self.dateFileView(self.dateChoice)
                self.uChoice=False
                exit(0)
            elif self.uChoice=="2":
                self.uChoice=str(input("Please Enter Specific Filename to View (MED_DATA_YYYYMMDDHHMMSS.csv) >: "))
                self.specificFile(self.uChoice)
                self.uChoice = False
                exit(0)
            elif self.uChoice=="3":
                exit(0)
            else:
                print("Enter Valid Data\n")


    def dateFileView(self,date):
        try:
            testCast=int(date)
        except:
            print("Wrong Data Format")
            exit(0)
        try:
            self.itemList = FTP.ftp_fetch()  # validation to check if there is a connection to FTP
        except:
            print("Couldn't connect to FTP Server, is config up to date? or is server running?")
            exit(0)
        for items in self.itemList:
            if date in str(items):
                FTP.ftp_pull(items, "tempFTPDownload/" + str(items))
                if parser.masterValidate("tempFTPDownload/",items):  # Validates all files before adding them to Show List
                    self.outputList.append(items)
        print("The Files for that current day are:")
        self.outputList=[print(file) for file in self.outputList]
        self.uChoice=str(input("Enter File to View >: "))
        if self.uChoice not in self.itemList:
            print("Wrong Filename")
            exit(0)
        else:
            parser.outputNiceCsv(self.uChoice,"tempFTPDownload/")

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
                print("Invalid Datafile on FTP Server")
                exit(0)
        else:
            print("Wrong Filename")
            exit(0)

if __name__=="__main__":
    cmdRunObj=runCmdline()
    cmdRunObj.decisionTree()
