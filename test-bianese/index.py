from urllib import request as rq
import tkinter as tk
from tkinter import ttk


# price = rq.urlopen('https://api.binance.com/api/v3/ticker/price')

# httpVal=price.read()

# 创建主窗口
win = tk.Tk()
# 设置标题
win.title("binanceTool")
# 设置大小和位置
win.geometry("800x400+200+50")

# 表格
# 定义列
columns = ("index", "coinName", "startPrice", "nowPrice", "rate")
tree = ttk.Treeview(win, show="headings", columns=columns)
tree.grid(row=0, column=0, sticky=tk.NSEW)

# 设置列，列还不显示
for i in columns:
    tree.column(i, width=100)

# 设置表头
for i in columns:
    tree.heading(i, text=i)

# 创建滚动条
scroll = ttk.Scrollbar(win, command=tree.yview)

# side放到窗体的哪一侧,  fill填充
scroll.grid(row=0, column=1, sticky=tk.NS)
# 关联
tree.config(yscrollcommand=scroll.set)

# 添加数据
for i in range(0, 100):
    tree.insert("", i, values=(i, "小郑", "34", "177cm", "70kg"))

win.mainloop()
