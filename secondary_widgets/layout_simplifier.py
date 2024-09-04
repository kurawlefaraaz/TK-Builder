
# TODO: FEATURE: Style Editor, Layout Treeview, Map Editor

import tkinter as tk
import tkinter.ttk as ttk

class LayoutSimplifier(ttk.Style): 
    def __init__(self, master, class_name):
        super().__init__(master)
        self.class_name = class_name
        self._elements = []

    def _blockify(self):
        blocks = []
        group_stack =[]
        
        inner_layout = ""
        # self._start defines the start of the layout
        self._start = self.layout(self.class_name)[0][0]
        rev_layout = reversed(str(self.layout(self.class_name)))

        # Uses Paretheises Validation Algoritm
        for char in rev_layout:
            if char in (')', ']', '}'):
                group_stack.append(char)
                continue
            
            if char in ('(', '[', '{'):
                blocks.append(f"{char}{inner_layout[::-1]}{group_stack.pop()}")
                inner_layout = ""
                continue
                
            inner_layout += char
        
        blocks = [i for i in reversed(blocks) if i != '[]']
        return blocks
    
    def simplify(self):
        blocks = self._blockify()

        # Detuplize the Element names
        for index in range(len(blocks)):
            if '(' in blocks[index]:
                vals = blocks[index].replace('(', "").replace(')', "").replace("'", "").replace(', ', "")
                blocks[index]=(vals)
        
        # Set children to Element names
        for index in range(0, len(blocks)):
            value = blocks[index]
            value = value.replace("'", '"')
            if "children" in value:
                value = value.replace('"children": ', f'"children": "{blocks[index+1]}"')
            blocks[index] = value

        # Group Element name with its attributes
        blocks = [[blocks[i], blocks[i+1]] for i in range(0, len(blocks)-1, 2)]

        # Convert Element names and its attributes from str format to its data type
        import json
        for index in range(len(blocks)):
            blocks[index][1] = json.loads(blocks[index][1])
            blocks[index] = tuple(blocks[index])
        
        blocks = tuple(blocks)
        del json

        # Map Element names with its attribute
        result = {val[0]: val[1] for val in blocks}
        
        return result
            
    def findElementOptions(self):
        import re

        str_layout = str(self.layout(self.class_name))
        matches = re.findall("[(]'(.*?)',", str_layout)
        
        self._elements = matches
        
        element_options = {match: self.element_options(match) for match in matches}
        
        return element_options

if __name__ == "__main__":
    # from pprint import pprint as print
    root = tk.Tk()
    s= ttk.Style(root)
    for i in s.theme_names():
        s.theme_use(i)
        for class_name in ("Treeview",):
            a=LayoutSimplifier(root, class_name)
            b = a.findElementOptions()
            print(b)