import tkinter as tk
import tkinter.ttk as ttk

class PopupEntry(tk.Entry):
    """
    Provides a temporary tk.Entry widget which can be used to show a temporaty entry widget to retrive data from user.
    After retriving data, it returns the value back and gets destroyed.

    Used internaly by EditableTreeview.

    """

    def __init__(
        self,
        parent,
        x,
        y,
        textvar,
        width,
        height,
        entry_value="",
        text_justify="left",
        **options
    ):
        super().__init__(
            parent,
            relief="flat",
            justify=text_justify,
            bg="white",
            textvariable=textvar,
            font="Times 10 ",
            **options
        )
        self.place(x=x + 1, y=y, width=width, height=height)

        self.textvar = textvar
        self.textvar.set(entry_value)
        self.focus_set()
        self.select_range(0, "end")
        # move cursor to the end
        self.icursor("end")

        self.wait_var = tk.StringVar(master=self)

        self._bind_widget()
        self.wait_window()

    def _bind_widget(self):
        self.bind("<Return>", self.retrive_value)
        self.bind("<FocusOut>", self.retrive_value)

    def retrive_value(self, e):
        value = self.textvar.get()
        self.destroy()
        self.textvar.set(value)

class EditableTreeview(ttk.Treeview):
    """Customized Treeview with editing feature

    All treeview attributes are valid"""

    def __init__(
        self,
        parent,
        columns,
        show,
        data: dict,
        bind_key="<Double-Button-1>",
        non_editable_columns="",
        readonly_entry_wid = "normal",
        **treeview_options
    ):
        super().__init__(parent,columns=columns, show=show, **treeview_options)
        self.parent = parent
        self.column_name = columns
        self.data = data
        self.bind_key = bind_key
        self.non_editable_columns = non_editable_columns
        self.readonly = readonly_entry_wid

        self.set_primary_key_column_attributes()
        self.set_headings()
        self.insert_data()
        self.set_edit_bind_key()

    def set_primary_key_column_attributes(self):
        self.column("#0", width=100, stretch=1)

    def set_headings(self):
        for i in self.column_name:
            self.heading(column=i, text=i)

    def insert_data(self):
        for values in self.data.items():
            self.insert("", tk.END, values=values)
        

    def set_edit_bind_key(self):
        self.bind("<Double Button-1>", self.edit)

    def get_absolute_x_cord(self):
        rootx = self.winfo_pointerx()
        widgetx = self.winfo_rootx()

        x = rootx - widgetx

        return x

    def get_absolute_y_cord(self):
        rooty = self.winfo_pointery()
        widgety = self.winfo_rooty()

        y = rooty - widgety
        return y

    def get_current_column(self):
        pointer = self.get_absolute_x_cord()
        return self.identify_column(pointer)

    def get_cell_cords(self, row, column):
        return self.bbox(row, column=column)

    def get_selected_cell_cords(self):
        row = self.focus()
        column = self.get_current_column()
        return self.get_cell_cords(row=row, column=column)

    def update_row(self, values, current_row, currentindex):
        self.delete(current_row)
        self.insert("", currentindex, values=values)

    def check_region(self):
        result = self.identify_region(
            x=(self.winfo_pointerx() - self.winfo_rootx()),
            y=(self.winfo_pointery() - self.winfo_rooty()),
        )
        if result == "cell":
            return True
        else:
            return False

    def check_non_editable(self):
        if self.get_current_column() in self.non_editable_columns:
            return False
        else:
            return True

    def edit(self, e):
        if self.check_region() == False:
            return
        elif self.check_non_editable() == False:
            return

        current_row = self.focus()
        currentindex = self.index(self.focus())
        current_row_values = list(self.item(self.focus(), "values"))
        current_column = int(self.get_current_column().replace("#", "")) - 1
        current_cell_value = current_row_values[current_column]

        entry_cord = self.get_selected_cell_cords()
        entry_x = entry_cord[0] - 1
        entry_y = entry_cord[1] 
        entry_w = entry_cord[2]
        entry_h = entry_cord[3] 

        entry_var = tk.StringVar()

        PopupEntry(
            self,
            x=entry_x,
            y=entry_y,
            width=entry_w,
            height=entry_h,
            entry_value=current_cell_value,
            textvar=entry_var,
            text_justify="left",
            state = self.readonly

        )

        if entry_var.get() != current_cell_value:
            current_row_values[current_column] = entry_var.get()
            self.update_row(
                values=current_row_values,
                current_row=current_row,
                currentindex=currentindex,
            )
    