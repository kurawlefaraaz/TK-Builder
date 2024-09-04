test_val = 0

if __name__ == "__main__":
    import tkinter as tk
    
    from secondary_widgets.custom_user_code_widget import demo
    demo()
if test_val == None:
    exit()
elif test_val == 0:
    from UI import Create_Update_UI
    Create_Update_UI.demo()
elif test_val == 1:
    from UI import widgetcatalog
    widgetcatalog.demo()