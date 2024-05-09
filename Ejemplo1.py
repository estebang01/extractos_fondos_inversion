from datetime import datetime
import PyPDF2
import pandas as pd
import re
import os

# Configuración inicial
carpeta = "C:/Users/esteb/Documents/Automatización/Extractos/Finanzas_Bancolombia"
df_transacciones_totales = pd.DataFrame()

# Expresiones regulares
regex_autorizacion = re.compile(r"(\d+)")
regex_fecha = re.compile(r"(\d{2}/\d{2}/\d{4})")
regex_descripcion = re.compile(r"\d{2}/\d{2}/\d{4} ([A-Z ÑÁÉÍÓÚ0-9-]+(?=\s\d+,\d{2}))")
regex_valor = re.compile(r"(\d{2}/\d{2}/\d{4} [A-Z ÑÁÉÍÓÚ0-9-]+\s)(\d{1,3}(?:,\d{3})*\.\d{2})")
regex_cuotas = re.compile(r"(\d+/\d+)$")

# Iterar a través de cada archivo en la carpeta
for i, archivo in enumerate(os.listdir(carpeta)):
    ruta_archivo = os.path.join(carpeta, archivo)
    if ruta_archivo.lower().endswith('.pdf') and 'tarjeta' in archivo.lower():
        with open(ruta_archivo, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if reader.is_encrypted and not reader.decrypt(password):
                print(f"Contraseña incorrecta o imposible desencriptar el PDF: {archivo}")
                continue

            texto_completo = ''.join([page.extract_text() + '\n' for page in reader.pages if page.extract_text()])

        # Extraer las transacciones
        patron_bloque_transacciones = re.compile(
            r"FacturadaCargos y Abonos Saldo a Diferir Cuotas\n(.*?)\n\"Defensor del Consumidor Financiero:",
            re.DOTALL)
        bloque_transacciones = re.search(patron_bloque_transacciones, texto_completo)
        if bloque_transacciones:
            texto_transacciones = bloque_transacciones.group(1)
            transacciones = texto_transacciones.strip().split('\n')
            for transaccion in transacciones:
                numero_autorizacion = regex_autorizacion.search(transaccion).group(1)
                fecha_transaccion = regex_fecha.search(transaccion).group(1)
                descripcion = regex_descripcion.search(transaccion).group(1)
                valor_original = regex_valor.search(transaccion).group(1)
                #numero_cuotas = regex_cuotas.search(transaccion).group(1)

                df_temp = pd.DataFrame([{
                    'Número de Autorización': numero_autorizacion,
                    'Fecha de Transacción': fecha_transaccion,
                    'Descripción': descripcion,
                    'Valor Original': valor_original,
                    #'Número de Cuotas': numero_cuotas,
                    'Archivo': i
                }])
                df_transacciones_totales = pd.concat([df_transacciones_totales, df_temp])

# Mostrar el DataFrame resultante
print(df_transacciones_totales)

