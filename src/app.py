from flask import Flask, render_template
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)
server = app.server


@app.route("/")
def index():
    return "Woohoo"


if __name__ == "__main__":
    app.run(debug=True)
