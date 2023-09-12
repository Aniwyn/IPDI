from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import imageio

root = Tk()

root.title("Introduccion al Procesamiento Digital de Imagenes")
root.configure(background='#474747')
root.geometry('820x760')

dir = Label(root, height=340, width=10, background='red')
dir.pack()

root.mainloop()