import tkinter as tk
import tkinter.ttk as ttk

from secondary_widgets import DropdownButton
from secondary_widgets import DynamicNotebook
from secondary_widgets import ExecuteCodeUI
from UI import Creation_UI

def Tk_Widget_dict():
    dict = {
        "Button": tk.Button,
        "Frame": tk.Frame,
        "Label": tk.Label,
        "Entry": tk.Entry,
        "Listbox": tk.Listbox,
        "Menubutton": tk.Menubutton,
        "Radiobutton": tk.Radiobutton,
        "Text": tk.Text,
        "Checkbutton": tk.Checkbutton,
        "Menu": tk.Menu,
        "LabelFrame": tk.LabelFrame,
        "PanedWindow": tk.PanedWindow,
        "SpinBox": tk.Spinbox,
        "Scrollbar": tk.Scrollbar,
        "Scale": tk.Scale,
        "Message": tk.Message,
        "Canvas": tk.Canvas,
    }
    return dict

def Ttk_Widget_dict():
    dict = {
        "Button": ttk.Button,
        "Frame": ttk.Frame,
        "Label": ttk.Label,
        "Entry": ttk.Entry,
        "Menubutton": ttk.Menubutton,
        "Radiobutton": ttk.Radiobutton,
        "LabelFrame": ttk.LabelFrame,
        "PanedWindow": ttk.PanedWindow,
        "SpinBox": ttk.Spinbox,
        "Scrollbar": ttk.Scrollbar,
        "Scrollbar": ttk.Scrollbar,
        "Checkbutton": ttk.Checkbutton,
        "ComboBox": ttk.Combobox,
        "NoteBook": ttk.Notebook,
        "ProgressBar": ttk.Progressbar,
        "Separator": ttk.Separator,
        "Sizegrip": ttk.Sizegrip,
        "TreeView": ttk.Treeview,
    }

    return dict

class WidgetCatalog(tk.Frame):  # An top level widget to create new widget in workspace.
    def __init__(self, parent, workspace_obj, **options):
        super().__init__(parent, **options)

        self.workspace_obj = workspace_obj
        self.parent = parent
        self.Button_Holder()

    def Button_Holder(self):  # Contains Buttons which displays All widgets
        self.create_btn_frame = tk.Frame(self)

        ### TK Frame ###
        tk_frame = self.tk_catalog_frame()
        tk_frame.pack()

        self.create_tk_widget_btn = DropdownButton(
            self.create_btn_frame,
            tk_frame,
            on_first_press_func=lambda: self.on_press((self.create_ttk_widget_btn, self.execute_code_btn)),
            on_second_press_func=lambda: self.on_release((self.create_ttk_widget_btn, self.execute_code_btn)),
            ttk_btn=1,
            text="Create Tk Widget",
        )
        self.create_tk_widget_btn.pack(side="left", padx=10, pady=5)

         ### Execute Code Frame ###
        excute_code_frame = self.execute_code_catalog_frame()
        excute_code_frame.pack()

        self.execute_code_btn = DropdownButton(
            self.create_btn_frame,
            excute_code_frame,
            on_first_press_func=lambda: self.on_press((self.create_ttk_widget_btn, self.create_tk_widget_btn)),
            on_second_press_func=lambda: self.on_release((self.create_ttk_widget_btn, self.create_tk_widget_btn)),
            ttk_btn=1,
            text="Execute Custom Code",
        )
        self.execute_code_btn.pack(side="left", padx=10, pady=5)

        ### TTK Frame ###
        ttk_frame = self.ttk_catalog_frame()
        ttk_frame.pack()

        self.create_ttk_widget_btn = DropdownButton(
            self.create_btn_frame,
            ttk_frame,
            on_first_press_func=lambda: self.on_press((self.create_tk_widget_btn, self.execute_code_btn)),
            on_second_press_func=lambda: self.on_release((self.create_tk_widget_btn, self.execute_code_btn)),
            ttk_btn=1,
            text="Create Ttk Widget",
        )
        self.create_ttk_widget_btn.pack(padx=10, side="right", pady=5)
        self.update()
        self.create_btn_frame.pack()
        

    def tk_catalog_frame(self):
        TK_Catalog_Frame = tk.LabelFrame(self, name="tk_cf", text="TK Widget Catalog")
        self._GridWidget_catalog(TK_Catalog_Frame, Tk_Widget_dict())
        return TK_Catalog_Frame

    def ttk_catalog_frame(self):
        TtK_Catalog_Frame = tk.LabelFrame(
            self, name="ttk_cf", text="TTK Widget Catalog"
        )
        self._GridWidget_catalog(TtK_Catalog_Frame, Ttk_Widget_dict())
        return TtK_Catalog_Frame

    def execute_code_catalog_frame(self):
        custom_code = DynamicNotebook(self)
        custom_code.setDefualtFrame(ExecuteCodeUI, master=custom_code)
        custom_code.intialize_Frames()
        custom_code.pack()
        return custom_code
        
    def on_press(self, buttons:tuple):
        for button in buttons:
            button.config(state="disabled")
           
    def on_release(self, buttons:tuple):
        for button in buttons:
            button.config(state="normal")
    
    def _disable_all_buttons(self):
        self.on_press(tuple(self.create_btn_frame.winfo_children()))

    def _find_active_button(self):
        buttons = self.create_btn_frame.winfo_children()
        for button in buttons:
            state = str(button.cget("state"))
            if state == "normal":
                return button
            
    def _toggle_active_button(self):
        active_button = self._find_active_button()
        active_button.toggle()
        return active_button

    def _wait_creation_ui(self, creation_window, prev_active_button):
        self.wait_window(creation_window)
        prev_active_button.configure(state= "normal")
        prev_active_button.toggle()

    def _widget_button_function(self, widget_class):
        notebook_frame = self.workspace_obj.get_current_frame_tcl_name()
        notebook_frame = self.parent.nametowidget(notebook_frame)

        active_button = self._toggle_active_button()
        self._disable_all_buttons()
        creation_window = Creation_UI(
                    parent=notebook_frame, widget_class=widget_class
                )
        self._wait_creation_ui(creation_window, active_button)
        
    def _GridWidget_catalog(self, FrameName, widget_dict):  # Creates Buttons for each widget in widget_dict.
        r, c = 0, 0
        for key, value in widget_dict.items():
            if c == 5:
                r += 1
                c = 0

            tk.Button(
                FrameName,
                text=key,
                bg="#008cba",
                fg="white",
                border=0,
                width=20,
                command=lambda widget_class=value: self._widget_button_function(widget_class=widget_class)
            ).grid(row=r, column=c, padx=5, pady=5)

            c += 1

def demo():
    
    root = tk.Tk()
    root.minsize(500, 500)
    a = DynamicNotebook(root)
    a.pack(fill="both", expand=1)
    WidgetCatalog(root, a)
    root.mainloop()
    
if __name__ == "__main__":
    demo()
