import json
import random
import paho.mqtt.client as mqtt
from shiny import App, reactive, render, ui

# Variables de conexión MQTT
THINGSBOARD_HOST = 'tb.ier.unam.mx'
ACCESS_TOKEN = 'vVMGeFfW2Ar5TiFkT8oY'

# Datos iniciales
sensor_data = {'e': 0, 'voto': 0, 'met': 0, 'clo': 0}

# Función para publicar los datos a ThingsBoard
def enviar_datos():
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()
    
    # Generar datos
    e = random.randint(800, 900)
    voto = random.randint(3000, 4000)
    met = random.randint(4000, 5000)
    clo = random.randint(1000, 2000)
    
    # Actualizar el diccionario
    sensor_data['e'] = e
    sensor_data['voto'] = voto
    sensor_data['met'] = met
    sensor_data['clo'] = clo
    
    # Publicar los datos
    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
    
    client.loop_stop()
    client.disconnect()
    
    return sensor_data

# Interfaz de usuario de Shiny
app_ui = ui.page_fluid(
    ui.input_action_button("enviar_button", "Enviar"),  # Botón para enviar datos
    ui.output_text_verbatim("output"),  # Mostrar los datos publicados
    ui.output_text("status_text")  # Mostrar el letrero de estado
)

# Servidor de Shiny
def server(input, output, session):
    @reactive.Effect
    @reactive.event(input.enviar_button)  # Ejecuta la función cuando se presiona el botón
    def _():
        datos = enviar_datos()  # Enviar los datos al pulsar el botón
        output.output.set(f"Datos enviados: {datos}")  # Mostrar los datos en la interfaz
        output.status_text.set("<span style='color:red;'>Datos enviados</span>")  # Mostrar letrero en color rojo

    @output
    @render.text
    def status_text():
        return ""  # Inicialmente vacío

    @reactive.Effect
    @reactive.event(input.enviar_button)
    def show_status_text():
        output.status_text.set("<span style='color:red;'>Datos enviados</span>")  # Actualiza el letrero después de enviar

# Crear la app de Shiny
app = App(app_ui, server)
