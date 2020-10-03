import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ExcelWidget(QWidget):
    def __init__(self, parent):
        super(ExcelWidget, self).__init__(parent)
        self.parent = parent
        self.title = "Excel Stuff Here BABY"
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        container.addWidget(QPushButton("PUSH ME"))
        self.setLayout(layout)
