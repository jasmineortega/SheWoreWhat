from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


color_aes = [
    "#73de83",  # green
    "#73d2de",  # light blue
    "#7373de",  # lavender
    "#b173de",  # purple
    "#de73a5",  # magenta
    "#dec773",  # gold
]


def closet_df(path="data/ClosetData.csv"):
    """
    Function to import CSV data and return df with unique identifiers.

    Parameters:
    -----------
        path : str
            Path to CSV file containing closet information.

    Returns:
    --------
        closet : pandas.DataFrame
            Dataframe containing 12 columns: ID, Item, Category, Subcategory,
            Color, Pattern, Brand, Bought, Price, 2023, Cost, Name
    """
    # avoid setting with copy warning
    pd.options.mode.chained_assignment = None

    closet = pd.read_csv(path)

    # create IDs per item
    closet = closet.reset_index().rename(columns={"index": "ID"})

    # format strings to create item name
    closet["Item"] = closet["Item"].map(str.title)
    closet["Brand"] = closet["Brand"].map(str.title)
    closet["PrimaryC"] = closet["Color"].str[:5]

    # create item name
    closet["Name"] = (
        closet["ID"].apply(str)
        + " "
        + closet["Brand"]
        + " "
        + closet["Item"]
        + " - "
        + closet["PrimaryC"]
    )

    # NaNs in 2023 addition column
    for i, value in enumerate(closet["2023"]):
        if value != "Yes":
            closet["2023"].iloc[i] = "No"

    return closet


def fetch_data():
    """
    Function to fetch data from Google Sheet.

    Returns:
    --------

    """
    sheet_url = "https://docs.google.com/spreadsheets/d/1TP7HQZxiP6as_HHexcwkmDTeXOQQOLbUesZjHwKA-Q4/edit?resourcekey#gid=1344494584"
    url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(url_1).drop("Timestamp", axis=1).melt("Date").dropna()

    df["Date"] = pd.to_datetime(df["Date"])
    df["ID"] = df.value.str.extract("(\d+)").astype(int)
    df = df[df.variable != "Note"]  # drop notes to self

    return df


def counts(df=fetch_data()):
    """
    Function to count number of times items have been worn in a dataframe.

    Parameters:
    ----------
        df : pandas.DataFrame
            Dataframe of items to count frequency worn. Default is Google Sheet data.

    Returns:
    --------
        worn_df : pandas.DataFrame
            Dataframe containing "ID", "Name", "Count", "Item",
            "Category", "Sub-Category", "Color", "Pattern", "Brand", "Cost", "2023"
    """
    df_counts = (
        df.groupby(["value", "ID"])
        .count()
        .reset_index()
        .rename(columns={"Date": "count"})
        .drop(["variable"], axis=1)
    )

    # left join closet + df
    closet = closet_df()
    worn_df = pd.merge(closet, df_counts, how="left", on="ID")
    worn_df["Name"] = worn_df["Brand"] + " " + worn_df["Item"]
    worn_df = worn_df[
        [
            "ID",
            "Name",
            "count",
            "Item",
            "Category",
            "Sub-Category",
            "Color",
            "Pattern",
            "Brand",
            "Bought",
            "Cost",
            "2023",
            "Price",
        ]
    ]
    worn_df = worn_df.fillna(0).rename(columns={"count": "Count"})
    worn_df["Count"] = worn_df["Count"].astype(int)

    return worn_df


def worn():
    """
    Function to merge raw closet data and collected 2023 data.

    Returns
    -------
        worn_df : pandas.DataFrame
            Complete and standardized dataframe containing "ID", "Name", "count", "Item",
            "Category", "Sub-Category", "Color", "Pattern", "Brand", "Cost", "2023"
    """
    df = fetch_data()
    worn_df = counts(df)

    return worn_df


def plot_mostworn(
    worn_df,
    item_name="Adidas Tennis Shoe",
    i=10,
    title="Ten Most Worn Pieces in 2023",
    highlight="#73d2de",
):
    most_worn = worn_df.nlargest(i, columns="Count")
    closet_comp = (
        alt.Chart(most_worn, title=title)
        .mark_bar(
            cornerRadiusBottomRight=10,
            cornerRadiusTopRight=10,
            opacity=0.85,
        )
        .encode(
            alt.Y("Name", title="", axis=alt.Axis(labelAngle=-0), sort="-x"),
            alt.X("Count", title="Times Worn", axis=alt.Axis(tickMinStep=1)),
            alt.Tooltip("Count"),
            color=alt.condition(
                alt.datum.Name == item_name,
                alt.value(highlight),  # highlighted bar
                alt.value("#e0ddd5"),
            ),
            opacity=alt.condition(
                alt.datum.Name == item_name, alt.value(0.85), alt.value(0.50)
            ),
        )
        # .configure_title(color="#706f6c")
        # .configure_axis(
        #     labelColor="#706f6c", titleColor="#706f6c", grid=False, domain=False
        # )
    )
    return closet_comp


def plot_color(worn_df):
    """
    Function for color composition of color.

    Parameters:
    -----------
        worn_df : pandas.DataFrame
            Standardized dataframe obtained from worn function.
    Returns:
    --------
        plot : altair.Chart
            Pie chart of colors present in closet.
    """
    color_df = pd.concat(
        [
            worn_df[["ID", "Item", "Count", "Category"]],
            worn_df["Color"].str.split(",", n=2, expand=True),
        ],
        axis=1,
    )

    color_df = color_df.melt(
        id_vars=["ID"], value_vars=[0], var_name="former_column", value_name="Color"
    ).fillna("Delete")

    # only keep multiple colors if present
    color_df = color_df[color_df["Color"] != "Delete"]

    base = alt.Chart(color_df, title="Color Composition of 2023 Closet").encode(
        theta=alt.Theta("count()", stack=True),
        color=alt.Color(
            "Color",
            scale=alt.Scale(
                range=[
                    "#edc59a",  # beige
                    "#1a1919",  # black
                    "#455ad1",  # blue
                    "#422d08",  # brown
                    "#6e353a",  # burgundy
                    "#9c501e",  # clay
                    "#ffffcc",  # cream
                    "#dbbb07",  # gold
                    "#6e6e6e",  # gray
                    "#056e0e",  # green
                    "#c2addb",  # lavender
                    "#243763",  # navy
                    "#fa9c3e",  # orange
                    "#e872cc",  # pink,
                    "#ff2930",  # red
                    "#bdb3b4",  # silver
                    "#ab8f72",  # tan
                    "#faf9f6",  # white
                    "#faf20a",  # yellow
                ]
            ),
            legend=None,
        ),
        tooltip=["Color", "count()"],
    )

    plot_color = (
        base.mark_arc(innerRadius=0, opacity=0.80)
        .configure_view(strokeWidth=0)
        .configure_title(color="#706f6c")
        .configure_axis(labelColor="#706f6c", titleColor="#706f6c")
    )
    return plot_color


def plot_newitems(worn_df):
    """
    Plots new items purchased in 2023.

    Parameters:
    -----------
        worn_df : pandas.DataFrame
            Standardized dataframe obtained from worn function.
    Returns:
    --------
        plot : altair.Chart
            Pie chart of new items purchased in 2023.
    """
    new_2023 = worn_df.loc[worn_df["2023"] == "Yes"]
    new_2023["Bought"] = new_2023["Bought"].str.replace(
        "Secondhand, Thrifted", "Thrifted"
    )
    new_2023["Bought"] = new_2023["Bought"].str.replace("Secondhand, Depop", "Vintage")
    new_2023["Bought"] = new_2023["Bought"].str.replace("Secondhand, Gifted", "Gifted")
    new_2023["Secondhand"] = [
        "New" if i == "New" else "Secondhand" for i in new_2023["Bought"]
    ]

    base = (
        alt.Chart(new_2023, title="New Items Purchased in 2023")
        .mark_arc()
        .encode(
            theta=alt.Theta("count()", stack=True),
            color=alt.Color(
                "Bought",
                scale=alt.Scale(range=color_aes),
                legend=None,
            ),
            tooltip=["Bought", "count()"],
        )
    )

    cat = base.mark_arc(innerRadius=0, opacity=0.85)

    txt = base.mark_text(angle=0, radius=180, size=15).encode(
        alt.Color(
            "Bought",
            scale=alt.Scale(range=color_aes),
            legend=None,
        ),
        text="Bought",
    )
    plot_bought = cat + txt
    plot_bought = (
        plot_bought.configure_title(color="#706f6c")
        .configure_axis(
            grid=False, domain=False, labelColor="#706f6c", titleColor="#706f6c"
        )
        .configure_view(strokeWidth=0)
    )

    return plot_bought


def plot_bought(worn_df):
    """
    Function for secondhand vs new closet items.

    Parameters:
    -----------
        worn_df : pandas.DataFrame
            Standardized closet dataframe obtained via the worn function.
    Returns:
    --------
        plot : altair.Chart
            Bar chart of secondhand vs new closet composition.
    """
    worn_df["Bought"] = worn_df["Bought"].str.replace(
        "Secondhand, Thrifted", "Thrifted"
    )
    worn_df["Bought"] = worn_df["Bought"].str.replace("Secondhand, Depop", "Vintage")
    worn_df["Bought"] = worn_df["Bought"].str.replace("Secondhand, Gifted", "Gifted")
    worn_df["Secondhand"] = [
        "New" if i == "New" else "Secondhand" for i in worn_df["Bought"]
    ]

    plot = (
        alt.Chart(worn_df, title="New vs Secondhand Items")
        .mark_bar(cornerRadiusBottomRight=10, cornerRadiusTopRight=10, opacity=0.80)
        .encode(
            alt.X("count()", title="Count"),
            alt.Y("Secondhand", sort="-x"),
            alt.Color(
                "Bought",
                scale=alt.Scale(range=color_aes),
            ),
            tooltip="count()",
        )
        .configure_title(color="#706f6c")
        .configure_axis(
            grid=False, domain=False, labelColor="#706f6c", titleColor="#706f6c"
        )
        .properties(height=200)
    )
    return plot


def top_10_df():
    """
    Function to return IDs and counts of top 10 most worn items.

    Parameters:
    -----------
        None

    Returns:
    --------
        top_id : list
            List containing the IDs of the top 10 most worn items.
        top_item : list
            List containing the item names of the top 10 most worn items.
        df : pandas.DataFrame
            Dataframe containing data only for top 10 most worn items.
    """
    df = fetch_data()

    # column of day of week for one calender year
    time_df = pd.DataFrame()
    time_df["Date"] = pd.date_range(df["Date"].min(), periods=365)
    time_df["Day"] = time_df["Date"].dt.day_name()

    # data wrangling to select top 10 most worn items
    closet = closet_df()
    worn_df = worn()
    most_worn = worn_df.nlargest(10, columns="Count")

    # merge dataframes
    df = pd.merge(closet, df, how="right", on="ID")
    top_id = most_worn["ID"].to_list()
    top_item = (most_worn["Brand"] + " " + most_worn["Item"]).to_list()

    df = df[["ID", "Item", "Color", "Pattern", "Category", "Date", "Brand"]]

    return top_id, top_item, df


def plot_heatmap(top_10, df, z=0):
    """
    Function for heatmap plot. This is some knarly code I apologize.

    Parameters:
    -----------
         top_10 : list
            List containing the IDs of the top 10 most worn items,
            obtained from top_10_df function

         df : pandas.DataFrame
            Dataframe obtained from top_10_df containing count and ID of most worn items.

        i : int
            Positional number of the item to plot (0-9 for top 10)
    Returns:
    --------
        heatplot : altair.Chart
            Heatmap plot for a single item over a single calender year.

    """

    # column of day of week for one calender year
    time_df = pd.DataFrame()
    time_df["Date"] = pd.date_range(df["Date"].min(), periods=365)
    time_df["Day"] = time_df["Date"].dt.day_name()

    heatmap_data = df.loc[df["ID"] == top_10[z]]  # need to make this dynamic in plot
    item_name = heatmap_data["Brand"].iloc[0] + " " + heatmap_data["Item"].iloc[0]

    # isolate item data
    year = pd.merge(time_df, heatmap_data, how="outer", on="Date")
    year["Item"] = year["Item"].replace(np.nan, 0)
    year["Bool"] = np.where(year["Item"] == 0, 0, 1)

    # this is horrible to read lol
    # wrangling for prettier plotting
    week = time_df["Date"].dt.isocalendar()
    year["Week"] = week["week"].fillna(52)
    year["Week"] = year["Week"].fillna(52)
    year["First_day"] = year["Date"].dt.to_period("W-SAT").dt.start_time
    week = time_df["Date"].dt.strftime("%m-%d-%y")
    year["Week"] = year["First_day"].dt.strftime("%m-%d")
    year = year[["Date", "Day", "Item", "ID", "Bool", "Week"]]

    weekdays = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Sunday",
    ]

    heat_plot = (
        alt.Chart(year, title=f"{item_name} in 2023")
        .mark_rect(
            stroke="white",
            strokeWidth=3,
        )
        .encode(
            alt.X(
                "Week:O",
                axis=alt.Axis(
                    labelAngle=-60,
                ),
            ),
            alt.Y("Day", sort=weekdays, title=""),
            alt.Color(
                "Bool",
                scale=alt.Scale(domain=[0, 1], range=["#e0ddd5", "#73d2de"]),
                legend=None,
            ),
            alt.Tooltip(["Date", "Day"]),
            opacity=alt.condition(
                alt.datum.Bool == 1, alt.value(0.85), alt.value(0.50)
            ),
        )
        .properties(height=200, width=600)
        .configure_axis(
            grid=False, domain=False, labelColor="#706f6c", titleColor="#706f6c"
        )
        .configure_title(color="#706f6c")
        .configure_view(strokeWidth=0)
    )
    return heat_plot


def plot_cpw():
    """
    Function for 2023 cost-per-wear plot.

    Parameters:
    -----------
        None

    Returns:
    --------
        plot : altair.Chart
            Scatter plot of item counts over price.
    """

    df = fetch_data()
    worn_df = worn()

    # calculate 2023 cost-per-wear
    complete_df = pd.merge(worn_df, df, how="inner", on="ID")
    complete_df = complete_df[
        [
            "ID",
            "Name",
            "Count",
            "Category",
            "Sub-Category",
            "Pattern",
            "Cost",
            "2023",
            "Date",
            "Price",
        ]
    ]
    complete_df["CPW"] = (complete_df["Price"] / complete_df["Count"]).round(2)
    complete_df["Cost Per Wear"] = "$" + complete_df["CPW"].astype(str)
    complete_df["Cost Per Wear"] = [
        i if i[-3] == "." else i + "0" for i in complete_df["Cost Per Wear"]
    ]
    complete_df = complete_df[complete_df["Price"] > 0]

    plot = (
        alt.Chart(complete_df, title="2023 Cost Per Wear (CPW)")
        .mark_circle(opacity=0.70, size=200)
        .encode(
            alt.X("Price", scale=alt.Scale(domain=(0, 185))),
            alt.Y("Count", scale=alt.Scale(domain=(0, 25)), title="Times Worn"),
            alt.Color(
                "Category",
                scale=alt.Scale(range=color_aes),
            ),
            # alt.Size("CPW", scale=alt.Scale(domain=[0, 25]), legend=None),
            alt.Tooltip(["Name", "Category", "Cost Per Wear", "Count"]),
        )
        .configure_axis(grid=False, labelColor="#706f6c", titleColor="#706f6c")
        .configure_title(color="#706f6c")
        .interactive()
    )

    return plot


def season(day):
    """
    Function to assign season to day of year

    Returns:
    --------
        s : str
            Season that day of year in in.
    """
    # March 20 (79th day of year) = Spring Equinox
    if day in range(79, 172):
        s = "Spring"
    # June 21 (172nd day of year) = Summer Solstice
    elif day in range(172, 265):
        s = "Summer"
    # September 22 (265 day of year) = Fall Equinox
    elif day in range(265, 355):
        s = "Fall"
    # December 21 (355th day of year) = Winter Solstice
    # also need to include Jan 1 - March 19, 2023
    else:
        s = "Winter"
    # also need to include Jan 1 - March 19, 2023

    return s


def split_seasons():
    """
    Function to return Google Sheet data parsed by season.

    Returns:
        spring : pandas.DataFrame
            Dataframe containing data from March 20, 2023 - June 20, 2023
        summer : pandas.DataFrame
            Dataframe containing data from June 21, 2023 - Sept 21, 2023
        fall : pandas.DataFrame
            Dataframe containing data from Sept 22, 2023 - Dec 20, 2023
        winter : pandas.DataFrame
            Dataframe containing data from January 1, 2023 - March 20, 2023
            and December 21, 2023 to DEcember 31, 2023
    """
    df = fetch_data()
    df["Day"] = df["Date"].dt.dayofyear
    df["Season"] = df["Day"].map(season)

    spring = df.loc[df["Season"] == "Spring"]
    summer = df.loc[df["Season"] == "Summer"]
    fall = df.loc[df["Season"] == "Fall"]
    winter = df.loc[df["Season"] == "Winter"]

    return spring, summer, fall, winter


def plot_seasons():
    """fill in plz"""
    # split data
    spring, summer, fall, winter = split_seasons()

    # conduct counts on all four splits
    spring = counts(spring)
    summer = counts(summer)
    fall = counts(fall)
    winter = counts(winter)

    season_list = ["Spring", "Summer", "Fall", "Winter"]
    season_df = [spring, summer, fall, winter]
    color = ["#d81159", "#73de83", "#ffbc42", "#73d2de"]
    plot_list = []

    for i in range(0, 4):
        x = plot_mostworn(
            season_df[i],
            title=f"{season_list[i]}: Most Worn Pieces",
            i=5,
            highlight=color[i],
        )  # change winter to i once spring starts
        x = x.properties(height=100, width=200)
        plot_list.append(x)

    row1 = alt.vconcat(plot_list[3], plot_list[1])
    row2 = alt.vconcat(plot_list[2], plot_list[0])
    final = (
        alt.hconcat(row1, row2)
        .configure_title(color="#706f6c")
        .configure_axis(
            labelColor="#706f6c", titleColor="#706f6c", grid=False, domain=False
        )
    )
    return final


closet = closet_df()
worn_df = worn()
top_id, top_item, heat_df = top_10_df()

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

app.title = "She Wore What 2023"

app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.B("She Wore What 2023"),
                style={"color": "#218380", "font-size": "200%"},
                className="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.B("by Jasmine Ortega"),
                style={"color": "#218380", "font-size": "150%"},
                className="text-center",
            )
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            html.I(
                                "Pardon my appearance: I'm still under construction :-) "
                            )
                        ),
                        html.P(
                            "Hi! My name is Jasmine and I'm tracking every single item of clothing I wore in 2023. "
                            "As a data scientist and sustainable fashion enthusiast, this is a  "
                            "fun side project to help me make smarter decisions about my purchases in the future.",
                        ),
                    ],
                    className="text-center",
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
                                                                "all 99 pieces. The most frequent colors that appeared in my closet were black and white, followed by navy and green"
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
                                                                        srcDoc=plot_color(
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
                                                            html.P(
                                                                "In 2023, I added 1 new item to my closet. Of these items, "
                                                                "100% of these items were pre-loved (obtained through secondhand "
                                                                "stores or hand me down)."
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
                                                                        srcDoc=plot_newitems(
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
                                                                        srcDoc=plot_bought(
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
                                                                "Currently, about 50% of my closet is secondhand!"
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
                                                        "My most worn pieces of clothing really ran the gamut. I'm not surprised that my most worn item is "
                                                        "my Adidas tennis shoes. They are my go-to workout shoe and I try to workout a few times a week!"
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
                                                                        srcDoc=plot_mostworn(
                                                                            worn_df,
                                                                            top_item[0],
                                                                        )
                                                                        .configure_title(
                                                                            color="#706f6c"
                                                                        )
                                                                        .configure_axis(
                                                                            labelColor="#706f6c",
                                                                            titleColor="#706f6c",
                                                                            grid=False,
                                                                            domain=False,
                                                                        )
                                                                        .to_html(),
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
                                                                        srcDoc=plot_heatmap(
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
                                                                "While this data is interesting, I'm curious how my style habits evolved with the seasons."
                                                                "So let's take a peek at the most worn item per season."
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ],
                                        title="Most Worn Items of 2023",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.P(
                                                            "In this section I will investigate the winter/spring/fall/summer trends of my daily outfits. "
                                                            "Unfortunately, we are only one month into winter so the data is not there (yet!)"
                                                        ),
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Iframe(
                                                                        id="seasons",
                                                                        style={
                                                                            "border-width": "0",
                                                                            "width": "100%",
                                                                            "height": "400px",
                                                                        },
                                                                        srcDoc=plot_seasons().to_html(),
                                                                    )
                                                                ]
                                                            )
                                                        ],
                                                        width={"size": 8},
                                                    ),
                                                ]
                                            )
                                        ],
                                        title="Seasonal Trends",
                                    ),
                                    # cost per wear
                                    dbc.AccordionItem(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H4(
                                                                "Cost-per-wear: price of item / number of times worn in a single year"
                                                            ),
                                                            html.P(
                                                                "Placeholder for fun yet insightful commentary. P.S. This plot is interactive, you can zoom in on items. "
                                                            ),
                                                            html.I(
                                                                "Note: cost-per-wear was only calculated for items for which the price"
                                                                " was known, including items purchased secondhand. "
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
                                                                        srcDoc=plot_cpw().to_html(),
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
                                        [
                                            html.P(
                                                "If you are interested in learning more about the environmental impact and ethics of clothing made in fast-fashion "
                                                "factories, I have included some links below:"
                                            ),
                                            html.A(
                                                "Why The Fashion Revolution Must Be Intersectional",
                                                href="https://peppermintmag.com/fashion-revolution-week-2021/",
                                            ),
                                            html.Br(),
                                            html.I(
                                                "If you are in a position to do so, decolonise your wardrobe and buy from ethical and Black-owned brands..."
                                                " The face of sustainability is white and affluent. Challenge the narrative!"
                                            ),
                                            html.Br(),
                                            html.Br(),
                                            html.A(
                                                "Can I Buy Fast Fashion and Not Feel Guilty?",
                                                href="https://www.nytimes.com/2022/05/20/fashion/fast-fashion-sustainable-clothing.html",
                                            ),
                                            html.Br(),
                                            html.I(
                                                "Wherever you buy, your solution — wear your products more — is absolutely key."
                                            ),
                                            html.Br(),
                                            html.Br(),
                                            html.A(
                                                "Binchtopia's SheInvestigation",
                                                href="https://podcasts.apple.com/us/podcast/sheinvestigation/id1542744511?i=1000585638727",
                                            ),
                                            html.Br(),
                                            html.I(
                                                "In this episode, the girlies investigate the fashion giant Shein and explore ideas of ethical labor, sustainability, and trend cycles. "
                                            ),
                                            html.Br(),
                                            html.Br(),
                                            html.P(
                                                "Above all, the most important action an individual can take is to buy less! While this isn't the most fun answer,"
                                                "it's important to not get caught up in the tantalizing marketing of 'sustainable fashion'. The most sustainable items are the ones that are already in your closet! :-)"
                                            ),
                                            html.Br(),
                                            html.P(
                                                "There were a lot of sources of inspiration for SheWoreWhat:"
                                            ),
                                            html.A(
                                                "BlondeBroke&Bougie's 2022 Closet Wrapped",
                                                href="https://www.tiktok.com/@blondebrokeandbougie/video/7175604635976355118?is_copy_url=1&is_from_webapp=v1&lang=en",
                                            ),
                                            html.P(
                                                "This TikTok came across my FYP and inspired me to see what insights I could gather from tracking my closet. "
                                                "Becca sells the Excel template she used in this video, which can be found at https://blondebrokeandbougie.com"
                                            ),
                                            html.A(
                                                "How the 20 Year Trend Cycle Collapsed",
                                                href="https://www.vice.com/en/article/bvmkm8/how-the-20-year-trend-cycle-collapsed",
                                            ),
                                            html.Br(),
                                            html.I(
                                                "The dark side of the trend cycle being shortened is that it’s inarguably happening, at least in part, "
                                                "because of fast fashion. Though we know of its devastating environmental impact, we are still buying "
                                                "cheap garments online. Instead of fashion being dominated by a couple of seasons and collections a year, "
                                                "companies push new clothes all year around and fuel our obsession with faster and faster micro-trends. "
                                                "As we’ve seen this year, as soon as something is coined on TikTok, it’ll be available to buy online."
                                            ),
                                            html.Br(),
                                            html.P(
                                                "The intersection of fast-fashion, personal style, and sustainability is something I'm really passionate about. "
                                                "However, oftentimes, the conversation around fashion feels inaccessible (which is maybe part of the problem). "
                                                "This project was a conglomeration of topics that have been bouncing around my head for a few years. I'm by no means "
                                                "an expert, but I did enjoy unpacking my own fashion habits as a path to improve my personal sustainability and personal style journey. :-) "
                                            ),
                                        ],
                                        title="Resources",
                                    ),
                                ],
                                start_collapsed=True,
                                always_open=True,
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
    return plot_mostworn(worn_df, x).to_html()


@app.callback(Output("heatmap_item", "srcDoc"), Input("item_name", "value"))
def update_output(item_name):
    y = item_name[0]
    return plot_heatmap(top_id, heat_df, y).to_html()


if __name__ == "__main__":
    app.run(debug=True)
