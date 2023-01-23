from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


import sheworewhat as sww

closet = sww.closet_df()
worn_df = sww.worn(closet)
top_id, top_item, heat_df = sww.top_10_df()

app = Dash(__name__)
server = app.server

app.title = "She Wore What 2023"

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
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
                    ]
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
                                                            html.H4("The process"),
                                                            html.P(
                                                                "The first thing I did was take stock of everything in my closet -- "
                                                                "all {x} pieces. The most popular colors in my closet were black and white"
                                                                " -- need to add secondary colors still and also these numbers dont add up (87 colors and 93 items?)."
                                                            ),
                                                            html.Br(),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="color_composition",
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
                                                        ],
                                                        width={"size": 4},
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
                                                                "There was a lot of interesting patterns to deduce from my existing closet."
                                                                "For example, almost all my tops are secondhands while all my pants were purchased brand-new."
                                                            ),
                                                        ],
                                                        width={"size": 8},
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.P(
                                                                "In 2023, I added {x} new items to my closet. Of these items, "
                                                                "__% of the items were pre-loved (obtained through secondhand "
                                                                "stores or hand me down."
                                                            )
                                                        ],
                                                        width={"size": 8},
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="facet-items",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_newitems(
                                                                            worn_df
                                                                        ).to_html(),
                                                                    )
                                                                ]
                                                            )
                                                        ],
                                                        width={"size": 4},
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
                                                            )
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Br(),
                                                            html.Br(),
                                                            html.P(
                                                                "I try my best to reduce buying 'new' clothing items as much as possible. "
                                                                "For ethical and sustainability reasons, I aspire for my closet for "
                                                                "the majority of my closet to be secondhand! "
                                                                "If you'd like to learn more about the exploitative labor practices of fast fashion, "
                                                                "I highly recommend listening to Binchtopia's 'SheInvestigation' episode, which inspired me to "
                                                                "track my own personal style patterns so I can spend more wisely."
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
                                                            html.H4(
                                                                "Top 10 Most Worn Items"
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    html.P(
                                                        "My most worn pieces of clothing really ran the gamut. I'm not surprised that my most worn item"
                                                        " so far is my green Hollister Puffer jacket. Winter was especially brutal in 2023, which also "
                                                        "explains that my second most worn piece is my Blondo waterproof boots!"
                                                    )
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
                                                                            worn_df,
                                                                            top_item[0],
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
                                                                    dcc.Dropdown(
                                                                        id="item_name",
                                                                        options=[
                                                                            {
                                                                                "label": item,
                                                                                "value": [
                                                                                    i,
                                                                                    item,
                                                                                ],
                                                                            }
                                                                            for i, item in enumerate(
                                                                                top_item
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Iframe(
                                                                        id="heatmap_item",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=sww.plot_heatmap(
                                                                            top_id,
                                                                            heat_df,
                                                                        ).to_html(),
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.P(
                                                                "My most worn pieces of clothing really ran the gamut. I'm not surprised that my most worn item"
                                                                " so far is my green Hollister Puffer jacket. Winter was especially brutal in 2023, which also "
                                                                "explains that my second most worn piece is my Blondo waterproof boots!"
                                                            ),
                                                            html.P(
                                                                "While this data is interesting, it's too general to learn which items are considered core staples."
                                                                " Let's take a peak at the most worn items per category (tops, bottoms, shoes) instead!"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ],
                                        title="Most Worn Items of 2023",
                                    ),
                                    dbc.AccordionItem(
                                        html.P(
                                            "This would be a fun section to look at winter/spring/fall/summer trends. "
                                            "Unfortunately, we are only 15 days into winter so the data is not there yet."
                                        ),
                                        title="Seasonal Trends",
                                    ),
                                    # cost per wear
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H4("Cost-per-wear"),
                                                            html.P(
                                                                "Cost-per-wear: price of item / number of times worn in a single year"
                                                            ),
                                                            html.Br(),
                                                            html.P(
                                                                "Note: cost-per-wear was only calculated for items for which the price"
                                                                "was known, including items purchased secondhand. "
                                                            ),
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


@app.callback(Output("top10", "srcDoc"), Input("item_name", "value"))
def update_highlight(item_name):
    x = item_name[1]
    return sww.plot_mostworn(worn_df, x).to_html()


@app.callback(Output("heatmap_item", "srcDoc"), Input("item_name", "value"))
def update_output(item_name):
    y = item_name[0]
    return sww.plot_heatmap(top_id, heat_df, y).to_html()


# if __name__ == "__main__":
#     app.run_server(port=8070, debug=False)

# for running production
if __name__ == "__main__":
    app.run_server(debug=True)
