import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ExcelWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        print("INIT:", self.model.getFiles())
        self.title = "Excel Stuff Here BABY"
        self.width = 800
        self.height = 800
        self.initUI()

    def initUI(self):
        window = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QPushButton("PUSH ME"))
        window.setLayout(layout)

        fg = window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        window.move(fg.topLeft())

        self.resize(self.width, self.height)
        self.setCentralWidget(window)
        self.setWindowTitle(self.title)
        self.show()

# 
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     files = ['/Users/howardwang/Desktop/excel-application/excel-files/8.7.2020 nj pm.xls.xlsx', '/Users/howardwang/Desktop/excel-application/excel-files/8.10.2020 nj am.xls.xlsx']
#     ex=ExcelWindow(files)
#     sys.exit(app.exec_())
