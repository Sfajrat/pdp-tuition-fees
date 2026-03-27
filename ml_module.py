import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

class ModelManager:
    def __init__(self):
        self.models = {}
        self.scaler = None
        self.feature_names = ['year', 'program_length', 'students_count']  # только эти 3 признака

    MODEL_PATH = "model.pkl"


    def load_model(self, model_name, path=None):
        # Загружает модель, если она существует. Если файла нет — обучает модель автоматически.
        if path is None:
            path = f"{model_name}_model.pkl"
        data = joblib.load(path)
        self.models[model_name] = data
        self.scaler = data["scaler"]
        return data["model"]


    def train_model(self, model_name, X, y, save_path=None):
        # Обучает модель для каждой образовательной программы. В x содержится только : year, program_length, students_count, в будущем можно добавить форму обучения
        if model_name == "linear":
            model = LinearRegression()
        elif model_name == "random_forest":
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_name == "gradient_boosting":
            model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError("Неизвестная модель")

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        model.fit(X_scaled, y)

        if save_path:
            joblib.dump({
                "model": model,
                "scaler": self.scaler,
                "feature_names": self.feature_names
            }, save_path)

        self.models[model_name] = {"model": model, "scaler": self.scaler}
        return model


    def predict_price(models, year, program):
        """
        Возвращает прогноз стоимости для выбранной программы.
        """
        if program not in models:
            raise ValueError(f"Нет обученной модели для программы: {program}")

        model = models[program]
        X = np.array([[year]])
        return float(model.predict(X)[0])
