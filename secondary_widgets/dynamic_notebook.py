import tkinter as tk
import tkinter.ttk as ttk

class DynamicNotebook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)

        self.root = parent
        self._tabDefualt= tk.Frame
        self._tabDefualt_options = {"master": self, "bg":"white"}
        self.frame_dict = {}


    def setDefualtFrame(self, widget_class, **widget_class_options):
        self._tabDefualt_options = widget_class_options
        self._tabDefualt= widget_class

    def intialize_Frames(self):
        frame1 = self._tabDefualt(**self._tabDefualt_options)

        self.add(frame1, text="Frame 1")
        self.add(tk.Label(self), text="-")
        self.add(tk.Label(self), text="+")

        self.frame_dict.update({"Frame 1": frame1})
        self.bind("<<NotebookTabChanged>>", self.watcher)

    def add_frame_button_func(self):
        c = self.index("current")
        self.insert_frame(c - 1)

    def insert_frame(self, index):
        tab_text = f"Frame {index+1}"
        frame = self._tabDefualt(**self._tabDefualt_options)
        
        self.insert(index, frame, text=tab_text)

        self.frame_dict.update({tab_text: frame})
        self.select(index)

    def remove_frame(self, index):
        self.forget(index)
        self.select(index - 1)

    def get_current_frame_tcl_name(self):
        current_index = self.index("current")
        return self.root.nametowidget(self.tabs()[current_index])

    def watcher(self, e):
        tab_name = self.tab(self.select(), "text")

        if tab_name not in ("-", "+"):
            return

        if tab_name == "-":
            c = self.index("current")
            if self.index("end") > 3:
                self.remove_frame(c - 1)
            else:
                self.select(c - 1)

        elif tab_name == "+":
            self.add_frame_button_func()

def demo():
    root = tk.Tk()
    wksp =DynamicNotebook(root)
    wksp.setDefualtFrame(tk.Button, master=wksp, text="hello")
    wksp.intialize_Frames()
    wksp.pack(fill="both", expand=1)
    root.mainloop()

if __name__ == "__main__":
    demo()
      