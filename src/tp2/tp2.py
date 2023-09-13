import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import os


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

        image1 = self.resize_image('resource/1024x600/1.jpg', size_image)
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
                                 text="Cargar Imagen",
                                 command=lambda: self.upload_image(size_image, self.img2))
        button_upload_2.grid(row=1, column=1)
        self.img2.grid(row=0, column=1)

        image3 = self.resize_image('resource/in_process.png', size_image)
        self.img3 = Label(self.root, background='red', image=image3, width=size_image, height=size_image)
        self.img3.image = image3
        self.path = Label(self.root)
        button_upload_3 = Button(self.root,
                                 text="Cargar Imagen",
                                 command=lambda: self.upload_image(size_image, self.img3))
        button_upload_3.grid(row=1, column=2)
        self.img3.grid(row=0, column=2)

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


app = App()
app.root.mainloop()
