import numpy as np

def mean_price(df):
    return float(np.mean(df["price"]))


def median_price(df):
    return float(np.median(df["price"]))


def std_price(df):
    return float(np.std(df["price"]))


def variance_price(df):
    return float(np.var(df["price"]))


def describe_statistics(df):

    stats = {
        "mean": mean_price(df),
        "median": median_price(df),
        "std": std_price(df),
        "variance": variance_price(df)
    }

    return stats
