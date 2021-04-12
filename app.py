import tkinter as tk

from pages.home import homePage
from pages.send import sendPage
from pages.extract import extractPage

from method.getConfig import getConfig

config = getConfig()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('文件')
        self.resizable(0,0)
        self.getConfig = config
        self.setPosition()
        self.initPage()
        self.setMenu()
    
    def setPosition(self):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        # 程序窗口宽高
        windowWidth = 600
        windowHeight = 400
        # 窗口位置
        x = (screenwidth - windowWidth) / 2
        y = (screenheight - windowHeight) / 2
        self.geometry("%dx%d+%d+%d" %(windowWidth, windowHeight, x, y))
    
    def setMenu(self):
        menubar = tk.Menu(self)
        menubar.add_command(label = "首页", command = lambda:self.changePage(1))
        menubar.add_command(label = "发送", command = lambda:self.changePage(2))
        menubar.add_command(label = "提取", command = lambda:self.changePage(3))
        self.config(menu = menubar)
    
    def initPage(self):
        self.homePage = homePage(self)
        self.sendPage = sendPage(self)
        self.extractPage = extractPage(self)
        self.changePage(1)

    def changePage(self, index):
        if index == 1:
            self.homePage.lift()
        elif index == 2:
            self.sendPage.updateData()
            self.sendPage.lift()
        elif index == 3:
            self.extractPage.lift()

app = App()
app.update()
app.mainloop()