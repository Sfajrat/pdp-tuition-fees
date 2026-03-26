import pandas as pd

def load_file(path):
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    elif path.endswith(".xlsx"):
        df = pd.read_excel(path)
    else:
        raise Exception("Неподдерживаемый формат файла")
    return df