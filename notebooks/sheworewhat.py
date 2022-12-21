import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
    closet["Name"] = closet["ID"].apply(str) + " " + closet["Brand"] + " " + closet["Item"] + " - " + closet["PrimaryC"]

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
            globals()[f'{i}_df'] = df[df["Category"] == i.title()]

    # hardcode bc running into global var issue with these two (empty df)
    acc_df = df[df["Category"] == "Accessory"]
    fb_df = df[df["Category"] == "Full Body"]
    out_df = df[df["Category"] == "Outerwear"]
    
    return acc_df, bottom_df, fb_df, out_df, shoes_df, top_df
