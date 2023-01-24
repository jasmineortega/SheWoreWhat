from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.title = "She Wore What 2023"


app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.B("She Wore What 2023"),
                style={"font-weight": "bold", "color": "#000000", "font-size": "150%"},
                width={"offset": 5},
            )
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
