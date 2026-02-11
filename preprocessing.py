def prepare_data(df):
    df = df.dropna()
    df = df[df["price"] > 0]
    return df
