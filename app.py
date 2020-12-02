import piexif
import os
import zipfile

import tkinter
from tkinter import messagebox

outputText = None

password = ['H', 'A', 'N', 'E', 'P', 'U', 'M', 'R', 'O', 'D']
bassword = ['0',  '1', '2',  '3', '4', '5',  '6',  '7',  '8', '9']


# 输出信息到gui界面
def outputInfo(str):
  outputText.insert(tkinter.END, str)
  outputText.see(tkinter.END)
pass

# 标记文件
def setMark(filePath, fileName, mark):
  exif_dict = piexif.load(filePath)
  # exif_dict["0th"][piexif.ImageIFD.Make] = mark.encode()
  # exif_dict["0th"][piexif.ImageIFD.Artist] = mark.encode()
  # 程序名称
  exif_dict["0th"][305] = mark.encode()
  # 相机型号
  exif_dict["0th"][272] = mark.encode()
  exif_bytes = piexif.dump(exif_dict)
  piexif.insert(exif_bytes, filePath)

# 遍历文件夹
def walkFile(path, mark):
  newmark = ''
  for i in str(mark):
    newmark += password[int(i)]
  pass

  for root, dirs, files in os.walk(path):
    for f in files:
      if '.jpg' in f or '.png' in f or '.JPG' in f or '.PNG' in f or '.jpeg' in f or '.JPEG' in f:
        setMark(os.path.join(root, f), f, newmark)

# 对目录进行深度优先遍历
# :param input_path:
# :param result:
# :return:
def get_zip_file(input_path, result):
  files = os.listdir(input_path)
  for file in files:
    if os.path.isdir(input_path + '/' + file):
      get_zip_file(input_path + '/' + file, result)
    else:
      result.append(input_path + '/' + file)

# 压缩文件
# :param input_path: 压缩的文件夹路径
# :param output_path: 解压（输出）的路径
# :param output_name: 压缩包名称
# :return:
def zip_file_path(input_path, output_path, output_name):
  if not os.path.exists(output_path):
    os.makedirs(output_path)
  pass
  f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
  filelists = []
  get_zip_file(input_path, filelists)
  for file in filelists:
    f.write(file)
  # 调用了close方法才会保证完成压缩
  f.close()
  return output_path + "/" + output_name

def startTask(workpath, listNumber, workName, iszip, outputTextArea):

  global outputText
  outputText = outputTextArea

  outputInfo('总数: ' + str(len(listNumber)) +  '\n\n')
  
  for number in listNumber:

    zipName = os.path.join(os.path.split(workpath)[0], str(number),  workName + '.zip')

    if os.path.exists(os.path.join(str(number), workName + '.zip')) == False:
      outputInfo('标记开始: ' + str(number) + '\n')

      walkFile(workpath, str(number))

      outputInfo('标记完成: ' + str(number) + '\n')

      if iszip == 1:
        outputInfo('正在压缩: ' + zipName + '\n')

        zip_file_path(workpath, os.path.join(os.path.split(workpath)[0], str(number)), workName + '.zip')

        outputInfo('完成压缩: ' + zipName + '\n\n')
      pass
    else:
      outputInfo('文件已存在: ' + zipName + '\n')
    pass
  pass

  outputInfo('任务完成')
pass