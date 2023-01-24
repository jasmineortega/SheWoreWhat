from flask import Flask, render_template
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.title = "She Wore What 2023"

path = "data/ClosetData.csv"

closet = pd.read_csv(path)


app.layout = html.Div(
    [
        dcc.Dropdown(id="ycol", value="release_year", options=[1, 2, 3]),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
