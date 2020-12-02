import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

from app import startTask


# 需要处理的文件夹
workpath = None

window = tkinter.Tk()
window.title('文件')

#屏幕宽度
sw = window.winfo_screenwidth()
#屏幕高度
sh = window.winfo_screenheight()

# 程序窗口宽高
ww = 600
wh = 400

# 窗口位置
x = (sw-ww) / 2
y = (sh-wh) / 2

window.geometry("%dx%d+%d+%d" %(ww,wh,x,y))


# 文件夹选择
def select_dir():
  global workpath
  workpath = filedialog.askdirectory()
  if workpath:
    Entry_var_select.set(workpath)
pass

# 是否生成压缩文件
def update_isZip():
  if iszip.get() == 0:
    Label_name.place_forget()
    Entry_name.place_forget()
  else:
    Label_name.place(x=80, y=158)
    Entry_name.place(x=200, y=158, width=120, height=26)
  pass
pass

# 开始任务
def start():
  lists = Entry_mark.get().split(',')
  listNumber = [var.replace(' ', '') for var in lists if var]

  if not workpath:
    return messagebox.showerror("Error", "请先选择文件夹")
  pass

  if len(listNumber) == 0:
    return messagebox.showerror("Error", "请先输入标记字符")
  pass

  if iszip.get() == 1 and not Entry_name.get():
    return messagebox.showerror("Error", "请先输入压缩包名称")
  pass

  startTask(workpath, listNumber, Entry_name.get(), iszip.get(), outputText)
pass

# 路径选择
Label_select = tkinter.Label(window, text="路径选择：")
Label_select.place(x=80, y=20)
Entry_var_select = tkinter.Variable()
Entry_select = tkinter.Entry(window, textvariable=Entry_var_select, state='disabled')
Entry_select.place(x=200, y=20, width=120, height=26)
Button_select = tkinter.Button(window, text ="选择", command = select_dir)
Button_select.place(x=330, y=20, height=26)

# 标记字符
Label_mark = tkinter.Label(window, text="标记字符：")
Label_mark.place(x=80, y=66)
Entry_mark = tkinter.Entry(window)
Entry_mark.place(x=200, y=66, width=120, height=26)
Label_mark_tip = tkinter.Label(window, text="(多个使用英文 , 隔开，仅限数字)")
Label_mark_tip.place(x=330, y=66)

# 是否压缩
Label_zip = tkinter.Label(window, text="是否压缩：")
Label_zip.place(x=80, y=112)
iszip = tkinter.IntVar()
Checkbutton_zip = tkinter.Checkbutton(window, text = '是否生成压缩包', variable = iszip, command = update_isZip)
Checkbutton_zip.place(x=190, y=112, width=120, height=26)
Checkbutton_zip.select()

# 压缩包名称
Label_name = tkinter.Label(window, text="压缩包名称：")
Label_name.place(x=80, y=158)
Entry_name = tkinter.Entry(window)
Entry_name.place(x=200, y=158, width=120, height=26)

Button_start = tkinter.Button(window, text ="开始", command = start)
Button_start.place(x=240, y=200, width=80)

scrolW = 83 # 设置文本框的长度
scrolH = 10 # 设置文本框的高度
outputText = scrolledtext.ScrolledText(window, width=scrolW, height=scrolH, wrap=tkinter.WORD)
outputText.place(x=0, y=240)

window.resizable(0,0)
window.mainloop()