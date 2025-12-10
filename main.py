from MainWindow import *
from PyQt6.QtWidgets import QApplication
import sys


## делаем: болт, гайку, шайбу, подшибник, пружину


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()