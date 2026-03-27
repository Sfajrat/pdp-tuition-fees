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

            self.refresh_table()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", str(e))
            
    # Обновление таблицы
    def refresh_table(self):
        try:
            df = self.db.load_all()
            if df.empty:
                return

            self.ui.dataTable.setRowCount(len(df))

            for i, row in df.iterrows():
                self.ui.dataTable.setItem(i, 0, QTableWidgetItem(str(row.get('year', ''))))
                self.ui.dataTable.setItem(i, 1, QTableWidgetItem(str(row.get('program', ''))))
                self.ui.dataTable.setItem(i, 2, QTableWidgetItem(str(row.get('program_length', ''))))
                self.ui.dataTable.setItem(i, 3, QTableWidgetItem(str(row.get('students_count', ''))))
                self.ui.dataTable.setItem(i, 4, QTableWidgetItem(f"{row.get('price', 0):,.0f}"))
                self.ui.dataTable.setItem(i, 5, QTableWidgetItem(str(row.get('university', 'Не указан'))))
        except:
            pass

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

        model_name = self.ui.modelCombo.currentText()
        try:
            year = int(self.ui.inputYear.text())
            length = int(self.ui.inputLength.text())
            students = int(self.ui.inputStudents.text())

            result = self.model_manager.predict(model_name, year, length, students)
            self.ui.labelResult.setText(f"Прогноз ({model_name}): {result:,.2f} руб.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка прогноза", str(e))

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
                QMessageBox.warning(self, "Ошибка", "Нет данных для отчёта")
                return

            report_text = generate_report(df)

            # Диалог сохранения TXT
            path_txt, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить аналитический отчёт",
                "report.txt",
                "Text Files (*.txt);;All Files (*)"
            )

            if not path_txt:
                return

            # Сохраняем TXT
            export_report(report_text, path_txt)

            # Автоматически сохраняем PDF с тем же именем
            path_pdf = path_txt.replace(".txt", ".pdf") if path_txt.endswith(".txt") else path_txt + ".pdf"

            try:
                export_report_to_pdf(report_text, path_pdf)
                QMessageBox.information(
                    self,
                    "Готово",
                    f"Отчёт успешно сохранён!\n\n"
                    f"TXT: {path_txt}\n"
                    f"PDF: {path_pdf}"
                )
            except Exception as pdf_error:
                QMessageBox.warning(
                    self,
                    "PDF не создан",
                    f"TXT сохранён успешно.\n\nОшибка создания PDF:\n{str(pdf_error)}"
                )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка отчёта", str(e))


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec_())
    