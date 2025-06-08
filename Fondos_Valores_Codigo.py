import os
import re
import json
import PyPDF2
import pandas as pd
from datetime import datetime
import locale

# Establecer configuración numérica
locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')

def convertir_a_numero(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        if valor.endswith('-'):
            valor = '-' + valor[:-1]
        try:
            return locale.atof(valor)
        except ValueError:
            return valor
    return valor

# Cargar JSON con ruta a PDFs
json_file_path = "C:/Users/esteb/Documents/Automatizacion/MutualFund_Info.json"
with open(json_file_path, 'r') as file:
    key_info = json.load(file)

pdf_dir = key_info["Path_MutualFunds_Valores"]

# Mapeo de ID a producto
id_producto_map = {
    "260736021": "RENTA LIQUIDEZ DOLARES",
    "261203811": "RENTA LIQUIDEZ"
}

# Regex
monto_regex = re.compile(r"\$\-?\d{1,3}(?:,\d{3})*\.\d{2}")
archivo_fecha_regex = re.compile(r"Extracto_Multiproducto_(\d{4})(\d{2})")
rentabilidad_regex = re.compile(r"(-?\d{1,2}\.\d+)%")
valor_unidad_regex = re.compile(r"\$\d{1,3}(?:,\d{3})*\.\d+")

# Data
datos_extractos = []
datos_rentabilidad = {}

# Iterar PDFs
for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if len(reader.pages) < 2:
                    continue

                page_text = reader.pages[1].extract_text()
                if not page_text:
                    continue

                lineas = page_text.splitlines()
                
                # Extraer fecha del archivo
                fecha_match = archivo_fecha_regex.search(filename)
                tiempo = None
                if fecha_match:
                    año = int(fecha_match.group(1))
                    mes = int(fecha_match.group(2))
                    tiempo = datetime(año, mes, 1)

                # Buscar rentabilidad por bloque de 3 líneas
                for i in range(len(lineas) - 2):
                    l1 = lineas[i].strip()
                    l2 = lineas[i+1].strip()
                    l3 = lineas[i+2].strip()
                    
                    if "RENTA" in l1 and "RENTABILIDAD DEL" in l2 and "VALOR UNIDAD" in l3:
                        if "DOLARES" in l1:
                            producto = "RENTA LIQUIDEZ DOLARES"
                        else:
                            producto = "RENTA LIQUIDEZ"

                        rentabilidad_match = rentabilidad_regex.search(l3)
                        valor_unidad_match = valor_unidad_regex.search(l3)

                        if rentabilidad_match and valor_unidad_match:
                            rentabilidad = rentabilidad_match.group(1)
                            valor_unidad = convertir_a_numero(valor_unidad_match.group(0))
                            datos_rentabilidad[(producto, tiempo)] = {
                                "Rentabilidad": rentabilidad,
                                "Valor_Unidad": valor_unidad
                            }

                # Buscar líneas de saldos por ID
                for linea in lineas:
                    linea = linea.strip()
                    if linea.startswith("261203811") or linea.startswith("260736021"):
                        partes = linea.split()
                        id_completo = partes[0].split("-")[0]
                        numero = id_completo[:7]
                        producto = id_producto_map.get(id_completo, "DESCONOCIDO")
                        montos = monto_regex.findall(linea)

                        if len(montos) >= 6:
                            datos_extractos.append({
                                "Fecha": tiempo,
                                "Fondo de Inversión": producto,
                                "Número": numero,
                                "Valor de la unidad": None,  # Se completa más adelante
                                "Saldo Anterior": montos[0],
                                "Adiciones": montos[1],
                                "Retiros": montos[2],
                                "Rendimientos Netos": montos[3],
                                "Retención": montos[4],
                                "Saldo Final": montos[5],
                                "Rentabilidad": None  # Se completa más adelante
                            })

        except Exception as e:
            print(f"Error procesando {filename}: {e}")

# Crear DataFrame
df_extractos = pd.DataFrame(datos_extractos)

# Completar Rentabilidad y Valor de la unidad
for i, row in df_extractos.iterrows():
    clave = (row["Fondo de Inversión"], row["Fecha"])
    if clave in datos_rentabilidad:
        df_extractos.at[i, "Rentabilidad"] = datos_rentabilidad[clave]["Rentabilidad"]
        df_extractos.at[i, "Valor de la unidad"] = datos_rentabilidad[clave]["Valor_Unidad"]

# Limpiar columnas monetarias (sin afectar Rentabilidad)
columnas_monetarias = [
    "Valor de la unidad", "Saldo Anterior", "Adiciones",
    "Retiros", "Rendimientos Netos", "Retención", "Saldo Final"
]

# Limpiar columnas monetarias (sin afectar Rentabilidad)
columnas_monetarias = [
    "Valor de la unidad", "Saldo Anterior", "Adiciones",
    "Retiros", "Rendimientos Netos", "Retención", "Saldo Final","Rentabilidad"
]

for col in columnas_monetarias:
    df_extractos[col] = (
        df_extractos[col]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .apply(pd.to_numeric, errors='coerce')
    )

# Reordenar columnas como solicitaste
df_extractos = df_extractos[
    [
        "Fecha", "Fondo de Inversión", "Número",
        "Valor de la unidad", "Saldo Anterior", "Adiciones", "Retiros",
        "Rendimientos Netos", "Retención", "Saldo Final", "Rentabilidad"
    ]
]

# Guardar DataFrame en Excel
ruta_excel = key_info.get("Path_DataBaseFunds_Valores")
if ruta_excel:
    df_extractos.to_excel(ruta_excel, index=False)
    print(f"\n✅ DataFrame guardado exitosamente en:\n{ruta_excel}")
else:
    print("❌ No se encontró la clave 'Path_DataBaseFunds_Valores' en el JSON.")
