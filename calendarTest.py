import tkinter as tk
from tkinter import ttk, LEFT, BOTH, END, RIGHT, BOTTOM
import tkcalendar
from datetime import date
import os
import CSVparsing

class App:

   def __init__(self):
        self.path = 'csvSamples/Samples - Valid/'
        self.window = tk.Tk()
        self.window.title("Medical Data")
        self.window.geometry("600x700")
        self.init_ui()



   def init_ui(self):

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

       #  drop down box code below
       self.dropDown= tk.Listbox(self.window)
       self.dropDown.pack(fill=BOTH)
       self.scrollbar=tk.Scrollbar(self.window)
       self.scrollbar.pack(side=RIGHT, fill= BOTH)
       self.dropDown.config(yscrollcommand=self.scrollbar.set)

   #     Button UI generation
       self.buttonSelect=tk.Button(self.window,text="Output Selected File",command=self.selectedItemOutput)
       self.buttonSelect.pack(side=BOTTOM)

   def get_date(self):
    self.outListItems = []
    date_string = self.calendar.selection_get()
    date_string=str(date_string).replace("-","")
    itemList=os.listdir(self.path)
    for items in itemList:
        if str(date_string) in str(items):
            if CSVparsing.masterValidate(self.path,items):#Validates all files before adding them to Show List
                self.outListItems.append(items)
    self.putInDropDown(self.outListItems)

   def putInDropDown(self,validFilesList):
       self.dropDown.delete(0,tk.END)
       for val in validFilesList:
           self.dropDown.insert(END,val)

   def selectedItemOutput(self):
        for item in self.dropDown.curselection():
            CSVparsing.outputNiceCsv(self.dropDown.get(item),self.path)



if __name__ == "__main__":
    app = App()
    app.window.mainloop()