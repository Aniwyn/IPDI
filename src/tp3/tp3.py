import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src import a_lib as lib
from PIL import ImageTk, Image
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
        self.operations = ['Raiz', 'Exponencial', 'Linear']
        self.operations_a = ['Raiz', 'Exponencial', 'Linear']
        self.operations_b = ['Lighter', 'Darker']
        self.format_a = ['RGB - Clampeada', 'RGB - Promediada', 'YIQ - Clampeada', 'YIQ - Promediada']
        self.format_b = ['RGB', 'YIQ']

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
            frame,
            text="Seleccionar...",
            width=10,
            command=lambda: self.upload_image(self.size_image, self.lb_img1, 1, self.path1)
        )
        self.lb_img1.place(x=15, y=15)
        button_upload_1.place(x=830, y=140)
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
        self.lb_img3.place(x=430, y=15)

        operations = ['Raiz', 'Exponencial', 'Linear']
        font_lb = Font(frame, family='Segoe UI', size=12)

        self.lb_operation = Label(frame, text='Filtros', anchor='w', font=font_lb)
        self.lb_operation.place(x=830, y=210)
        self.combo_operation = ttk.Combobox(frame, state='readonly', values=operations)
        self.combo_operation.place(x=830, y=180)

        button_process = ttk.Button(
            frame,
            text="Calcular",
            width=10,
            command=lambda: self.process()
        )
        button_process.place(x=830, y=100)

        button_process = ttk.Button(
            frame,
            text="Guardar",
            width=10,
            command=lambda: self.save_image()
        )
        button_process.place(x=960, y=100)

        button_process = ttk.Button(
            frame,
            text="Salir",
            width=10,
            command=lambda: self.root.quit()
        )
        button_process.place(x=960, y=140)


        lb_histograma = tk.Label(
            frame,
            width=50,
            height=20
        )
        lb_histograma.place(x=370, y=15)

        lb_min = Label(frame, text='Min', anchor='w', font=font_lb).place(x=900, y=210)
        self.entry_min = Entry(frame, width=6)
        self.entry_min.place(x=900, y=240)
        lb_max = Label(frame, text='Max', anchor='w', font=font_lb).place(x=980, y=210)
        self.entry_max = Entry(frame, width=6)
        self.entry_max.place(x=980, y=240)


    def upload_image(self, size, img, image_n_path, path_lb):
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
            lib.save_image(self.image_resultant, file)
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
                result = ImageTk.PhotoImage(Image.fromarray(libK.linearPartialFiler(self.image1_path, 5, self.entry_min.get(),self.entry_max.get())))
                self.image_resultant = result

            self.lb_img3.config(image=result)
            self.lb_img3.image = result

            plt.clf()
            self.mostrar_histograma(libK.RGBtoYIQ(self.image1_path)[:,:,0], 15, 300)
            #self.mostrar_histograma(libK.RGBtoYIQ_array(libK.raizFilter(self.image1_path))[:,:,0], 400, 300)
        else:
            messagebox.showerror(
                'Campos incompletos',
                'Complete correctamente los campos de operacion y formato antes de continua.'
            )

    def mostrar_histograma(self, datos, x, y):
        print(np.max(datos), np.min(datos))
        datos = datos.flatten()
        hist, bin_edges = np.histogram(datos, bins=10)
        porcentajes = (hist / len(datos)) * 100
        print(hist)

        # Crea el histograma
        plt.bar(bin_edges[:-1], porcentajes, width=0.1, color='blue', alpha=0.7)
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.title('Histograma de Datos')
        plt.gca().set_ylim(0.0, 100.0)

        plt.gcf().set_size_inches(4, 2.5)

        # Crea un widget FigureCanvasTkAgg para incorporar el gráfico en el widget Label
        canvas = FigureCanvasTkAgg(plt.gcf())
        canvas.get_tk_widget().place(x=x, y=y)
        canvas.draw()

app = App()
app.root.mainloop()