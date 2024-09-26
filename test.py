import pandas as pd
import os

# Directorio donde se encuentran los archivos CSV
directorio_csv = 'graficas'

# Obtener la lista de todos los archivos CSV en el directorio
archivos_csv = [os.path.join(directorio_csv, archivo) for archivo in os.listdir(directorio_csv) if archivo.endswith('.csv')]

# DataFrame vacío para almacenar todos los datos
df_completo = pd.DataFrame()

for archivo in archivos_csv:
    # Leer el archivo CSV
    df = pd.read_csv(archivo)
    # Concatenar el DataFrame actual con el DataFrame completo
    df_completo = pd.concat([df_completo, df], ignore_index=True)

# Guardar el DataFrame completo en un único archivo CSV
df_completo.to_csv('comportamiento_completo.csv', index=False)

print("Todos los archivos se han combinado y guardado en 'graficas/comportamiento_completo.csv'.")
