import pandas as pd

# Crear un DataFrame de ejemplo
data = {
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50]
}

df = pd.DataFrame(data)

# Multiplicar la columna A por la columna B para obtener la columna C
df['C'] = df['A'] * df['B']

# Mostrar el resultado
print(df)