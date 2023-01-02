import sys
if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
else:
    # Python 3
    import tkinter as tk

root = tk.Tk()
#root.resizable(False, False)
#root.geometry('800x600')
root.title("MedDP")

tk.Button(root, text="Placeholder Button").pack()
tk.mainloop()