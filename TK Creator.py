import tkinter as tk
from tkinter import ttk
from tkinter import Listbox as lb
from tkinter import messagebox as mb


class Movement:
    def on_mouse_move(self, event):
        global focus_widget
        widget = event.widget
        focus_widget = widget
        locx, locy = widget.winfo_x(), widget.winfo_y()
        xpos = locx + event.x
        ypos = locy + event.y
        widget.place(x=xpos, y=ypos)

    def kb_Left(self, e):
        widget = e.widget
        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx - 1
        widget.place(x=x, y=locy)

    def kb_Right(self, e):
        widget = e.widget
        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx + 1
        y = locy
        widget.place(x=x, y=y)

    def kb_Up(self, e):
        widget = e.widget
        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx
        y = locy - 1
        widget.place(x=x, y=y)

    def kb_Down(self, e):
        widget = e.widget
        locx, locy = widget.winfo_x(), widget.winfo_y()
        x = locx
        y = locy + 1
        widget.place(x=x, y=y)


class WidgetMethod(Movement):
    def Create(self, widget_name, root, destroy_toplevel):
        widget_attributes = self.take_attributes(
            label="Enter Vaild Attributes: ",
            title="Create Widget",
            popup=1,
            entry_bg="#343a40",
            entry_fg="white",
        )
        try:
            par = dict(e.split("=") for e in widget_attributes.split(","))

            if "master" not in par:
                if "ttk" not in str(widget_name):
                    widget = widget_name(root, par)
                else:
                    widget = widget_name(root)
                    for i, j in par.items():
                        widget[i] = j
            else:
                sub_root = root.nametowidget(par.get("master"))
                par.pop("master")
                if "ttk" not in str(widget_name):
                    widget = widget_name(sub_root, par)
                else:
                    widget = widget_name(sub_root)
                    for i, j in par.items():
                        widget[i] = j
            widget.place(x=0, y=0)
        except ValueError as e:
            mb.showerror("Error", e)
        except IndexError:
            mb.showerror("Error", "Please input atleast one command!")
        except Exception as tk_e:
            mb.showerror("Error", tk_e)
        else:
            root.bind("<Button-1>", lambda e: self.on_click_chose_widget(e, root))
            widget.bind("<B1-Motion>", self.on_mouse_move)
            widget.bind("<Left>", self.kb_Left)
            widget.bind("<Right>", self.kb_Right)
            widget.bind("<Up>", self.kb_Up)
            widget.bind("<Down>", self.kb_Down)
            destroy_toplevel.destroy()

    def take_attributes(self, **options):
        if options.get("popup"):
            Attri_take = tk.Toplevel()
            Attri_take.title(options.get("title"))
            Attri_take.config(bg="white")
            Attri_take.grab_set()
        else:
            root = options.get("mroot")
            Attri_take = options.get("root")

        def submit():
            global data
            data = attributes.get()
            if options.get("popup"):
                Attri_take.destroy()
            else:
                root.destroy()

        Title = tk.Label(
            Attri_take, text=options.get("label"), bg="white", font="sublime 10 bold"
        )
        Title.pack(fill=tk.X)
        attributes = tk.Entry(
            Attri_take, bg=options.get("entry_bg"), fg=options.get("entry_fg")
        )
        attributes.pack(fill=tk.X)

        b = ttk.Button(Attri_take, text="Submit", command=submit)

        if options.get("anc"):
            b.pack(anchor="w")
        else:
            b.pack()
        if options.get("popup") or options.get("wait"):
            Attri_take.wait_window()
            return data

    def Update_widget(self, update_options, widget_name):

        try:
            par = dict(e.split("=") for e in update_options.split(","))
            widget_name.config(par)
        except IndexError:
            mb.showerror("Error", "Please input atleast one command!")
        except Exception as tk_e:
            mb.showerror("Error", tk_e)

    def on_click_chose_widget(self, e, root):
        x, y = root.winfo_pointerxy()
        widget = root.winfo_containing(x, y)
        widget.focus_set()
        self.focus_widget = widget


class Attribute(WidgetMethod):
    def __init__(self, root):
        self.root = root

    def Editor(self, e):
        self.widget = e.widget
        self.destroyed = False
        AEW = tk.Toplevel(self.root)
        AEW.config(bg="white")
        AEW.title("Attributes")
        AEW.resizable(0, 0)
        AEW.overrideredirect(1)

        Editor_frame = tk.LabelFrame(AEW, text="Edit Widget", bg="white")

        self.ShowAttributes(AEW)
        Editor_frame.pack(expand=1, fill=tk.X)

        def delete():
            self.destroyed = True
            self.widget.destroy()
            AEW.destroy()

            return

        delete_btn = ttk.Button(AEW, text="Delete this widget?", command=delete)
        delete_btn.pack()
        Result = self.take_attributes(
            label="Edit Attributes: ",
            title="Create Widget",
            mroot=AEW,
            root=Editor_frame,
            wait=1,
            anc=0,
            entry_bg="#343a40",
            entry_fg="white",
        )
        if not self.destroyed:
            self.Update_widget(widget_name=self.widget, update_options=Result)

    def ShowAttributes(self, root):
        Attribute_frame = tk.LabelFrame(root, text="Attributes Values", bg="white")
        Attribute_frame.pack()

        attri_container = lb(Attribute_frame, width=50, height=30, bg="white")
        attri_container.pack()

        attribute_list = [i for i in self.widget.keys()]
        attribute_value_list = [self.widget.cget(i) for i in attribute_list]
        attribute = list(zip(attribute_list, attribute_value_list))
        attri_container.insert(tk.END, f"widget_name: {self.widget}")
        for key, value in attribute:
            attri_container.insert(tk.END, f"{key}: {value}")
        try:
            for key, value in self.widget.place_info().items():
                attri_container.insert(tk.END, f"{key}: {value}")
        except Exception as e:
            print(e)


class WidgetManager(WidgetMethod):
    def __init__(self, root) -> None:
        self.Tk_Widget_dict = {
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
        self.Ttk_Widget_dict = {
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
        self.root = root

    def _Create_Tk_Buttons(self):
        self.C_TK_B_toplevel = tk.Toplevel()
        self.C_TK_B_toplevel.config(bg="white")
        self.C_TK_B_toplevel.overrideredirect(1)
        self.C_TK_B_toplevel.resizable(0, 0)
        for key, value in self.Tk_Widget_dict.items():
            tk.Button(
                self.C_TK_B_toplevel,
                text=key,
                bg="#008cba",
                fg="white",
                border=0,
                width=20,
                command=lambda widget_name=value: self.Create(
                    widget_name=widget_name,
                    root=self.root,
                    destroy_toplevel=self.C_TK_B_toplevel,
                ),
            ).pack(pady=7, padx=15)

    def _Create_Ttk_Buttons(self):
        self.C_TtK_B_toplevel = tk.Toplevel()
        self.C_TtK_B_toplevel.config(bg="white")
        self.C_TtK_B_toplevel.overrideredirect(1)
        self.C_TtK_B_toplevel.resizable(0, 0)
        for key, value in self.Ttk_Widget_dict.items():
            tk.Button(
                self.C_TtK_B_toplevel,
                text=key,
                bg="#008cba",
                fg="white",
                border=0,
                width=20,
                command=lambda widget_name=value: self.Create(
                    widget_name=widget_name,
                    root=self.root,
                    destroy_toplevel=self.C_TtK_B_toplevel,
                ),
            ).pack(pady=7, padx=15)

    def Create_buttons_WINDOW(self):
        CBW = tk.Toplevel(self.root)
        CBW.title("Create Widgets")
        CBW.config(bg="white")
        CBW.resizable(0, 0)
        Create_Tk_widget_btn = ttk.Button(
            CBW, text="Create Tk Widget", command=self._Create_Tk_Buttons
        )
        Create_Tk_widget_btn.pack(side="left", padx=10, pady=5)

        Create_Ttk_widget_btn = ttk.Button(
            CBW, text="Create Ttk Widget", command=self._Create_Ttk_Buttons
        )
        Create_Ttk_widget_btn.pack(padx=10, side="right", pady=5)

        Execute_code_btn = ttk.Button(CBW, text="Execute code", command=self.Code_exec)
        Execute_code_btn.pack(padx=10, pady=5)

        # Image_button_frame = ttk.LabelFrame(
        #     CBW, text="Images", style="ButtonFrame.TLabelframe"
        # )

        # Image_button_frame.pack(padx=10, pady=5, fill=tk.X)

    def Code_exec(self):
        CE = tk.Toplevel(self.root)
        CE.title("Execute code")
        CE.config(bg="white")
        CE.resizable(0, 0)
        code_from_user = tk.Text(CE)
        code_from_user.pack()
        code_from_user.insert(
            0.0,
            'Use root.nametowidget to access the widget, and use "name" option which is available in all widget to name the widget.',
        )

        def executeion():
            exec(code_from_user.get(0.0, tk.END))
            self.root.update()

        Execute_btn = ttk.Button(
            CE,
            text="Execute",
            command=executeion,
        )
        Execute_btn.pack(ipadx=10, ipady=5)

    def main(self):
        self.Create_buttons_WINDOW()
        att = Attribute(root=self.root)
        self.root.bind("<Button-3>", att.Editor)
        self.root.bind("<Button-2>", lambda e: self.Create_buttons_WINDOW())


if __name__ == "__main__":
    root = tk.Tk()
    root.config(bg="white")
    root.title("Main")
    wc = WidgetManager(root=root)
    wc.main()
    root.mainloop()
