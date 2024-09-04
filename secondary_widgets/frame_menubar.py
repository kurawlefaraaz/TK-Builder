import tkinter as tk

class FrameMenubar(tk.Frame):
    """A workaround to achive a menubar that can be attached to a particular frame."""
    def __init__(self, master, **frame_options):
        super().__init__(master, **frame_options)

        self._menu_button_dict = {}

        self._menu_button_pack_options = {}

        self._menu_options = {}
    
    def addMenubutton(self, menu_button_name, **menu_btn_options):
        menu_btn = tk.Menubutton(self, **menu_btn_options)
        menu = tk.Menu(menu_btn, **self._menu_options)
        menu_btn.config(menu=menu)

        self._menu_button_dict.update({menu_button_name: {"menu_button": menu_btn, "menu": menu}})
        menu_btn.pack(self._menu_button_pack_options)
    
    def setMenuButtonPackOptions(self, **options):
        self._menu_button_pack_options = options

    def setMenuOptions(self, **options):
        self._menu_options = options
    
    def getMenuButtonRef(self, menu_btn_name):
        return self._menu_button_dict.get(menu_btn_name).get("menu_button")
    
    def getMenuRef(self, menu_btn_name):
        return self._menu_button_dict.get(menu_btn_name).get("menu")
