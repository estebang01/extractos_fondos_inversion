# funciones.py

def clasificar_transaccion(descripcion):
    descripcion = descripcion.upper()  # Convertir a mayúsculas
    categorias = {
        "Transporte": ["MOTOR", "LOCALIZA", "PRONTOWASH", "CAR", "METRO", "VEHICULO", "TRANSPORTE PÚBLICO"],
        "Gasolina": ["PRIMAX","ESSO","TERPEL"],
        "Comida": ["ALQUIMICO", "FOOD", "DOG", "PIZZA", "CHEF", "WING", "PARMESSANO", "PRESTO", "CHIP","BURRITO","TACO","GRILL","FRISBY","PASTA","HAMBURGUESAS","BURGER","WAFFLE","MISTURA",
                   "FORNO","MCDONALD","SANTA LENA","BURGUERS","OLIVIA","GRETTA","JUAN VALDEZ","NONNA","RISTORANTE","CAFE","LAVOCADERIA","BAKERY","MADELO","MAMASITA","MUNDO VERDE"
                   ,"CAFETERIA","PERCIMON","BIGOS","KIMCHI","STARBUCK","OMA","CORRAL","ROMERO","SARKU","DONUTS","NIKKEI","STRABUCKS","MIJITA","PANE","DOMINOS","URBANIA","PARADOR ALDEA",
                   "TEX MEX","COUNTRY CLUB","SUB EAFIT","MIKAELA","SUSHI","CLUB CAMPESTRE","TACO","MILONGA","MIMO","BURGUER KING ZONA SUR","FIRE HOUSE HAMB Y ALIT"],
        "Peajes y Parqueaderos":["FLYPASS"],
        "Entretenimiento": ["CMK", "CINEPOLIS", "CONCIERTO", "PARQUE DE ATRACCIONES", "STREAMING", "JUEGOS", "MÚSICA", "EVENTO"],
        "Ocio": ["ALIEXPRESS","ALI","MERCADOPAGO","WOMPI","PAYU","BOLETA"],
        "Apuestas": ["CODERE","RUSH STREET","xmglobal",],
        "Barbería": ["BARBER"],
        "Gastos Terjeta": ["CUOTA DE MANEJO ","COMISION","IVA"],
        "Viajes":["HOTEL"],
        "Salud": ["FARMACIA", "PASTEUR", "SEGURO MÉDICO", "RADIO", "BODYTECH", "SALUD"],
        "Mercado": ["CARULLA", "EURO", "EXITO","D1", "FARMATODO", "SUPERMERCADO", "DOLLARCITY ", "CASA"],
        "Educación": ["UNIVERSIDAD EAFIT", "COLOMBO AMERIC","PANAMERICANA","ARTES"],
        "Ropa": ["AMERICAN EAGLE", "MOVIES", "NAF NAF", "ZARA"],
        "Abonos y Saldo a Favor": ["ABONO", "SALDO A FAVO"],
        "Tecnología": ["APPLE.COM", "ORDENADOR", "ACCESORIO ELECTRÓNICO", "TECNOLOGÍA", "GADGET"],
        "Otros": ["OTROS GASTOS", "MISCELÁNEOS", "OTROS"]
    }
    
    for categoria, palabras_clave in categorias.items():
        for palabra in palabras_clave:
            if palabra in descripcion:
                return categoria
    return "Otro"
