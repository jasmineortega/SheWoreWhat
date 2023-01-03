from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import sheworewhat as sww

alt.data_transformers.disable_max_rows()

closet = sww.closet_df()
worn_df = sww.complete_df(closet)
top_10, heat_df = sww.top_10_df()

app = Dash(__name__)
server = app.server

app.title = "She Wore What 2023"

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])  # QUARTZ OR LUX
app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.B("She Wore What 2023"),
                style={"font-weight": "bold", "color": "#000000", "font-size": "150%"},
            )
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            "Hi! My name is Jasmine and I tracked every single item of clothing I wore in 2023. "
                            "As a data scientist and sustainable fashion enthusiast, I thought "
                            "this would be a fun project to help me analyze my personal style"
                            "trends so I can make smarter decisions about my purchases in the future.",
                        )
                    ],
                    width={"size": 6},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [  #
                        html.Div(
                            dbc.Accordion(
                                [
                                    # top 10 plots + facet plots
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="top10",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_mostworn(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Br(),
                                                            html.P(
                                                                "My top 10 most worn items of the year. Some of these seem"
                                                                " obvious -- my Hollister puffer coat is my go-to winter coat. My gold brand "
                                                                "hoop earrings are a daily staple. But this plot doesn't tell us much on it's own"
                                                                "let's break down the items by category. "
                                                                "Note to self: would be cool to insert images here"
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [html.Br(), html.P("Facets!")]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="top5_cat",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "800px",
                                                                        },
                                                                        srcDoc=sww.plot_facet(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                        title="Most Worn Items Overall",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Br(),
                                                            html.P(
                                                                "Fun little heatmap of the top 10 items -- need to work on drop down menu."
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="heatmap",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "300px",
                                                                        },
                                                                        srcDoc=sww.plot_heatmap(
                                                                            top_10,
                                                                            heat_df,
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                        title="Item Heatmap Throughout 2023",
                                    ),
                                    # cost per wear
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.P(
                                                                "Cost-per-wear: price of item / number of time worn"
                                                                "Please note, the cost-per-wear was only calculated for items for which price"
                                                                "was known, including items purchased secondhand. "
                                                            )
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="costperwear",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_cpw(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ],
                                        title="Cost Per Wear",
                                    ),
                                    dbc.AccordionItem(
                                        "This is the content of the third section",
                                        title="Item 3",
                                    ),
                                ],
                                start_collapsed=True,
                            )
                        )
                    ]
                ),
            ]
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(port=8078, debug=False)

# for running remotely
# if __name__ == "__main__":
#     app.run_server(debug=True)
