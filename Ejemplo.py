
import re
from datetime import datetime
import PyPDF2
import pandas as pd
import os
import email
import imaplib
import locale
from locale import atof
# Reemplaza esto con la ruta de la carpeta que contiene los archivos PDF
carpeta = "C:/Users/esteb/Documents/Automatización/Extractos/Finanzas_Bancolombia"

# Reemplaza esto con la contraseña real del PDF
password = '1001367767'

# Lista para almacenar el texto de todos los archivos PDF
textos = []

# Iterar a través de cada archivo en la carpeta
for archivo in os.listdir(carpeta):
    ruta_archivo = os.path.join(carpeta, archivo)

    # Asegurarse de que el archivo sea un PDF
    if ruta_archivo.lower().endswith('.pdf') and 'tarjeta' in archivo.lower():
        # Abrir el archivo PDF
        with open(ruta_archivo, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            # Verificar si el archivo PDF está encriptado
            if reader.is_encrypted:
                # Intentar desencriptar el PDF
                if reader.decrypt(password):
                    # Inicializar una variable para almacenar el texto de todas las páginas
                    texto_completo = ''
                    # Extraer texto de cada página y concatenarlo
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            texto_completo += text + '\n'  # Añadir un salto de línea entre páginas
                    # Añadir el texto completo del PDF a la lista 'textos'
                    textos.append(texto_completo)
                else:
                    print(f"Contraseña incorrecta o imposible desencriptar el PDF: {archivo}")
            else:
                print(f"El PDF no está encriptado: {archivo}")
# Supongamos que esta es tu lista de textos (cada elemento es el contenido de un archivo PDF)
lista_textos = textos  # Reemplaza esto con tu lista de textos
df_transacciones_totales = pd.DataFrame()
regex_autorizacion = re.compile(r"(\d+)")
regex_fecha = re.compile(r"(\d{2}/\d{2}/\d{4})")
regex_descripcion = re.compile(r"\d{2}/\d{2}/\d{4} ([A-Z ÑÁÉÍÓÚ0-9-]+(?=\s\d+,\d{2}))")
regex_valor = re.compile(r"(\d{2}/\d{2}/\d{4} [A-Z ÑÁÉÍÓÚ0-9-]+\s)(\d{1,3}(?:,\d{3})*\.\d{2})")
regex_cuotas = re.compile(r"(\d+/\d+)$")
# Procesar cada texto en la lista
for i, texto in enumerate(lista_textos):
    patron_bloque_transacciones = re.compile(
    r"FacturadaCargos y Abonos Saldo a Diferir Cuotas\n(.*?)\n\"Defensor del Consumidor Financiero:",
    re.DOTALL)
    bloque_transacciones = re.search(patron_bloque_transacciones, texto)
    if bloque_transacciones:
        print("si")
        texto_transacciones = bloque_transacciones.group(1)
        transacciones= texto_transacciones.strip().split('\n')
        for transaccion in transacciones:
            numero_autorizacion = regex_autorizacion.search(transaccion).group(1)
            fecha_transaccion = regex_fecha.search(transaccion).group(1)
            descripcion = regex_descripcion.search(transaccion).group(1)
            valor_original = regex_valor.search(transaccion).group(1)
            numero_cuotas = regex_cuotas.search(transaccion).group(1)
            datos_transacciones.append({
                'Número de Autorización': numero_autorizacion,
                'Fecha de Transacción': fecha_transaccion,
                'Descripción': descripcion,
                'Valor Original': valor_original,
                'Número de Cuotas': numero_cuotas
            })

            regex_autorizacion = re.compile(r"(\d+)")
            transacciones = patron_transacciones.findall(texto_transacciones)
            df_temp = pd.DataFrame(transacciones, columns=['Número de Autorización', 'Fecha de Transacción', 'Descripción', 'Valor Original', 'Número de Cuotas'])
            df_temp['Archivo'] = i  # Añadir un identificador del archivo
            df_transacciones_totales = pd.concat([df_transacciones_totales, df_temp])


#df_transacciones_totales['Valor Original'] = df_transacciones_totales['Valor Original'].str.replace(',', '').astype(float)
#df_transacciones_totales['Fecha de Transacción'] = pd.to_datetime(df_transacciones_totales['Fecha de Transacción'], format='%d/%m/%Y')
print(transacciones)