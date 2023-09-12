import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import imageio.v2 as imageio

from PIL import ImageTk, Image
import os
import numpy as np
import matplotlib.pyplot as plt


def to_yiq(im_rgb):
    new_yiq = np.zeros(im_rgb.shape)
    new_yiq[:, :, 0] = np.clip(
        0.229 * im_rgb[:, :, 0] + 0.587 * im_rgb[:, :, 1] + 0.114 * im_rgb[:, :, 2],
        a_min=0,
        a_max=1
    )
    new_yiq[:, :, 1] = np.clip(
        0.595716 * im_rgb[:, :, 0] + -0.274453 * im_rgb[:, :, 1] + -0.321263 * im_rgb[:, :, 2],
        a_min=-0.5957,
        a_max=0.5957
    )
    new_yiq[:, :, 2] = np.clip(
        0.211456 * im_rgb[:, :, 0] + -0.522591 * im_rgb[:, :, 1] + 0.311135 * im_rgb[:, :, 2],
        a_min=-0.5226,
        a_max=0.5226
    )
    return new_yiq


def to_rgb(im_yiq):
    new_rgb = np.zeros(im_yiq.shape)
    new_rgb[:, :, 0] = im_yiq[:, :, 0] + 0.9663 * im_yiq[:, :, 1] + 0.6210 * im_yiq[:, :, 2]
    new_rgb[:, :, 1] = im_yiq[:, :, 0] + -0.2721 * im_yiq[:, :, 1] + -0.6474 * im_yiq[:, :, 2]
    new_rgb[:, :, 2] = im_yiq[:, :, 0] + -1.1070 * im_yiq[:, :, 1] + 1.7046 * im_yiq[:, :, 2]
    new_rgb = (new_rgb * 255).astype(int)
    return np.clip(new_rgb, 0, 255)


class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.style = ttk.Style()
        self.style.theme_use("vista")
        self.root.title("Introduccion al Procesamiento Digital de Imagenes - TP2")
        self.root.configure(background='#f2f2f9')
        self.root.geometry('1024x600')
        self.path_img = StringVar()
        size_image = 340


        image1 = self.resize_image('resource/Img_oscura.bmp', size_image)
        self.img1 = Label(self.root, background='red', image=image1, width=size_image, height=size_image)
        self.img1.image = image1
        button_upload_1 = Button(self.root,
                                 text="Cargar Imagen",
                                 command=lambda: self.upload_image(size_image, self.img1))
        self.path = Label(self.root)
        button_upload_1.grid(row=1, column=0)
        self.img1.grid(row=0, column=0)

        image2 = self.resize_image('resource/1024x600/2.jpg', size_image)
        self.img2 = Label(self.root, background='red', image=image2, width=size_image, height=size_image)
        self.img2.image = image2
        self.path = Label(self.root)
        button_upload_2 = Button(self.root,
                                 text="raiz",
                                 command=lambda: self.filtroRaiz(size_image, image1))
        button_upload_2.grid(row=1, column=1)
        self.img2.grid(row=0, column=1)


        button_upload_4 = Button(self.root,
                                 text="cuadratica",
                                 command=lambda: self.filtroCuadratica(size_image, image1))
        button_upload_4.grid(row=2, column=2)
        button_upload_5 = Button(self.root,
                                 text="Cargar Imagen",
                                 command=lambda: self.filtroLineal(size_image, image1))
        button_upload_5.grid(row=3, column=2)

    def upload_image(self, size, img):
        try:
            self.path_img.set(filedialog.askopenfilename(
                initialdir='./src/',
                title='Selecciona una imagen',
                filetypes=(('Todos los archivos', '*.*'), ('jpg', '*.jpg'), ('png', '*.png'))))
            image = self.resize_image(self.path_img.get(), size)

            self.path.config(text=self.path_img.get())
            img.config(image=image)
            img.image = image
        except ValueError:
            print('Hubo un error al cargar la imagen')

    def resize_image(self, image, size):
        old_image = Image.open(os.path.abspath(image))
        width, height = old_image.size
        if width > height:
            new_width = size
            new_height = int(height * (size / width))
        else:
            new_width = int(width * (size / height))
            new_height = size
        image = ImageTk.PhotoImage(Image.open(os.path.abspath(image)).resize((new_width, new_height)))
        return image

    def filtroRaiz(self, size, image):
        im = imageio.imread('resource/Img_oscura.bmp')
        im = np.clip(im / 255., 0., 1.)
        yiq = to_yiq(im)
        yiq[:,:,0] = np.sqrt(yiq[:,:,0])
        rgb = to_rgb(yiq)
        plt.imshow(rgb)
        plt.show()

    def filtroCuadratica(self, size, image):
        im = imageio.imread('resource/Img_oscura.bmp')
        im = np.clip(im / 255., 0., 1.)
        yiq = to_yiq(im)
        yiq[:,:,0] = yiq[:,:,0] ** 2
        rgb = to_rgb(yiq)
        plt.imshow(rgb)
        plt.show()


    def filtroLineal(self, size, image):
        im = imageio.imread('resource/Img_oscura.bmp')
        im = np.clip(im / 255., 0., 1.)
        yiq = to_yiq(im)
        yiq[:,:,0] *= 1
        asd = plt.hist(yiq[:,120,0], bins=10)
        fig, ax = plt.subplots()
        ax.hist(yiq[:,:,0])
        plt.show()
        rgb = to_rgb(yiq)
        plt.imshow(rgb)
        plt.show()






app = App()
app.root.mainloop()
