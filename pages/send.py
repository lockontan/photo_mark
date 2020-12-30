import tkinter as tk
import threading
from tkinter import messagebox
from tasks.send import sendMail

class sendPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =parent
        self.outbox = ''
        self.inbox = []
        self.place(x=0, y=0, relwidth=1, relheight=1)
        # 配置读取
        self.getConfig = parent.getConfig
        self.initLayout()
        self.initData()
    
    def initLayout(self):
        self.setOutbox()
        self.setInbox()
        self.setSendButton()

    def initData(self):
        outbox = self.getConfig.getValue('sendData', 'outbox')
        if outbox:
            self.outbox = outbox
            self.Entry_var_outboxt.set(outbox)

    def saveData(self):
        self.getConfig.setValue('sendData', 'outbox', self.outbox)

    # 发件箱
    def setOutbox(self):
        self.Label_outboxt = tk.Label(self, text="发件箱：")
        self.Label_outboxt.place(x=80, y=20)
        self.Entry_var_outboxt = tk.Variable()
        self.Entry_outboxt = tk.Entry(self, textvariable=self.Entry_var_outboxt)
        self.Entry_outboxt.place(x=200, y=20, width=220, height=26)

        def input(eventObj):
            self.outbox = self.Entry_outboxt.get()
        self.Entry_outboxt.bind('<KeyRelease>', input)
    
    # 收件箱
    def setInbox(self):
        self.Label_inboxt = tk.Label(self, text="收件箱：")
        self.Label_inboxt.place(x=80, y=66)
        self.Entry_var_inboxt = tk.Variable()
        self.Entry_inboxt = tk.Entry(self, textvariable=self.Entry_var_inboxt)
        self.Entry_inboxt.place(x=200, y=66, width=220, height=26)

        def input(eventObj):
            inboxStr = self.Entry_inboxt.get()
            self.inbox = [var.replace(' ', '') for var in inboxStr.split(';') if var]
        self.Entry_inboxt.bind('<KeyRelease>', input)

    # 更新收件箱
    def updateData(self):
        markList = self.parent.homePage.markList
        self.inbox = [var.replace(' ', '') + '@qq.com' for var in markList if var]
        self.Entry_var_inboxt.set('; '.join(self.inbox))
    
    # 开始发送
    def setSendButton(self):
        self.Button_send = tk.Button(self, text ="发送", command = self.setSendButtonCommand)
        self.Button_send.place(x=240, y=112, width=80)
    
    def setSendButtonCommand(self):
        workpath = self.parent.homePage.workpath
        zipName = self.parent.homePage.zipName
        if len(self.outbox) == 0:
            return messagebox.showinfo("提示", "请先填写发件箱")
        if len(self.inbox) == 0:
            return messagebox.showinfo("提示", "请先填写收件箱")
        self.saveData()
        self.thread_it(self, sendMail, self.outbox, self.inbox, workpath, zipName)
    
    @staticmethod
    def thread_it(self, func, *args):
        self.zip_thread = threading.Thread(target=func, args=args) 
        self.zip_thread.setDaemon(True) # 守护线程
        self.zip_thread.start()