from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.input_selectize(  
        "selectize",  
        "Select options below:",  
        {"1A": "Camisa",
         "1B": "Pantalon", 
         "1C": "Calcetines"},  
        multiple=True,  
    ),  
    ui.output_text("value"),
)

def server(input, output, session):
    @render.text
    def value():
        return f"{input.selectize()}"

app = App(app_ui, server)