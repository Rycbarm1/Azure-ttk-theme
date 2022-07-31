import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, ttk


class Switch(ttk.Frame):
    def __init__(self, parent, screenwidth, screenheight):
        ttk.Frame.__init__(self)

        self.winfo_screenwidth = screenwidth
        self.winfo_screenheight = screenheight

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        # Create widgets :)
        self.setup_widgets()


    def setup_widgets(self):

        # Panedwindow
        self.paned = ttk.PanedWindow(self, orient="horizontal")
        self.paned.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 10), rowspan=3, columnspan=3, sticky="nsew"
        )

        # Notebook, pane #2
        self.pane_1 = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.pane_1, weight=4)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_1)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.pack(fill="both", side = "right", expand=True)
        self.notebook.add(self.tab_1, text="状态")

        # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="信息")

        # Progressbar
        self.progress = ttk.Progressbar(
            self.tab_1, value=0, variable=self.var_5, mode="determinate"
        )
        self.progress.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")
        # Label
        self.label = ttk.Label(
            self.tab_1,
            text="Azure theme for ttk",
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label.grid(row=1, column=0, pady=10, columnspan=2)

if __name__ == "__main__":
    surface = tk.Tk()
    surface.title("study")
    surface.resizable(0, 0)
    # Simply set the theme
    surface.tk.call("source", "azure.tcl")
    surface.tk.call("set_theme", "light")

    winfo_screenwidth = 1000
    winfo_screenheight = 500

    switch = Switch(surface, winfo_screenwidth, winfo_screenheight)
    switch.pack(fill="both", expand=True)

    # Set the window size can not change, and place it in the middle
    surface.update()
    x_cordinate = int((surface.winfo_screenwidth() / 2) - (winfo_screenwidth / 2))
    y_cordinate = int((surface.winfo_screenheight() / 2) - (winfo_screenheight / 2))
    surface.geometry("{}x{}+{}+{}".format(winfo_screenwidth,winfo_screenheight,x_cordinate, y_cordinate-20))

    surface.mainloop()