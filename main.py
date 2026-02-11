import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui_mainwindow import Ui_MainWindow
from data_loader import load_file
from preprocessing import prepare_data
from ml_module import load_model, predict_price
from visualization import plot_price_dynamics
from database import Database

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database("tuition.db")
        self.model = load_model("model.pkl")

        self.ui.btnLoad.clicked.connect(self.load_data)
        self.ui.btnPredict.clicked.connect(self.make_prediction)
        self.ui.btnPlot.clicked.connect(self.show_plot)

    def load_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "CSV/XLSX (*.csv *.xlsx)")
        if not path:
            return

        df = load_file(path)
        df = prepare_data(df)
        self.db.save_dataframe(df)

        QMessageBox.information(self, "Готово", "Данные успешно загружены.")

    def make_prediction(self):
        year = int(self.ui.inputYear.text())
        program = self.ui.comboProgram.currentText()

        result = predict_price(self.model, year, program)
        self.ui.labelResult.setText(f"Прогноз: {result:.2f} руб.")

    def show_plot(self):
        df = self.db.load_all()
        plot_price_dynamics(df)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
