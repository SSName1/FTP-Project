# importing all required modules
import tkinter as tk
from tkinter import END
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar
import CSVparsing
import ftp_connect
import displayCSV
import os
import shutil


class App:
    """
    CREATING UI, largely created by Adam D
    """
    def __init__(self):
        """
        CONFIGURING WINDOW
        """

        # defining widgets
        self.calendar = None
        self.btn_upload = None
        self.btn_choose_file = None
        self.scrollbar = None
        self.dropDown = None
        self.entries_to_use = None
        self.frm_scroll_box = None
        self.btn_view = None
        self.btn_today = None
        self.btn_filter = None
        self.ent_filter = None
        self.lbl_filter = None
        self.frm_filter = None

        # creates window
        self.window = tk.Tk()
        self.window.title("Medical Data")

        # configures grid layout
        self.window.rowconfigure(0, minsize=250, weight=1)
        self.window.rowconfigure(1, minsize=100, weight=1)
        self.window.columnconfigure(0, minsize=230, weight=1)
        self.window.columnconfigure(1, minsize=100, weight=1)
        self.window.columnconfigure(2, minsize=100, weight=1)
        self.init_ui()

    def init_ui(self):
        """
        CREATING WIDGETS
        """
        # configuring filter widgets
        self.frm_filter = tk.Frame(master=self.window)

        self.lbl_filter = tk.Label(master=self.frm_filter,
                                   text="Filter by Date")
        # creating calendar widget
        self.calendar = Calendar(master=self.frm_filter,
                                 selectmode="day")
        self.btn_filter = \
            tk.Button(
                master=self.frm_filter,
                text="Get Date",
                command=self.get_date
            )

        # other button widgets
        self.btn_view = tk.Button(
            master=self.window,
            text="View Selected File",
            command=self.selectedItemOutput
        )

        # configuring scrollable list
        self.frm_scroll_box = tk.Frame(master=self.window)
        self.dropDown = tk.Listbox(self.frm_scroll_box)
        self.scrollbar = tk.Scrollbar(self.frm_scroll_box)
        self.dropDown.config(yscrollcommand=self.scrollbar.set)

        # configuring file upload widgets
        self.btn_choose_file = tk.Button(
            master=self.window,
            text="Choose File",
            command=self.choose_file
        )
        self.btn_upload = tk.Button(
            master=self.window,
            text="Upload"
            # command=
        )

        """
        CREATING WIDGET LAYOUT
        """
        # laying out widgets on the main window
        self.frm_scroll_box.grid(row=0, column=0)
        self.frm_filter.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.btn_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.btn_choose_file.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        self.btn_upload.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # laying out filtering widgets within frm_filter
        self.lbl_filter.grid(row=0)
        self.calendar.grid(row=1)
        self.btn_filter.grid(row=2, padx=5, pady=5, sticky="nsew")

        # laying out scrollable list widgets within frm_scroll_box
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.dropDown.pack(side=tk.LEFT, fill="y")

    """
    FUNCTIONS, largely created by Harry A and Sunil S
    """

    """
    when choose file button is clicked, a dialogue box opens 
    which allows the user to select a file, the filepath is returned
    """
    def choose_file(self):
        filepath = askopenfilename(filetypes=(("csv files", "*.csv"),))
        if not filepath:
            return
        self.btn_choose_file["text"] = filepath
        return filepath

    """
    Once the get_Date button is pressed the validated files
    are grabbed from the server and added to the dropdown list
    """
    def get_date(self):

        self.outListItems = []
        date_string = self.calendar.selection_get()
        date_string = str(date_string).replace("-", "")
        try:
            itemList = ftp_connect.ftp_fetch()  # validation to check if there is a connection to FTP
        except:
            print("Couldnt connect to FTP Server, is config up to date? or is server running?")
            exit(0)

        for items in itemList:
            if CSVparsing.validateFilename(items):
                if str(date_string) in str(items):
                    os.makedirs("tempFTPDownload/", exist_ok=True)
                    ftp_connect.ftp_pull(items, "tempFTPDownload/" + str(items))
                    if CSVparsing.masterValidate("tempFTPDownload/",
                                                 items):  # Validates all files before adding them to Show List
                        os.makedirs("FTPDownload/" + str(date_string[:4]) + "/" + str(date_string[4:6]) + "/" + str(date_string[6:8]), exist_ok=True)
                        self.outListItems.append(items)

        if len(self.outListItems) != 0:
            for files in self.outListItems:
                os.rename("tempFTPDownload/" + files,
                          "FTPDownload/" + files[9:13] + "/" + files[13:15] + "/" + files[15:17] + "/" + files)
            shutil.rmtree("tempFTPDownload")
        self.putInDropDown(self.outListItems)

    """Adds all the valid files to the drop down list in the UI"""
    def putInDropDown(self, validFilesList):
        self.dropDown.delete(0, tk.END)
        for val in validFilesList:
            self.dropDown.insert(END, val)

    """
    Method outputs the given selected file into a Tkinter GUI for easy user reading
    """
    def selectedItemOutput(self):
        self.fileToOutput = ""
        for item in self.dropDown.curselection():
            self.fileToOutput = self.dropDown.get(item)
        ftp_connect.ftp_pull(self.fileToOutput, "FTPDownload/" + self.fileToOutput[9:13] + "/"
                             + self.fileToOutput[13:15] + "/" + self.fileToOutput[15:17] + "/" + self.fileToOutput)  # Creates a temp file to store Pulled FTP CSV data
        outputObj = displayCSV.DisplayCSV("FTPDownload/" + self.fileToOutput[9:13] + "/" +
                                          self.fileToOutput[13:15] + "/" + self.fileToOutput[15:17] + "/" + self.fileToOutput)


"""
LAUNCHING UI
"""
def launch_gui():
    app = App()  # Launches the Tkinter UI
    app.window.mainloop()


if __name__ == "__main__":
    launch_gui()
