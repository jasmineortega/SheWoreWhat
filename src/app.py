from flask import Flask, render_template
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
server = app.server


app.layout = html.Div(
    [
        dcc.Dropdown(id="ycol", value="release_year", options=[1, 2, 3]),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
