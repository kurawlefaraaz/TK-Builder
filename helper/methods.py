import tkinter as tk
from tkinter import ttk

class Movement:
    def bind_methods(self, widget, baseroot):
        from UI.Create_Update_UI import Updation_UI
        
        widget.bind("<B1-Motion>", self.on_mouse_move)
        widget.bind("<Button-1>", lambda e: self.on_click_chose_widget(e, root = baseroot))
        widget.bind("<Button-3>", lambda event:Updation_UI(parent=baseroot, widget_refrence=widget))

        widget.bind("<Down>", self.kb_Down)
        widget.bind("<Left>", self.kb_Left)
        widget.bind("<Right>", self.kb_Right)
        widget.bind("<Up>", self.kb_Up)
        
    def on_mouse_move(self, event, widget = None):
        if widget == None:
            widget = event.widget

        if widget.winfo_manager() != "place":
            return
        
        parent = widget.nametowidget(widget.winfo_parent())
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        locx, locy = widget.winfo_x(), widget.winfo_y()
        xpos = locx + event.x
        ypos = locy + event.y

        if xpos >= parent_w: xpos = parent_w - 10
        if ypos >= parent_h: ypos = parent_h - 10

        if xpos <= 0: xpos = 0
        if ypos <= 0: ypos = 0
        
        widget.place(anchor="center", x=xpos, y=ypos, relx=0, rely=0)
        parent.update()

    def kb_Left(self, e):
        widget = e.widget
        if widget.winfo_manager() != "place":
            return
        
        locx, locy = widget.winfo_x(), widget.winfo_y()

        x = locx - 1
        if x <= 0: x = 0
        widget.place(x=x, y=locy, relx=0, rely=0)

    def kb_Right(self, e):
        widget = e.widget
        if widget.winfo_manager() != "place":
            return
        
        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx + 1
        y = locy

        parent = widget.nametowidget(widget.winfo_parent())
        parent_w = parent.winfo_width()

        if x >= parent_w: x = parent_w - 10

        widget.place(x=x, y=y, relx=0, rely=0)

    def kb_Up(self, e):
        widget = e.widget
        if widget.winfo_manager() != "place":
            return
        
        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx
        y = locy - 1

        if y <= 0: y = 0
        widget.place(x=x, y=y, relx=0, rely=0)

    def kb_Down(self, e):
        widget = e.widget
        if widget.winfo_manager() != "place":
            return

        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx
        y = locy + 1

        parent = widget.nametowidget(widget.winfo_parent())
        parent_h = parent.winfo_height()

        if y >= parent_h: y = parent_h - 10
        widget.place(x=x, y=y, relx=0, rely=0)
    
    def on_click_chose_widget(self, e, root):
        x, y = root.winfo_pointerxy()
        widget = root.winfo_containing(x, y)
        widget.focus_set()

class WidgetMethods(Movement):
    def create_widget(
        self,
        widget_class,
        widget_manager:str,
        widget_name:str, 
        widget_master,
        manager_options: dict,
        baseroot,
    ):  
        
        w =widget_class(widget_master, name= widget_name)
 
        self.bind_methods(widget=w, baseroot=baseroot)
        getattr(w, widget_manager)(manager_options)

        return w

    def update_widget(
        self,
        widget_refrence,
        widget_manager,
        widget_options: dict,
        manager_options: dict,
    ):
        widget_refrence.configure(widget_options)
        getattr(widget_refrence, widget_manager)(**manager_options)
    
    def delete_widget(self, widget_refrence): widget_refrence.destroy() 

    def reset_widget(self, 
                     widget_refrence, 
                     manager_options:dict, 
                     widget_manager:str, 
                     baseroot):
        master = baseroot.nametowidget(widget_refrence.winfo_parent())
        name = widget_refrence.winfo_name()

        class_ref = getattr(tk, widget_refrence.winfo_class())
        
        self.create_widget(widget_class=class_ref,
                           widget_manager=widget_manager,
                           widget_name=name,
                           widget_master=master,
                           manager_options=manager_options,
                           baseroot=baseroot)

        
    