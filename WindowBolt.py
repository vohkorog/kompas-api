from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QWidget, QDialog, QLabel, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from Bolt import *

class WindowBolt(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание болта")
        self.setFixedSize(450, 300)
        
        self.__mainLayout = QVBoxLayout()
        self.__layout1 = QHBoxLayout()
        self.__layout2 = QHBoxLayout()
        self.__layout3 = QHBoxLayout()
        self.__layout4 = QHBoxLayout()

        self.__DiametrSterzhnya = QTextEdit()
        self.__DlinnaSterzh = QTextEdit()
        self.__VisotaGolovkiBolta = QTextEdit()
        self.__KlychevoyRazmerGolovkiBolta = QTextEdit()

        self.__createModelBtn = QPushButton("Создать")
        self.__close_btn = QPushButton("Закрыть")
      
        self.setLayout(self.__mainLayout)

        self.__initField()
        self.__ui()
        self.__event()
        self.__style()
    
    def __initField(self):
        self.__DiametrSterzhnya.setFixedSize(200,35)
        self.__DlinnaSterzh.setFixedSize(200,35)
        self.__VisotaGolovkiBolta.setFixedSize(200,35)
        self.__KlychevoyRazmerGolovkiBolta.setFixedSize(200,35)


    def __ui(self):
        self.__mainLayout.addLayout(self.__layout1)
        self.__mainLayout.addLayout(self.__layout2)
        self.__mainLayout.addLayout(self.__layout3)
        self.__mainLayout.addLayout(self.__layout4)


        self.__layout1.addWidget(QLabel("Диаметр стержня (d)"))
        self.__layout1.addWidget(self.__DiametrSterzhnya)
        self.__layout2.addWidget(QLabel("Длинна стержня (l)"))
        self.__layout2.addWidget(self.__DlinnaSterzh)
        self.__layout3.addWidget(QLabel("Высота головки болта (Hб)"))
        self.__layout3.addWidget(self.__VisotaGolovkiBolta)
        self.__layout4.addWidget(QLabel("Ключевой размер головки болта (S)"))
        self.__layout4.addWidget(self.__KlychevoyRazmerGolovkiBolta)


        self.__mainLayout.addWidget(self.__createModelBtn)
        self.__mainLayout.addWidget(self.__close_btn)

    def __event(self):
        self.__close_btn.clicked.connect(self.close)
        
        self.__DiametrSterzhnya.textChanged.connect(lambda: self.__validate_numeric_input(self.__DiametrSterzhnya))
        self.__DlinnaSterzh.textChanged.connect(lambda: self.__validate_numeric_input(self.__DlinnaSterzh))
        self.__VisotaGolovkiBolta.textChanged.connect(lambda: self.__validate_numeric_input(self.__VisotaGolovkiBolta))
        self.__KlychevoyRazmerGolovkiBolta.textChanged.connect(lambda: self.__validate_numeric_input(self.__KlychevoyRazmerGolovkiBolta))
        self.__createModelBtn.clicked.connect(self.__createBolt)


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
        
        self.__DiametrSterzhnya.setStyleSheet(styleTextEdit)
        self.__DlinnaSterzh.setStyleSheet(styleTextEdit)
        self.__VisotaGolovkiBolta.setStyleSheet(styleTextEdit)
        self.__KlychevoyRazmerGolovkiBolta.setStyleSheet(styleTextEdit)


    def __createBolt(self):
        edge_length = float(self.__KlychevoyRazmerGolovkiBolta.toPlainText())
        head_height = float(self.__VisotaGolovkiBolta.toPlainText())
        kernel_dia = float(self.__DiametrSterzhnya.toPlainText())
        kernel_height = float(self.__DlinnaSterzh.toPlainText())
        
        model =  Bolt(edge_length, head_height, kernel_dia, kernel_height)
        model.createBolt()