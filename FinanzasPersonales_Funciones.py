# funciones.py

def clasificar_transaccion(descripcion):
    descripcion = descripcion.upper()  # Convertir a mayúsculas
    categorias = {
        "Transporte": ["MOTOR", "LOCALIZA", "PRONTOWASH", "CAR", "METRO","MOBILITY","VEHICULOS","VALENCIA ALVAREZ SAN D ","MALL AUTOS"],
        "Gasolina": ["PRIMAX","ESSO","TERPEL","EDS PREMIUM"],
        "Comida": ["ALQUIMICO", "FOOD", "DOG", "PIZZA", "CHEF", "WING", "PARMESSANO", "PRESTO", "CHIP","BURRITO","TACO","GRILL","FRISBY","PASTA","HAMBURGUESAS","BURGER","BURGUER","WAFFLE","MISTURA",
                   "FORNO","MCDONALD","SANTA LENA","BURGUERS","OLIVIA","GRETTA","JUAN VALDEZ","NONNA","RISTORANTE","CAFE","LAVOCADERIA","BAKERY","MADELO","MAMASITA","MUNDO VERDE"
                   ,"CAFETERIA","PERCIMON","BIGOS","KIMCHI","STARBUCK","OMA","CORRAL","ROMERO","SARKU","DONUTS","NIKKEI","STRABUCKS","MIJITA","PANE","DOMINOS","URBANIA","PARADOR ALDEA",
                   "TEX MEX","COUNTRY CLUB","SUB EAFIT","MIKAELA","SUSHI","CLUB CAMPESTRE","TACO","MILONGA","MIMO","BURGUER KING ZONA SUR","FIRE HOUSE HAMB Y ALIT","D GREEN",
                   "HAMBURGUESIA","LA TIENDA DE PEDRO","LA ESQUINA DEL VERONA","HAMBURGUESA","SANCHO PAISA","MERO","TOMO MONTERIA","MADEROS","ALTAS VISTAS","MECADO DEL SUR DELICAT"
                   ,"INVERSIONES MONTOLIVO"],
        "Peajes y Parqueaderos":["FLYPASS","PARQUE COMERCIAL EL"],
        "Entretenimiento": ["CMK", "CINEPOLIS", "DTV","GRUPO AMADOR"],
        "Ocio": ["ALIEXPRESS","ALI","MERCADOPAGO","WOMPI","PAYU","BOLETA","FALABELLA COM"],
        "Apuestas": ["CODERE","RUSH STREET","XMGLOBAL","HOLLYWOOD CASINO Y CAF"],
        "Barbería": ["BARBER"],
        "Gastos Tarjeta": ["CUOTA DE MANEJO ","COMISION","IVA"],
        "Viajes y Alojamiento":["HOTEL","MUSEO","LATAM","INV GACELA DE COLOMBIA","RIVER DEUS","LRFN FREEDOM CHASERS "],
        "Salud": ["FARMACIA", "PASTEUR", "SEGURO MÉDICO", "RADIO", "BODYTECH","DROGAS"],
        "Mercado": ["CARULLA", "EURO", "EXITO","D1", "FARMATODO", "SUPERMERCADO", "DOLLARCITY ","JUMBO","VAQUITA"],
        "Educación": ["UNIVERSIDAD EAFIT", "COLOMBO AMERIC","PANAMERICANA","ARTES"],
        "Ropa": ["AMERICAN EAGLE", "MOVIES", "NAF NAF", "ZARA","MASSIMO DUTTI","LOUIS BARTON ","MANGO","H&M","PULL&BEAR","PAT PRIMO","GEF Y PUNTO BLANCO","ALDO"],
        "Abonos y Saldo a Favor": ["ABONO", "SALDO A FAVO","AJUSTE MANUAL A FAVOR"],
        "Tecnología": ["APPLE.COM","MAC CENTER"],
        "Bold Co": ["BOLD"],
        "Gastos Alcaldía y Gobernación": ["SOMOS RIONEGRO","TRANSITO","CAMARA DE COMERCIO"],
        "Otros": ["OTROS GASTOS", "MISCELÁNEOS", "OTROS","HERBARIO","MASCOTAS CLUB CAMPESTR"]
    }
    
    for categoria, palabras_clave in categorias.items():
        for palabra in palabras_clave:
            if palabra in descripcion:
                return categoria
    return "No Clasificado"
