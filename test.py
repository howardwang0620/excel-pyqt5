from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import sys

class Main(QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        self.kod = []
        # main button
        self.addButton = QPushButton('button to add other widgets')
        self.addButton.clicked.connect(self.addWidget)

        self.removeButton=QPushButton("remove widget")
        self.removeButton.clicked.connect(self.remove_widget)

        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.removeButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def addWidget(self):
        temp = Test()
        self.kod.append(temp)
        self.scrollLayout.addRow(temp)

    def remove_widget(self):
        self.kod.pop().deleteLater()


class Test(QWidget):
  def __init__( self, parent=None):
      super(Test, self).__init__(parent)

      self.lineEdit = QLineEdit('I am in Test widget')

      layout = QHBoxLayout()
      layout.addWidget(self.lineEdit)
      self.setLayout(layout)

  def remove_widget(self):
      self.lineEdit.deleteLater()




app = QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()
