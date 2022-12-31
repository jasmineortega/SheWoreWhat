from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

alt.data_transformers.disable_max_rows()


def plot_mostworn():
    most_worn = worn_df.nlargest(15, columns="Count")
    closet_comp = (
        alt.Chart(most_worn, title="2023 Most Worn Pieces")
        .mark_bar(color="#6ce4d8")
        .encode(
            alt.X("Name", title="", axis=alt.Axis(labelAngle=-45), sort="-y"),
            alt.Y("Count", title="Times Worn", axis=alt.Axis(tickMinStep=1)),
            alt.Tooltip("Count"),
        )
        .configure_axis(grid=False, domain=False)
    )

    return closet_comp


def plot_facet():

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


def top_10_df(path="../data/2023TestData.csv"):
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

    # data wrangling to select top 10 most worn items
    closet = sww.closet_df()
    worn_df = sww.complete_df(closet)
    most_worn = worn_df.nlargest(10, columns="Count")

    # merge dataframes
    df = pd.merge(closet, df, how="right", on="ID")
    df = df[["ID", "Item", "Color", "Pattern", "Category", "Date", "Brand"]]

    top_10 = most_worn["ID"].to_list()

    return top_10, df


def plot_heatmap(df, top_10, i=0):
    """
    Function for heatmap plot.

    Parameters:
    -----------
         df : pandas.DataFrame

         top_10 : list
            List containing the IDs of the top 10 most worn items.

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
