import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font

import numpy as np
from RangeSlider import RangeSliderH
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src import a_lib as lib
from PIL import Image
from src import PixelArithmetic as libK

import sv_ttk

class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Introduccion al Procesamiento Digital de Imagenes - TP4")
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
        self.format_a = ['3x3', '5x5', '7x7']
        self.format_b = ['RGB', 'YIQ']

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

        operations = ['Raiz', 'Exponencial', 'Linear']
        font_lb = Font(frame, family='Segoe UI', size=12)

        self.lb_operation = Label(self.root, text='Filtros', anchor='w', font=font_lb)
        self.lb_operation.place(x=550, y=130)
        self.combo_operation = ttk.Combobox(self.root, width=10, state='readonly', values=operations)
        self.combo_operation.place(x=550, y=100)

        self.combo_operation.bind('<<ComboboxSelected>>',
                                  lambda _: self.graficar_funcion(self.hSlider.getValues()[0], self.hSlider.getValues()[1]))

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

        lb_histograma = tk.Label(
            frame,
            width=50,
            height=20
        )
        lb_histograma.place(x=370, y=15)

        hLeft = tk.DoubleVar(value=0.2)
        hRight = tk.DoubleVar(value=0.85)
        self.hSlider = RangeSliderH(frame, [hLeft, hRight], padX=10,step_size=0.025, Width=300, Height=58, font_size=14)
        self.hSlider.place_forget()


app = App()
app.root.mainloop()