import matplotlib.pyplot as plt

def plot_price_dynamics(df):
    df = df.sort_values("year")
    plt.figure(figsize=(8, 5))
    plt.plot(df["year"], df["price"], marker="o")
    plt.xlabel("Год")
    plt.ylabel("Стоимость обучения")
    plt.title("Динамика стоимости образовательных услуг")
    plt.grid()
    plt.show()