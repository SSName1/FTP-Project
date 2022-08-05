import csv,re
from tabulate import tabulate
from datetime import datetime,timezone

def outputNiceCsv(filename):
    with open('output/csv/'+filename, newline='') as csvfile:
        dataReader = csv.reader(csvfile)
        print(tabulate(dataReader, headers='firstrow',tablefmt='pipe'))

def validateFilename(filename):
    '''Takes filename parameter, returns true|false for valid or invalid filename'''
    foundData=re.search("MED_DATA_[0-9]{14}.csv",filename)
    if foundData:
        return True
    else:
        return False

def validateDateTime(fileDate):
    '''Takes fileDate parameter as string in YYYYMMDDHHMMSS format'''
    '''output is True|False'''
    currentSystemDateTime="".join([datetime.now().strftime("%Y"),
datetime.now().strftime("%m"),datetime.now().strftime("%d"),datetime.now().strftime("%H"),
datetime.now().strftime("%M"),datetime.now().strftime("%S")])
    if fileDate<=currentSystemDateTime:
        return True
    else:
        return False


def validateFileData(filename):
    '''WIP'''
    with open('output/csv/'+filename, newline='') as csvfile:
        dataReader = csv.reader(csvfile)

def masterValidate(filename):
    '''here will run the master validation (composite of all other validaiton functions)'''

if __name__=='__main__':
    # print(validateFilename('MED_DATA_20220605142519.csv'))
    print(validateDateTime("20220605142519"))