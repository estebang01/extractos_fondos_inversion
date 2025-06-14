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
from dateutil.relativedelta import relativedelta


# Configuración del locale
locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')

# Función para convertir valores con el signo '-' al final
def convertir_a_numero(valor):
    if isinstance(valor, str):
        # Elimina cualquier espacio en blanco alrededor
        valor = valor.strip()
        
        # Verifica si el signo '-' está al final y lo mueve al principio
        if valor.endswith('-'):
            valor = '-' + valor[:-1]
        
        try:
            # Intenta convertir a número
            return locale.atof(valor)
        except ValueError:
            # Si la conversión falla, retorna el valor original
            return valor
    return valor

json_file_path= "C:/Users/esteb/Documents/Automatizacion/MutualFund_Info.json"
with open(json_file_path, 'r') as file:
    # Carga los datos JSON del archivo
    key_info = json.load(file)



nombre_archivo_excel = key_info["Path_DataBaseFunds"]


# Leer el archivo Excel existente (si existe) o crear un DataFrame vacío si no existe
df_existente = pd.read_excel(nombre_archivo_excel, index_col=0)  # Asegúrate de que los índices múltiples se mantengan
df_existente.index = pd.to_datetime(df_existente.index)
# Email credentials
email_user = key_info["email"]
email_pass = key_info["email_code"]

# Connect to the Gmail server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_user, email_pass)
mail.select('inbox')

# Obtener el primer día de hace dos meses
hoy = datetime.now()
fecha_dos_meses_atras = hoy - relativedelta(months=5)
primer_dia_mes = fecha_dos_meses_atras.replace(day=1).strftime('%d-%b-%Y')

# Search for emails from a specific sender received since the first day of two months ago
tipo, data = mail.search(None, f'(FROM "{key_info["bank_email"]}")')
tipo, data = mail.search(None, f'(FROM "{key_info["bank_email"]}" SINCE "{primer_dia_mes}")')

fondos_path = key_info["Path_MutualFunds"]
finanzas_personales_path = key_info["Path_PersonalFinance"]

# Make sure the directories exist
os.makedirs(fondos_path, exist_ok=True)
os.makedirs(finanzas_personales_path, exist_ok=True)
# Resto del código para procesar los correos y descargar los archivos...

for num in data[0].split():
    typ, msg_data = mail.fetch(num, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                # Check if part has Content-Disposition header (indicative of an attachment)
                if part.get('Content-Disposition') is not None:
                    filename = part.get_filename()
                    if filename:
                        # Determine the correct path based on the filename
                        if any(keyword in filename.upper() for keyword in ["FIDUCUENTA", "FIDURENTA", "RENTA_ACCIONES","RENTA_FIJAPLAZO"]):
                            filepath = os.path.join(fondos_path, filename)
                        else:
                            filepath = os.path.join(finanzas_personales_path, filename)

                        # Check if file already exists
                        if not os.path.isfile(filepath):
                            with open(filepath, 'wb') as fp:
                                fp.write(part.get_payload(decode=True))
                            print(f'Saved {filename}')
                        else:
                            print(f'File {filename} already exists. Skipping download.')

# Close the mail connection
mail.close()
mail.logout()


# Reemplaza esto con la ruta de la carpeta que contiene los archivos PDF
carpeta = key_info["Path_MutualFunds"]

# Reemplaza esto con la contraseña real del PDF
password = key_info["Id"]

# Lista para almacenar el texto de todos los archivos PDF
textos = []

# Iterar a través de cada archivo en la carpeta
for archivo in os.listdir(carpeta):
    ruta_archivo = os.path.join(carpeta, archivo)

    # Asegurarse de que el archivo sea un PDF
    if ruta_archivo.lower().endswith('.pdf'):
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

# Crear un DataFrame vacío para almacenar los resultados
df_resultados = pd.DataFrame(columns=["Fondo de Inversión", "Número", "Valor de la unidad", "Saldo Anterior", "Adiciones", "Retiros", "Rendimientos Netos", "Retención", "Saldo Final","Rentabilidad"])

# Patrones de expresiones regulares
patron_numero = re.compile(r'Cuenta de Inversión: (\d+)')
patron_valor_unidad = re.compile(r'Valor Unidad al Final: ([\d\.,]+)')
patron_saldoanterior = re.compile(r'SALDO ANTERIOR ADICIONES RETIROS\nVALOR EN PESOS VALOR EN UNIDADES VALOR EN PESOS VALOR EN PESOS\n(.+?)\n')
patron_rendimientos = re.compile(r'REND. NETOS RETENCIÓN NUEVO SALDO\nVALOR EN PESOS VALOR EN PESOS VALOR EN PESOS VALOR EN UNIDADES\n(.+?)\n')
patron_fecha = re.compile(r'Hasta: (\d+)')
patron_rentabilidad = re.compile(r'Rentabilidad Periodo:\s*([\d\.,\-+% ]+)\s*%')

# Procesar cada texto en la lista
for texto in lista_textos:
    numero = patron_numero.search(texto).group(1)
    valor_unidad = patron_valor_unidad.search(texto).group(1)
    rendimientoss= patron_rendimientos.search(texto).group(1)
    resultado_fecha = patron_fecha.search(texto).group(1)
    resultado_rentabilidad = patron_rentabilidad.search(texto).group(1)

# Verifica si el texto contiene "Pag. 2"
    if "Pág. 2" in texto:
    # Para documentos de dos páginas, toma la segunda coincidencia
        todas_coincidencias = patron_saldoanterior.findall(texto)
        saldoanterior = todas_coincidencias[1]
    else:
    # Para documentos de una página, toma la primera coincidencia
        saldoanterior = patron_saldoanterior.search(texto).group(1) if patron_saldoanterior.search(texto) else "No encontrado"

    if numero == '252000001274':
        fondo_inversion = "Renta Acciones"
    elif numero == '1111000544148':
        fondo_inversion = "Fidurenta"
    elif numero == '342000006519':
        fondo_inversion = "Fiducuenta"
    elif  numero == "252000011589" :
        fondo_inversion = "Renta Fija Plazo"
    else:
        fondo_inversion = "Otro Fondo"
    
# Saldo Anterior
    partes_saldoanterior=saldoanterior.split()
    saldo_anterior= partes_saldoanterior[0]
    adiciones=partes_saldoanterior[2]
    retiros= partes_saldoanterior[-1]

#Rendimientos
    partes_rendimientos= rendimientoss.split()
    rendimientos= partes_rendimientos[0]
    retencion=partes_rendimientos[1]
    saldofinal= partes_rendimientos[2]

    fecha = datetime.strptime(resultado_fecha, "%Y%m%d")
    if fecha in df_existente.index:
        continue
# Agregar la información extraída al DataFrame
    nueva_fila = pd.DataFrame({"Fondo de Inversión": fondo_inversion, "Número": numero, "Valor de la unidad": valor_unidad,
                            "Saldo Anterior": saldo_anterior,"Adiciones": adiciones,"Retiros": retiros, "Rendimientos Netos":rendimientos,
                            "Retención": retencion,"Saldo Final": saldofinal,"Rentabilidad": resultado_rentabilidad},index=[fecha])
    df_resultados = pd.concat([df_resultados, nueva_fila], ignore_index=False)
    
    
    
    
locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')
# Aplicar la conversión a las columnas seleccionadas
columnas_para_convertir = ["Valor de la unidad", "Saldo Anterior", "Adiciones", "Retiros", "Rendimientos Netos", "Retención", "Saldo Final", "Rentabilidad"]

# Aplicar la conversión a las columnas seleccionadas
for columna in columnas_para_convertir:
    # Eliminar puntos y reemplazar comas para convertir a formato decimal estándar
    df_resultados[columna] = df_resultados[columna].apply(convertir_a_numero)
df_resultados_reset = df_resultados.reset_index()
df_resultados_reset = df_resultados_reset.rename(columns={"index":"Fecha"})

# Establecer la fecha y el 'Fondo de Inversión' como índices múltiples
df_resultados_multi_index = df_resultados_reset.set_index('Fecha')
df_resultados_multi_index= df_resultados_multi_index.sort_index()

columnas_para_convertir = ["Valor de la unidad","Saldo Anterior", "Adiciones","Retiros","Rendimientos Netos","Retención","Saldo Final"]
df_resultados_multi_index[columnas_para_convertir] = df_resultados_multi_index[columnas_para_convertir].apply(pd.to_numeric, errors='coerce')


df_resultados_combinados = pd.concat([df_existente, df_resultados_multi_index], axis= 0)
df_resultados_combinados.to_excel(nombre_archivo_excel, index=True)



