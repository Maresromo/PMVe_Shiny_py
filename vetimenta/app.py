from shiny import render
from shiny.express import input, ui

ui.h3("Selecciona tu vestimenta (todas las opciones que desses)")
ui.input_selectize(  
    "ropa_interior",  
    "Ropa interior",  
    {"0.04": "Boxers", 
     "0.03": "Bragas", 
     "0.01": "Sostén"},  
    multiple=True,  
)  
ui.input_selectize(  
    "calzado",  
    "Calzado",  
    {"0.02": "Calcetines deportivos hasta el tobillo", 
     "0.03": "Calcetines hasta la pantorrilla", 
     "0.06": "Calcetines hasta la rodilla (gruesos)", 
     "0.020": "pantimedias", 
     "0.0200": "Sandalias/chanclas", 
     "0.030": "Pantuflas (acolchadas)", 
     "0.1": "Botas"},  
    multiple=True,  
)  
ui.input_selectize(  
    "camisas_blusas",  
    "Camisas y Blusas",  
    {"0.12": "Blusa sin mangas", 
     "0.19": "Camisa de vestir de manga corta", 
     "0.25": "Camisa de vestir de manga larga", 
     "0.34": "Camisa de franela de manga larga", 
     "0.17": "Camisa deportiva de punto de manga corta", 
     "0.08": "Playera"},  
    multiple=True,  
)  
ui.input_selectize(  
    "pantalones_overoles",  
    "Pantalones, shorts y overoles", 
    {"0.7": "Shorts",
    "0.15": "Pantalón recto (delgado)",
    "0.24": "Pantalón recto (grueso)",
    "0.28": "Pants",
    "0.3": "Overol",
    "0.49": "Mono"},  
    multiple=True,  
)  
ui.input_selectize(  
    "sacos",  
    "Sacos", 
    {"0.36": "Saco (delgado)",
    "0.44": "Saco (grueso)"},  
    multiple=True,  
)  
ui.input_selectize(  
    "sueteres",  
    "Suéteres", 
    {"0.13": "Chaleco (delgado)",
    "0.22": "Chaleco (grueso)",
    "0.25": "Manga larga (fina)",
    "0.36": "Manga larga (grueso)",
    "0.34": "Sudadera"},  
    multiple=True,  
)  
ui.input_selectize(  
    "vestidos_faldas",  
    "Vestidos y faldas", 
    {"0.14": "Falda (delgada)",
    "0.23": "Falda (gruesa)",
    "0.33": "Vestido de manga larga (delgado)",
    "0.47": "Vestido de manga larga (grueso)",
    "0.29": "Vestido de manga corta (delgado)",
    "0.230": "Vestido sin mangas (delgado)",
    "0.27": "Vestido sin mangas (grueso)"},
    multiple=True,  
)  
ui.input_selectize(  
    "batas",  
    "Batas de laboratorio", 
    {"0.34": "Bata corta y de manga corta (fina)",
    "0.48": "Bata corta y de manga larga (gruesa)",
    "0.46": "Bata larga de manga larga (gruesa)"},  
    multiple=True,  
)  

def suma(x):
    return sum([float(elemento) for elemento in list(x)])

def CLO():
    return sum([suma(input.ropa_interior()),
            suma(input.calzado()),
            suma(input.camisas_blusas()),
            suma(input.pantalones_overoles()),
            suma(input.sacos()),
            suma(input.sueteres()),
            suma(input.vestidos_faldas()),
            suma(input.batas())])

@render.text
def value():
    return f"{CLO()}"