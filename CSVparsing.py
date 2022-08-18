import csv,re
from tabulate import tabulate
from datetime import datetime

def outputNiceCsv(filename,path):
    with open(path+filename, newline='') as csvfile:
        dataReader = csv.reader(csvfile)
        print(tabulate(dataReader, headers='firstrow',tablefmt='pipe'))

def validateFilename(filename):
    '''Takes filename parameter, returns true|false for valid or invalid filename Returns: True|False'''
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
    if (fileDate<=currentSystemDateTime) and (len(fileDate)==len(currentSystemDateTime)):
        return True
    else:
        return False


def validateFileData(filename,path):
    '''Fully Validates the files data and determines if the file is valid Returns: True|False'''
    validFile=True
    checkListDataValues=[]
    with open(path+filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for index,row in enumerate(reader):
            if index==0:
                if row[0]!="batch_id": # check for invalid batch_id as batch
                    validFile=False
                if len(row)!=12: # check for correct amount of CSV headers
                    validFile=False
            if index>0:
                if row[0] in checkListDataValues: # check for duplicate batch_ids
                    validFile=False
                checkListDataValues.append(row[0])

                for dataPoint in row[2:]: # check for if the dataPoints are invalid e.g greater than 10
                    if float(dataPoint)>=10:
                        validFile=False
                    if dataPoint==None: # if dataPoint has no value assigned then file is invalid
                        validFile=False
    return validFile

def masterValidate(path,filename):
    '''here will run the master validation (composite of all other validaiton functions) returns true if completely valid otherwise false'''
    dateTimeOrder=filename.replace("MED_DATA_","")
    dateTimeOrder=dateTimeOrder.replace(".csv","")
    validationFuncs=[validateFilename(filename),validateDateTime(dateTimeOrder),validateFileData(filename,path)]
    if validationFuncs[0]==True and validationFuncs[1]==True and validationFuncs[2]==True:
        completeValid=True
    else:
        print(filename+" is invalid")
        completeValid=False
    return completeValid
