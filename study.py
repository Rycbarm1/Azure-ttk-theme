from itertools import product
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, ttk
from multiprocessing import Process, Manager, Lock, Queue

from traitlets import Bool
from time import sleep


class App_study(ttk.Frame):

    def __init__(self, parent, screenwidth = 300, screenheight = 200):
        ttk.Frame.__init__(self)

        # set winfo
        self.parent = parent

        self.producer_count = 2
        self.consumer_count = 2
        self.project_num    = 100

        self.manger = Share()
        self.Work = Work(self.manger, self.producer_count, self.consumer_count, self.project_num)

        # Create control variables
        self.treeview_data = { x : tk.StringVar(value="start init....") for x in range (self.producer_count) }
        self.test = tk.StringVar(value="start init....")

        print(self.test)

        # Create widgets :)
        self.setup_widgets()

        self.set_win_center()

    def setup_widgets(self):

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            show="headings",
            columns=(0, 1),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column(0, anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)

        # Treeview headings
        self.treeview.heading(0, text="生产者编号", anchor="center")
        self.treeview.heading(1, text="生产者信息", anchor="center")

        # Insert treeview data
        for item in range (self.producer_count):

            self.treeview.insert(
                "", index="end", iid=item, values=[ f"生产者{item}", self.treeview_data[item].get()]
            )

    def set_win_center(self):

        # Set the window size can not change, and place it in the middle
        self.parent.update()
        self.parent.minsize(self.parent.winfo_width(), self.parent.winfo_height())
        x_cordinate = int((self.parent.winfo_screenwidth() / 2) - (self.parent.winfo_width() / 2))
        y_cordinate = int((self.parent.winfo_screenheight() / 2) - (self.parent.winfo_height() / 2))
        self.parent.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))


class Share:
    def __init__(self) -> None:

        self.messages     = Queue(200)
        self.project      = Manager().list([0,0])
        self.project_lock = Manager().Lock()

        pass


class Work:
    def __init__(self, manger, producer_count, consumer_count, project_num) -> None:

        self.manger          = manger
        self.manger.project[0]  = project_num

        self.producer = { x : "" for x in range (producer_count) }
        self.consumer = { x : "" for x in range (consumer_count) }

        for x in range (producer_count):

            producer = Process(target=self.run_producer, args=(x,))
            producer.daemon = True
            producer.start()

        pass

    def run_producer(self, id) -> None:

        count = 0

        while True:

            self.manger.project_lock.acquire()

            if self.func():

                count = self.manger.project[1]

            else:

                count = self.manger.project[0] + 1

            self.manger.project_lock.release()

            if count > self.manger.project[0] :

                print("{} 结束生产任务".format(id))
                self.manger.messages.put("{} 结束生产任务".format(id))
                break

            print("{} 生产出第 {} 张票".format(id, count))
            self.manger.messages.put("{} 生产出第 {} 张票".format(id, count))

            sleep(2)

    def func(self) -> Bool:

        if self.manger.project[1] < self.manger.project[0]:

            self.manger.project[1] += 1

            return True

        else:

            return False


if __name__ == "__main__":

    surface = tk.Tk()
    surface.title("study")
    surface.resizable(0, 0)

    # Simply set the theme
    surface.tk.call("source", "azure.tcl")
    surface.tk.call("set_theme", "light")

    root = App_study(surface)
    root.pack(fill="both", expand=True)

    surface.mainloop()