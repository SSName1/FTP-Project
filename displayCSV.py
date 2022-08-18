import tkinter as tk, csv
import tkinter.ttk as ttk
from tkinter import TOP, HORIZONTAL, VERTICAL, NO, W, BOTTOM, RIGHT


class DisplayCSV:

    def __init__(self, path): #building blocks for tkinter window
        self.path = path
        self.window = tk.Tk()
        self.window.title(path)
        self.window.geometry('600x700')
        self.width = 500
        self.height = 400
        self.newinit_ui() #method to make window to open csvfile


    def newinit_ui(self):
        window_frame = tk.Frame(self.window, width=500) #frame
        window_frame.pack(side=TOP)

        scrollbary = tk.Scrollbar(window_frame, orient=HORIZONTAL) #scrollbars to navigate page
        scrollbarx = tk.Scrollbar(window_frame, orient=VERTICAL)

        data = ttk.Treeview(window_frame,
                            columns=("batch_id", "timestamp", "reading1", "reading2", "reading3", "reading4",
                                     "reading5", "reading6", "reading7", "reading8", "reading9", "reading10"),
                            yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set, height=400, selectmode="extended") #table style tkk widget
        #set each column name, scrollbars to navigate table

        scrollbary.config(command=data.xview)
        scrollbarx.config(command=data.yview)


        scrollbary.pack(side=BOTTOM, fill="x")
        scrollbarx.pack(side=RIGHT, fill="y")

        #table headings to write data in the columns
        data.heading('batch_id', text="batch_id", anchor=W)
        data.heading('timestamp', text="timestamp", anchor=W)
        data.heading('reading1', text="reading1", anchor=W)
        data.heading('reading2', text="reading2", anchor=W)
        data.heading('reading3', text="reading3", anchor=W)
        data.heading('reading4', text="reading4", anchor=W)
        data.heading('reading5', text="reading5", anchor=W)
        data.heading('reading6', text="reading6", anchor=W)
        data.heading('reading7', text="reading7", anchor=W)
        data.heading('reading8', text="reading8", anchor=W)
        data.heading('reading9', text="reading9", anchor=W)
        data.heading('reading10', text="reading10", anchor=W)
        data.column('#0', stretch=NO, minwidth=0, width=0)
        data.column('#1', stretch=NO, minwidth=0, width=200)
        data.column('#2', stretch=NO, minwidth=0, width=200)
        data.column('#3', stretch=NO, minwidth=0, width=300)
        data.pack()

        #assigned each row with type of data being stored
        with open(self.path, newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                batch_id = row['batch_id']
                timestamp = row['timestamp']
                reading1 = row['reading1']
                reading2 = row['reading2']
                reading3 = row['reading3']
                reading4 = row['reading4']
                reading5 = row['reading5']
                reading6 = row['reading6']
                reading7 = row['reading7']
                reading8 = row['reading8']
                reading9 = row['reading9']
                reading10 = row['reading10']

                #inserted corresponding value from CSV file into Tree tkinter object for each row from 0
                data.insert("", 0, values=(batch_id, timestamp, reading1, reading2, reading3, reading4, reading5,
                                           reading6, reading7, reading8, reading9, reading10))



