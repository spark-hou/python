from urllib import request as rq
import tkinter as tk
from tkinter import ttk
import provider as pr
import json
import os
import operator


price = rq.urlopen('https://api.binance.com/api/v3/ticker/price')

httpVal = price.read()
# 转码
httpVal = httpVal.decode('utf-8')
# json转数组
httpVal = json.loads(httpVal)
# print(pr.typeof(httpVal), httpVal)


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
# 当前价格对象
nowPrice = {}
# 历史价格
historyPrice = {}
# 组合之后的价格列表
changeData = []
# 拼接当前价格
for i in httpVal:
    length = len(i['symbol'])
    # print(i, length, i['symbol'][(length-3):])
    if i['symbol'][(length-3):] == "BTC":
        nowPrice[i['symbol'][:(length-3)]] = i['price']
# nowPrice{}拼接完成
print("当前文件夹路径", os.path.abspath(__file__))
pathLen = len(os.path.abspath(__file__))
nowPath = os.path.abspath(__file__)[:(pathLen-9)]
# 历史价格路径
pricePath = nowPath+"\historyPrice.txt"
print(nowPath, pricePath)

if os.path.exists(pricePath):
    with open(pricePath, mode='r', encoding='utf-8') as f:
        historyPrice = json.loads(f.read())
        print("历史价格获取成功")

else:
    with open(pricePath, mode='w', encoding='utf-8') as ff:
        print("文件创建成功！")
        # 写入当前价格为历史价格
        ff.write(json.dumps(nowPrice))
# 拼接列表
for i in httpVal:
    length = len(i['symbol'])
    # print(i, length, i['symbol'][(length-3):])
    if i['symbol'][(length-3):] == "BTC":
        obj = {}
        obj['symbol'] = i['symbol'][:(length-3)]
        obj['nowPrice'] = i['price']
        if i['symbol'][:(length-3)] in historyPrice:
            obj['startPrice'] = historyPrice[i['symbol'][:(length-3)]]
        else:
            obj['startPrice'] = i['price']
        obj['rate'] = float(obj['nowPrice'])/float(obj['startPrice'])
        changeData.append(obj)
# 根据rate排序
sort_changeData = sorted(changeData, key=operator.itemgetter('rate'))
# 添加数据
count = 1
for i in sort_changeData:
    tree.insert("", count, values=(
        count, i['symbol'], i['startPrice'], i['nowPrice'], i['rate']))
    count += 1
# 每次运行完写入更新后的价格
runTimePrice = {}
for key in nowPrice:
    if key in historyPrice:
        runTimePrice[key] = historyPrice[key]
    else:
        runTimePrice[key] = nowPrice[key]
with open(pricePath, mode='w', encoding='utf-8') as f:
    print("写入更新后的价格为历史价格")
    f.write(json.dumps(runTimePrice))

win.mainloop()
