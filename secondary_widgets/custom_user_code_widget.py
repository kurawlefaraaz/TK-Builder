import tkinter as tk
from tkinter.filedialog import asksaveasfile as saveCodeFile, askopenfile as openCodeFile

from .numberedtext import NumberedText
from .frame_menubar import FrameMenubar

class ExecuteCodeUI(tk.LabelFrame):
    def __init__(self, master, **options) -> tk.LabelFrame:
        super().__init__(master, **options)
        ExecuteCodeUI.root = self.nametowidget(".")
        
        self.textbox = NumberedText(master=self)

        self.menu_bar()
        self.textbox.pack(padx=20, pady=5, fill="x")
    
    def menu_bar(self):
        menuFrame = FrameMenubar(self, relief= "flat")
        common_params = {"relief": "flat", "borderwidth": 0, "activebackground": "#A4D8E1", "padx": 10, "font": ("", "12")}

        menuFrame.setMenuButtonPackOptions(side="left")
        menuFrame.setMenuOptions(tearoff = 0)

        menuFrame.addMenubutton("file_menu_btn", text="Files", **common_params)
        menuFrame.getMenuRef("file_menu_btn").add_command(label="Save", command=self.save_code)
        menuFrame.getMenuRef("file_menu_btn").add_command(label="Open", command=self.open_code)

        menuFrame.addMenubutton("execute_btn", text="Execute", **common_params)
        menuFrame.getMenuRef("execute_btn").add_command(label="Execute", command=self.execute_code)

        menuFrame.pack(side="top", fill='x', padx=20)

    def execute_code(self):
        textarea_content = self.textbox.textarea.get(0.0, "end")
        exec(textarea_content,{"root": self.nametowidget(".")},{})

    def save_code(self):
        file_path = saveCodeFile()
        if file_path == None: return

        with file_path as file :
            textarea_content = self.textbox.textarea.get(0.0, "end")
            file.write(textarea_content)

    def open_code(self):
        file_path = openCodeFile()
        if file_path == None: return

        with file_path as file:
            content = file.read()
        self.textbox.textarea.delete(0.0, "end")
        self.textbox.textarea.insert(0.0, content)
        self.textbox.textarea.edit_modified(0)
    
def demo():
    root = tk.Tk()
    a=ExecuteCodeUI(root)
    a.pack()
    root.mainloop()

if __name__ == "__main__":
    demo()