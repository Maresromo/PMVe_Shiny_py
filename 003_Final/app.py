import json
import paho.mqtt.client as mqtt
import pandas as pd
from shiny import App, render, ui, reactive

# Variables de conexión MQTT
THINGSBOARD_HOST = 'tb.ier.unam.mx'
ACCESS_TOKEN = 'vVMGeFfW2Ar5TiFkT8oY'

# Función para publicar los datos a ThingsBoard
def enviar_datos(datos):
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()
    
    # Publicar los datos al canal de ThingsBoard
    client.publish('v1/devices/me/telemetry', json.dumps(datos), 1)
    
    client.loop_stop()
    client.disconnect()

# Interfaz de usuario
app_ui = ui.page_fluid(
    # Sección para seleccionar uso de aire acondicionado
    ui.h3("¿Normalmente eres usuario de aire acondicionado de enfriamiento?"),
    ui.input_select("select_ac", "Selecciona una opción:", {"No": "No", "Si": "Si"}),

    # Sección para seleccionar sensación térmica
    ui.h3("¿Cuál es tu sensación térmica?"),
    ui.input_slider("n", "Desliza (-3 mucho frío, 3 mucho calor)", -3, 3, 0, step=0.2),
    ui.output_text_verbatim("thermal_output"),

    # Sección para seleccionar actividad realizada
    ui.h3("¿Qué opción representa mejor la actividad que has estado realizando los últimos 30 minutos?"),
    ui.input_select("select_activity", "Selecciona una opción:", {
        "1": "Sentado: Leyendo, escribiendo o reposando", 
        "4": "Sentado tecleando", 
        "5": "De pie y relajado", 
        "6": "Caminando",
        "7": "Trotando",
        "8": "Conduciendo auto o moto"
    }),

    # Sección para seleccionar vestimenta (nuevas opciones)
    ui.h3("Selecciona tu vestimenta (todas prendas que estes usando)"),
    ui.input_selectize("ropa_interior", "Ropa Interior", {     
        "0.06": "Camiseta sin mangas",
        "0.09": "Camiseta manga corta",
        }, multiple=True),
    ui.input_selectize("calcetines", "Calcetines", {
        "0.02": "Calcetines cortos",
        "0.020": "Medias",
        "0.0200": "Calcetines deportivos hasta el tobillo",
        "0.03": "Calcetines hasta la pantorrilla",
        "0.06": "Calcetines hasta la rodilla (gruesos)"
    }, multiple=True),
    ui.input_selectize("calzado", "Calzado, Guantes", {
        "0.02": "Sandalias, chanclas o zapato abierto",
        "0.03": "Pantuflas (acolchadas, con forro de pelo)",
        "0.030": "Tenis o zapato de suela fina",
        "0.04": "Tenis o zapato de suela gruesa",
        "0.05": "Guantes",
        "0.10": "Botas"
    }, multiple=True),
    ui.input_selectize("pantalones", "Shorts, Pantalones, Pants", {
        "0.06": "Shorts (arriba de la rodilla)",
        "0.08": "Shorts (abajo de la rodilla)",
        "0.11": "Shorts tipo cargo",
        "0.24": "Pantalón recto (grueso)",
        "0.25": "Pantalones normales (jeans)",
        "0.28": "Pantalones de franela",
        "0.280": "Pants"
    }, multiple=True),
    ui.input_selectize("vestidos_faldas", "Faldas y Vestidos", {
        "0.10": "Falda sobre rodilla (delgada)",
        "0.17": "Falda sobre rodilla (gruesa)",
        "0.18": "Falda bajo rodilla (delgada)",
        "0.25": "Falda bajo rodilla (gruesa)",
        "0.23": "Vestido sin mangas (delgado)",
        "0.27": "Vestido sin mangas (grueso)",
        "0.29": "Vestido de manga corta (delgado)",
        "0.33": "Vestido de manga larga (delgado)",
        "0.47": "Vestido de manga larga (grueso)"
    }, multiple=True),
    ui.input_selectize("camisas_blusas", "Blusas, Playeras y Camisas", {
        "0.06": "Top",
        "0.10": "Blusa o playera sin mangas",
        "0.12": "Blusa o playera de manga corta",
        "0.15": "Blusa o playera de manga larga",
        "0.17": "Camiseta deportiva de manga corta",
        "0.19": "Camisa de manga corta",
        "0.20": "Camisa de manga larga (delgada)",
        "0.25": "Camisa de manga larga (gruesa)",
        "0.34": "Camisa de franela de manga larga"
    }, multiple=True),
    ui.input_selectize("sueteres", "Chalecos, Suéteres, Sudadera", {
        "0.13": "Chaleco (delgado)",
        "0.22": "Chaleco (grueso)",
        "0.25": "Suéter (delgado)",
        "0.36": "Suéter (grueso)",
        "0.34": "Sudadera",
        "0.30": "Chamarra impermeable con capucha"
    }, multiple=True),
    ui.input_selectize("sacos", "Sacos", {
        "0.36": "Saco (delgado)",
        "0.44": "Saco (grueso)"
    }, multiple=True),
    ui.input_selectize("overoles", "Overoles", {
        "0.30": "Overol (tirantes)",
        "0.49": "Mono (cerrado)"
    }, multiple=True),
    ui.input_selectize("batas", "Batas de Laboratorio", {
        "0.34": "Bata corta y de manga corta (delgada)",
        "0.46": "Bata corta y de manga larga (gruesa)",
        "0.48": "Bata larga de manga larga (gruesa)"
    }, multiple=True),
    ui.input_selectize("pijama", "Pijama", {
        "0.10": "Pantalón corto",
        "0.50": "Pijama de mangas y pantalones largos"
    }, multiple=True),
    ui.h3("Esta encuesta es anónima, solo recolectan los siguientes datos que fueron calculados con tus repuestas:"),

    # Mostrar tabla con los resultados
    ui.output_table("result_table"),
    ui.input_action_button("enviar_button", "Enviar"),
    
    # Letrero para indicar que los datos han sido enviados
    ui.output_text("status_text")
)

# Servidor
def server(input, output, session):
    
    def suma(x):
        return sum([float(elemento) for elemento in list(x)])

    def CLO():
        a = 0.03 + sum([suma(input.ropa_interior()), suma(input.calcetines()), suma(input.calzado()), suma(input.camisas_blusas()), suma(input.pantalones()), suma(input.overoles()), suma(input.sacos()), suma(input.sueteres()), suma(input.vestidos_faldas()), suma(input.batas()), suma(input.pijama())])
        return a

    def get_e():
        return 0.8 if input.select_ac() == "Si" else 0.7

    def get_met():
        actividad = input.select_activity()
        return {"1": 1.0, "4": 1.1, "5": 1.2, "6": 1.7,"7": 2.6,"8": 1.5}.get(actividad, 1.0)

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

    @output
    @render.text
    def thermal_output():
        r, voto = get_thermal()
        return f"Sientes {r}, con {voto}"

    @output
    @render.table
    def result_table():
        e_value = get_e()
        met_value = get_met()
        thermal_value, voto = get_thermal()
        if met_value < 1.2:
            clo_value = CLO() + 0.1
        else: 
            clo_value = CLO()

        # Crear un DataFrame con los valores calculados
        df = pd.DataFrame({
            "clo": [clo_value],
            "e": [e_value],
            "met": [met_value],
            "voto": [voto]
        })

        return df

    # Letrero que se mostrará después de enviar los datos
    @output
    @render.text
    def status_text():
        return ""
        
    @reactive.Effect
    @reactive.event(input.enviar_button)
    def enviar():
        e_value = get_e()
        met_value = get_met()
        thermal_value, voto = get_thermal()
        if met_value < 1.2:
            clo_value = CLO() + 0.1
        else: 
            clo_value = CLO()

        datos = {
            "e": e_value,
            "voto": voto,
            "met": met_value,
            "clo": clo_value
        }

        # Publicar los datos en ThingsBoard
        enviar_datos(datos)

        ui.notification_show(
            f'''----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
                ----------------- Datos enviados -----------------------
                --------------- Muchas gracias por -------------------
                ------------- contestar esta encuesta -------------------
                -----------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------
            ----------------------------------------------------------------''',
            duration=200,
            )


        # Mostrar el letrero de "Datos enviados" en el navegador
        output.status_text.set("")


# Crear la aplicación Shiny
app = App(app_ui, server)
