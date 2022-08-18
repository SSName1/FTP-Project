import tkinter as tk
from tkinter import BOTH, END, RIGHT, BOTTOM
import tkcalendar
import CSVparsing
import ftp_connect
import displayCSV
from pathlib import Path
import os
import shutil

class App:
   def __init__(self):
        '''Initalizes the important variables for the Tkinter Calendar GUI'''
        self.window = tk.Tk()
        self.window.title("Medical Data")
        self.window.geometry("600x700")
        self.init_ui()

   def init_ui(self):
       '''Initalizes the UI elements for positioning on the Tkinter UI'''
       self.output_label = tk.Label(self.window, text="")
       self.output_label.pack(fill=tk.X, padx=10)
       self.date_label = tk.Label(self.window,
                                   text="Please enter a date.")
       self.date_label.pack(pady=10)
       self.calendar = tkcalendar.Calendar(self.window,
                                  selectmode="day")
       self.calendar.pack(fill=tk.X, padx=10, pady=10)

       self.date_button = tk.Button(self.window, text="Get Date",
                                     command=self.get_date)
       self.date_button.pack()

       #  drop down box packing and positioning
       self.dropDown= tk.Listbox(self.window)
       self.dropDown.pack(fill=BOTH)
       self.scrollbar=tk.Scrollbar(self.window)
       self.scrollbar.pack(side=RIGHT, fill= BOTH)
       self.dropDown.config(yscrollcommand=self.scrollbar.set)

       #  Button UI generation
       self.buttonSelect=tk.Button(self.window,text="Output Selected File",command=self.selectedItemOutput)
       self.buttonSelect.pack(side=BOTTOM)

   def get_date(self):
    '''Once the get_Date button is pressed the validated files are grabbed from the server and added to the dropdown list'''
    self.outListItems = []
    date_string = self.calendar.selection_get()
    date_string=str(date_string).replace("-","")
    try:
        itemList=ftp_connect.ftp_fetch() # validation to check if there is a connection to FTP
    except:
        print("Couldnt connect to FTP Server, is config up to date? or is server running?")
        exit(0)

    for items in itemList:
        if CSVparsing.validateFilename(items):
            if str(date_string) in str(items):
                os.makedirs("tempFTPDownload/",exist_ok=True)
                ftp_connect.ftp_pull(items,"tempFTPDownload/"+str(items))
                if CSVparsing.masterValidate("tempFTPDownload/",items):#Validates all files before adding them to Show List
                    os.makedirs("FTPDownload/" + str(date_string[:4]) +"/"+ str(date_string[4:6]) +"/"+ str(date_string[6:8]),exist_ok=True)
                    self.outListItems.append(items)

    if len(self.outListItems)!=0:
        for files in self.outListItems:
            os.rename("tempFTPDownload/"+files,"FTPDownload/"+files[9:13]+"/"+files[13:15]+"/"+files[15:17]+"/"+files)
        shutil.rmtree("tempFTPDownload")
    self.putInDropDown(self.outListItems)

   def putInDropDown(self,validFilesList):
       '''Adds all the valid files to the drop down list in the UI'''
       self.dropDown.delete(0,tk.END)
       for val in validFilesList:
           self.dropDown.insert(END,val)

   def selectedItemOutput(self):
        '''Method outputs the given selected file into a Tkinter GUI for easy user reading'''
        self.fileToOutput=""
        for item in self.dropDown.curselection():
            self.fileToOutput=self.dropDown.get(item)
        ftp_connect.ftp_pull(self.fileToOutput, "FTPDownload/"+self.fileToOutput[9:13]+"/"+self.fileToOutput[13:15]+"/"+self.fileToOutput[15:17]+"/"+self.fileToOutput) #Creates a temp file to store Pulled FTP CSV data
        outputObj=displayCSV.DisplayCSV("FTPDownload/"+self.fileToOutput[9:13]+"/"+self.fileToOutput[13:15]+"/"+self.fileToOutput[15:17]+"/"+self.fileToOutput)

def launch_gui():
    app = App() # Launches the Tkinter UI
    app.window.mainloop()