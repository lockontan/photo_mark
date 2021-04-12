import piexif

password = ['H', 'A', 'N', 'E', 'P', 'U', 'M', 'R', 'O', 'D']
bassword = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def extract(filePath, messagebox):
    exif_dict = piexif.load(filePath)

    # ImageID
    if exif_dict['0th'].__contains__(32781):
        value = exif_dict['0th'][32781]
        if type(value) == bytes:
            value = value.decode()
            newValue = []
            for i in value:
                v = bassword[password.index(i)]
                newValue.append(v)
            strs = ''.join(newValue)
            if strs:
                messagebox.showinfo("结果(ImageID)：", strs)
                return

    # Software
    if exif_dict['0th'].__contains__(305):
        value = exif_dict['0th'][305]
        if type(value) == bytes:
            value = value.decode()
            newValue = []
            for i in value:
                v = bassword[password.index(i)]
                newValue.append(v)
            strs = ''.join(newValue)
            if strs:
                messagebox.showinfo("结果", strs)
                return
    # Model
    if exif_dict['0th'].__contains__(272):
        value = exif_dict['0th'][272]
        if type(value) == bytes:
            value = value.decode()
            newValue = []
            for i in value:
                v = bassword[password.index(i)]
                newValue.append(v)
            strs = ''.join(newValue)
            if strs:
                messagebox.showinfo("结果", strs)
                return