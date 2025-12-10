from PyQt6.QtWidgets import QWidget, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from WindowBolt import WindowBolt
from WindowGayka import WindowGayka
from WindowPruzh import WindowPruzh
from WindowShayba import WindowShayba

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__centralWidget = QWidget()
        self.__mainLayout = QVBoxLayout(self.__centralWidget)
        
        self.__leftColum = QHBoxLayout()
        self.__rightColum = QHBoxLayout()
        self.__centerColum = QHBoxLayout()

        self.__buttonBolt = QPushButton("Болт")
        self.__buttonGayka = QPushButton("Гайка")
        self.__buttonShayba = QPushButton("Шайба")
        self.__buttonPruzh = QPushButton("Пружина")


        self.__initField()
        self.__ui()
        self.__event()
        self.__style()

    def __initField(self):
        self.setWindowTitle("Lib Kompas")
        self.resize(500,400)
        self.setCentralWidget(self.__centralWidget)

        self.__buttonBolt.setFixedSize(200,50)
        self.__buttonGayka.setFixedSize(200,50)
        self.__buttonShayba.setFixedSize(200,50)
        self.__buttonPruzh.setFixedSize(200, 50)


    def __ui(self):

        self.__mainLayout.addLayout(self.__leftColum)
        self.__mainLayout.addLayout(self.__rightColum)
        self.__leftColum.addWidget(self.__buttonBolt)
        self.__leftColum.addWidget(self.__buttonGayka)
        self.__rightColum.addWidget(self.__buttonShayba)
        self.__mainLayout.addLayout(self.__centerColum)
        self.__centerColum.addWidget(self.__buttonPruzh )
       

    def __event(self):
        self.__buttonBolt.clicked.connect(self.__openBolt)
        self.__buttonGayka.clicked.connect(self.__openGayka)
        self.__buttonPruzh.clicked.connect(self.__openPruzh)
        self.__buttonShayba.clicked.connect(self.__openShayba)

    def __openBolt(self):
        window = WindowBolt()
        window.exec()

    def __openGayka(self):
        window = WindowGayka()
        window.exec()

    def __openPruzh(self):
        window = WindowPruzh()
        window.exec()

    def __openShayba(self):
        window = WindowShayba()
        window.exec()

    def __style(self):

        styleBotton = """
            QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            }
    
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """

        #self.__buttonPruzh.setStyleSheet(styleBotton)