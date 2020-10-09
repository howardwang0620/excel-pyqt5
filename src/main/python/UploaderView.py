import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Widgets.UploaderViewWidgets import *


class UploadWindow(QMainWindow):
    # signal for upload events
    uploadSignal = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.title = "Upload Window"
        self.width = 800
        self.height = 400

        self.model = model
        self.initUI()

    def initUI(self):
        window = QWidget()
        container = QHBoxLayout()

        fileContainer = QVBoxLayout()
        self.fileList = DragAndDropListWidget(self.model)
        self.fileList.addFileSignal.connect(self.addFile)
        self.fileList.removeFileSignal.connect(self.removeFile)
        fileContainer.addWidget(self.fileList)

        self.initFileList()

        btnContainer = QVBoxLayout()
        addBtn = QPushButton('Add File')
        addBtn.clicked.connect(self.fileList.promptFileDialog)

        removeBtn = QPushButton('Remove File')
        removeBtn.clicked.connect(self.fileList.removeWidgetItem)

        submitBtn = QPushButton('Submit')
        submitBtn.clicked.connect(self.uploadFiles)

        quitBtn = QPushButton('Quit')
        quitBtn.clicked.connect(self.close)

        # btnContainer.addWidget(self.state)
        btnContainer.addWidget(addBtn)
        btnContainer.addWidget(removeBtn)
        btnContainer.addWidget(submitBtn)
        btnContainer.addWidget(quitBtn)

        container.addLayout(fileContainer)
        container.addLayout(btnContainer)

        window.setLayout(container)

        self.resize(self.width, self.height)
        self.setCentralWidget(window)
        self.setWindowTitle(self.title)

    # inits model into itemlistwidget
    def initFileList(self):
        if self.model.getFiles():
            for file in self.model.getFiles():
                self.fileList.addWidgetItem(file)

    def addFile(self, filename):
        self.model.addFile(filename)

    def removeFile(self, filename):
        self.model.removeFile(filename)

    def uploadFiles(self):
        if self.fileList.toList():
            self.uploadSignal.emit()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No files selected!")
            msg.setStyleSheet("QLabel{min-width: 150px; min-height: 50px;}")
            msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UploadWindow()
    sys.exit(app.exec_())
