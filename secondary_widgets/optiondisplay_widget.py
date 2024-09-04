import tkinter as tk
import tkinter.ttk as ttk

from secondary_widgets import EditableTreeview
from helper import Attributes

class OptionDisplay(tk.LabelFrame):
    treecolumns = ("Attributes", "Value")
    def __init__(self, parent, widget,**options):
        super().__init__(parent, **options)
        self.parent = parent
        self.attribute_class = Attributes(widget)
        
    @staticmethod
    def disable_treeview(tree):
        tree.state(("disabled",))
        tree.bind('<Button-1>', lambda e: 'break')

    @staticmethod
    def enable_treeview(tree):
        tree.state(("!disabled",))
        tree.unbind('<Button-1>')

    @staticmethod
    def add_Editable_Treeview(tree_parent, func):
        data = func()

        treeview = EditableTreeview(
            tree_parent,
            columns=OptionDisplay.treecolumns,
            show="headings",
            data=data,
            non_editable_columns="#1"
        )
        return treeview

    @staticmethod
    def retrive_data_from_treeview(treeview):
        retrived_data = dict()

        for tree_index in treeview.get_children():
            values = treeview.item(tree_index, "values")
            retrived_data.update({values[0]: values[1]})

        return retrived_data


class WidgetOptionDisplay(OptionDisplay):
    def __init__(self, parent, widget, master_name_code_dict, **options):
        self.widget = widget
        super().__init__(parent=parent, widget=widget, **options)

        non_editables_frame = tk.Frame(self)
        tk.Label(non_editables_frame, text="Non-Editables", justify="left").pack(anchor="w")
        non_edit_tree = EditableTreeview(non_editables_frame, columns=self.treecolumns, non_editable_columns ="#1", readonly_entry_wid="readonly", show="headings", data=master_name_code_dict)
        # for name in self.treecolumns:
        #     non_edit_tree.heading(name, text=name)

        # for values in master_name_dict.items():
        #     non_edit_tree.insert('', tk.END, values=values)
        
        non_edit_tree.pack(fill="x")
        non_editables_frame.pack(pady=10, padx=10, fill="x")

        editables_frame = tk.Frame(self)
        tk.Label(editables_frame, text="Editables", justify="left").pack(anchor="w")
        self.tree = self.add_Editable_Treeview(
            tree_parent=editables_frame, func=self.attribute_class.retrive_widget_attributes
        )
        self.tree.pack(fill="x")
        editables_frame.pack(pady=10, padx=10, fill="x")
    
    def update_treeview(self):
        rows = self.tree.get_children()
        for item in rows:
            self.tree.delete(item)

        widget_attributes = self.attribute_class.retrive_widget_attributes()
    
        for values in widget_attributes:
            a=self.tree.insert("", tk.END, values=(values, widget_attributes.get(values)))

        self.tree.selection_set(self.tree.get_children()[0])
            
        
class ManagerOptionDisplay(OptionDisplay):
    def __init__(self, parent, widget,**options):
        super().__init__(parent=parent, widget=widget, **options)
        self.widget = widget
        self.manager_selection()

    def manager_selection(self):
        self.button_frame = tk.LabelFrame(self, text="Select Widget Manager")
        self.button_frame.pack(
            anchor="n",
            padx=10,
            pady=10,
        )

        self.RadioSelectedVar = tk.StringVar(self)

        self.selected_place = tk.Radiobutton(
            self.button_frame,
            text="Place",
            value="place",
            variable=self.RadioSelectedVar,
            command=self.update_treeview,
        )
        self.selected_place.pack(side="left", padx=10, pady=5, anchor="w", expand=0)

        self.selected_grid = tk.Radiobutton(
            self.button_frame,
            text="Grid",
            value="grid",
            variable=self.RadioSelectedVar,
            command=self.update_treeview,
        )
        self.selected_grid.pack(side="left", padx=10, pady=5, anchor="center", expand=0)

        self.selected_pack = tk.Radiobutton(
            self.button_frame,
            text="Pack",
            value="pack",
            variable=self.RadioSelectedVar,
            command=self.update_treeview,
        )
        self.selected_pack.pack(side="left", padx=10, pady=5, anchor="e", expand=0)
        
        self.tree = self.add_Editable_Treeview(
            tree_parent=self, func=lambda: {"Test": "1", "Test": "2"}
        )
        self.tree.pack(fill="x", padx=20, pady=20)

        

        manager = self.widget.winfo_manager()
        if manager:
            self.RadioSelectedVar.set(manager)
            try:
                getattr(self, f"selected_{manager}").invoke()
            except:
                self.parent.destroy()
        else:
            self.selected_place.invoke()

    def update_treeview(self):
        rows = self.tree.get_children()
        for item in rows:
            a=self.tree.delete(item)

        manager_attributes = getattr(
            self.attribute_class, f"retrive_{self.RadioSelectedVar.get()}_attributes"
        )()
        if manager_attributes != None:
            self.enable_treeview(self.tree)
            for values in manager_attributes:
                a=self.tree.insert("", tk.END, values=(values, manager_attributes.get(values)))

            self.tree.selection_set(self.tree.get_children()[0])
            
        else:
            self.tree.insert("", tk.END, values=("Error", f"Can not use geometry manager"))
            self.tree.insert("", tk.END, values=("Error", f"{self.RadioSelectedVar.get()} along with {'pack' if self.RadioSelectedVar.get() == 'grid' else 'grid'}"))
            
            self.disable_treeview(self.tree)
        
    def get_selected_manager_and_tree(self):
        return self.RadioSelectedVar.get(), self.tree
