import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
from src import a_lib as lib

import sv_ttk


class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Introduccion al Procesamiento Digital de Imagenes - TP2")
        self.root.geometry('1080x500')
        self.style = ttk.Style()
        sv_ttk.use_light_theme()
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both')

        self.path_img = StringVar()
        self.size_image = 340
        self.image_resultant = ''
        self.operations_a = ['Suma', 'Resta', 'Multiplicación', 'División']
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
        button_upload_1.place(x=15, y=360)
        self.path1.place(x=120, y=365)

        self.image2_path = '../../resource/1024x600/2.png'  # asdasdasdasd
        image2 = lib.resize_image(self.image2_path, self.size_image)
        self.lb_img2 = Label(
            self.root,
            image=image2,
            width=self.size_image,
            height=self.size_image,
            borderwidth=0
        )
        self.lb_img2.image = image2
        self.path2 = Label(frame, text='', padx=5, width=31, anchor='w')
        button_upload_2 = ttk.Button(
            frame,
            text="Seleccionar...",
            width=10,
            command=lambda: self.upload_image(self.size_image, self.lb_img2, 2, self.path2)
        )
        self.lb_img2.place(x=370, y=15)
        button_upload_2.place(x=370, y=360)
        self.path2.place(x=475, y=365)

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

        operations = ['Suma', 'Resta', 'Multiplicación', 'División', 'Lighter', 'Darker']
        font_lb = Font(frame, family='Segoe UI', size=12)

        self.lb_operation = Label(frame, text='Operación', anchor='w', font=font_lb)
        self.lb_operation.place(x=15, y=420)
        self.combo_operation = ttk.Combobox(frame, state='readonly', values=operations)
        self.combo_operation.place(x=15, y=450)

        self.lb_format = Label(frame, text='Formato', anchor='w', font=font_lb)
        self.lb_format.place(x=250, y=420)
        self.combo_format = ttk.Combobox(frame, state='disabled')
        self.combo_format.place(x=250, y=450)

        self.combo_operation.bind('<<ComboboxSelected>>', lambda _: self.selection_changed(self.combo_operation.get()))

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

    def process(self):
        op = self.combo_operation.get()
        fmt = self.combo_format.get()
        if op in self.operations_a and fmt in self.format_a:
            if op == self.operations_a[0] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.rgb_operations_clamp(self.image1_path, self.image2_path,
                                                                        '+', self.size_image)
            elif op == self.operations_a[0] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.rgb_operations_prom(self.image1_path, self.image2_path, '+',
                                                                       self.size_image)
            elif op == self.operations_a[0] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.yiq_operations_clamp(self.image1_path, self.image2_path, '+',
                                                                        self.size_image)
            elif op == self.operations_a[0] and fmt == self.format_a[3]:
                result, self.image_resultant = lib.yiq_operations_prom(self.image1_path, self.image2_path, '+',
                                                                       self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.rgb_operations_clamp(self.image1_path, self.image2_path, '-',
                                                                        self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.rgb_operations_prom(self.image1_path, self.image2_path, '-',
                                                                       self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.yiq_operations_clamp(self.image1_path, self.image2_path, '-',
                                                                        self.size_image)
            elif op == self.operations_a[1] and fmt == self.format_a[3]:
                result, self.image_resultant = lib.yiq_operations_prom(self.image1_path, self.image2_path, '-',
                                                                       self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.rgb_operations_clamp(self.image1_path, self.image2_path, '*',
                                                                        self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.rgb_operations_prom(self.image1_path, self.image2_path, '*',
                                                                       self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.yiq_operations_clamp(self.image1_path, self.image2_path, '*',
                                                                        self.size_image)
            elif op == self.operations_a[2] and fmt == self.format_a[3]:
                result, self.image_resultant = lib.yiq_operations_prom(self.image1_path, self.image2_path, '*',
                                                                       self.size_image)
            elif op == self.operations_a[3] and fmt == self.format_a[0]:
                result, self.image_resultant = lib.rgb_operations_clamp(self.image1_path, self.image2_path, '/',
                                                                        self.size_image)
            elif op == self.operations_a[3] and fmt == self.format_a[1]:
                result, self.image_resultant = lib.rgb_operations_prom(self.image1_path, self.image2_path, '/',
                                                                       self.size_image)
            elif op == self.operations_a[3] and fmt == self.format_a[2]:
                result, self.image_resultant = lib.yiq_operations_clamp(self.image1_path, self.image2_path, '/',
                                                                        self.size_image)
            elif op == self.operations_a[3] and fmt == self.format_a[3]:
                result, self.image_resultant = lib.yiq_operations_prom(self.image1_path, self.image2_path, '/',
                                                                       self.size_image)
            self.lb_img3.config(image=result)
            self.lb_img3.image = result
        elif op in self.operations_b and fmt in self.format_b:
            if op == self.operations_b[0] and fmt == self.format_b[0]:
                result, self.image_resultant = lib.rgb_operations_clamp(self.image1_path, self.image2_path, 'light',
                                                                        self.size_image)
            elif op == self.operations_b[0] and fmt == self.format_b[1]:
                result, self.image_resultant = lib.yiq_operations_clamp(self.image1_path, self.image2_path, 'light',
                                                                        self.size_image)
            elif op == self.operations_b[1] and fmt == self.format_b[0]:
                result, self.image_resultant = lib.rgb_operations_clamp(self.image1_path, self.image2_path, 'dark',
                                                                        self.size_image)
            elif op == self.operations_b[1] and fmt == self.format_b[1]:
                result, self.image_resultant = lib.yiq_operations_clamp(self.image1_path, self.image2_path, 'dark',
                                                                        self.size_image)
            self.lb_img3.config(image=result)
            self.lb_img3.image = result
        else:
            messagebox.showerror(
                'Campos incompletos',
                'Complete correctamente los campos de operacion y formato antes de continua.'
            )


app = App()
app.root.mainloop()
