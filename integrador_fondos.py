import pandas as pd
import os
import json
from datetime import datetime

# === Cargar rutas desde JSON ===
json_file_path = "C:/Users/esteb/Documents/Automatizacion/MutualFund_Info.json"
with open(json_file_path, 'r') as file:
    key_info = json.load(file)

ruta_base = key_info["Path_DataBaseFunds"]
ruta_valores = key_info["Path_DataBaseFunds_Valores"]

# === Leer DataFrames existentes ===
if os.path.exists(ruta_base):
    df_existente = pd.read_excel(ruta_base, parse_dates=["Fecha"])
    df_existente["Fecha"] = pd.to_datetime(df_existente["Fecha"])
else:
    df_existente = pd.DataFrame()

if os.path.exists(ruta_valores):
    df_multiproducto = pd.read_excel(ruta_valores, parse_dates=["Fecha"])
    df_multiproducto["Fecha"] = pd.to_datetime(df_multiproducto["Fecha"])
else:
    df_multiproducto = pd.DataFrame()

# === Ruta opcional a fondos individuales procesados ===
ruta_fondos_individuales = key_info.get("Path_DataBaseFunds_Individuales")  # opcional

if ruta_fondos_individuales and os.path.exists(ruta_fondos_individuales):
    df_individual = pd.read_excel(ruta_fondos_individuales, parse_dates=["Fecha"])
    df_individual["Fecha"] = pd.to_datetime(df_individual["Fecha"])
else:
    df_individual = pd.DataFrame()

# === Combinar todos los datos ===
columnas_estandar = [
    "Fecha", "Fondo de Inversión", "Número", "Valor de la unidad",
    "Saldo Anterior", "Adiciones", "Retiros", "Rendimientos Netos",
    "Retención", "Saldo Final", "Rentabilidad"
]

# Unificar columnas y tipos
for df in [df_existente, df_multiproducto, df_individual]:
    for col in columnas_estandar:
        if col not in df.columns:
            df[col] = None

# Concatenar todos
df_combinado = pd.concat([df_existente, df_multiproducto, df_individual], ignore_index=True)

# Eliminar duplicados por clave lógica
df_combinado = df_combinado.drop_duplicates(subset=["Fecha", "Fondo de Inversión", "Número"], keep="last")

# Ordenar y guardar
df_combinado = df_combinado.sort_values("Fecha")
df_combinado.to_excel(ruta_base, index=False)

print(f"✅ Integración completada. Consolidado guardado en:\n{ruta_base}")
