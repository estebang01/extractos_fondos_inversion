import re
from datetime import datetime
import PyPDF2
import pandas as pd
import os
import email
import imaplib
import locale
from locale import atof

regex_autorizacion = re.compile(r"([A-Za-z0-9]{6})")
regex_fecha = re.compile(r"(\d{2}/\d{2}/\d{4})")
regex_descripcion = re.compile(r"\d{2}/\d{2}/\d{4}\s+([A-Za-z ÑÁÉÍÓÚñáéíóú0-9-]+)")
regex_valor = re.compile(r"(\d{2}/\d{2}/\d{4} .+?)\s(-?\d{1,3}(?:,\d{3})*\.\d{2})")
regex_cuotas = re.compile(r"(\d+/\d+)$")
regex_valor_tasa = re.compile(r"(\d{2},\d{4})")
regex_valor_saldomes = re.compile(r"(\d+\.\d{2})\s")
transaccion="031101 22/11/2023 xmglobal 162,966.96 2,7335 37,5271 162,966.96 0.00 1/1"
match_cuotas = regex_cuotas.search(transaccion).group(1)
match_fecha = regex_fecha.search(transaccion)
match_descripcion = regex_descripcion.search(transaccion)
match_tasa= regex_valor_tasa.search(transaccion)
match_saldomes= regex_valor_saldomes.search(transaccion)
match_valor = regex_valor.search(transaccion)
match_autorizacion = regex_autorizacion.search(transaccion)
numero_autorizacion = match_autorizacion.group(1)
fecha_transaccion = match_fecha.group(1)
descripcion = match_descripcion.group(1)
tasa= match_tasa.group(1)
saldomes=match_saldomes.group(1)
                        
valor_original_str = match_valor.group(2)
valor_original_float = atof(valor_original_str.replace(',', ''))
if match_autorizacion and match_fecha and match_descripcion and match_valor and match_cuotas:
    print(valor_original_float,match_cuotas)