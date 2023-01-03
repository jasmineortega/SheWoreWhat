import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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


def complete_df(closet, path="../data/2023Data.csv"):
    """
    Function to merge raw closet data and collected 2023 data.

    Parameters
    ----------
        closet : pandas.DataFrame
            Dataframe containing complete closet log.
        path : string
            String containing path of CSV of collected data.

    Returns
    -------
        complete_df : pandas.DataFrame
            Dataframe containing "ID", "Name", "count", "Item",
            "Category", "Sub-Category", "Color", "Pattern", "Brand", "Cost", "2023"
    """

    form = pd.read_csv(path).drop("Timestamp", axis=1).melt("Date").dropna()

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
    complete_df = pd.merge(closet, form_counts, how="left", on="ID")
    complete_df["Name"] = complete_df["Brand"] + " " + complete_df["Item"]
    complete_df = complete_df[
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
            "Cost",
            "2023",
            "Price",
        ]
    ]
    complete_df = complete_df.fillna(0).rename(columns={"count": "Count"})
    complete_df["Count"] = complete_df["Count"].astype(int)

    return complete_df


def plot_mostworn(worn_df):
    most_worn = worn_df.nlargest(15, columns="Count")
    closet_comp = (
        alt.Chart(most_worn, title="2023 Most Worn Pieces")
        .mark_bar(color="#6ce4d8")
        .encode(
            alt.Y("Name", title="", axis=alt.Axis(labelAngle=-0), sort="-x"),
            alt.X("Count", title="Times Worn", axis=alt.Axis(tickMinStep=1)),
            alt.Tooltip("Count"),
        )
        .configure_axis(grid=False, domain=False)
    )

    return closet_comp


def plot_facet(worn_df):

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

    category_plot = alt.vconcat(row1, row2).configure_axis(grid=False, domain=False)
    return category_plot


def top_10_df(path="../data/2023Data.csv"):
    """
    Function to return IDs and counts of top 10 most worn items.

    Parameters:
    -----------
         path : str
            Path to CSV file containing closet information.

    Returns:
    --------
        top_10 : list
            List containing the IDs of the top 10 most worn items.

        df : pandas.DataFrame
            Dataframe containing data only for top 10 most worn items.
    """
    df = pd.read_csv(path).drop("Timestamp", axis=1).melt("Date").dropna()
    df["Date"] = pd.to_datetime(df["Date"])
    df["ID"] = df.value.str.extract("(\d+)").astype(int)

    # column of day of week for one calender year
    time_df = pd.DataFrame()
    time_df["Date"] = pd.date_range(df["Date"].min(), periods=365)
    time_df["Day"] = time_df["Date"].dt.day_name()

    # data wrangling to select top 10 most worn items
    closet = closet_df()
    worn_df = complete_df(closet)
    most_worn = worn_df.nlargest(10, columns="Count")

    # merge dataframes
    df = pd.merge(closet, df, how="right", on="ID")
    df = df[["ID", "Item", "Color", "Pattern", "Category", "Date", "Brand"]]

    top_10 = most_worn["ID"].to_list()

    return top_10, df


def plot_heatmap(top_10, df, i=0):
    """
    Function for heatmap plot.

    Parameters:
    -----------
         top_10 : list
            List containing the IDs of the top 10 most worn items.

         df : pandas.DataFrame

    Returns:
    --------
        heatplot : altair.Chart
            Heatmap plot for a single item over a single calender year.

    """

    # column of day of week for one calender year
    time_df = pd.DataFrame()
    time_df["Date"] = pd.date_range(df["Date"].min(), periods=365)
    time_df["Day"] = time_df["Date"].dt.day_name()

    heatmap_data = df.loc[df["ID"] == top_10[i]]  # need to make this dynamic in plot
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
    year["First_day"] = year["Date"] - year["Date"].dt.weekday * np.timedelta64(1, "D")
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
            opacity=0.9,
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
                scale=alt.Scale(domain=[0, 1], range=["#e0ddd5", "#74a675"]),
                legend=None,
            ),
            alt.Tooltip(["Date", "Day"]),
        )
        .properties(height=200, width=600)
        .configure_axis(grid=False, domain=False)
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
    df = (
        pd.read_csv("../data/2023Data.csv")
        .drop("Timestamp", axis=1)
        .melt("Date")
        .dropna()
    )
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
    complete_df["CPW"] = (complete_df["Price"] / complete_df["Count"]).round(2)

    plot = (
        alt.Chart(complete_df, title="2023 Cost Per Wear (CPW)")
        .mark_circle(opacity=0.80)
        .encode(
            alt.X("Price"),
            alt.Y("Count", title="Times Worn"),
            alt.Color(
                "Category",
                scale=alt.Scale(
                    range=[
                        "#bb8c9d",
                        "#9a8ca6",
                        "#8ba88a",
                        "#5bccc1",
                        "#e0ddd5",
                        "#7c9e7b",
                    ]
                ),
            ),
            alt.Size("CPW", legend=None),
            alt.Tooltip(["Name", "Category", "CPW"]),
        )
        .configure_axis(grid=False)
    )

    return plot
