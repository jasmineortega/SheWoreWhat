from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

alt.data_transformers.disable_max_rows()

# for future reference here are the plots I've worked on
# TO DO: functionize them

# PLOT 1
# most_worn = worn_df.nlargest(15, columns="Count")
# closet_comp = alt.Chart(most_worn, title="2023 Most Worn Pieces"
#                        ).mark_bar(color="Maroon"
#                          ).encode(alt.X("Name", axis=alt.Axis(labelAngle=-45), sort="-y"),
#                                   alt.Y("Count",
#                                         title="# of Times Worn",
#                                         axis=alt.Axis(tickMinStep=1)),
#                                   alt.Tooltip("Count")
#                                  )

# closet_comp

# PLOT(S) 2
# categories = ["Top", "Bottom", "Full Body", "Outerwear", "Accessory", "Shoes"]

# cat_plots = []

# for i in categories:
#     category_worn = worn_df.loc[worn_df["Category"] == i].nlargest(5, columns="Count")

#     category_plot = alt.Chart(category_worn, title=f"2023 Most Worn {i}"
#                        ).mark_bar(color="#B40490"
#                        ).encode(alt.X("Name", title="", axis=alt.Axis(labelAngle=-45), sort="-y"),
#                                 alt.Y("Count",
#                                 title="# of Times Worn",
#                                 axis=alt.Axis(tickMinStep=1)),
#                                 alt.Tooltip(["Name", "Count"])
#                         ).resolve_scale(x='independent')
#     cat_plots.append(category_plot)

# # configure altair charts
# row1 = alt.hconcat(cat_plots[0], cat_plots[1], cat_plots[2])
# row2 = alt.hconcat(cat_plots[3], cat_plots[4], cat_plots[5])

# category_plot = alt.vconcat(row1, row2)
# category_plot
