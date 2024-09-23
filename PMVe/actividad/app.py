from shiny import App, render, ui

# Interfaz de usuario
app_ui = ui.page_fluid(
    # Sección para seleccionar uso de aire acondicionado
    ui.h3("¿Normalmente eres usuario de aire acondicionado de enfriamiento?"),
    ui.input_select(
        "select_ac",
        "Selecciona una opción:",
        {"Si": "Si", "No": "No"}
    ),
    ui.output_text_verbatim("ac_value"),  # Mostrar valor de 'e'

    # Sección para seleccionar sensación térmica
    ui.input_slider("n", "¿Cuál es tu sensación térmica?", -3, 3, 0, step=0.2),
    ui.output_text_verbatim("thermal_value"),  # Mostrar sensación térmica

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
    ui.output_text_verbatim("activity_value")  # Mostrar valor de MET
)

# Servidor
def server(input, output, session):
    
    # Renderizar valor de 'e' en función de la selección de aire acondicionado
    @output
    @render.text
    def ac_value():
        # Establecemos el valor de 'e' en función de la selección
        if input.select_ac() == "Si":
            e = 0.8
        else:
            e = 0.7
        
        return f"El valor de e es: {e}"
    
    # Renderizar resultado de sensación térmica
    @output
    @render.text
    def thermal_value():
        voto = input.n()  # Sensación térmica seleccionada
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
        
        return f"Sientes {r}, con {voto}"

    # Renderizar valor de MET en función de la actividad seleccionada
    @output
    @render.text
    def activity_value():
        met = 0
        # Asignamos el valor de 'met' en función de la opción seleccionada
        if input.select_activity() == "1":  # Sentado reposando
            met = 1.0
        elif input.select_activity() == "2":  # Leyendo sentado
            met = 1.0
        elif input.select_activity() == "3":  # Sentado escribiendo
            met = 1.0
        elif input.select_activity() == "4":  # Sentado tecleando
            met = 1.0
        elif input.select_activity() == "5":  # De pie y relajado
            met = 1.2
        elif input.select_activity() == "6":  # Caminando
            met = 1.7

        # Devolvemos el valor de 'met'
        return f"El valor de MET es: {met}"

# Crear la aplicación Shiny
app = App(app_ui, server)
