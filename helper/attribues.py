import tkinter as tk
class Attributes:
    def __init__(self, widget_ref) -> None:
        self.widget_ref = widget_ref

    def retrive_master(self) -> str:
        return self.widget_ref.winfo_parent()
    
    def retrive_name(self) -> str:
        return self.widget_ref.winfo_name()

    def retrive_widget_attributes(self) -> dict:
        widget = self.widget_ref
        
        remove_attributes_tuple = ("class", "colormap", "container", "visual", "bg", "bd", "fg" )
        
        attribute = widget.keys()
        attribute_value = [widget.cget(i) for i in attribute]
        attributes_dict = dict(zip(attribute, attribute_value))
        
        ### Remove Some Attributes
        for keys in remove_attributes_tuple: attributes_dict.pop(keys, None)
        
        return attributes_dict

    def retrive_pack_attributes(self) -> dict:
        widget = self.widget_ref

        if widget.winfo_manager() != "pack":
            try:
                widget.pack()
            except Exception as exception:
                # showerror("Error", exception)
                return

        pack_attributes = widget.pack_info()
        pack_attributes.pop("in")

        return pack_attributes

    def retrive_grid_attributes(self) -> dict:
        widget = self.widget_ref

        if widget.winfo_manager() != "grid":
            try:
                widget.grid()
            except Exception as exception:
                # showerror("Error", exception)
                return

        grid_attributes = widget.grid_info()
        grid_attributes.pop("in")

        return grid_attributes

    def retrive_place_attributes(self) -> dict:
        widget = self.widget_ref

        if widget.winfo_manager() != "place":
            widget.place(x=0, y=0)

        place_attributes = widget.place_info()   
        place_attributes.pop("in")

        return place_attributes

    def widget_to_code(self):
        widget_attrs = self.retrive_widget_attributes()
        mgr = self.widget_ref.winfo_manager()
        mgr_attrs = getattr(self, f"retrive_{mgr}_attributes")()

        widget_class = self.widget_ref.winfo_class()
        widget_master = self.retrive_master()
        widget_name = self.retrive_name()

        widget_attrs_code = ", ".join((f'{key}= "{value}"' for key, value in widget_attrs.items()))
        mgr_attrs_code = ", ".join((f'{key}= "{value}"' for key, value in mgr_attrs.items()))

        if widget_class.startswith("T"):
            module = "ttk"
        else:
            module = "tk"
        
        CODE = f'''{module}.{widget_class}(master= "{widget_master}", name= "{widget_name}", {widget_attrs_code}).{mgr}({mgr_attrs_code})'''
        return CODE



def demo():
    root = tk.Tk()

    widget = tk.Label(root)
    widget.pack()
    frame = tk.Frame(root)

    a = Attributes(frame)
    a.retrive_widget_attributes()
    a.retrive_pack_attributes()
    a.retrive_grid_attributes()
    a.retrive_place_attributes()
    print(a.widget_to_code())


if __name__ == "__main__":
    demo()
