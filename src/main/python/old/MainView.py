import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from UploaderView import UploadWidget

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.width = 800
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setCentralWidget(UploadWidget(self))
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.show()

    def uploaderFilesSubmitted(self):
        print(self.files)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
