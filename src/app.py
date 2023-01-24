from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.title = "She Wore What 2023"

path = "data/ClosetData.csv"

closet = pd.read_csv(path)


app.layout = html.Div(
    [
        dcc.Dropdown(id="ycol", value="optionz", options=[1, 2, 3]),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
