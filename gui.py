import tkinter as tk
from tkinter.filedialog import askopenfilename


def choose_file():
    filepath = askopenfilename(filetypes=(("csv files", "*.csv"),))
    if not filepath:
        return
    btn_choose_file["text"] = filepath
    return filepath


# creates window
window = tk.Tk()
window.title("Medical Data")

# configures grid layout
window.rowconfigure(0, minsize=250, weight=1)
window.rowconfigure(1, minsize=100, weight=1)
window.columnconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=100, weight=1)
window.columnconfigure(2, minsize=100, weight=1)


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

# frm_upload_file = tk.Frame(master=window)
# lbl_upload = tk.Label(master=frm_upload_file,  text="Upload and validate a new csv file")
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


frm_scroll_box.grid(row=0, column=0, padx=5, pady=5)
frm_filter.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
# frm_upload_file.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
btn_view.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

lbl_filter.grid(row=0)
ent_filter.grid(row=1, column=0)
btn_filter.grid(row=1, column=1)
btn_today.grid(row=2)

# lbl_upload.grid(row=0)
btn_choose_file.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
btn_upload.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

scrollbar.pack(side=tk.RIGHT, fill="y")
data_entries.pack(side=tk.LEFT, fill="y")

window.mainloop()
