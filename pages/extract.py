import tkinter as tk
import threading
from tkinter import messagebox
from tkinter import filedialog

from tasks.extract import extract

class extractPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =parent
        self.outbox = ''
        self.inbox = []
        self.place(x=0, y=0, relwidth=1, relheight=1)
        # 配置读取
        self.getConfig = parent.getConfig
        self.initLayout()
    
    def initLayout(self):
        self.setPathSelect()
        self.setSendButton()

   # 路径选择
    def setPathSelect(self):
        self.Label_select = tk.Label(self, text="文件选择：")
        self.Label_select.place(x=80, y=20)
        self.Entry_var_select = tk.Variable()
        self.Entry_select = tk.Entry(self, textvariable=self.Entry_var_select, state='disabled')
        self.Entry_select.place(x=200, y=20, width=120, height=26)
        self.Button_select = tk.Button(self, text ="选择", command = self.setPathSelectCommand)
        self.Button_select.place(x=330, y=20, height=26)
    
    # 路径选择绑定事件
    def setPathSelectCommand(self):
        workpath = filedialog.askopenfilename(filetypes=[('image', '*.jpg'), ('image', '*.jpeg')])
        print(workpath)
        if workpath:
            self.workpath = workpath
            self.Entry_var_select.set(self.workpath)
    
    # 开始提取
    def setSendButton(self):
        self.Button_send = tk.Button(self, text ="提取", command = self.setSendButtonCommand)
        self.Button_send.place(x=240, y=112, width=80)
    
    def setSendButtonCommand(self):
        extract(self.workpath, messagebox)