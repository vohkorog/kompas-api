from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QWidget, QDialog, QLabel, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from Pruzh import *

class WindowPruzh(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание гайки")
        self.setFixedSize(450, 300)
        
        self.__mainLayout = QVBoxLayout()
        self.__layout1 = QHBoxLayout()
        self.__layout2 = QHBoxLayout()
        self.__layout3 = QHBoxLayout()
        self.__layout4 = QHBoxLayout()

        self.__DiametrPrutka = QTextEdit()
        self.__VnutrenyDiametrPruzh = QTextEdit()
        self.__ShagNavivki = QTextEdit()
        self.__ChisloVitkov = QTextEdit()

        self.__createModelBtn = QPushButton("Создать")
        self.__close_btn = QPushButton("Закрыть")
      
        self.setLayout(self.__mainLayout)

        self.__initField()
        self.__ui()
        self.__event()
        self.__style()
    
    def __initField(self):
        self.__DiametrPrutka.setFixedSize(200,35)
        self.__VnutrenyDiametrPruzh.setFixedSize(200,35)
        self.__ShagNavivki.setFixedSize(200,35)
        self.__ChisloVitkov.setFixedSize(200,35)

    def __ui(self):
        self.__mainLayout.addLayout(self.__layout1)
        self.__mainLayout.addLayout(self.__layout2)
        self.__mainLayout.addLayout(self.__layout3)
        self.__mainLayout.addLayout(self.__layout4)

        self.__layout1.addWidget(QLabel("Диаметр прутка (d)"))
        self.__layout1.addWidget(self.__DiametrPrutka)
        self.__layout2.addWidget(QLabel("Внутренний диаметр пружины (D1)"))
        self.__layout2.addWidget(self.__VnutrenyDiametrPruzh)
        self.__layout3.addWidget(QLabel("Шаг навивки (t)"))
        self.__layout3.addWidget(self.__ShagNavivki)
        self.__layout4.addWidget(QLabel("Число витков (n)"))
        self.__layout4.addWidget(self.__ChisloVitkov)


        self.__mainLayout.addWidget(self.__createModelBtn)
        self.__mainLayout.addWidget(self.__close_btn)

    def __event(self):
        self.__close_btn.clicked.connect(self.close)
        self.__DiametrPrutka.textChanged.connect(lambda: self.__validate_numeric_input(self.__DiametrPrutka))
        self.__VnutrenyDiametrPruzh.textChanged.connect(lambda: self.__validate_numeric_input(self.__VnutrenyDiametrPruzh))
        self.__ShagNavivki.textChanged.connect(lambda: self.__validate_numeric_input(self.__ShagNavivki))
        self.__ChisloVitkov.textChanged.connect(lambda: self.__validate_numeric_input(self.__ChisloVitkov))
        self.__createModelBtn.clicked.connect(self.__createPruzh)


    def __validate_numeric_input(self, text_edit):
        """Универсальная функция валидации для числового ввода"""
        text = text_edit.toPlainText()
        
        cleaned = ''
        has_dot = False
        for char in text:
            if char.isdigit():
                cleaned += char
            elif char == '.' and not has_dot:
                cleaned += char
                has_dot = True
        
        if text != cleaned:
            cursor = text_edit.textCursor()
            position = cursor.position()
            
            text_edit.blockSignals(True)
            text_edit.setPlainText(cleaned)
            text_edit.blockSignals(False)
            
            cursor.setPosition(min(position, len(cleaned)))
            text_edit.setTextCursor(cursor)

    def __style(self):
        styleTextEdit = """
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #000;
                border-radius: 4px;
                color: #212529;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 14px;
                line-height: 1.5;
                selection-background-color: #007bff;
                selection-color: white;
            }

            QTextEdit:focus {
                border: 2px solid #007bff;
                background-color: #ffffff;
            }

            QScrollBar:vertical {
                background: #f1f3f4;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e0;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: #a0aec0;
            }
        """
        
        self.__DiametrPrutka.setStyleSheet(styleTextEdit)
        self.__VnutrenyDiametrPruzh.setStyleSheet(styleTextEdit)
        self.__ShagNavivki.setStyleSheet(styleTextEdit)
        self.__ChisloVitkov.setStyleSheet(styleTextEdit)

    def __createPruzh(self):
       
        dia_prut = float(self.__DiametrPrutka.toPlainText())
        diam = float(self.__VnutrenyDiametrPruzh.toPlainText())
        step = float(self.__ShagNavivki.toPlainText())
        turn = float(self.__ChisloVitkov.toPlainText())
        
        model = Pruzh(diam, step, turn, dia_prut)
        model.createPruzh()