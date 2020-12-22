import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

from tasks.home import startZipMisson
from method.stopThread import stop_thread

class homePage(tk.Frame):
    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        self.place(x=0, y=0, relwidth=1, relheight=1)
        # 选择的路径
        self.workpath = None
        # 标记符号列表
        self.markList = []
        # 是否压缩
        self.isZipValue = 1
        # 压缩包名字
        self.zipName = None
        # 配置读取
        self.getConfig = parent.getConfig
        # 判断压缩进程是否已结束
        self.isZipEnd = False
        self.initLayout()
        self.initData()
    
    def initLayout(self):
        self.setPathSelect()
        self.setMarkInput()
        self.setIsZipSelect()
        self.setZipNameInput()
        self.setStartButton()
        self.setStopButton()
        self.setOutputText()

    def initData(self):
        workpath = self.getConfig.getValue('homeData', 'workpath')
        mark = self.getConfig.getValue('homeData', 'mark')
        if workpath:
            self.workpath = workpath
            self.Entry_var_select.set(workpath)
        if mark:
            self.markList = mark.split(';')
            self.Entry_var_mark.set(mark)

    def saveData(self):
        self.getConfig.setValue('homeData', 'workpath', self.workpath)
        self.getConfig.setValue('homeData', 'mark', self.Entry_mark.get())

    # 路径选择
    def setPathSelect(self):
        self.Label_select = tk.Label(self, text="文件夹选择：")
        self.Label_select.place(x=80, y=20)
        self.Entry_var_select = tk.Variable()
        self.Entry_select = tk.Entry(self, textvariable=self.Entry_var_select, state='disabled')
        self.Entry_select.place(x=200, y=20, width=120, height=26)
        self.Button_select = tk.Button(self, text ="选择", command = self.setPathSelectCommand)
        self.Button_select.place(x=330, y=20, height=26)
    
    # 路径选择绑定事件
    def setPathSelectCommand(self):
        self.workpath = filedialog.askdirectory()
        if self.workpath:
            self.Entry_var_select.set(self.workpath)
    
    # 标记字符
    def setMarkInput(self):
        self.Label_mark = tk.Label(self, text="标记字符：")
        self.Label_mark.place(x=80, y=66)
        self.Entry_var_mark = tk.Variable()
        self.Entry_mark = tk.Entry(self, textvariable=self.Entry_var_mark)
        self.Entry_mark.place(x=200, y=66, width=120, height=26)
        self.Label_mark_tip = tk.Label(self, text="(多个使用 ; 隔开，仅限数字)")
        self.Label_mark_tip.place(x=330, y=66)

        def input(eventObj):
            lists = self.Entry_mark.get().split(';')
            self.markList = [var.replace(' ', '') for var in lists if var]
        self.Entry_mark.bind('<KeyRelease>', input)

    # 是否压缩
    def setIsZipSelect(self):
        self.Label_zip = tk.Label(self, text="是否压缩：")
        self.Label_zip.place(x=80, y=112)
        self.isZip = tk.IntVar()
        self.Checkbutton_zip = tk.Checkbutton(self, text = '是否生成压缩包', variable = self.isZip, command = self.setIsZipSelectCommand)
        self.Checkbutton_zip.place(x=190, y=112, width=120, height=26)
        self.Checkbutton_zip.select()
    
    # 是否压缩绑定事件
    def setIsZipSelectCommand(self):
        self.isZipValue = self.isZip.get()
        if self.isZip.get() == 0:
            self.Label_name.place_forget()
            self.Entry_name.place_forget()
        else:
            self.Label_name.place(x=80, y=158)
            self.Entry_name.place(x=200, y=158, width=120, height=26)

    # 压缩包名称
    def setZipNameInput(self):
        self.Label_name = tk.Label(self, text="压缩包名称：")
        self.Label_name.place(x=80, y=158)
        self.Entry_name = tk.Entry(self)
        self.Entry_name.place(x=200, y=158, width=120, height=26)

        def input(eventObj):
            self.zipName = self.Entry_name.get()
        self.Entry_name.bind('<KeyRelease>', input)

    # 开始任务键
    def setStartButton(self):
        self.Button_start = tk.Button(self, text ="开始", command = self.setStartButtonCommand)
        self.Button_start.place(x=240, y=200, width=80)
    
    # 开始任务
    def setStartButtonCommand(self):
        if not self.workpath:
            return messagebox.showinfo("提示", "请先选择文件夹")
        if len(self.markList) == 0:
            return messagebox.showinfo("提示", "请先输入标记字符")
        if not ''.join(self.markList).isdigit():
            return messagebox.showinfo("提示", "标记字符只能是数字")
        if self.isZipValue == 1 and not self.zipName:
            return messagebox.showinfo("提示", "请先输入压缩包名称")

        if self.isZipEnd == False:
            self.isZipEnd = True
            self.thread_it(self, startZipMisson, self)
            self.saveData()
        else:
            messagebox.showinfo("提示", "请先等待当前文件压缩完成")
    
    # 停止任务键
    def setStopButton(self):
        self.Button_stop = tk.Button(self, text ="停止压缩", command = self.setStopButtonCommand)
        self.Button_stop.place(x=340, y=200, width=80)
    
    def setStopButtonCommand(self):
        if self.isZipEnd == False:
            messagebox.showinfo("提示", "当前没有正在执行的压缩任务")
        else:
            stop_thread(self.zip_thread)
            self.outputInfo('\n已停止压缩\n')
            self.isZipEnd = False
    
    # 输出信息文本框
    def setOutputText(self):
        scrolW = 83 # 设置文本框的长度
        scrolH = 10 # 设置文本框的高度
        self.outputText = scrolledtext.ScrolledText(self, width=scrolW, height=scrolH, wrap=tk.WORD)
        self.outputText.place(x=0, y=260)

    # 输出信息到gui界面
    def outputInfo(self, str):
        self.outputText.insert(tk.END, str)
        self.outputText.see(tk.END)
    
    @staticmethod
    def thread_it(self, func, *args):
        self.zip_thread = threading.Thread(target=func, args=args) 
        self.zip_thread.setDaemon(True) # 守护线程
        self.zip_thread.start()

