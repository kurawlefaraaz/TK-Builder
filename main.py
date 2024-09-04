import tkinter as tk
import tkinter.ttk as ttk

from UI import MenuBar
from UI import WidgetCatalog
from secondary_widgets import DynamicNotebook
from secondary_widgets import WidgetOptionDisplay
from helper import Attributes, Movement

class UpdateFrameUI(tk.Toplevel):
    def update_widget_func(self):
        widget_options = self.widget_option_frame.retrive_data_from_treeview(self.widget_option_frame.tree)
        self.frame.config(**widget_options)

    def __init__(self, parent, frame, **options):
        super().__init__(parent, **options)

        self.frame = frame

        master_name_dict = {"master": frame.winfo_parent(), "name": frame.winfo_name(), "widget_path": f"{frame.winfo_parent()}.{frame.winfo_name()}"}

        self.widget_reset_val = Attributes(widget_ref=frame).retrive_widget_attributes()

        self.widget_option_frame = WidgetOptionDisplay(parent=self, widget=frame,master_name_dict=master_name_dict, text="Frame Attributes")
        self.widget_option_frame.pack(fill="both", expand=1)

        self.widget_option_frame.tree.bind("<<TreeviewSelect>>", lambda e : self.update_widget_func())
        
        button_frame = tk.Frame(self)
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_btn_func)
        reset_button.grid(row=0, column=1, sticky="ew", padx=20, pady=10)
        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit_btn_func)
        submit_button.grid(row=0, column=2, rowspan=2, sticky="ew", padx=20, pady=10)
        button_frame.pack(side="top", anchor="n")
    
    def reset_btn_func(self):
        self.frame.config(**self.widget_reset_val)
        self.widget_option_frame.update_treeview()

    def submit_btn_func(self):
        self.destroy()
    
class UpdatableFrame(tk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.bind("<Button-3>", lambda event:UpdateFrameUI(parent=master, frame=event.widget))

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Workspace")
        self.state("zoomed")

        s = ttk.Style(self)
        s.theme_use("clam")
        
        self.workspace()
        self.catalog_window()
        self.addMenubar()
        
    def catalog_window(self):
        self.w_catlog_container = tk.Frame(self)

        w_catlog_title_bar = tk.Frame(self.w_catlog_container, height=30, highlightbackground="black", highlightthickness=1)
        title = tk.Label(w_catlog_title_bar, text= "Create Widgets")
        title.pack(side="left", fill='y')

        self.minimize = tk.Button(w_catlog_title_bar, text= "_", relief="flat", anchor="n", font = ("","0", "bold"), borderwidth=0, )
        self.minimize.pack(side="right")

        on_hover = lambda e: self.minimize.config(bg = "lightblue")
        on_leave = lambda e: self.minimize.config(bg = "SystemButtonFace")
        self.minimize.bind("<Enter>", on_hover)
        self.minimize.bind("<Leave>", on_leave)

        w_catlog_title_bar.pack(fill="both", expand=1, )

        w_catlog = WidgetCatalog(self.w_catlog_container, self.workspace_widget, pady=10, padx=10)
        w_catlog.pack()

        widget_mtds = Movement()
        w_catlog_title_bar.bind("<B1-Motion>", lambda e: widget_mtds.on_mouse_move(e, widget=self.w_catlog_container))
        self.w_catlog_container.bind("<B1-Motion>", lambda e: widget_mtds.on_mouse_move(e, widget=self.w_catlog_container))
        w_catlog.bind("<B1-Motion>", lambda e: widget_mtds.on_mouse_move(e, widget=self.w_catlog_container))

        
    def addMenubar(self):
        self.menubar= MenuBar(self, catalog_ref=self.w_catlog_container)
        self.minimize.config(command= self.menubar.toggle_catalog_menu.toggle)
        self.w_catlog_container.place(relx=0.5, rely=0.5, anchor="center")

    def workspace(self):
        self.workspace_widget = DynamicNotebook(self)
        self.workspace_widget.setDefualtFrame(UpdatableFrame, master=self.workspace_widget, bg="white")
        self.workspace_widget.intialize_Frames()
        self.workspace_widget.pack(fill="both", expand=1, padx=5, pady=5)


if __name__ == "__main__":
    A = GUI()
    A.mainloop()