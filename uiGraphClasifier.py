import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def render_plot():
    clear_plot()
    # Leer valores de los campos de texto
    saveFile = save_file_entry.get().strip()
    fileName = file_name_entry.get().strip()

    # Construir las rutas
    csvFilePath = f'./txtFiles/{fileName}'
    ruta_carpeta = f'./graficas/{saveFile}'
    archivo_plot  = 'graph.png'
    graph_path = os.path.join(ruta_carpeta, archivo_plot)

    if not os.path.isfile(csvFilePath):
        messagebox.showerror("Error", f'El archivo de origen no existe: {csvFilePath}')
        return

    # Leer datos
    data = pd.read_csv(csvFilePath)

    # Convertir y filtrar datos
    data['Temp'] = pd.to_numeric(data['Temp'], errors='coerce')
    max_temp = 1500
    data_filtered = data[data['Temp'] <= max_temp]
    data_filtered['Temp'] = data_filtered['Temp'] / 25.6

    # Preparar datos para graficar
    day = data_filtered[['tDays']]
    temp = data_filtered[['Temp']]
    energy = np.sqrt(data_filtered['Energy'])

    # Crear la gráfica
    os.makedirs(ruta_carpeta, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(8, 6))
    # Graficar la temperatura en el eje izquierdo (Temp vs Actual Day)
    ax1.plot(day, temp, color='g', label='Temperature')
    ax1.set_xlabel('Actual Day')
    ax1.set_ylabel('Temperature', color='g')
    ax1.tick_params(axis='y', labelcolor='g')

    ax2 = ax1.twinx()
    ax2.plot(day, energy, color='b', label='Energy')
    ax2.set_ylabel('Energy', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    plt.yscale('log')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

    # Mostrar la gráfica en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def clear_plot():
    # Limpiar la gráfica actual en la interfaz
    for widget in plot_frame.winfo_children():
        widget.destroy()

def classify_graph():
    saveFile = save_file_entry.get().strip()
    comportamiento = "-"+comportamiento_entry.get().strip()

    # Construir las rutas
    ruta_carpeta = f'./graficas/{saveFile}'
    new_folder_path = ruta_carpeta + comportamiento 
    if not os.path.exists(new_folder_path):
        move_csv()
        # Renombrar la carpeta
        os.rename(ruta_carpeta, new_folder_path)
    else:
        messagebox.showwarning("Advertencia", f'La carpeta de destino ya existe: {new_folder_path}')

def move_csv():
    # Leer valores de los campos de texto
    saveFile = save_file_entry.get().strip()
    fileName = file_name_entry.get().strip()

    # Construir las rutas
    csvFilePath = f'./txtFiles/{fileName}'
    ruta_carpeta = f'./graficas/{saveFile}'
    # Mover el archivo CSV
    new_csv_file_path = os.path.join(ruta_carpeta, f'{fileName}')
    shutil.move(csvFilePath, new_csv_file_path)

def save_plot():
    # Leer valores de los campos de texto
    saveFile = save_file_entry.get().strip()
    fileName = file_name_entry.get().strip()

    # Construir las rutas
    csvFilePath = f'./txtFiles/{fileName}'
    ruta_carpeta = f'./graficas/{saveFile}'
    archivo_plot  = 'graph.png'
    graph_path = os.path.join(ruta_carpeta, archivo_plot)
    
    # Guardar la gráfica actual
    plt.savefig(graph_path, format='png')
    classify_graph()

# Crear la ventana principal
root = tk.Tk()
root.title("Clasificador de datos")

# Crear el marco para la gráfica
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Campos de entrada
tk.Label(root, text="Save File:").pack(pady=5)
save_file_entry = tk.Entry(root)
save_file_entry.pack(pady=5)

tk.Label(root, text="File Name:").pack(pady=5)
file_name_entry = tk.Entry(root)
file_name_entry.pack(pady=5)

tk.Label(root, text="Comportamiento:").pack(pady=5)
comportamiento_entry = tk.Entry(root)
comportamiento_entry.pack(pady=5)

# Botones
tk.Button(root, text="Render Gráfica", command=render_plot, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
tk.Button(root, text="Guardar Gráfica", command=save_plot, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

root.mainloop()
