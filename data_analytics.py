import pandas as pd

def calculate_average_price(df):
    return df["price"].mean()

def calculate_max_price(df):
    return df["price"].max()

def calculate_min_price(df):
    return df["price"].min()

def calculate_growth_rate(df):
    df = df.sort_values("year")
    prices = df["price"].values
    if len(prices) < 2:
        return 0
    growth = ((prices[-1] - prices[0]) / prices[0]) * 100
    return growth

def analyze_dataset(df):
    return {
        "avg_price": calculate_average_price(df),
        "max_price": calculate_max_price(df),
        "min_price": calculate_min_price(df),
        "growth_rate": calculate_growth_rate(df)
    }
    