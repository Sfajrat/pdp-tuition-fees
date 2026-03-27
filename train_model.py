import pandas as pd
from ml_module import ModelManager

# Загружаем данные и используем только 3 признака, в будущем планируется добавить и другие признаки
df = pd.read_csv("tuition_data.csv")

X = df[["year", "program_length", "students_count"]]
y = df["price"]

manager = ModelManager()

for name in ["linear", "random_forest", "gradient_boosting"]:
    manager.train_model(name, X, y, save_path=f"model_{name}.pkl")
    print(f"Модель {name} успешно обучена и сохранена")

print("Все модели переобучены с 3 признаками!")
