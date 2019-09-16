
import tkinter as tk
from setting import *
import hashlib as hb
import random as rm


"""
    说明：本游戏基于python的tkinter模块实现，非常简单的界面布局；
        整个游戏分为四个窗口，一个进入游戏的窗口、一个选关窗口、
        一个游戏进行窗口和一个游戏结束的窗口。

    游戏规则：玩家点击按钮进入游戏窗口后，通过点击屏幕下方的按键输入问题的答案，
        答案正确则会生成进入下一关的按钮，否则无法进入下一关。

    游戏扩展：1.目前游戏暂定30关，玩家可自由地添加关数，无需修改任何代码；
            2.在setting模块中按照三个字典的格式直接往里添加新的关数的数据即可，在if __name__ == "__main__"中
              有str1和str2两个变量用来对答案加密和对键盘上的字进行乱序操作。

    实现的功能：1.对答案都使用了md5算法加密；源码中无明文答案；
              2.支持自由选关的操作；
              3.支持返回上一关的操作；
              4.支持答案提示操作，提示最多为一个字；
              5.自动永久记录已经回答正确的问题，其选关按钮会由红色变成绿色；如果想要重置，运行
                mygame模块if __name__ == "__main__"中注释的代码或直接修改player_answers.txt文件，
                将里面所有的数据置为0.

    缺陷或bug：1.点击按钮将答案输入显示，每个答案点击按钮都通过了自定义一个类来实现，原因是无法找到简单的方法
                记录回调函数的传参，不知大家有没有好的建议；同理选关按钮也是一样。

    修改记录：1.增加了选关界面；
            2.修改了答案和问题等数据资源的配置方式，拆分为3个字典；
            3.修改了四个界面的控制方式，集中到一个函数中进行管理。

    修改的优点：1.可以自由选择关数，增加可玩性；
              2.3个字典虽然增加了代码量，但是数据更加有条理和直观，方便扩展；
              3.所有界面集中一个函数管理，后续如果再扩展增加新的界面很方便。
"""

__author__ = {'author': 'caiwanpeng',
              'Email': '626004181@qq.com',
              'Blog': 'http://www.cnblogs.com/cwp-bg/',
              'Created': '2017-09-25',
              'Version': '1.1'}


class ButtonSelect(object):
    """创建选择关卡的按钮"""

    def __init__(self, win, num, game_screen, elements, player_answer):
        self.win = win
        self.name = tk.StringVar(self.win)
        self.sum_sc = len(dict_problems)
        self.num_sc = num
        self.start_game = game_screen
        self.eles = elements
        self.player_answer = player_answer

    def set_name(self, value):
        """设置按钮的数值"""
        self.name.set(value)

    def set_bg(self):
        """设置按钮的背景色"""
        if self.player_answer == "1":
            return "green"
        return "red"

    def create_button(self, place=(0, 0)):
        """创建按钮"""
        button = tk.Button(self.win, textvariable=self.name,
                           command=self._select_sc,
                           bg=self.set_bg(), fg="black",
                           activebackground="orange",
                           font=("宋体", 16, "bold"))
        button.place(width=40, height=40,
                     relx=0.1 + place[0] * 0.8,
                     rely=0.1 + place[1] * 0.9)
        return button

    def _select_sc(self):
        """选择按钮响应函数"""
        #  改变窗口记录的关数值
        self.num_sc[0] = int(self.name.get())
        #  清除界面所有的元素
        try:
            for ele in self.eles:
                ele.destroy()  # 删除所有的元素
        except Exception as re:
            print(re)
        self.eles.clear()  # 清空记录
        #  加载游戏窗口
        self.start_game()


class ButtonNew(object):
    """创建键盘按钮"""

    def __init__(self, wins, v1, v2, result, screen_num, bg='red',
                 fg="green", height=1, width=3,
                 font=("宋体", 20, "bold")):
        self.win = wins
        self.v1 = v1
        self.v2 = v2
        self.v_name = tk.StringVar(self.win)  # 一个显示按钮文字的标签
        self.results = result
        self.screen_num = screen_num  # 获得目前的关卡数
        # 相关属性
        self.bg = bg
        self.fg = fg
        self.height = height
        self.width = width
        self.font = font

    def create_button(self, place_b=(0, 0)):
        """键盘按钮"""
        # 创建按钮，按钮上的标签内容，command点击按钮执行函数，bg背景颜色，fg标签颜色
        key_answer = tk.Button(self.win, textvariable=self.v_name,
                               command=lambda: self._button_event(self.v_name.get()),
                               activebackground="blue",
                               bg=self.bg, fg=self.fg,
                               height=self.height,
                               width=self.width, font=self.font)
        # 设置按钮的位置
        key_answer.place(x=place_b[0], y=place_b[1])
        return key_answer

    def _button_event(self, name1):
        """创建一个点击按钮响应的函数"""
        # 先清空v2标签
        self.v2.set("")
        if len(self.v1.get()) < 4:  # 小于成语的长度
            self.results.append(name1)
        else:
            self.results.clear()

        result = ""
        for i in self.results:  # 拼接字符串
            result += i
        self.v1.set(result)

        # 判断答案是否正确
        if abt.the_answer is True:
            abt.the_answer = False
        password = dict_result[str(self.screen_num[0])]
        if len(self.results) >= 4 and self.get_md5(result) == password:
            abt.the_answer = True  # 将答案开关设置为正确
            # print(abt.the_answer)

    @staticmethod
    def get_md5(str1):
        """对st1字符串MD5加密"""
        return hb.md5(str1.encode("utf-8")).hexdigest()


class GameWindow(object):
    """创建游戏运行窗口并加载相关的控件"""

    def __init__(self):
        """初始化窗口"""
        # 创建一个根窗口
        self.win = tk.Tk()
        self.win.title("史上最污猜成语")  # 标题
        self.win.geometry("500x500+500+100")  # 设置尺寸
        self.win.resizable(width=False, height=False)  # 宽高不可变
        self.v1 = tk.StringVar(self.win)  # 显示答案的标签
        self.v2 = tk.StringVar(self.win)  # 答案是否正确的标签
        self.v_screen = tk.StringVar(self.win)  # 显示下一关的标签
        self.v_problems = tk.StringVar(self.win)  # 一个显示问题的可变标签
        self.results = []  # 创建一个记录答案长度的变量
        self.eles = []  # 创建一个记录界面元素的列表
        self.list_button = []  # 存放键盘可变文字对象
        self.screen_num = [1]  # 记录当前是第几关,使用可变类型将地址引用
        self.sum_screen = len(dict_problems)  # 获取当前的总关卡数
        self.player_answers = self.player_answer()  # 记录目前已回答的关数的情况

    def create_label(self):
        """创建窗口所有的标签"""
        # 标签显示第几关
        dir1 = tk.Label(self.win, bg="yellow", textvariable=self.v_screen,
                        fg="blue", font=("宋体", 20, "bold"))
        dir1.pack(side=tk.TOP, fill=tk.X)
        self.eles.append(dir1)
        # 创建一个标签"答案"
        dir2 = tk.Label(self.win, bg="red", text="答案:",
                        font=("宋体", 20, "bold"))
        dir2.place(x=0, y=200)  # 位置坐标控制
        self.eles.append(dir2)
        # 创建一个换行标签
        dir3 = tk.Label(self.win, bg="#00F000", textvariable=self.v_problems,
                        wraplength=400, justify="left",
                        fg="blue", font=("宋体", 20, "bold"), height=4)
        dir3.pack(fill=tk.X)
        self.eles.append(dir3)
        # 一个空白的标签等待用户输入答案
        dir4 = tk.Label(self.win, bg="green", textvariable=self.v1,
                        font=("宋体", 20, "bold"))
        dir4.place(x=100, y=200)
        self.eles.append(dir4)
        # 一个空白标签显示答案错误时
        dir5 = tk.Label(self.win, textvariable=self.v2, fg="red",
                        font=("宋体", 12, "bold"))
        dir5.place(x=100, y=240)
        self.eles.append(dir5)

    def create_button(self):
        """创建游戏窗口所有的按钮"""
        # 采用嵌套循环创建4*8个按钮
        for j in range(4):
            for g in range(8):
                button1 = ButtonNew(self.win, v1=self.v1,
                                    v2=self.v2, result=self.results,
                                    screen_num=self.screen_num)
                # 设置按钮的位置
                key_b = button1.create_button(place_b=(30 + g * 54, 280 + j * 45))
                self.list_button.append(button1.v_name)  # 将每一个标签加入列表
                self.eles.append(key_b)  # 所有的按钮加入列表
        self._set_key(self.screen_num[0])  # 设置相应关数的值

        # 创建一个用来清除答案的按钮
        cls = tk.Button(self.win, text="清除", command=self._cls_function,
                        bg="black", fg="white", font=("宋体", 16, "bold"))
        cls.place(x=250, y=200)
        self.eles.append(cls)
        # 创建一个用来提示答案的按钮
        pmt = tk.Button(self.win, text="提示",
                        command=lambda: self._prompt_button(self.screen_num[0]),
                        bg="red", fg="white", font=("宋体", 16, "bold"))
        pmt.place(x=320, y=200)
        self.eles.append(pmt)
        # 创建一个用来确定答案的按钮
        istrue = tk.Button(self.win, text="确定", command=self._ensure_button,
                           bg="red", fg="white", font=("宋体", 16, "bold"))
        istrue.place(x=390, y=200)
        self.eles.append(istrue)
        # 创建一个返回上一关的按钮
        last_sc = tk.Button(self.win, text="上一关", command=self._last_sc_button,
                            bg="red", fg="white", font=("宋体", 16, "bold"))
        last_sc.place(x=250, y=155)
        self.eles.append(last_sc)
        # 创建一个返回选关窗口的按钮
        return_button = tk.Button(self.win, text="返回选关", command=self._return_lock,
                                  bg="red", fg="white", font=("宋体", 16, "bold"))
        return_button.place(x=10, y=155)
        self.eles.append(return_button)

    def before_screen(self):
        """创建一个进入游戏的窗口所有元素"""
        # 空白标签
        label1 = self.the_label()
        # 标签显示"史上最污猜成语"
        label2 = self.the_label("史上最污猜成语")
        # 空白标签
        label3 = self.the_label()
        # 显示淡绿色背景
        label4 = self.the_label(font=("宋体", 250, "bold"), bg="#00ee00")
        # 显示作者“天宇之游”
        dirx = tk.Label(self.win, bg="#00ee00", text="----天宇之游",
                        fg="blue", font=("宋体", 20, "bold"))
        dirx.place(x=250, y=200)
        list_labels = [label1, label2, label3, label4, dirx]
        # 创建一个进入游戏的按钮
        go_game = tk.Button(self.win, text="开启污旅程",
                            command=lambda: self._start_game(go_game, *list_labels),
                            bg="red", fg="white", activebackground="yellow",
                            activeforeground="red", font=("宋体", 30, "bold"))
        go_game.place(x=130, y=300)

    def lock_screen(self):
        """创建一个展示所有的关卡及关卡解锁的窗口"""
        # 空白区域
        dir_k = tk.Label(self.win, bg="#3b9dff", font=("宋体", 20, "bold"))
        dir_k.pack(fill=tk.X)
        self.eles.append(dir_k)
        # 显示相关信息
        dir1 = tk.Message(self.win, bg="blue", text="选择关卡",
                          fg="red", font=("宋体", 20, "bold"),
                          width=200)
        dir1.pack(fill=tk.X)
        self.eles.append(dir1)
        # 创建一块画布,所有的元素都放置在画布上
        cans = tk.Canvas(self.win,  # 根窗口
                         bg="#92dba0",  # 设置画布的颜色
                         height=500,
                         borderwidth=0)
        cans.pack(fill=tk.X)
        self.eles.append(cans)  # 添加到列表便于删除

        for i in range(self.sum_screen):  # 按照已有的关卡数生成相应的按钮数量
            j = i % 10 / 10.0
            k = i // 10 / 10
            # 传入当前的关数和加载游戏窗口的函数
            bn_st = ButtonSelect(cans, self.screen_num,
                                 self._game_go, self.eles,
                                 self.player_answers[i])
            bn_st.create_button(place=(j, k))
            bn_st.set_name(str(i + 1))

    def after_screen(self):
        """一个游戏结束的画面窗口"""
        self.the_label()  # 空白标签
        text1 = "恭喜你！"
        text2 = "成功晋升为老司机！"
        # 标签显示结束语
        self.the_label(text1)
        self.the_label(text2)
        self.the_label()  # 空白标签
        # 创建一个结束的按钮
        go_game = tk.Button(self.win, text="再见！",
                            command=lambda: exit(),
                            bg="red", fg="white",
                            activebackground="yellow",
                            activeforeground="red",
                            font=("宋体", 30, "bold"))
        go_game.place(x=170, y=300)

    def the_label(self, text=None, side=tk.TOP,
                  font=("宋体", 40, "bold"), bg="green"):
        """创建显示标签"""
        dir1 = tk.Label(self.win, bg=bg, text=text,
                        fg="black", font=font)
        dir1.pack(side=side, fill=tk.X)
        return dir1

    def _return_lock(self):
        """返回选择关卡的界面"""
        # 清空标签
        self.list_button.clear()
        # 清除界面的所有元素
        self.clear_screen()
        # 清空元素记录列表
        self.eles.clear()
        # 将关数记录还原到1
        self.screen_num[0] = 1
        # 调用界面创建函数
        self.screen_control(1)

    def clear_screen(self):
        """清除界面所有元素的函数"""
        try:
            for ele in self.eles:
                ele.destroy()  # 删除所有的元素
        except Exception as re:
            print(re)

    def _set_key(self, num):
        """设置所有的按键变量的值"""
        listx = rm.sample(dict_key[str(num)], len(dict_key[str(num)]))  # 打乱顺序
        #  设置所有的键盘上的文字
        for j, k in enumerate(self.list_button):
            k.set(listx[j])  # 获取文字设置按键值

    def _next_screen(self):
        """当答案正确时生成下一关的按钮"""
        # 创建一个用来确定答案的按钮
        next_b = tk.Button(self.win, text="下一关", command=lambda: self._next_button(next_b),
                           bg="red", fg="white",
                           font=("宋体", 16, "bold"))
        next_b.place(x=390, y=155)
        return next_b

    def _next_button(self, next_b):
        """当点击下一关按钮时响应函数"""
        try:
            # 判断是否已经是最后一关
            if self.screen_num[0] >= len(dict_problems):
                # print("这已经是最后一关")
                # 清除界面所有的元素
                self.clear_screen()
                # 加载游戏结束的界面
                self.screen_control(3)
            else:
                if abt.the_answer is True:
                    self.__update_screen()  # 更新窗口
                else:
                    self.v2.set("答案错误！")

            # 将上一关的选关按钮变为绿色
            self.player_answers[self.screen_num[0] - 2] = "1"
            # 同时将当前的数据同步到文件
            file = open("./player_answers.txt", "w")
            file.write("".join(self.player_answers))  # 转化成字符串
        except Exception as re:
            print(re)
        else:
            # 删除按钮本身
            next_b.destroy()
        finally:
            file.close()

    def _last_sc_button(self):
        """上一关按钮的响应函数"""
        # 判断目前是不是第一关
        if self.screen_num[0] == 1:
            self.v2.set("这是第一关！")
        else:
            self.screen_num[0] -= 2  # 减少一关
            self.__update_screen()

    def __update_screen(self):
        """更新窗口的的函数"""
        # 显示问题
        self.v_problems.set(dict_problems[str(self.screen_num[0] + 1)])
        self.screen_num[0] += 1  # 指针指向下一关
        # 改变关数的标签
        self.v_screen.set("第" + str(self.screen_num[0]) + "关")
        # 更新所有的按键值
        self._set_key(self.screen_num[0])
        # 清除v1和v2标签的内容
        self._cls_function()
        self.v2.set("")
        # print("成功执行！")

    def _start_game(self, *args):
        """进入游戏的响应函数"""
        try:
            for ele in args:
                ele.destroy()  # 删除所有的元素
        except Exception as re:
            print(re)
        self.screen_control(num=1)  # 进入选关界面

    def _game_go(self):
        str_num = str(self.screen_num[0])
        self.v_screen.set("第" + str_num + "关")  # 设置第几关标签
        self.v_problems.set(dict_problems[str_num])  # 设置问题
        self.screen_control(2)  # 进入游戏界面

    def _cls_function(self):
        """清除按钮响应事件函数"""
        self.results.clear()
        self.v1.set("")  # 清空标签

    def _ensure_button(self):
        """确定开关的事件函数"""
        if abt.the_answer is True:
            self.v2.set("答案正确！")
            self._next_screen()  # 在窗口创建一个按钮
        else:
            self.v2.set("答案错误！")

    def _prompt_button(self, key):
        """提示开关的事件函数"""
        if abt.the_answer is True:  # 将可能打开的开关关闭
            abt.the_answer = False
        self.results.clear()  # 先清空原来的答案
        self.results.append(list_answer[int(key)])  # 加入提示
        self.v1.set(list_answer[int(key)])  # 设置提示答案

    def screen_control(self, num=0):
        """创建一个窗口控件显示的控制函数"""
        if num == 0:
            self.before_screen()  # 开始显示游戏进入界面
        elif num == 1:
            self.lock_screen()  # 进入选关界面
        elif num == 2:
            self.create_label()  # 传入所有可变的参数创建所有的标签
            self.create_button()  # 传入空白标签对象创建所有的按钮
        elif num == 3:
            self.after_screen()  # 进入游戏结束界面

    def run(self):
        self.win.mainloop()  # 窗口运行

    def player_answer(self):
        """更新记录的玩家回答的状态"""
        # 获取目前的总关数
        number1 = self.sum_screen
        try:
            # 读取文件中的关数信息，如果数目不变则不更新文件，改变则初始化文件
            f = open("./player_answers.txt", "r")
            str3 = f.read()
            # print(str3)
        except Exception as re:
            print(re)
        finally:
            f.close()

        if number1 == len(str3):
            return list(iter(str3))
        else:  # 初始化
            str2 = "0" * number1
            try:
                f1 = open("./player_answers.txt", "w")
                f1.write(str2)  # 更新信息
            except Exception as re:
                print(re)
            finally:
                f1.close()
            return list(iter(str2))


win = GameWindow()
sc = win.screen_control
bs = win.before_screen
as_ = win.after_screen
ls = win.lock_screen
run = win.run


def main():
    sc()
    run()  # 游戏运行


if __name__ == "__main__":
    main()
    # 初始化记录文件
    # str2 = "0"*len(dict_key)
    # f1 = open("./player_answers.txt", "w")
    # f1.write(str2)  # 更新信息
    # f1.close()
