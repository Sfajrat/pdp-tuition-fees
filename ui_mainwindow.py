from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit,
    QVBoxLayout, QComboBox
)

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Прогноз стоимости обучения")

        # Поле ввода года
        self.inputYear = QLineEdit()
        self.inputYear.setPlaceholderText("Введите год (например, 2026)")

        # Выбор программы
        self.comboProgram = QComboBox()
        self.comboProgram.addItems([
            "Экономика",
            "Менеджмент",
            "Программная инженерия",
            "Юриспруденция",
            "Психология",
            "ГМУ"
        ])

        # Кнопки
        self.btnLoad = QPushButton("Загрузить данные")
        self.btnPredict = QPushButton("Сделать прогноз")
        self.btnPlot = QPushButton("Показать график")

        # Результат
        self.labelResult = QLabel("Прогноз: —")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.inputYear)
        layout.addWidget(self.comboProgram)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnPredict)
        layout.addWidget(self.labelResult)
        layout.addWidget(self.btnPlot)

        central = QWidget()
        central.setLayout(layout)
        MainWindow.setCentralWidget(central)
