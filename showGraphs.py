import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Función para abrir una ventana nueva y mostrar la gráfica ampliada
def open_full_image(image_path, folder_name):
    # Crear una nueva ventana para mostrar la imagen ampliada
    top = tk.Toplevel()
    top.title(f"Gráfica completa de la carpeta: {folder_name}")

    # Cargar la imagen completa
    img = Image.open(image_path)
    img = img.resize((800, 600), Image.Resampling.LANCZOS)  # Cambia el tamaño si es necesario
    img_tk = ImageTk.PhotoImage(img)

    # Mostrar la imagen
    full_image_label = tk.Label(top, image=img_tk)
    full_image_label.image = img_tk  # Necesario para mantener la referencia de la imagen
    full_image_label.pack()

# Función para cargar las miniaturas de las gráficas en una cuadrícula
def load_thumbnails():
    folder_path = './graficas'
    
    # Limpiar el marco antes de cargar nuevas miniaturas
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Obtener todas las carpetas
    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    row = 0
    col = 0
    for folder in folders:
        folder_full_path = os.path.join(folder_path, folder)
        
        # Buscar archivos .png en la carpeta
        for file in os.listdir(folder_full_path):
            if file.endswith(".png"):
                graph_path = os.path.join(folder_full_path, file)

                # Cargar la imagen como miniatura
                img = Image.open(graph_path)
                img = img.resize((100, 80), Image.Resampling.LANCZOS)  # Tamaño de la miniatura
                img_tk = ImageTk.PhotoImage(img)

                # Crear un botón con la imagen de miniatura
                thumb_button = tk.Button(grid_frame, image=img_tk, command=lambda p=graph_path, f=folder: open_full_image(p, f))
                thumb_button.image = img_tk  # Necesario para mantener la referencia de la imagen
                thumb_button.grid(row=row, column=col, padx=10, pady=10)

                # Mostrar el nombre de la carpeta debajo de cada miniatura
                folder_label = tk.Label(grid_frame, text=folder)
                folder_label.grid(row=row+1, column=col, padx=10, pady=5)

                # Controlar el salto de fila cada 4 columnas
                col += 1
                if col > 3:  # 4 columnas por fila
                    col = 0
                    row += 2

# Crear la ventana principal
root = tk.Tk()
root.title("Visualizador de Gráficas")

# Crear un marco para el canvas y la barra de desplazamiento
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

# Crear un canvas que contendrá el frame con miniaturas
canvas = tk.Canvas(canvas_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Añadir la barra de desplazamiento
scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configurar el canvas para interactuar con la barra de desplazamiento
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Crear el frame dentro del canvas para contener las miniaturas
grid_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=grid_frame, anchor="nw")

# Botón para cargar las miniaturas
load_button = tk.Button(root, text="Cargar Miniaturas", command=load_thumbnails)
load_button.pack(pady=10)

# Iniciar el loop de la aplicación
root.mainloop()
