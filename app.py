import threading
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

from zipMethod import startZipMisson
from stopThread import stop_thread

class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('文件')
        self.resizable(0,0)
        # 选择的路径
        self.workpath = None
        # 标记符号列表
        self.markList = []
        # 是否压缩
        self.isZipValue = 1
        # 压缩包名字
        self.zipName = None
        self.setWindowPosition()
        self.setPathSelect()
        self.setMarkInput()
        self.setIsZipSelect()
        self.setZipNameInput()
        self.setStartButton()
        self.setStopButton()
        self.setOutputText()
        # 判断压缩进程是否已结束
        self.isZipEnd = False
    
    # 窗口位置
    def setWindowPosition(self):
        # 屏幕宽高度
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        # 程序窗口宽高
        ww = 600
        wh = 400
        # 窗口位置
        x = (sw-ww) / 2
        y = (sh-wh) / 2
        self.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
        
    # 路径选择
    def setPathSelect(self):
        self.Label_select = tkinter.Label(self, text="路径选择：")
        self.Label_select.place(x=80, y=20)
        self.Entry_var_select = tkinter.Variable()
        self.Entry_select = tkinter.Entry(self, textvariable=self.Entry_var_select, state='disabled')
        self.Entry_select.place(x=200, y=20, width=120, height=26)
        self.Button_select = tkinter.Button(self, text ="选择", command = self.setPathSelectCommand)
        self.Button_select.place(x=330, y=20, height=26)
    
    # 路径选择绑定事件
    def setPathSelectCommand(self):
        self.workpath = filedialog.askdirectory()
        if self.workpath:
            self.Entry_var_select.set(self.workpath)
    
    # 标记字符
    def setMarkInput(self):
        self.Label_mark = tkinter.Label(self, text="标记字符：")
        self.Label_mark.place(x=80, y=66)
        self.Entry_mark = tkinter.Entry(self)
        self.Entry_mark.place(x=200, y=66, width=120, height=26)
        self.Label_mark_tip = tkinter.Label(self, text="(多个使用英文 , 隔开，仅限数字)")
        self.Label_mark_tip.place(x=330, y=66)

    # 是否压缩
    def setIsZipSelect(self):
        self.Label_zip = tkinter.Label(self, text="是否压缩：")
        self.Label_zip.place(x=80, y=112)
        self.isZip = tkinter.IntVar()
        self.Checkbutton_zip = tkinter.Checkbutton(self, text = '是否生成压缩包', variable = self.isZip, command = self.setIsZipSelectCommand)
        self.Checkbutton_zip.place(x=190, y=112, width=120, height=26)
        self.Checkbutton_zip.select()
    
    # 是否压缩绑定事件
    def setIsZipSelectCommand(self):
        if self.isZip.get() == 0:
            self.Label_name.place_forget()
            self.Entry_name.place_forget()
        else:
            self.Label_name.place(x=80, y=158)
            self.Entry_name.place(x=200, y=158, width=120, height=26)

    # 压缩包名称
    def setZipNameInput(self):
        self.Label_name = tkinter.Label(self, text="压缩包名称：")
        self.Label_name.place(x=80, y=158)
        self.Entry_name = tkinter.Entry(self)
        self.Entry_name.place(x=200, y=158, width=120, height=26)

    # 开始任务键
    def setStartButton(self):
        self.Button_start = tkinter.Button(self, text ="开始", command = self.setStartButtonCommand)
        self.Button_start.place(x=240, y=200, width=80)
    
    # 开始任务
    def setStartButtonCommand(self):
        lists = self.Entry_mark.get().split(',')
        listNumber = [var.replace(' ', '') for var in lists if var]

        if not self.workpath:
            return messagebox.showinfo("提示", "请先选择文件夹")
        if len(listNumber) == 0:
            return messagebox.showinfo("提示", "请先输入标记字符")
        if self.isZip.get() == 1 and not self.Entry_name.get():
            return messagebox.showinfo("提示", "请先输入压缩包名称")
        
        self.markList = listNumber
        self.isZipValue = self.isZip.get()
        self.zipName = self.Entry_name.get()

        if self.isZipEnd == False:
            self.isZipEnd = True
            self.thread_it(self, startZipMisson, self)
        else:
            messagebox.showinfo("提示", "请先等待当前文件压缩完成")
    
    # 停止任务键
    def setStopButton(self):
        self.Button_stop = tkinter.Button(self, text ="停止压缩", command = self.setStopButtonCommand)
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
        self.outputText = scrolledtext.ScrolledText(self, width=scrolW, height=scrolH, wrap=tkinter.WORD)
        self.outputText.place(x=0, y=240)

    # 输出信息到gui界面
    def outputInfo(self, str):
        self.outputText.insert(tkinter.END, str)
        self.outputText.see(tkinter.END)
    
    @staticmethod
    def thread_it(self, func, *args):
        self.zip_thread = threading.Thread(target=func, args=args) 
        self.zip_thread.setDaemon(True) # 守护线程
        self.zip_thread.start()

app = Application()
app.mainloop()