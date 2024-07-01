import tkinter as tk

root = tk.Tk()

frame = tk.Frame(root)
frame.pack(expand=True, anchor='center')

label1 = tk.Label(frame, text="Label 1")
label1.pack(side=tk.LEFT)

label2 = tk.Label(frame, text="Label 2")
label2.pack(side=tk.LEFT)

root.mainloop()
