from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
import sort

SORT_OPTIONS = ["DATE", "TYPE", "NAME"]
CURRENT_DIR = None
SUGGESTED_FOLDER = None
UNSORTED_DIR = None

class dir_frame(tk.LabelFrame):
    '''A Frame that displays directories'''
    def __init__(self, master: tk.Tk, name: str, button_name: str, callback: callable):
        tk.LabelFrame.__init__(self, master=master, text=name)
        self.directory_view = tk.Listbox(self)
        self.askdir_button = tk.Button(self, text=button_name, command=lambda: callback(self))
        self.askdir_button.pack(fill="both", expand=True)
        self.directory_view.pack(fill="both", expand=True)
        self.dir = None


def show_directory(folder: dir_frame):
    '''Updates the view of the directory'''
    global CURRENT_DIR
    global UNSORTED_DIR
    directory_view = folder.directory_view
    # Ask user dor what directory they want to display
    file_path = Path(filedialog.askdirectory())
    folder.dir = file_path
    CURRENT_DIR = file_path
    content = list(file_path.iterdir())
    # SOrt the folders seperately
    folders = [x.name for x in content if x.is_dir()]
    folders.sort()
    # Sort the files seperately
    content = [x.name for x in content]
    files = list(set(content) - set(folders))
    files.sort()
    # Erase the existing display
    end = directory_view.size()
    directory_view.delete(0, end)
    counter = 0
    # DIsplay folders and files
    for dir_file in folders:
        directory_view.insert(counter, f"+{dir_file}")
        counter += 1
    for dir_file in files:
        directory_view.insert(counter, dir_file)
        counter += 1


def show_suggested(folder: dir_frame, results: dict):
    '''Displays the sorted folders and files before applying it'''
    directory_view = folder.directory_view
    folder.dir = results
    # Clears display
    end = directory_view.size()
    directory_view.delete(0, end)
    counter = 0
    # Displays folders and files
    for folder, contents in results.items():
        directory_view.insert(counter, f"+{folder}")
        counter += 1
        for file in contents:
            directory_view.insert(counter, f"  -{file.name}")
            counter += 1


class option_menu(tk.LabelFrame):
    '''
    Contain option menu
    '''
    def __init__(self, root):
        tk.LabelFrame.__init__(self, master=root, text="Sort Menu")
        self.sort_type = tk.StringVar()
        self.additional = tk.IntVar()
        self._DATE_frame = None
        self._TYPE_frame = None
        self._NAME_frame = None
        self.draw()
    

    def add_output(self, display: tk.Frame):
        '''Adds a output display to the option menu and sort function'''
        self.output = display


    def draw(self):
        '''Creates default sort option menu contain 
        the three options, submit button, and option to expand'''
        self.details_frame = tk.Frame(master=self)
        # Advanced Detail Button creation
        self.details = tk.Checkbutton(master=self.details_frame, text="Advanced Details", variable=self.additional, command=lambda: self.toggle_details(), height=1, pady=0)
        self.details.pack(side=tk.RIGHT, pady=0)
        self.details_frame.pack(fill="x", side=tk.TOP)
        
        # 3 options to sort: date, type, name
        for count in range(len(SORT_OPTIONS)):
            temp_frame = tk.Frame(master=self, height=3, width=10)
            temp_frame.pack(pady=0, ipadx=0, ipady=0)
            if SORT_OPTIONS[count] == "NAME":
                temp_frame.pack_forget()
            setattr(self, f"_{SORT_OPTIONS[count]}_frame", temp_frame)
            radiobutton = tk.Radiobutton(master=temp_frame, text=SORT_OPTIONS[count], \
                                        value=SORT_OPTIONS[count], \
                                        variable=self.sort_type, \
                                        width=50, \
                                        height=1, \
                                        anchor="w", pady=0)
            radiobutton.pack(expand=True, pady=0, ipadx=0, ipady=0)
        
                
        # Sort Button
        self.submit_button = tk.Button(master=self, text="Sort", command=lambda: self.auto_sort(self.sort_type.get()), height=1)
        self.submit_button.pack(side=tk.BOTTOM)


    def create_date_range(self):
        '''Creates an option to select 2 dates and sort through the range'''
        self.date_details = tk.Frame(self._DATE_frame)
        self.date_details.pack(side=tk.LEFT)
        x = tk.Label(self.date_details, text="From")
        x.grid(row=0, column=0)
        self.date_start = DateEntry(self.date_details)
        self.date_start.grid(row=0, column=1)
        y = tk.Label(self.date_details, text="To")
        y.grid(row=0, column=2)
        self.date_end = DateEntry(self.date_details)
        self.date_end.grid(row=0, column=3)
    

    def create_field(self, detail: str, label: str):
        '''Creates a label and text field'''
        detail_frame = f"self.{detail.lower()}_details"
        exec(f"self.{detail.lower()}_details = tk.Frame(self._{detail.upper()}_frame)")
        exec(f"{detail_frame}.pack(side=tk.LEFT)")
        exec(f"x = tk.Label({detail_frame}, text=\"{label}: \")")
        exec("x.grid(row=0, column=0, sticky=\"NEWS\")")
        exec(f"self.{detail.lower()}_field = tk.Text({detail_frame}, height=1, width=10)")
        exec(f"self.{detail.lower()}_field.grid(row=0, column=1)")


    def toggle_details(self):
        '''Toggles additional detail for each option'''
        if self.additional.get():
            self.create_date_range()
            self.create_field("type", "Extension")
            self._NAME_frame.pack()
            self.create_field("name", "Name")
        else:
            self.date_details.destroy()
            self.type_details.destroy()
            self.name_details.destroy()
            self._NAME_frame.pack_forget()
    
    def auto_sort(self, sort_type):
        '''Sorts the files depending on button choices and additional details fiels'''
        if self.additional.get():
            match sort_type:
                case "DATE":
                    start_date = self.date_start.get_date()
                    end_date = self.date_end.get_date()
                    results = sort.sort_all_date(CURRENT_DIR)
                    results = {date: contents for date, contents in results.items() if start_date <= datetime.strptime(date, '%m/%d/%Y').date() <= end_date}
                    show_suggested(self.output, results)
                case "TYPE":
                    show_suggested(self.output, {self.type_field.get("1.0", tk.END).strip(): sort.sort_type(CURRENT_DIR, self.type_field.get("1.0", tk.END).strip())})
                case "NAME":
                    show_suggested(self.output, {self.name_field.get("1.0", tk.END).strip(): sort.sort_name(CURRENT_DIR, self.name_field.get("1.0", tk.END).strip())})
        else:
            match sort_type:
                case "DATE":
                    show_suggested(self.output, sort.sort_all_date(CURRENT_DIR))
                case "TYPE":
                    show_suggested(self.output, sort.sort_all_type(CURRENT_DIR))
        

def apply(display: dir_frame):
    '''Applies the sorted folder and files'''
    global UNSORTED_DIR
    UNSORTED_DIR = sort.organize(display.dir)


def run():
    # Create program
    global UNSORTED_DIR
    window = tk.Tk()
    window.resizable(width=False, height=False)
    window.title("File Organizer")
    window.geometry("510x450")

    # Create Sort Menu
    sort_frame = option_menu(window)
    sort_frame.grid(sticky="NEWS", row=0, column=0, rowspan=1)

    # Create Directory View
    current_folder = dir_frame(window, "Directory", "Select Folder", show_directory)
    current_folder.grid(row=0, column=1, sticky="NWES")

    # Create Projected View
    new_folder = dir_frame(window, "New Folders", "Apply", apply)
    new_folder.grid(row=1, column=0, columnspan=2, sticky="NEWS")

    # Create Undo Button
    undo_button = tk.Button(window, text="Undo", command=lambda: sort.undo(UNSORTED_DIR))
    undo_button.grid(row=2, column=0, columnspan=2, sticky="NEWS")

    sort_frame.add_output(new_folder)

    tk.mainloop()

if __name__ == "__main__":
    run()