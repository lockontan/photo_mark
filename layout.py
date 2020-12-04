import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

class Layout:
    def __init__(self, callback):
        self.startMisson = callback
        window = tkinter.Tk()
        window.title('文件')
        window.resizable(0,0)
        self.window = window
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
        self.setOutputText()
        self.window.mainloop()
    
    # 窗口位置
    def setWindowPosition(self):
        # 屏幕宽高度
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        # 程序窗口宽高
        ww = 600
        wh = 400
        # 窗口位置
        x = (sw-ww) / 2
        y = (sh-wh) / 2
        self.window.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
        
    # 路径选择
    def setPathSelect(self):
        self.Label_select = tkinter.Label(self.window, text="路径选择：")
        self.Label_select.place(x=80, y=20)
        self.Entry_var_select = tkinter.Variable()
        self.Entry_select = tkinter.Entry(self.window, textvariable=self.Entry_var_select, state='disabled')
        self.Entry_select.place(x=200, y=20, width=120, height=26)
        self.Button_select = tkinter.Button(self.window, text ="选择", command = self.setPathSelectCommand)
        self.Button_select.place(x=330, y=20, height=26)
    
    # 路径选择绑定事件
    def setPathSelectCommand(self):
        self.workpath = filedialog.askdirectory()
        if self.workpath:
            self.Entry_var_select.set(self.workpath)
    
    # 标记字符
    def setMarkInput(self):
        self.Label_mark = tkinter.Label(self.window, text="标记字符：")
        self.Label_mark.place(x=80, y=66)
        self.Entry_mark = tkinter.Entry(self.window)
        self.Entry_mark.place(x=200, y=66, width=120, height=26)
        self.Label_mark_tip = tkinter.Label(self.window, text="(多个使用英文 , 隔开，仅限数字)")
        self.Label_mark_tip.place(x=330, y=66)

    # 是否压缩
    def setIsZipSelect(self):
        self.Label_zip = tkinter.Label(self.window, text="是否压缩：")
        self.Label_zip.place(x=80, y=112)
        self.isZip = tkinter.IntVar()
        self.Checkbutton_zip = tkinter.Checkbutton(self.window, text = '是否生成压缩包', variable = self.isZip, command = self.setIsZipSelectCommand)
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
        self.Label_name = tkinter.Label(self.window, text="压缩包名称：")
        self.Label_name.place(x=80, y=158)
        self.Entry_name = tkinter.Entry(self.window)
        self.Entry_name.place(x=200, y=158, width=120, height=26)

    # 开始任务键
    def setStartButton(self):
        self.Button_start = tkinter.Button(self.window, text ="开始", command = self.setStartButtonCommand)
        self.Button_start.place(x=240, y=200, width=80)
    
    # 开始任务
    def setStartButtonCommand(self):
        lists = self.Entry_mark.get().split(',')
        listNumber = [var.replace(' ', '') for var in lists if var]

        if not self.workpath:
            return messagebox.showerror("Error", "请先选择文件夹")
        if len(listNumber) == 0:
            return messagebox.showerror("Error", "请先输入标记字符")
        if self.isZip.get() == 1 and not self.Entry_name.get():
            return messagebox.showerror("Error", "请先输入压缩包名称")
        
        self.markList = listNumber
        self.isZipValue = self.isZip.get()
        self.zipName = self.Entry_name.get()

        self.startMisson(self)
    
    # 输出信息文本框
    def setOutputText(self):
        scrolW = 83 # 设置文本框的长度
        scrolH = 10 # 设置文本框的高度
        self.outputText = scrolledtext.ScrolledText(self.window, width=scrolW, height=scrolH, wrap=tkinter.WORD)
        self.outputText.place(x=0, y=240)

    # 输出信息到gui界面
    def outputInfo(self, str):
        self.outputText.insert(tkinter.END, str)
        self.outputText.see(tkinter.END)