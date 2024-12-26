from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Slot
import random

class MainSanctumWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
    
        self.hello = ['Hello', 'KraNf']

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel('Hello world!', alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.say_hello)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    @Slot()
    def say_hello(self):
        self.text.setText('Hello Nigger')
