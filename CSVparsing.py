import csv,re
from tabulate import tabulate

def outputNiceCsv(filename):
    with open('output/csv/'+filename, newline='') as csvfile:
        dataReader = csv.reader(csvfile)
        print(tabulate(dataReader, headers='firstrow',tablefmt='pipe'))

def validateFilename(filename):
    foundData=re.search("MED_DATA_[0-9]{14}.csv",filename)
    if foundData:
        return True
    else:
        return False

def validateFileData(filename):
    with open('output/csv/'+filename, newline='') as csvfile:
        dataReader = csv.reader(csvfile)

if __name__=='__main__':
    # outputNiceCsv('MED_DATA_20220606141559.csv')
    # x=validateFilename('MED_DATA_20220606141559.csv')
    validateFileData('MED_DATA_20220606141559.csv')