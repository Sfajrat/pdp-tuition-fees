from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox
)


class Ui_MainWindow:

    def setupUi(self, MainWindow):

        MainWindow.setWindowTitle("Система анализа стоимости образовательных программ")
        MainWindow.resize(400, 400)

        self.centralwidget = QWidget()

        # Заголовок
        self.titleLabel = QLabel("Анализ стоимости обучения")
        self.titleLabel.setStyleSheet("font-size:18px; font-weight:bold;")

        # Кнопки работы с данными
        self.btnLoad = QPushButton("Загрузить данные")
        self.btnPlot = QPushButton("Построить график")

        # Блок ввода параметров
        self.groupPrediction = QGroupBox("Параметры прогнозирования")

        self.inputYear = QLineEdit()
        self.inputYear.setPlaceholderText("Год")

        self.inputLength = QLineEdit()
        self.inputLength.setPlaceholderText("Длительность программы")

        self.inputStudents = QLineEdit()
        self.inputStudents.setPlaceholderText("Количество студентов")

        self.btnPredict = QPushButton("Сделать прогноз")

        self.labelResult = QLabel("Прогноз: ")

        predictionLayout = QVBoxLayout()

        predictionLayout.addWidget(QLabel("Год"))
        predictionLayout.addWidget(self.inputYear)

        predictionLayout.addWidget(QLabel("Длительность программы"))
        predictionLayout.addWidget(self.inputLength)

        predictionLayout.addWidget(QLabel("Количество студентов"))
        predictionLayout.addWidget(self.inputStudents)

        predictionLayout.addWidget(self.btnPredict)
        predictionLayout.addWidget(self.labelResult)

        self.groupPrediction.setLayout(predictionLayout)

        # Кнопка генерации отчета
        self.btnReport = QPushButton("Сформировать аналитический отчет")

        # Главный layout
        layout = QVBoxLayout()

        layout.addWidget(self.titleLabel)
        layout.addWidget(self.btnLoad)
        layout.addWidget(self.btnPlot)

        layout.addWidget(self.groupPrediction)

        layout.addWidget(self.btnReport)

        self.centralwidget.setLayout(layout)

        MainWindow.setCentralWidget(self.centralwidget)