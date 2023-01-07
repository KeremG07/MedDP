import sys
if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
else:
    # Python 3
    import tkinter as tk

query_list = ["Query 1", "Query 2", "Query 3"]

root = tk.Tk()
root.resizable(False, False)
root.geometry('318x480')
root.title("MedDP")

variable = tk.StringVar(root)
variable.set(query_list[0]) # default value

query_dropdown = tk.OptionMenu(root, variable, *query_list)
query_dropdown.pack()

button = tk.Button(root, text="OK", command=lambda: query_result_label.config(text=variable.get()))
button.pack()

query_result_label = tk.Label(root)
query_result_label.pack()

root.mainloop()