import tkinter as tk
from tkinter import END
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar
import CSVparsing
import ftp_connect
import displayCSV


class App:

    def __init__(self):
        """
        CONFIGURING WINDOW
        """

        # creates window
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

        self.window = tk.Tk()
        self.window.title("Medical Data")

        # configures grid layout
        self.window.rowconfigure(0, minsize=250, weight=1)
        self.window.rowconfigure(1, minsize=100, weight=1)
        self.window.columnconfigure(0, minsize=200, weight=1)
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
        self.calendar = Calendar(master=self.frm_filter,
                                 selectmode="day")
        self.btn_filter = tk.Button(
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
        self.frm_scroll_box.grid(row=0, column=0, padx=5, pady=5)
        self.frm_filter.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.btn_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.btn_choose_file.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.btn_upload.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # laying out filtering widgets within frm_filter
        self.lbl_filter.grid(row=0)
        self.calendar.grid(row=1, column=0)
        self.btn_filter.grid(row=1, column=1)

        # laying out scrollable list widgets within frm_scroll_box
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.dropDown.pack(side=tk.LEFT, fill="y")

    """Initializes the UI elements for positioning on the Tkinter UI"""

    # self.output_label = tk.Label(self.window, text="")
    # elf.output_label.pack(fill=tk.X, padx=10)

    def choose_file(self):
        filepath = askopenfilename(filetypes=(("csv files", "*.csv"),))
        if not filepath:
            return
        self.btn_choose_file["text"] = filepath
        return filepath

    def get_date(self):
        """Once the get_Date button is pressed the validated files are grabbed from the server and added to the dropdown list"""
        self.outListItems = []
        date_string = self.calendar.selection_get()
        date_string = str(date_string).replace("-", "")

        try:
            itemList = ftp_connect.ftp_fetch()  # validation to check if there is a connection to FTP
        except:
            print("Couldnt connect to FTP Server, is config up to date? or is server running?")
            exit(0)

        for items in itemList:
            if str(date_string) in str(items):
                ftp_connect.ftp_pull(items, "tempFTPDownload/" + str(items))
                if CSVparsing.masterValidate("tempFTPDownload/",
                                             items):  # Validates all files before adding them to Show List
                    self.outListItems.append(items)
        self.putInDropDown(self.outListItems)

    def putInDropDown(self, valid_files_list):
        """Adds all the valid files to the drop-down list in the UI"""
        self.dropDown.delete(0, tk.END)
        for val in valid_files_list:
            self.dropDown.insert(END, val)

    def selectedItemOutput(self):
        """Method outputs the given selected file into a Tkinter GUI for easy user reading"""

        self.fileToOutput = ""
        for item in self.dropDown.curselection():
            self.fileToOutput = self.dropDown.get(item)
        ftp_connect.ftp_pull(self.fileToOutput,
                             "tempFTPDownload/tempL.csv")  # Creates a temp file to store Pulled FTP CSV data
        outputObj = displayCSV.DisplayCSV("tempFTPDownload/tempL.csv")


def launch_gui():
    app = App()  # Launches the Tkinter UI
    app.window.mainloop()


if __name__ == "__main__":
    launch_gui()
