import pandas as pd
import numpy as np
import altair as alt
import dash_bootstrap_components as dbc


def closet_df(path="../data/ClosetData.csv"):
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


def closet_cat(df):
    """
    Function to parse closet df into five distinct datasets

    1) Accessories
    2) Bottoms
    3) Full Body
    4) Outerwear
    5) Shoes
    6) Tops

    Parameters:
    -----------
        df : pandas.DataFrame
            Dataframe obtained from closet_df function

    Returns:
    --------
        acc_df : pandas.DataFrame
            Dataframe containing only accessory data.

        bottom_df : pandas.DataFrame
            Dataframe containing only bottom data.

        fb_df : pandas.DataFrame
            Dataframe containing only full-body data.

        out_df : pandas.DataFrame
            Dataframe containing only outerwear data.

        shoes_df : pandas.DataFrame
            Dataframe containing only shoe data.

        top_df : pandas.DataFrame
            Dataframe containing only top data.

    """
    categories = ["top", "bottom", "fb", "outerwear", "acc", "shoes"]

    for i in categories:
        if i != "fb" or i != "acc":
            globals()[f"{i}_df"] = df[df["Category"] == i.title()]

    # hardcode bc running into global var issue with these two (empty df)
    acc_df = df[df["Category"] == "Accessory"]
    fb_df = df[df["Category"] == "Full Body"]
    out_df = df[df["Category"] == "Outerwear"]

    return acc_df, bottom_df, fb_df, out_df, shoes_df, top_df


def worn(closet):
    """
    Function to merge raw closet data and collected 2023 data.

    Parameters
    ----------
        closet : pandas.DataFrame
            Dataframe containing complete closet log.

    Returns
    -------
        worn_df : pandas.DataFrame
            Complete and standardized dataframe containing "ID", "Name", "count", "Item",
            "Category", "Sub-Category", "Color", "Pattern", "Brand", "Cost", "2023"
    """

    sheet_url = "https://docs.google.com/spreadsheets/d/1TP7HQZxiP6as_HHexcwkmDTeXOQQOLbUesZjHwKA-Q4/edit?resourcekey#gid=1344494584"
    url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")
    form = pd.read_csv(url_1).drop("Timestamp", axis=1).melt("Date").dropna()

    # extract ID number from value
    form["ID"] = form.value.str.extract("(\d+)").astype(int)

    form_counts = (
        form.groupby(["value", "ID"])
        .count()
        .reset_index()
        .rename(columns={"Date": "count"})
        .drop(["variable"], axis=1)
    )

    # left join closet + df
    worn_df = pd.merge(closet, form_counts, how="left", on="ID")
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


def plot_mostworn(worn_df, item_name="Adidas Tennis Shoe"):
    most_worn = worn_df.nlargest(10, columns="Count")
    closet_comp = (
        alt.Chart(most_worn, title="Ten Most Worn Pieces in 2023")
        .mark_bar(
            color="#d81159",
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
                alt.value("#218380"),  # highlights selected bar
                alt.value("#e0ddd5"),
            ),
        )
        .configure_title(color="#706f6c")
        .configure_axis(
            labelColor="#706f6c", titleColor="#706f6c", grid=False, domain=False
        )
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
    # change this to "Yes"
    new_2023 = worn_df.loc[worn_df["2023"] == "No"]
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
                scale=alt.Scale(
                    range=[
                        "#ffbc42",
                        "#d81159",
                        "#652d8f",
                        "#25592a",
                        "#218380",
                        "#73d2de",
                    ]
                ),
                legend=None,
            ),
            tooltip=["Bought", "count()"],
        )
    )

    cat = base.mark_arc(innerRadius=0, opacity=0.85)

    txt = base.mark_text(angle=0, radius=180, size=15).encode(
        alt.Color(
            "Bought",
            scale=alt.Scale(
                range=[
                    "#ffbc42",
                    "#d81159",
                    "#652d8f",
                    "#25592a",
                    "#218380",
                    "#73d2de",
                ]
            ),
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


def plot_categories(worn_df):
    """
    Function for categorial composition of closet.

    Parameters:
    -----------
        worn_df : pandas.DataFrame
            Standardized dataframe obtained from worn function.
    Returns:
    --------
        plot : altair.Chart
            Pie chart of clothing categories present in closet.
    """
    worn_df["Bought"] = worn_df["Bought"].str.replace(
        "Secondhand, Thrifted", "Thrifted"
    )
    worn_df["Bought"] = worn_df["Bought"].str.replace("Secondhand, Depop", "Vintage")
    worn_df["Bought"] = worn_df["Bought"].str.replace("Secondhand, Gifted", "Gifted")

    base = alt.Chart(worn_df, title="Closet Categories").encode(
        theta=alt.Theta("count()", stack=True),
        color="Category",
        tooltip=["Category", "count()"],
    )

    cat = base.mark_arc(innerRadius=0, opacity=0.80)
    txt = base.mark_text(radius=177, size=15).encode(
        alt.Color(
            "Category",
            scale=alt.Scale(
                range=["#ffbc42", "#d81159", "#652d8f", "#25592a", "#218380", "#73d2de"]
            ),
            legend=None,
        ),
        text="Category",
    )

    plot_categories = cat + txt
    plot_categories = (
        plot_categories.configure_view(strokeWidth=0)
        .configure_title(color="#706f6c")
        .configure_axis(labelColor="#706f6c", titleColor="#706f6c")
    )

    return plot_categories


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
                scale=alt.Scale(
                    range=[
                        "#ffbc42",
                        "#d81159",
                        "#652d8f",
                        "#25592a",
                        "#218380",
                        "#73d2de",
                    ]
                ),
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


def plot_facet(worn_df):
    """
    Function to plot top 5 most worn items per clothing category.

    Parameters:
    ----------
        worn_df : pandas.DataFrame
            Standardized dataframe obtained from worn function.

    Returns:
    --------
        category_plot : altair.Chart
            Six concatenated altair plots for Top, Bottom, Full Body, Outerwear, Accesories,
            and Shoe categories.
    """
    categories = ["Top", "Bottom", "Full Body", "Outerwear", "Accessory", "Shoes"]

    cat_plots = []

    for i in categories:
        category_worn = worn_df.loc[worn_df["Category"] == i].nlargest(
            5, columns="Count"
        )

        category_plot = (
            alt.Chart(category_worn, title=f"2023 Most Worn {i}")
            .mark_bar(
                color="#827191",
            )
            .encode(
                alt.X("Name", title="", axis=alt.Axis(labelAngle=-45), sort="-y"),
                alt.Y("Count", title="# of Times Worn", axis=alt.Axis(tickMinStep=1)),
                alt.Tooltip(["Name", "Count"]),
            )
            .properties(height=200, width=150)
        )
        cat_plots.append(category_plot)

    # configure altair charts
    row1 = alt.hconcat(cat_plots[0], cat_plots[1], cat_plots[2])
    row2 = alt.hconcat(cat_plots[3], cat_plots[4], cat_plots[5])

    category_plot = (
        alt.vconcat(row1, row2)
        .configure_axis(
            grid=False, domain=False, labelColor="#706f6c", titleColor="#706f6c"
        )
        .configure_title(color="#706f6c")
    )
    return category_plot


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
    sheet_url = "https://docs.google.com/spreadsheets/d/1TP7HQZxiP6as_HHexcwkmDTeXOQQOLbUesZjHwKA-Q4/edit?resourcekey#gid=1344494584"
    url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(url_1).drop("Timestamp", axis=1).melt("Date").dropna()

    df["Date"] = pd.to_datetime(df["Date"])
    df["ID"] = df.value.str.extract("(\d+)").astype(int)

    # column of day of week for one calender year
    time_df = pd.DataFrame()
    time_df["Date"] = pd.date_range(df["Date"].min(), periods=365)
    time_df["Day"] = time_df["Date"].dt.day_name()

    # data wrangling to select top 10 most worn items
    closet = closet_df()
    worn_df = worn(closet)
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
            opacity=0.80,
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
                scale=alt.Scale(domain=[0, 1], range=["#e0ddd5", "#218380"]),
                legend=None,
            ),
            alt.Tooltip(["Date", "Day"]),
        )
        .properties(height=200, width=600)
        .configure_axis(
            grid=False, domain=False, labelColor="#706f6c", titleColor="#706f6c"
        )
        .configure_title(color="#706f6c")
        .configure_view(strokeWidth=0)
    )
    return heat_plot


def plot_cpw(worn_df):
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

    # read in Google sheet idea
    sheet_url = "https://docs.google.com/spreadsheets/d/1TP7HQZxiP6as_HHexcwkmDTeXOQQOLbUesZjHwKA-Q4/edit?resourcekey#gid=1344494584"
    url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(url_1).drop("Timestamp", axis=1).melt("Date").dropna()

    df["Date"] = pd.to_datetime(df["Date"])
    df["ID"] = df.value.str.extract("(\d+)").astype(int)

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
    complete_df["CPW"] = (complete_df["Price"] / complete_df["Count"]).round(1)
    complete_df["Cost Per Wear"] = "$" + complete_df["CPW"].astype(str) + "0"

    plot = (
        alt.Chart(complete_df, title="2023 Cost Per Wear (CPW)")
        .mark_circle(opacity=0.70)
        .encode(
            alt.X("Price", scale=alt.Scale(domain=(0, 200))),
            alt.Y("Count", scale=alt.Scale(domain=(0, 60)), title="Times Worn"),
            alt.Color(
                "Category",
                scale=alt.Scale(
                    range=[
                        "#ffbc42",
                        "#d81159",
                        "#652d8f",
                        "#25592a",
                        "#218380",
                        "#73d2de",
                    ]
                ),
            ),
            alt.Size("CPW", scale=alt.Scale(domain=[0, 35]), legend=None),
            alt.Tooltip(["Name", "Category", "Cost Per Wear"]),
        )
        .configure_axis(grid=False, labelColor="#706f6c", titleColor="#706f6c")
        .configure_title(color="#706f6c")
    )

    return plot
