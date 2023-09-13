from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import imageio

root = Tk()

root.title("Introduccion al Procesamiento Digital de Imagenes")
root.configure(background='#474747')
root.geometry('820x760')
# root.attributes("-fullscreen", True)

def cargar_imagen():
    try:
        path_img.set(filedialog.askopenfilename(initialdir='./src/',
                                                title='Selecciona una imagen',
                                                filetypes=(
                                                ('todos los archivos', '*.*'), ('jpg', '*.jpg'), ('png', '*.png'))))
        image = ImageTk.PhotoImage(Image.open(path_img.get()))

        dir.config(text=path_img.get())

        imgBase.config(image=image)
        imgBase.image = image
    except ValueError:
        print('Hubo un error al cargar la imagen')


def actualizarRGB():
    try:
        imgModify = np.clip(imageio.v2.imread(path_img.get()) / 255., 0, 1)
        imgModify[:, :, 0] *= int(r.get())
        imgModify[:, :, 1] *= int(g.get())
        imgModify[:, :, 2] *= int(b.get())

        imgModify = (imgModify * 255).astype(np.uint8)
        imageio.imwrite("mi_imagen.png", imgModify)

        image = ImageTk.PhotoImage(Image.open("mi_imagen.png"))
        imgTest.config(image=image)
        imgTest.image = image
    except ValueError:
        print('Hubo un error al modificar los canales de la imagen')




path_img = StringVar()

boton = Button(root, text="Cargar Imagen", command=cargar_imagen)
boton.pack()

dir = Label(root)
dir.pack()
imgBase = Label(root)
imgBase.pack()

redLabel = Label(root, text='Valor de Red').pack()
r = Entry(root,width=9)
r.pack()
greenLabel = Label(root, text='Valor de Green').pack()
g = Entry(root,width=9)
g.pack()
blueLabel = Label(root, text='Valor de Blue').pack()
b = Entry(root,width=9)
b.pack()

actualizarBtn = Button(root, text="Actualizar Valores", command=actualizarRGB)
actualizarBtn.pack()

imgTest = Label(root)
imgTest.pack()

root.mainloop()