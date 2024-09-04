import tkinter as tk
from tkinter.ttk import Separator, Style

class NumberedText(tk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)

        self.config(bg='red')
        style = Style(self)
        self.configure(bg="white")
        style.configure("TSeparator", relief="flat")
        
        self.uniscrollbar = tk.Scrollbar(self, relief="flat") # Scrollbar for listbox and text y-axis
        self.uniscrollbar.pack(side="right", fill="y")

        self.xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL,  relief="flat")
        self.xscrollbar.pack(side="bottom", fill="x")
        
        self.scroll_text()

        separator = Separator(self, orient='vertical')
        separator.pack(side="right", fill="y", padx=2)

        self.number_widget()
        
        self.textarea.config(spacing1=0, spacing2=0, spacing3=1)

        self.textarea.bind("<Control-BackSpace>", lambda e: self.wordDelete(e, "1.0", backword=1, forward=0))
        self.textarea.bind("<Control-Delete>", lambda e: self.wordDelete(e, "end", backword=0, forward=1))
        
    def scroll_text(self):
        self.textarea = tk.Text(self, relief="flat", font="times 15", wrap="none", undo=1)

        self.uniscrollbar.config(command= self.scroll_both)
        self.xscrollbar.config(command=self.textarea.xview)
        self.textarea.config(xscrollcommand= self.xscrollbar.set, yscrollcommand = self.update_scroll_both)

        self.textarea.pack(side="right", fill="both", expand=1)
    
    def number_widget(self):
        self.linenumber = LineNumbers(self, self.textarea, relief="flat", state="disabled")

        self.uniscrollbar["command"] = self.scroll_both
        self.linenumber["yscrollcommand"] = self.update_scroll_both

        self.linenumber.pack(side="right", fill="y")
        
    def mouse_wheel(self, event):
        self.scrolltext.yview_scroll(int(-1*(event.delta/120)), "units")
        self.number_widget.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def scroll_both(self, action, position):
        self.textarea.yview_moveto(position)
        self.linenumber.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.textarea.yview_moveto(first)
        self.linenumber.yview_moveto(first)
        self.uniscrollbar.set(first, last)
    
    def wordDelete(self, event, stopindex:str, backword:bool, forward:bool):
        wordStart = self.textarea.search(pattern=r"\s", regexp=1, index="insert", stopindex=stopindex, backwards=backword, forwards=forward)
        if wordStart is None or wordStart == "": return

        if backword and not forward:
            self.textarea.delete(wordStart, "insert")
            return "break"
        else:
            self.textarea.delete("insert", wordStart)
        

class LineNumbers(tk.Listbox):
    def __init__(self, master, textwidget, **options):
        super().__init__(master, **options)

        self.textwidget = textwidget

        self.textwidget.bind("<Return>", self.update_num_list)
        self.textwidget.bind("<KeyRelease-BackSpace>", self.update_num_list)
        self.textwidget.bind("<KeyRelease-Delete>", self.update_num_list)
        self.textwidget.bind("<<Modified>>", self.update_num_list)

        self.number_var = tk.Variable(self, value=["1"])

        self.configure(listvariable=self.number_var, selectmode=tk.SINGLE)
        self.set_width(1)
        self.set_font()

    def set_font(self):
        font = self.textwidget.cget("font")
        self.configure(font = font)

    def set_width(self, num_len):
        self.configure(width=num_len+1)

    def update_num_list(self, event):
        linenums = self.get_num_lines()

        number_list = list(range(1, linenums+1)) if event.keysym == "Return" else list(range(1, linenums))

        self.set_width(len(str(linenums)))
        self.number_var.set(number_list)
        self.yview("end")
        
    def get_num_lines(self):
        num_lines = int(self.textwidget.index("end").split(".")[0])
        return (num_lines)

    def get_current_colomn(self):
        curr_column = int(self.textwidget.index("insert").split(".")[1])
        return (curr_column)

    def get_current_row(self):
        curr_row = int(self.textwidget.index("insert").split(".")[0])
        return (curr_row)

def test(master):
    r = tk.Frame(master)
    tk.Label(r, text="Listbox Implementation").pack()
    a=NumberedText(r)
    a.pack()
    return r


def demo():
    root = tk.Tk()
    root.title("NumberedText Demo")
    NumberedText.test(root).pack(side="left")
    root.mainloop()

if __name__ == "__main__":
    demo()