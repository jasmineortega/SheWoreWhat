from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


import sheworewhat as sww

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
                    [
                        html.Div(
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Br(),
                                                            html.P(
                                                                "The first thing I did was log everything in my closet. "
                                                                "A tedious process, but in the end I had {y} pieces."
                                                                "The majority of my closet is black or white."
                                                                "Colors represented in my closet -- need to add secondary colors."
                                                            ),
                                                        ],
                                                        width={"size": 6, "offset": 3},
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    html.P(
                                                                        "In 2023, I added {x} new items to my closet. Of these items, "
                                                                        "__% of the items were pre-loved (obtained through secondhand "
                                                                        "stores or hand me down. It's my goal for 90% of my closet to be secondhand!"
                                                                    )
                                                                ],
                                                                width={"offset": 3},
                                                            ),
                                                            #                                         dbc.Col[(
                                                            #                                                 html.H4("Well done!")
                                                            #                                         )],
                                                            dbc.Col(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            html.Iframe(
                                                                                id="new-items",
                                                                                style={
                                                                                    "border-width": "0",
                                                                                    "width": "100%",
                                                                                    "height": "400px",
                                                                                },
                                                                                srcDoc=sww.plot_color(
                                                                                    worn_df
                                                                                ).to_html(),
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="color",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_color(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="catwheel",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_categories(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.P(
                                                                "I own a lot of tops and very few coats."
                                                            ),
                                                        ],
                                                        width={"size": 3},
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Br(),
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="bought",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_bought(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                        title="Wardrobe Analysis",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.P(
                                                                "My top 10 most worn items ..."
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
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
                                                                            "height": "300px",
                                                                        },
                                                                        srcDoc=sww.plot_mostworn(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            ),
                                                        ],
                                                        width={"size": 5},
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
                                        title="Most Worn Items of 2023",
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
                                                                            "height": "425px",
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
    app.run_server(port=8076, debug=False)

# for running remotely
# if __name__ == "__main__":
#     app.run_server(debug=True)
