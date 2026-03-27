import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow
from data_loader import load_file
from preprocessing import prepare_data
from ml_module import ModelManager
from visualization import plot_price_dynamics
from database import Database
from report_generator import generate_report
from export_module import export_report
from comparative_analysis import ComparativeAnalysis

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database("tuition.db")
        self.model_manager = ModelManager()

        # Загрузка моделей при старте
        for name in ["linear", "random_forest", "gradient_boosting"]:
            try:
                self.model_manager.load_model(name)
            except Exception:
                QMessageBox.warning(self, "Ошибка", f"Файл модели model_{name}.pkl не найден")

        # подключение кнопок интерфейса
        self.ui.btnLoad.clicked.connect(self.load_data)
        self.ui.btnTrainModels.clicked.connect(self.train_models)
        self.ui.btnPredict.clicked.connect(self.make_prediction)
        self.ui.btnPlot.clicked.connect(self.show_plot)
        self.ui.btnCompare.clicked.connect(self.compare_analysis)
        self.ui.btnReport.clicked.connect(self.create_report)

    # загрузка данных
    def load_data(self):

        path, _ = QFileDialog.getOpenFileName(self,
            "Выберите файл",
            "",
            "CSV/XLSX (*.csv *.xlsx)"
        )

        if not path:
            return

        try:
            df = load_file(path)
            df = prepare_data(df)

            if df.empty:
                QMessageBox.warning(self, "Ошибка", "Файл не содержит корректных данных")
                return

            self.db.save_dataframe(df)

            QMessageBox.information(self, "Успех", f"Загружено {len(df)} записей")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", str(e))

    #обучение моделей
    def train_models(self):
        try:
            df = self.db.load_all()
            if df.empty:
                QMessageBox.warning(self, "Ошибка", "Сначала загрузите данные")
                return

            X = df[["year", "program_length", "students_count"]]
            y = df["price"]

            self.model_manager = ModelManager()

            for name in ["linear", "random_forest", "gradient_boosting"]:
                self.model_manager.train_model(name, X, y, save_path=f"model_{name}.pkl")

            QMessageBox.information(self, "Успех", "Все три модели успешно обучены и сохранены!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка обучения", str(e))

    # прогнозирование
    def make_prediction(self):

        if self.model is None:
            QMessageBox.warning(self, "Ошибка", "Модель не загружена")
            return

        if not self.ui.inputYear.text():
            QMessageBox.warning(self, "Ошибка", "Введите год")
            return

        if not self.ui.inputLength.text():
            QMessageBox.warning(self, "Ошибка", "Введите длительность программы")
            return

        if not self.ui.inputStudents.text():
            QMessageBox.warning(self, "Ошибка", "Введите количество студентов")
            return

        try:

            year = int(self.ui.inputYear.text())
            length = int(self.ui.inputLength.text())
            students = int(self.ui.inputStudents.text())

            result = predict_price(self.model, year, length, students)

            self.ui.labelResult.setText(f"Прогноз: {result:.2f} руб.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка прогнозирования", str(e))

    # построение графика
    def show_plot(self):

        try:

            df = self.db.load_all()

            if df.empty:
                QMessageBox.warning(self, "Ошибка", "Нет данных для построения графика")
                return

            plot_price_dynamics(df)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка графика", str(e))

    # создание аналитического отчёта
    def create_report(self):

        try:

            df = self.db.load_all()

            if df.empty:
                QMessageBox.warning(self, "Ошибка", "Нет данных для формирования отчёта")
                return

            report_text = generate_report(df)

            path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить отчет",
                "report.txt",
                "Text Files (*.txt)"
            )

            if not path:
                return

            export_report(report_text, path)

            QMessageBox.information(self, "Готово", "Отчет успешно сохранён")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка отчета", str(e))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec_())
    