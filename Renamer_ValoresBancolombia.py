import os
import re
import json
import PyPDF2

# Cargar ruta de PDFs desde JSON
json_file_path = "C:/Users/esteb/Documents/Automatizacion/MutualFund_Info.json"
with open(json_file_path, 'r') as file:
    key_info = json.load(file)

pdf_dir = key_info["Path_MutualFunds_Valores"]

month_map = {
    "ENE": "01", "FEB": "02", "MAR": "03", "ABR": "04",
    "MAY": "05", "JUN": "06", "JUL": "07", "AGO": "08",
    "SEP": "09", "OCT": "10", "NOV": "11", "DIC": "12"
}

periodo_regex = re.compile(r"DESDE\s+\d{2}-(\w{3})-(\d{4})", re.IGNORECASE)

for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)

        try:
            # Abrir PDF
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                if len(reader.pages) == 0:
                    continue

                first_page = reader.pages[0].extract_text()
                if not first_page:
                    continue

                match = periodo_regex.search(first_page)
                if match:
                    mes_abrev = match.group(1).upper()
                    anio = match.group(2)
                    mes_num = month_map.get(mes_abrev)

                    if mes_num:
                        nuevo_nombre = f"Extracto_Multiproducto_{anio}{mes_num}.pdf"
                        nuevo_path = os.path.join(pdf_dir, nuevo_nombre)

                        # Guardar texto de segunda página si existe
                        second_page_text = ""
                        if len(reader.pages) > 1:
                            second_page_text = reader.pages[1].extract_text()

            # Renombrar después de cerrar el archivo
            os.rename(pdf_path, nuevo_path)
            print(f"Renombrado: {filename} → {nuevo_nombre}")
        except Exception as e:
            print(f"Error procesando {filename}: {e}")
