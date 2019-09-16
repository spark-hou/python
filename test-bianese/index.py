import tkinter as tk

root = tk.Tk()
li = ["C", "python", "php", "html", "SQL", "java"]
listb = tk.Listbox(root)

for item in li:  # 第一个小部件插入数据
    listb.insert(0, item)


listb.pack()

root.mainloop()
