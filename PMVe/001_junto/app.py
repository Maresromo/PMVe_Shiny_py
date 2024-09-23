from shiny import App, render, ui
import pandas as pd

# Interfaz de usuario
app_ui = ui.page_fluid(
    # Sección para seleccionar uso de aire acondicionado
    ui.h3("¿Normalmente eres usuario de aire acondicionado de enfriamiento?"),
    ui.input_select(
        "select_ac",
        "Selecciona una opción:",
        {"No": "No", "Si": "Si"}
    ),

    # Sección para seleccionar sensación térmica
    ui.input_slider("n", "¿Cuál es tu sensación térmica?", -3, 3, 0, step=0.2),

    # Sección para seleccionar actividad realizada
    ui.h3("¿Qué actividad que has estado realizando los últimos 30 minutos?"),
    ui.input_select(
        "select_activity",
        "Selecciona una opción:",
        {
            "1": "Sentado reposando", 
            "2": "Leyendo sentado",
            "3": "Sentado escribiendo", 
            "4": "Sentado tecleando", 
            "5": "De pie y relajado", 
            "6": "Caminando"
        }
    ),

    # Sección para seleccionar vestimenta
    ui.h3("Selecciona tu vestimenta (todas las opciones que desees)"),
    ui.input_selectize(
        "ropa_interior",  
        "Ropa interior",  
        {"0.04": "Boxers", "0.03": "Bragas", "0.01": "Sostén"},  
        multiple=True
    ),
    ui.input_selectize(
        "calzado",  
        "Calzado",  
        {
            "0.02": "Calcetines deportivos hasta el tobillo", 
            "0.03": "Calcetines hasta la pantorrilla", 
            "0.06": "Calcetines hasta la rodilla (gruesos)", 
            "0.020": "pantimedias", 
            "0.0200": "Sandalias/chanclas", 
            "0.030": "Pantuflas (acolchadas)", 
            "0.1": "Botas"
        },  
        multiple=True
    ),
    ui.input_selectize(
        "camisas_blusas",  
        "Camisas y Blusas",  
        {
            "0.12": "Blusa sin mangas", 
            "0.19": "Camisa de vestir de manga corta", 
            "0.25": "Camisa de vestir de manga larga", 
            "0.34": "Camisa de franela de manga larga", 
            "0.17": "Camisa deportiva de punto de manga corta", 
            "0.08": "Playera"
        },  
        multiple=True
    ),
    ui.input_selectize(
        "pantalones_overoles",  
        "Pantalones, shorts y overoles", 
        {
            "0.7": "Shorts",
            "0.15": "Pantalón recto (delgado)",
            "0.24": "Pantalón recto (grueso)",
            "0.28": "Pants",
            "0.3": "Overol",
            "0.49": "Mono"
        },  
        multiple=True
    ),
    ui.input_selectize(
        "sacos",  
        "Sacos", 
        {
            "0.36": "Saco (delgado)",
            "0.44": "Saco (grueso)"
        },  
        multiple=True
    ),
    ui.input_selectize(
        "sueteres",  
        "Suéteres", 
        {
            "0.13": "Chaleco (delgado)",
            "0.22": "Chaleco (grueso)",
            "0.25": "Manga larga (fina)",
            "0.36": "Manga larga (grueso)",
            "0.34": "Sudadera"
        },  
        multiple=True
    ),
    ui.input_selectize(
        "vestidos_faldas",  
        "Vestidos y faldas", 
        {
            "0.14": "Falda (delgada)",
            "0.23": "Falda (gruesa)",
            "0.33": "Vestido de manga larga (delgado)",
            "0.47": "Vestido de manga larga (grueso)",
            "0.29": "Vestido de manga corta (delgado)",
            "0.230": "Vestido sin mangas (delgado)",
            "0.27": "Vestido sin mangas (grueso)"
        },  
        multiple=True
    ),
    ui.input_selectize(
        "batas",  
        "Batas de laboratorio", 
        {
            "0.34": "Bata corta y de manga corta (fina)",
            "0.48": "Bata corta y de manga larga (gruesa)",
            "0.46": "Bata larga de manga larga (gruesa)"
        },  
        multiple=True
    ),

    # Mostrar tabla con los resultados
    ui.output_table("result_table")
)

# Servidor
def server(input, output, session):
    
    # Función para sumar los valores de las opciones seleccionadas
    def suma(x):
        return sum([float(elemento) for elemento in list(x)])

    # Cálculo del valor CLO total
    def CLO():
        return sum([
            suma(input.ropa_interior()),
            suma(input.calzado()),
            suma(input.camisas_blusas()),
            suma(input.pantalones_overoles()),
            suma(input.sacos()),
            suma(input.sueteres()),
            suma(input.vestidos_faldas()),
            suma(input.batas())
        ])

    # Obtener el valor de 'e' en función de la selección de aire acondicionado
    def get_e():
        return 0.8 if input.select_ac() == "Si" else 0.7

    # Obtener el valor de MET en función de la actividad seleccionada
    def get_met():
        met = 0
        if input.select_activity() == "1":
            met = 1.0
        elif input.select_activity() == "2":
            met = 1.0
        elif input.select_activity() == "3":
            met = 1.0
        elif input.select_activity() == "4":
            met = 1.0
        elif input.select_activity() == "5":
            met = 1.2
        elif input.select_activity() == "6":
            met = 1.7
        return met

    # Obtener el resultado de sensación térmica
    def get_thermal():
        voto = input.n()
        if voto < -2:
            r = "mucho frío"
        elif voto < -1:
            r = "frío"
        elif -1 <= voto < 0:
            r = "poco frío"
        elif voto == 0:
            r = "neutralidad"
        elif 0 < voto <= 1:
            r = "poco calor"
        elif 1 < voto <= 2:
            r = "calor"
        elif 2 < voto <= 3:
            r = "mucho calor"
        return r, voto

    # Renderizar la tabla con los valores de e, met, sensación térmica y CLO
    @output
    @render.table
    def result_table():
        e_value = get_e()
        met_value = get_met()
        thermal_value, voto = get_thermal()
        clo_value = CLO()

        # Crear un DataFrame con los valores, donde los nombres de las variables son los encabezados de las columnas
        df = pd.DataFrame({
            "e": [e_value],
            "voto": [voto],
            "met": [met_value],
            "clo": [clo_value]
        })

        return df

# Crear la aplicación Shiny
app = App(app_ui, server)
