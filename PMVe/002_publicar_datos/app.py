import random
import json
import paho.mqtt.client as mqtt
from shiny import App, ui, reactive

# Configuración de ThingsBoard
THINGSBOARD_HOST = 'iot.ier.unam.mx'
ACCESS_TOKEN = 'vVMGeFfW2Ar5TiFkT8oY'

# Crear cliente MQTT y conectarse a ThingsBoard
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

# Definimos la interfaz de usuario (UI)
app_ui = ui.page_fluid(
    ui.h2("Publicador de Encuesta"),
    ui.input_numeric("input1", "Valor de 'e'", value=random.uniform(0, 10)),
    ui.input_numeric("input2", "Valor de 'voto'", value=random.uniform(0, 10)),
    ui.input_numeric("input3", "Valor de 'met'", value=random.uniform(0, 10)),
    ui.input_numeric("input4", "Valor de 'clo'", value=random.uniform(0, 10)),
    ui.input_action_button("submit_btn", "Enviar"),  # Botón para enviar
    ui.output_text_verbatim("output")  # Área para mostrar el resultado
)

# Definimos la lógica de la aplicación (Server)
def server(input, output, session):

    # Efecto reactivo que se activa cuando se presiona el botón "Enviar"
    @reactive.Effect
    @reactive.event(input.submit_btn)
    def _():
        # Obtener los valores de las entradas
        e_value = input.input1()
        voto_value = input.input2()
        met_value = input.input3()
        clo_value = input.input4()

        # Crear diccionario con los datos de la encuesta
        encuesta = {
            'e': e_value,
            'voto': voto_value,
            'met': met_value,
            'clo': clo_value
        }

        # Publicar los datos en ThingsBoard usando MQTT
        client.publish('v1/devices/me/telemetry', json.dumps(encuesta), 1)

        # Mostrar los datos en la app
        output["output"].set_text(f"Datos enviados:\n{json.dumps(encuesta, indent=2)}")

# Crear la aplicación Shiny
app = App(app_ui, server)
