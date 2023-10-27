import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src import a_lib as lib
from PIL import Image
from src import PixelArithmetic as libK
import sv_ttk

class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Introduccion al Procesamiento Digital de Imagenes - TP3")
        self.root.geometry('1080x600')
        self.style = ttk.Style()
        sv_ttk.use_light_theme()
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both')

        self.path_img = StringVar()
        self.size_image = 340
        self.image_resultant = ''
        self.operations = ['Erosion', 'Dilatacion', 'Apertura','Cierre', 'BordeMorf', 'Mediana', 'Meanshift']

        self.image1_path = '../../resource/1024x600/1.png'
        image1 = lib.resize_image(self.image1_path, self.size_image)
        self.lb_img1 = Label(
            frame,
            image=image1,
            width=self.size_image,
            height=self.size_image,
            borderwidth=0
        )
        self.lb_img1.image = image1
        self.path1 = Label(frame, text='', padx=5, width=31, anchor='w')
        button_upload_1 = ttk.Button(
            self.root,
            text="Seleccionar...",
            width=10,
            command=lambda: self.upload_image(self.size_image, self.lb_img1, 1, self.path1)
        )
        self.lb_img1.place(x=15, y=15)
        button_upload_1.place(x=420, y=100)
        self.path1.place(x=120, y=365)

        self.image3_path = os.path.abspath('../../resource/1024x600/2.png')
        image3 = lib.resize_image(self.image3_path, 2)
        self.lb_img3 = Label(
            self.root,
            image=image3,
            width=self.size_image,
            height=self.size_image,
            borderwidth=0
        )
        self.lb_img3.image = image3
        self.path3 = Label(self.root)
        self.lb_img3.place(x=720, y=15)

        font_lb = Font(frame, family='Segoe UI', size=12)

        self.lb_operation = Label(self.root, text='Filtros', anchor='w', font=font_lb)
        self.lb_operation.place(x=550, y=130)
        self.combo_operation = ttk.Combobox(self.root, width=10, state='readonly', values=self.operations)
        self.combo_operation.place(x=550, y=100)

        button_process = ttk.Button(
            self.root,
            text="Calcular",
            width=10,
            command=lambda: self.process()
        )
        button_process.place(x=420, y=60)


        button_process = ttk.Button(
            self.root,
            text="Guardar",
            width=10,
            command=lambda: self.save_image()
        )
        button_process.place(x=570, y=60)

        button_process = ttk.Button(
            self.root,
            text="Salir",
            width=10,
            command=lambda: self.root.quit()
        )
        button_process.place(x=900, y=550)


    def upload_image(self, size, img, image_n_path,  path_lb):
        try:
            self.path_img.set(filedialog.askopenfilename(
                initialdir='./src/',
                title='Selecciona una imagen',
                filetypes=(('Archivos de imagen', '*.bmp *.png'), ('Todos los archivos', '*.*'))
            ))
            image = lib.resize_image(self.path_img.get(), size)
            if image_n_path == 1:
                self.image1_path = self.path_img.get()
            else:
                self.image2_path = self.path_img.get()
            path_lb.config(text=self.path_img.get())
            img.config(image=image)
            img.image = image
        except ValueError:
            print('Hubo un error al cargar la imagen')

    def save_image(self):
        try:
            file = filedialog.asksaveasfile(
                mode='w',
                defaultextension=".png",
                filetypes=[("png", "*.png"), ("All files", "*.*")]
            )
            if file is None:
                return
            libK.saveImgTk(self.image_resultant, file)
        except ValueError:
            print('Hubo un error inesperado')

    def process(self):
        op = self.combo_operation.get()
        if op in self.operations:
            if op == self.operations[0]:
                result = libK.resize_image_dir(Image.fromarray(libK.raizFilter(self.image1_path)), self.size_image)
                self.image_resultant = result
            elif op == self.operations[1]:
                result = libK.resize_image_dir(Image.fromarray(libK.expFilter(self.image1_path)), self.size_image)
                self.image_resultant = result
            elif op == self.operations[2]:
                result = libK.resize_image_dir(Image.fromarray(
                    libK.linearPartialFiler(self.image1_path, self.hSlider.getValues()[0], self.hSlider.getValues()[1])),
                                               self.size_image)
                self.image_resultant = result

            self.lb_img3.config(image=result)
            self.lb_img3.image = result
        else:
            messagebox.showerror(
                'Campos incompletos',
                'Complete correctamente los campos de operacion y formato antes de continua.'
            )

app = App()
app.root.mainloop()