import tkinter.ttk as ttk
import tkinter as tk

from layout_simplifier import LayoutSimplifier
class LayoutTreeview(ttk.Treeview):
    def __init__(self, master, widget_class_name, **treeviewOptions):
        super().__init__(master, **treeviewOptions)
        
        if "style" in treeviewOptions:
            widget_style = treeviewOptions.get("style")
        else:
            widget_style = "Layout.Treeview"

        self.heading("#0", text="Layout")

        widget_simplfy_class_ref = LayoutSimplifier(self, widget_class_name)
        widget_layout = widget_simplfy_class_ref.simplify()

        parent = ""
        
        for item in widget_layout:
            name, attributes = item, widget_layout.get(item)
            self.insert(parent, "end", text=name, iid=name,)
            for attr_name in attributes:
                self.insert(name, "end", text=f"{attr_name}: {attributes.get(attr_name)}")  
            parent = name   


if __name__ == "__main__":
    root = tk.Tk()
    a=LayoutTreeview(root, "Treeview")
    a.pack()
    root.mainloop()
            
        
            