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

# Connect to the Gmail server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(key_info["email"], key_info["email_code"])
mail.select('inbox')

# Search for emails from a specific sender received since the first day of two months ago
tipo, data = mail.search(None, f'(FROM "{key_info["bank_email"]}")')

fondos_path = key_info["Path_MutualFunds"]
finanzas_personales_path = key_info["Path_PersonalFinance"]

# Make sure the directories exist
os.makedirs(fondos_path, exist_ok=True)
os.makedirs(finanzas_personales_path, exist_ok=True)

# Procesar correos y descargar los archivos
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