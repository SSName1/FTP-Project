import tkinter as tk
from tkinter import ttk, LEFT, BOTH, END, RIGHT
import tkcalendar
from datetime import date
import os

class App:

   def __init__(self):
        self.window = tk.Tk()
        self.window.title("Medical Data")
        self.window.geometry("600x600")
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
       self.dropDown.pack(side=LEFT,fill=BOTH)
       self.scrollbar=tk.Scrollbar(self.window)
       self.scrollbar.pack(side=RIGHT, fill= BOTH)



   def get_date(self):
    outListItems = []
    date_string = self.calendar.selection_get()
    date_string=str(date_string).replace("-","")
    print(date_string)
    itemList=os.listdir('csvSamples/Samples - Valid')
    for items in itemList:
        if str(date_string) in str(items):
            outListItems.append(items)
    self.putInDropDown(outListItems)

   def putInDropDown(self,validFilesList):
       for val in validFilesList:
           self.dropDown.insert(END,val)
       self.dropDown.config(yscrollcommand=self.scrollbar.set)


if __name__ == "__main__":
    app = App()
    app.window.mainloop()