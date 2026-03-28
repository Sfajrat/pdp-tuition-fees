from PyQt5.QtWidgets import (
    QWidget, 
    QPushButton, 
    QLineEdit, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout,
    QGroupBox, 
    QComboBox, 
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView,
    QScrollArea
)


class Ui_MainWindow:

    def setupUi(self, MainWindow):

        MainWindow.setWindowTitle("Система анализа стоимости образовательных программ")
        MainWindow.resize(1000, 700)

        self.centralwidget = QWidget()

        # Заголовок
        self.titleLabel = QLabel("Анализ стоимости обучения")
        self.titleLabel.setStyleSheet("font-size:18px; font-weight:bold;")

        # Кнопки
        self.btnLoad = QPushButton("Загрузить данные")
        self.btnTrainModels = QPushButton("Обучить модели заново")
        self.btnPlot = QPushButton("Построить график")
        self.btnCompare = QPushButton("Сравнить модели / анализ")
        self.btnReport = QPushButton("Сформировать аналитический отчет")

        # Таблица для отображения данных
        self.dataTable = QTableWidget()
        self.dataTable.setColumnCount(7)
        self.dataTable.setHorizontalHeaderLabels([
            "Год", "Программа", "Длительность", "Форма обучения", "Студентов", "Стоимость (руб.)", "Вуз"
        ])
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dataTable.setAlternatingRowColors(True)

        # Блок прогнозирования
        self.groupPrediction = QGroupBox("Прогнозирование")

        self.modelCombo = QComboBox()
        self.modelCombo.addItems(["linear", "random_forest", "gradient_boosting"])

        self.inputYear = QLineEdit();     
        self.inputYear.setPlaceholderText("Год")
        self.inputLength = QLineEdit();   
        self.inputLength.setPlaceholderText("Длительность программы")
        self.inputStudents = QLineEdit(); 
        self.inputStudents.setPlaceholderText("Количество студентов")

        self.btnPredict = QPushButton("Сделать прогноз")
        self.labelResult = QLabel("Прогноз: ")

        predLayout = QVBoxLayout()
        predLayout.addWidget(QLabel("Модель:"))
        predLayout.addWidget(self.modelCombo)
        predLayout.addWidget(QLabel("Год"));           
        predLayout.addWidget(self.inputYear)
        predLayout.addWidget(QLabel("Длительность"));  
        predLayout.addWidget(self.inputLength)
        predLayout.addWidget(QLabel("Студентов"));     
        predLayout.addWidget(self.inputStudents)
        predLayout.addWidget(self.btnPredict)
        predLayout.addWidget(self.labelResult)
        self.groupPrediction.setLayout(predLayout)

        # Главный layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.titleLabel)

        # Кнопки в одну строку
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnLoad)
        btnLayout.addWidget(self.btnTrainModels)
        btnLayout.addWidget(self.btnPlot)
        btnLayout.addWidget(self.btnCompare)
        btnLayout.addWidget(self.btnReport)
        mainLayout.addLayout(btnLayout)

        # Таблица данных
        mainLayout.addWidget(QLabel("Загруженные данные:"))
        mainLayout.addWidget(self.dataTable, stretch=1)   # растягиваем таблицу

        # Блок прогнозирования
        mainLayout.addWidget(self.groupPrediction)

        self.centralwidget.setLayout(mainLayout)
        MainWindow.setCentralWidget(self.centralwidget)