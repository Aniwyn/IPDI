import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font

import imageio.v2 as imageio
import numpy as np

from src import a_lib as lib

import sv_ttk


class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Introduccion al Procesamiento Digital de Imagenes - TP4")
        self.root.geometry('1080x500')
        self.style = ttk.Style()
        sv_ttk.use_light_theme()
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both')

        self.path_img = StringVar()
        self.size_image = 340
        self.image_resultant = ''
        self.operations = ['Plano', 'Bartlett', 'Gaussiano', 'Laplaciano', 'Sobel']
        self.operations_a = ['Plano', 'Bartlett', 'Gaussiano']
        self.operations_b = ['Laplaciano']
        self.operations_c = ['Sobel']
        self.format_a = ['3x3', '5x5', '7x7']
        self.format_b = ['4 vecino', '8 vecino']
        self.format_c = ['Norte', 'Noreste', 'Este', 'Sureste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste']

        self.image1_path = '../../resource/Charly.bmp'
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
        button_upload_1.place(x=15, y=360)
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
        self.lb_img3.place(x=725, y=15)

        font_lb = Font(frame, family='Segoe UI', size=12)

        self.lb_operation = Label(frame, text='Operación', anchor='w', font=font_lb)
        self.lb_operation.place(x=15, y=420)
        self.combo_operation = ttk.Combobox(frame, state='readonly', values=self.operations)
        self.combo_operation.place(x=15, y=450)

        self.lb_format = Label(frame, text='Formato', anchor='w', font=font_lb)
        self.lb_format.place(x=250, y=420)
        self.combo_format = ttk.Combobox(frame, state='disabled')
        self.combo_format.place(x=250, y=450)

        self.combo_operation.bind(
            '<<ComboboxSelected>>',
            lambda _: self.selection_changed(self.combo_operation.get())
        )

        button_process = ttk.Button(
            frame,
            text="Calcular",
            width=10,
            command=lambda: self.process()
        )
        button_process.place(x=480, y=450)

        button_process = ttk.Button(
            frame,
            text="Guardar",
            width=10,
            command=lambda: self.save_image()
        )
        button_process.place(x=840, y=450)

        button_process = ttk.Button(
            frame,
            text="Salir",
            width=10,
            command=lambda: self.root.quit()
        )
        button_process.place(x=960, y=450)

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

    def selection_changed(self, option):
        self.combo_format.config(values=[''])
        self.combo_format.current(0)
        if option in self.operations_a:
            self.combo_format.config(
                state='readonly',
                values=self.format_a
            )
        elif option in self.operations_b:
            self.combo_format.config(
                state='readonly',
                values=self.format_b
            )
        elif option in self.operations_c:
            self.combo_format.config(
                state='readonly',
                values=self.format_c
            )

    def process(self):
        op = self.combo_operation.get()
        fmt = self.combo_format.get()

        if op in self.operations_a and fmt in self.format_a:
            if op == self.operations_a[0] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'BoxBlur3', self.size_image)
            elif op == self.operations_a[0] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'BoxBlur5', self.size_image)
            elif op == self.operations_a[0] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'BoxBlur7', self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'Bartlett3', self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'Bartlett5', self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'Bartlett7', self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'GaussianBlur3', self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'GaussianBlur5', self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'GaussianBlur7', self.size_image)
        elif op in self.operations_b and fmt in self.format_b:
            if op == self.operations_b[0] and fmt == self.format_b[0]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'Laplace4', self.size_image)
            elif op == self.operations_b[0] and fmt == self.format_b[1]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'Laplace8', self.size_image)
        elif op in self.operations_c and fmt in self.format_c:
            if op == self.operations_c[0] and fmt == self.format_c[0]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelN', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[1]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelNE', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[2]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelE', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[3]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelSE', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[4]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelS', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[5]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelSO', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[6]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelO', self.size_image)
            elif op == self.operations_c[0] and fmt == self.format_c[7]:
                result, self.image_resultant = lib.convolve_operation(self.image1_path, 'SobelNO', self.size_image)
        else:
            messagebox.showerror(
                'Campos incompletos',
                'Complete correctamente los campos de operacion y formato antes de continua.'
            )
        self.lb_img3.config(image=result)
        self.lb_img3.image = result


app = App()
app.root.mainloop()
