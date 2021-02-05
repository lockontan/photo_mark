import piexif
import os
import random
import shutil
import subprocess

password = ['H', 'A', 'N', 'E', 'P', 'U', 'M', 'R', 'O', 'D']
bassword = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def getRandomStr():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = []
    for i in range(10):
        s.append(random.choice(seed))
    return ''.join(s)

# 标记文件
def setMark(filePath, fileName, mark):
   exif_dict = piexif.load(filePath)
   # exif_dict["0th"][piexif.ImageIFD.Make] = mark.encode()
   # exif_dict["0th"][piexif.ImageIFD.Artist] = mark.encode()
   # 程序名称
   # exif_dict["0th"][305] = mark.encode()
   # 相机型号
   # exif_dict["0th"][272] = mark.encode()
   # ImageId
   exif_dict["0th"][32781] = mark.encode()
   exif_bytes = piexif.dump(exif_dict)
   piexif.insert(exif_bytes, filePath)

# 遍历文件夹
def walkFile(path, mark):
   newmark = ''
   for i in str(mark):
        newmark += password[int(i)]

   for root, dirs, files in os.walk(path):
        for f in files:
            if '.jpg' in f or '.JPG' in f or '.jpeg' in f or '.JPEG' in f:
                setMark(os.path.join(root, f), f, newmark)

# 调用winRar压缩
def zip_file_with_winRar(input_path, output_path, output_name):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        shutil.rmtree(output_path)
        os.makedirs(output_path)
    password = getRandomStr()
    command = os.path.join(os.getcwd(), 'tools', 'WinRAR.exe')  + " a -r -ep1 -hp" + password +" " + os.path.join(output_path, output_name + '_'+ password + '.rar')+ " "  + os.path.join(input_path, '*')
    subprocess.run(command)

def startZipMisson(app):

    markList = app.markList
    workpath = app.workpath
    zipName = app.zipName
    isZipValue = app.isZipValue
    outputInfo = app.outputInfo

    outputInfo('总数: ' + str(len(markList)) +   '\n\n')
   
    for number in markList:

        outputInfo('标记开始: ' + str(number) + '\n')

        walkFile(workpath, str(number))

        outputInfo('标记完成: ' + str(number) + '\n')

        if isZipValue == 1:
            zipFullPath = os.path.join(os.path.split(workpath)[0], zipName, str(number), zipName + '.rar')
            if os.path.exists(os.path.join(str(number), zipName)) == False:
                outputInfo('正在压缩: ' + zipFullPath + '\n')

                base_output_path = os.path.join(os.path.split(workpath)[0], zipName)
                if not os.path.exists(base_output_path):
                    os.makedirs(base_output_path)
                
                zip_file_with_winRar(workpath, os.path.join(base_output_path, str(number)), zipName)

                outputInfo('完成压缩: ' + zipFullPath + '\n\n')
                
            else:
            
                outputInfo('文件已存在: ' + zipFullPath + '\n')
    outputInfo('任务完成')

    app.isZipEnd = False
