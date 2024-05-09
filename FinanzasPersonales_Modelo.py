import pandas as pd
from FinanzasPersonales_Funciones import clasificar_transaccion

# Cargar el archivo Excel en un DataFrame
ruta_archivo = "C:/Users/esteb/Documents/Automatización/PruebaTransacciones.xlsx"
datos = pd.read_excel(ruta_archivo)

datos["Categoría"] = ""

# Iterar por cada fila del DataFrame y clasificar la transacción
for indice, fila in datos.iterrows():
    descripcion = fila["Descripción"]
    categoria = clasificar_transaccion(descripcion)
    datos.at[indice, "Categoría"] = categoria

# Guardar el DataFrame con las categorías asignadas en un nuevo archivo Excel
ruta_archivo_salida = "C:/Users/esteb/Documents/Automatización/PruebaTransacciones_con_categorias.xlsx"
datos.to_excel(ruta_archivo_salida, index=False)

print("Se ha guardado el DataFrame con las categorías asignadas en:", ruta_archivo_salida)