import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("tuition_data.csv")

X = df[["year", "program_length", "students_count"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Модель сохранена")
