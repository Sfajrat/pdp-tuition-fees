import pandas as pd

def load_file(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_excel(path)
