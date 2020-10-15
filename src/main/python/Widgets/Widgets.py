from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# 100x50 fixed size QPushButton
class StyledPushButton(QPushButton):
    def __init__(self, parent=None):
        super(StyledPushButton, self).__init__(parent)
        self.setMinimumWidth(100)
        self.setMinimumHeight(50)


class CustomQMessageBox(QMessageBox):
    def __init__(self, type, text):
        super().__init__()

        switch = {
            'Information': QMessageBox.Information,
            'Warning': QMessageBox.Warning,
            'Critical': QMessageBox.Critical
        }

        self.setIcon(switch.get(type))
        self.setText(text)
        self.exec()
