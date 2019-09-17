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
win.geometry("800x800+200+50")

# 表格
# 定义列
columns = ("coinName", "startPrice", "nowPrice", "rate")
tree = ttk.Treeview(win, columns=columns)
tree.pack()


# 设置列，列还不显示
tree.column("coinName", width=100)
tree.column("startPrice", width=100)
tree.column("nowPrice", width=100)
tree.column("rate", width=100)

# 设置表头
for i in columns:
    tree.heading(i, text=i)


# 添加数据
tree.insert("", 0, values=("小郑", "34", "177cm", "70kg"))
tree.insert("", 0, values=("小张", "43", "188cm", "90kg"))

win.mainloop()
