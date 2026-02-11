import joblib
import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LinearRegression


MODEL_PATH = "model.pkl"


def load_model(path=MODEL_PATH):
    """
    Загружает модель, если она существует.
    Если файла нет — обучает модель автоматически.
    """
    if not os.path.exists(path):
        print("⚠ model.pkl не найден — выполняю обучение модели...")
        model = train_default_model()
        joblib.dump(model, path)
        print("✔ Модель обучена и сохранена.")
        return model

    return joblib.load(path)


def train_default_model():
    """
    Обучает отдельную модель для каждой образовательной программы.
    Требования:
    - файл data.csv должен лежать рядом с main.py
    - колонки: year, university, program, form, cost
    """
    if not os.path.exists("data.csv"):
        raise FileNotFoundError("Файл data.csv не найден. Невозможно обучить модель.")

    df = pd.read_csv("data.csv")

    required = {"year", "university", "program", "form", "cost"}
    if not required.issubset(df.columns):
        raise ValueError(f"В data.csv должны быть колонки: {required}")

    models = {}

    # Обучаем отдельную модель для каждой программы
    for program in df["program"].unique():
        df_prog = df[df["program"] == program]

        X = df_prog[["year"]]
        y = df_prog["cost"]

        model = LinearRegression()
        model.fit(X, y)

        models[program] = model

    return models


def predict_price(models, year, program):
    """
    Возвращает прогноз стоимости для выбранной программы.
    """
    if program not in models:
        raise ValueError(f"Нет обученной модели для программы: {program}")

    model = models[program]
    X = np.array([[year]])
    return float(model.predict(X)[0])
