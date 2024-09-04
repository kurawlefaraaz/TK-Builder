from tkinter import ttk
import tkinter as tk

class ToggleButton(tk.Button, ttk.Button):
    """Tkinter Button which can be used to executes FUNCTION A on first press and Function B at second.
        Can be used to execute and undo the effect of a function.
        Provide Functions with in lambda altogether with parameters.

        All Tkinter Button and Themed Tkinter Button options are vaild.
        Used Internally by DropDownButton
        """
    
    def __init__(self, master,
        on_first_press_func, on_second_press_func, ttk_btn=0,
        **button_options):

        if ttk_btn:
            ttk.Button.__init__(self, master)
            self.config(button_options)
        else:
            tk.Button.__init__(self, master, button_options)
        
        self.on_first_press_func = on_first_press_func
        self.on_second_press_func = on_second_press_func
        self.counter = 0

        self.config(command = self.toggle)

    def toggle(self):
        if not self.counter:self.on_first_press_func(); self.counter =1
        else:self.on_second_press_func(); self.counter = 0

class DropdownButton(ToggleButton):
    def __init__(
        self,
        master,
        Frame,
        on_first_press_func=lambda:None,
        on_second_press_func=lambda:None,
        ttk_btn=0,
        symbol=("▼", "▲"),
        **button_options,
    ):
        """
        Provides a drop-down button which displays and hides the 'Frame' depending on 'counter'

        All valid tk.button and ttk.button attribute are acceptable
        """

        super().__init__(master,self.on_frame_invisible, self.on_frame_visible, ttk_btn, **button_options)

        self.symbol_down, self.symbol_up = symbol[0], symbol[1]

        self.mgr, self.button_text =   Frame.winfo_manager(), self.cget("text"), 

        self.onpresscmd, self.onnextpresscmd = on_first_press_func, on_second_press_func

        self.mgr_options = getattr(Frame, f"{self.mgr}_info")()
        self.mgr_options.pop("in")

        self.Show = lambda: getattr(Frame, self.mgr)(self.mgr_options)
        self.Hide = lambda: getattr(Frame, f"{self.mgr}_forget")()

        self.config(text=f"{self.button_text} {self.symbol_down}", command=self.toggle)
        self.Hide()
    
    def on_frame_visible(self):
        self.Hide()

        if self.onnextpresscmd != None:
            self.onnextpresscmd()

        self.config(text=f"{self.button_text} {self.symbol_down}")
        
    def on_frame_invisible(self):
        self.Show()

        if self.onpresscmd != None:
            self.onpresscmd()

        self.config(text=f"{self.button_text} {self.symbol_up}")
            
