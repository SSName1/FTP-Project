# importing tkinter libraries
import tkinter as tk
from tkinter.filedialog import askopenfilename

"""
function which allows user to select file and changes the text of the
choose file button to the filepath of the selected file. 
returns the filepath.
"""


def choose_file():
    filepath = askopenfilename(filetypes=(("csv files", "*.csv"),))
    if not filepath:
        return
    btn_choose_file["text"] = filepath
    return filepath


"""
CONFIGURING WINDOW
"""
# creates window
window = tk.Tk()
window.title("Medical Data")

# configures grid layout
window.rowconfigure(0, minsize=250, weight=1)
window.rowconfigure(1, minsize=100, weight=1)
window.columnconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=100, weight=1)
window.columnconfigure(2, minsize=100, weight=1)

"""
CREATING WIDGETS
"""
# configuring filter widgets
frm_filter = tk.Frame(master=window)
lbl_filter = tk.Label(master=frm_filter, text="Filter by Date")
ent_filter = tk.Entry(master=frm_filter)
btn_filter = tk.Button(
    master=frm_filter,
    text="Go",
    # command=
)
btn_today = tk.Button(
    master=frm_filter,
    text="Today",
    # command=
)
# other button widgets
btn_view = tk.Button(
    master=window,
    text="View",
    # command=
)

# configuring scrollable list
frm_scroll_box = tk.Frame(master=window)
# placeholder data
entries = ["a", "b", "c", "d", "e", "a", "b", "c", "d", "e", "a", "b", "c", "d",
           "e", "a", "b", "c", "d", "e", "a", "b",
           "c", "d", "e", "a", "b", "c", "d", "e"]
entries_to_use = tk.StringVar(value=entries)
data_entries = tk.Listbox(
    master=frm_scroll_box,
    listvariable=entries_to_use,
    selectmode="browse"
)
scrollbar = tk.Scrollbar(
    master=frm_scroll_box,
    orient="vertical",
    command=data_entries.yview
)
data_entries["yscrollcommand"] = scrollbar.set

# configuring file upload widgets
btn_choose_file = tk.Button(
    master=window,
    text="Choose File",
    command=choose_file
)
btn_upload = tk.Button(
    master=window,
    text="Upload"
    # command=
)

"""
CREATING WIDGET LAYOUT
"""
# laying out widgets on the main window
frm_scroll_box.grid(row=0, column=0, padx=5, pady=5)
frm_filter.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
btn_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
btn_choose_file.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
btn_upload.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

# laying out filtering widgets within frm_filter
lbl_filter.grid(row=0)
ent_filter.grid(row=1, column=0)
btn_filter.grid(row=1, column=1)
btn_today.grid(row=2)

# laying out scrollable list widgets within frm_scroll_box
scrollbar.pack(side=tk.RIGHT, fill="y")
data_entries.pack(side=tk.LEFT, fill="y")

"""
LAUNCHING GUI
"""
window.mainloop()
