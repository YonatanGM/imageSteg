from tkinter import filedialog
from tkinter import *
from Steg import STEG
import os, pathlib

file_path = None
img_path = ''
root = Tk()
t = Text(root)

def choosefile():
    global file_path, t
    file = filedialog.askopenfile(title = "choose the file you want to hide")
    file_path = str(pathlib.PureWindowsPath(os.path.abspath(file.name)).as_posix())
    t.insert(INSERT, 'file: {}\n'.format(file_path))
    
    
def chooseimage():
    global img_path, t
    img = filedialog.askopenfile(title = "choose the carrier image", filetypes = [('ICO', '*.ico'), ('PNG', '*.png'), ('TIFF', ['*.tif', '*.TIFF']), ('BMP', '*.bmp')])
    img_path = str(pathlib.PureWindowsPath(os.path.abspath(img.name)).as_posix())
    t.insert(INSERT, 'Image: {}\n'.format(img_path))
def onhide():
    global t
    try:
        t.insert(INSERT, "hiding...\n")
        i = STEG(img_path, file_path)
        i.hide()
        t.insert(INSERT, '[+] {} created\n'.format('new.' + i.img_type))
    
    except Exception as e:
        t.insert(INSERT, str(e)+'\n')
        t.pack()
        
def onextract():
    global t
    try:
        t.insert(INSERT, "extracting...\n")
        i = STEG(img_path)
        i.extract()
        t.insert(INSERT, '[+] Successfully extracted message\n')
    except Exception as e:
        t.insert(INSERT, str(e)+'\n')
        t.pack()
        

t.insert(INSERT, "Choose the carrier image and file to hide, leave file unselected for extracting\n")
t.pack()

Button(root, text = 'Select carrier image', fg = 'black', command = chooseimage).pack()
Button(root, text = 'Select file to hide', fg = 'black', command = choosefile).pack()

Button(root, text = 'Hide', fg = 'black', command = onhide).pack()
Button(root, text = 'Extract', fg = 'black', command = onextract).pack()


