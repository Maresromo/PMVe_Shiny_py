from shiny import render
from shiny.express import input, ui


ui.h3("¿Normalmente eres usuario de aire acondicionado de enfriamiento?")
ui.input_select(  
    "select",  
    "Selecciona una opción:",  
    {"Si": "Si", "No": "No" },  
)  

@render.text
def value():
    # Establecemos el valor de 'e' en función de la selección
    if input.select() == "Si":
        e = 0.8
    else:
        e = 0.7
    
    return f"El valor de e es: {e}"
