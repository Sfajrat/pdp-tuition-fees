import matplotlib.pyplot as plt

def plot_price_dynamics(df):
    df = df.sort_values("year")
    plt.figure(figsize=(10, 6))
    plt.plot(df["year"], df["price"], marker="o", linewidth=2, color="navy")
    plt.xlabel("Год")
    plt.ylabel("Стоимость обучения (руб.)")
    plt.title("Динамика стоимости образовательных услуг")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()