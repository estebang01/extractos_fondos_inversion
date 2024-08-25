import re
from datetime import datetime
import PyPDF2
import pandas as pd
import os
import email
import imaplib
import locale
from locale import atof
import json

json_file_path= "C:/Users/esteb/Documents/Automatizacion/MutualFund_Info.json"
with open(json_file_path, 'r') as file:
    # Carga los datos JSON del archivo
    key_info = json.load(file)


# Reemplaza esto con la ruta de la carpeta que contiene los archivos PDF
carpeta = key_info["Path_PersonalFinance"]

# Reemplaza esto con la contraseña real del PDF
password = key_info["Id"]

# Lista para almacenar el texto de todos los archivos PDF
textos = []

# Iterar a través de cada archivo en la carpeta
for archivo in os.listdir(carpeta):
    ruta_archivo = os.path.join(carpeta, archivo)

    # Asegurarse de que el archivo sea un PDF
    if ruta_archivo.lower().endswith('.pdf') and 'tarjeta' in archivo.lower():
        # Abrir el archivo PDF
        #print(f"Leyendo el archivo: {archivo}") #Identificar si está abriendo el archivo correctamente
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
                    #print("Texto extraído correctamente.") #Lee bien el texto
                else:
                    print(f"Contraseña incorrecta o imposible desencriptar el PDF: {archivo}")
            else:
                print(f"El PDF no está encriptado: {archivo}")
# Supongamos que esta es tu lista de textos (cada elemento es el contenido de un archivo PDF)
lista_textos = textos  # Reemplaza esto con tu lista de textos
df_transacciones_totales = pd.DataFrame()

def eliminar_numeros_y_puntos_si_abono(texto):
    if "ABONO SUCURSAL VIRTUAL" in texto or "CUOTA DE MANEJO" in  texto or "TRASLADO SALDO A FAVOR" in  texto or "APLICACION SALDO A FAVO" in  texto or "AJUSTE MANUAL A FAVOR" in  texto or "COMISION TARJETA REEXPEDIDA" in  texto or "IVA POR REEXPEDICION" in  texto or "COMISION AVANCE CORRESP" in  texto:
        return re.sub(r'[\d.-]+', '', texto)
    else:
        return texto

regex_autorizacion = re.compile(r"([A-Za-z0-9]{6})")
regex_fecha = re.compile(r"(\d{2}/\d{2}/\d{4})")
regex_descripcion = re.compile(r"\d{2}/\d{2}/\d{4}\s+([A-Za-z ÑÁÉÍÓÚñáéíóú0-9-.]+)")
regex_valor_dollar = re.compile(r"(\d{2}/\d{2}/\d{4} [A-Za-z ÑÁÉÍÓÚñáéíóú0-9\-/\*]+)\.(-?\d+(?:,\d{3})*\.\d{2})")
regex_valor = re.compile(r"(\d{2}/\d{2}/\d{4} .+?)\s(-?\d{1,3}(?:,\d{3})*\.\d{2})")
regex_cuotas = re.compile(r"(\d+/\d+)$")
marcador_fin_pagina = "Pag."
# Procesar cada texto en la lista
for i, texto_completo in enumerate(lista_textos):
    paginas=texto_completo.split(marcador_fin_pagina)
    for j, texto in enumerate(paginas):
        patron_bloque_transacciones_1 = re.compile(
        r"FacturadaCargos y Abonos Saldo a Diferir Cuotas\s+(.*?)\s+\"Defensor del Consumidor Financiero:",
        re.DOTALL)
        patron_bloque_transacciones_2 = re.compile(
        r"FacturadaCargos y Abonos Saldo a Diferir Cuotas\s+(.*?)\s+Defensor del Consumidor Financiero:",
        re.DOTALL)
        patron_bloque_transacciones_3 = re.compile(
        r"FacturadaCargos y Abonos Saldo a Diferir Cuotas\s+(.*?)\s+\"En casos de inconsistencias ",
        re.DOTALL)
        patron_bloque_transacciones_4 = re.compile(
        r"FacturadaCargos y Abonos Saldo a Diferir Cuotas\s+(.*?)\sDCF:defensor@bancolombia.com.co",
        re.DOTALL)
        bloque_transacciones = re.search(patron_bloque_transacciones_4, texto)
        if not bloque_transacciones:
            bloque_transacciones = re.search(patron_bloque_transacciones_2, texto)
            if not bloque_transacciones:
                bloque_transacciones = re.search(patron_bloque_transacciones_3, texto)
                if not bloque_transacciones:
                    bloque_transacciones = re.search(patron_bloque_transacciones_1, texto)
        if bloque_transacciones:
            texto_transacciones = bloque_transacciones.group(1)
            transacciones= texto_transacciones.strip().split('\n')
            for transaccion in transacciones:
                match_fecha = regex_fecha.search(transaccion)
                match_descripcion = regex_descripcion.search(transaccion)

                match_valor = regex_valor.search(transaccion)
                if "VR MONEDA ORIG" in transaccion:
                    continue
                if "ABONO SUCURSAL VIRTUAL" in transaccion or "CUOTA DE MANEJO" in transaccion or "TRASLADO SALDO A FAVOR" in transaccion or "APLICACION SALDO A FAVO" in transaccion or "AJUSTE MANUAL A FAVOR" in transaccion or "COMISION TARJETA REEXPEDIDA" in transaccion or "IVA POR REEXPEDICION" in transaccion or "COMISION AVANCE CORRESP" in transaccion:
                    match_cuotas = 777
                else:
                    match_cuotas = regex_cuotas.search(transaccion)
                if "INTERESES CORRIENTES" in transaccion:
                    match_autorizacion= 0
                else:
                    match_autorizacion = regex_autorizacion.search(transaccion)
                
                    if match_autorizacion and match_fecha and match_descripcion and match_valor and match_cuotas:
                        numero_autorizacion = match_autorizacion.group(1)
                        fecha_transaccion = match_fecha.group(1)
                        descripcion = match_descripcion.group(1)
                        
                        valor_original_str = match_valor.group(2)
                
                        valor_original_float = atof(valor_original_str.replace(',', ''))
                        if match_cuotas != 777:
                            numero_cuotas = match_cuotas.group(1)
                        else:
                            numero_cuotas=match_cuotas
                        df_temp = pd.DataFrame([{
                            'Número de Autorización': numero_autorizacion,
                            'Fecha de Transacción': fecha_transaccion,
                            'Descripción': descripcion,
                            'Valor Original': valor_original_float,
                            "Número de Cuotas": numero_cuotas,
                            'Archivo': i
                        }])
                        df_transacciones_totales = pd.concat([df_transacciones_totales, df_temp])
                    else:
                        print("Transacción Internacional Anterior",transaccion)
df_transacciones_totales['Fecha de Transacción'] = pd.to_datetime(df_transacciones_totales['Fecha de Transacción'], format='%d/%m/%Y')

##Eliminar los números al final
def eliminar_numeros_final(texto):
    return re.sub(r'\d+$', '', texto)
df_transacciones_totales['Descripción'] = df_transacciones_totales['Descripción'].apply(eliminar_numeros_final)
df_transacciones_totales['Descripción'] = df_transacciones_totales['Descripción'].apply(eliminar_numeros_y_puntos_si_abono)

nombre_archivo = key_info["Path_DataBasePersonalFinance"]
df_transacciones_totales.to_excel(nombre_archivo, index=True, engine='openpyxl')

