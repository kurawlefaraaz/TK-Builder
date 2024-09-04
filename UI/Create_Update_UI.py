import tkinter as tk
import tkinter.ttk as ttk
from secondary_widgets import WidgetOptionDisplay, ManagerOptionDisplay, ExecuteCodeUI
from helper.attribues import Attributes
from helper.methods import WidgetMethods

class BaseUI(tk.Toplevel, WidgetMethods):
    def __init__(self, parent, title, widget) -> tk.Toplevel:
        super().__init__(parent)
        self.minsize(700, 500)
        self.title(title)
        
        self.parent = parent
        self.widget = widget
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", padx=10, pady=10, expand=1)
        self.lift()
        return self


    def update_widget_func(self):
        mgr = self.widget.winfo_manager()
        widget_options = self.widget_option_frame.retrive_data_from_treeview(self.widget_option_frame.tree)
        mgr_options = self.mgr_option_frame.retrive_data_from_treeview(self.mgr_option_frame.tree)

        self.update_widget(widget_refrence=self.widget, widget_manager= mgr, widget_options= widget_options, manager_options= mgr_options)

    def add_paned_windows(self):
        self.paned_window =  tk.PanedWindow(self.container, orient ='horizontal', showhandle=1)
        self.paned_window.configure(sashpad=10, sashwidth=10, sashrelief='ridge')
        self.paned_window.pack(fill = "both", expand=1)

        self.paned_window_2 = tk.PanedWindow(self.paned_window, orient=tk.VERTICAL, sashpad=10, sashwidth=10, sashrelief='ridge')

    def insert_into_paned_window(self):
        self.paned_window.add(self.widget_option_frame, minsize = 300, padx=10)
        self.paned_window_2.add(self.mgr_option_frame)
        self.paned_window_2.add(self.textarea, height=100)
        self.paned_window.add(self.paned_window_2)

    def button_init(self, master_name_dict):
        self.protocol('WM_DELETE_WINDOW', lambda: self.on_exit())
    
        self.add_paned_windows()
        self.widget_option_frame = WidgetOptionDisplay(
            parent=self.paned_window,
            widget=self.widget,
            text="Widget Options",
            master_name_code_dict=master_name_dict
        )

        self.mgr_option_frame = ManagerOptionDisplay(
            parent=self.paned_window_2,
            widget=self.widget,
            text="Manager Options",
        )
        
        self.textarea = ExecuteCodeUI(self, text="Custom Code Block")

        self.insert_into_paned_window()

        self.widget_option_frame.tree.bind("<<TreeviewSelect>>", lambda e : self.update_widget_func())
        self.mgr_option_frame.tree.bind("<<TreeviewSelect>>", lambda e : self.update_widget_func())
        self.update_treeview_func_id = lambda e: self.mgr_option_frame.update_treeview()
        self.widget.bind("<ButtonRelease-1>", self.update_treeview_func_id)

         # TODO: Styling
        button_frame = tk.Frame(self.container)
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_btn_func)
        reset_button.grid(row=0, column=1, sticky="ew", padx=20, pady=10)
        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit_btn_func)
        submit_button.grid(row=0, column=2, rowspan=2, sticky="ew", padx=20, pady=10)
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_btn_func)
        delete_button.grid(row=0, column=3, sticky="ew", padx=20, pady=10)
        button_frame.pack(side="top", anchor="n")

    def delete_btn_func(self):
        self.delete_widget(self.widget)
        self.destroy()

    def submit_btn_func(self): 
        self.widget.unbind("<ButtonRelease-1>")
        self.destroy()

class Creation_UI(BaseUI):
    def reset_btn_func(self):
        mgr, mgr_options = self.mgr_option_frame.get_selected_manager_and_tree()
        mgr_options = self.mgr_option_frame.retrive_data_from_treeview(mgr_options)

        self.reset_widget(widget_refrence=self.widget, manager_options=mgr_options, widget_manager=mgr, baseroot=self.parent)
        self.widget_option_frame.update_treeview()

    def on_exit(self):
        self.delete_btn_func()

    def __init__(self, parent, widget_class):
        self.parent = parent
        self.widget_class = widget_class
        
        self.UI_window = super().__init__(parent, widget=widget_class, title = "Create Widget")
        self.widget_init()

        self.UI_window.widget = self.widget_refrence
        
        self.lift()
        attr = Attributes(self.widget_refrence)
        self.user_based_master_name.update({"widget_code": attr.widget_to_code()})
        master_name_code_dict = self.user_based_master_name
        self.button_init(master_name_code_dict)
    
    def get_master_and_name_detail(self, default_vals: tuple):
        
        def submit_func(self):
            import tkinter.messagebox as mb
            master_text = master_entry.get()
            name_text = name_entry.get()
            
            retry = 0
            if not name_text and not master_text:
                retry = not(mb.askyesno(title="Warning", message="All values are missing.\nIf you wish to set defalut values, press Yes."))

            elif not master_text:
                retry = not(mb.askyesno(title="Warning", message="Master value is missing.\nIf you wish to set defalut values, press Yes."))
                
            elif not name_text:
                retry = not(mb.askyesno(title="Warning", message="Name value is missing.\nIf you wish to set defalut values, press Yes."))
            else:
                master_text = self.parent.nametowidget(master_text)
                name_text = (name_text)
            
            if retry:
                    return
            else:
                master_text = self.parent.nametowidget(default_vals[0]) if master_text == "" else self.parent.nametowidget(master_text)
                name_text = default_vals[1] if name_text == "" else name_text

            attribute_values.update({"master": master_text, "name": name_text, "widget_path": f"{master_text}.{name_text}"})
            get_master_name_frame.destroy()
            
        attribute_values = dict()
        self.protocol('WM_DELETE_WINDOW', lambda: 0)
        get_master_name_frame = tk.Frame(self.UI_window)

        title_frame = tk.Frame(get_master_name_frame)
        title = tk.Label(title_frame, text="Enter Values", font="Times 50 bold", justify="left")
        title.grid(row=0, column=0, sticky="w")
        subtitle = tk.Label(title_frame, text="Leave blank for default values.", font="sublime 15", justify="left")
        subtitle.grid(row=1, column=0, sticky="w")
        title_frame.grid(row=0, column=0, pady=20, sticky="w")

        submit_btn = tk.Button(get_master_name_frame, text= "Submit", font = "Times 15", command=lambda: submit_func(self))
        submit_btn.grid(row=0,column=1, columnspan=2,rowspan=2, pady=20, padx=5,)

        master_label = tk.Label(get_master_name_frame, text="Master: ", font=("Times", 15,), justify="left")
        master_label.grid(row = 1, column = 0, padx=2, sticky="w", columnspan=2)
        master_entry = tk.Entry(get_master_name_frame, font=("", 40))
        master_entry.grid(row = 2, column = 0, padx=2, sticky="ew", columnspan=2)

        name_label = tk.Label(get_master_name_frame, text="Name: ", font=("Times", 15,), justify="left")
        name_label.grid(row = 3, column = 0, padx=2, sticky="w", columnspan=2)
        name_entry = tk.Entry(get_master_name_frame, font=("", 40))
        name_entry.grid(row = 4, column = 0, padx=2, sticky="ew", columnspan=2)
        
        get_master_name_frame.place(relx = 0.5, rely = 0.5, anchor="center")
        self.parent.wait_window(get_master_name_frame)

        return attribute_values
    
    def widget_init(self):
        self.temp_widget_ref = self.widget_class(self.parent)
        self.temp_widget_ref.place(x=0, y=0)

        attr = Attributes(self.temp_widget_ref)

        defalut_master = attr.retrive_master()
        defalut_name = attr.retrive_name()

        manager_options = attr.retrive_place_attributes()
        self.temp_widget_ref.destroy()
        del self.temp_widget_ref

        self.user_based_master_name = self.get_master_and_name_detail(default_vals=(defalut_master, defalut_name))
        
        self.widget_refrence = self.create_widget(
            widget_class=self.widget_class,
            widget_master=self.user_based_master_name.get("master"),
            widget_name=self.user_based_master_name.get("name"),
            widget_manager="place",
            manager_options=manager_options,
            baseroot= self.parent,
        )

class Updation_UI(BaseUI):
    def on_exit(self):
        self.reset_btn_func()
        self.destroy()
        
    def reset_btn_func(self):
        mgr, mgr_options = self.mgr_option_frame.get_selected_manager_and_tree()
        mgr_options = self.mgr_option_frame.retrive_data_from_treeview(mgr_options)

        self.update_widget(widget_refrence=self.widget, manager_options=mgr_options, widget_manager=mgr, widget_options=self.widget_reset_vals)
        self.widget_option_frame.update_treeview()

    def __init__(self, parent, widget_refrence):
        super().__init__(parent, widget=widget_refrence, title="Update Widget")

        attr = Attributes(widget_refrence)
        master_name_dict = {"master": attr.retrive_master(), "name": attr.retrive_name()}

        self.widget_reset_vals = attr.retrive_widget_attributes()

        attr = Attributes(widget_refrence)
        master_name_dict.update({"widget_path": f'''{master_name_dict.get("master")}.{master_name_dict.get("name")}''',"widget_code": attr.widget_to_code()})
        master_name_code_dict =master_name_dict
        self.button_init(master_name_code_dict)

def demo():
    root = tk.Tk()
    Create = Creation_UI(root, tk.Button)
    # Updation_UI already binded when widget is created by Creation UI
    root.mainloop()

if __name__ == "__main__":
    demo()

