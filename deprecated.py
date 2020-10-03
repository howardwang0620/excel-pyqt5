import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Excel File Merging BOI'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        # tmp = "File: ASCACDASCADSCASCASDCADCAS"
        # self.files = [(tmp, id(tmp))]
        self.files = []
        self.initUI()

    def initUI(self):

        fileContainer = QVBoxLayout()

        #File box containing all the file names added
        # self.fileBox = QGridLayout()
        fileList = QListView()
        self.fileBox = QVBoxLayout()
        # self.fileList = QListWidget()
        # self.fileList.setMinimumWidth(self.fileList.sizeHintForColumn(0))
        # self.fileBox.addWidget(self.fileList)
        # self.fileBox.setVerticalSpacing(0)
        self.initFileBox()

        #Select file box containing select file button
        fileBtnBox = QVBoxLayout()
        fileBtn = QPushButton("Upload a File")
        fileBtn.clicked.connect(self.promptFileDialog)
        fileBtn.setFixedSize(300, 25)
        fileBtnBox.addWidget(fileBtn)
        fileBtnBox.setAlignment(Qt.AlignCenter)

        #Add filebox and filebtnbox to fileContainer
        fileContainer.addLayout(self.fileBox)
        fileContainer.addLayout(fileBtnBox)

        actionBox = QHBoxLayout()
        quitBtn = QPushButton("Quit")
        actionBox.addWidget(quitBtn)
        actionBox.addStretch(1)
        submitBtn = QPushButton("Submit")
        actionBox.addWidget(submitBtn)

        container = QVBoxLayout()
        container.addLayout(fileContainer)
        container.addLayout(actionBox)

        self.setLayout(container)

        self.setGeometry(self.left, self.top, self.width, self.height);
        self.setWindowTitle(self.title)
        self.show()

    def initFileBox(self):
        print(self)
        for tuple in self.files:
            self.fileBox.addWidget(FileRecordWidget(self, tuple))

    def promptFileDialog(self):
        home_dir = str(Path.home())
        filename = QFileDialog.getOpenFileName(self, 'Open file', home_dir)[0]
        tuple = (filename, id(filename))
        self.files.append(tuple)
        self.fileBox.addWidget(FileRecordWidget(self, tuple))

class FileRecordWidget(QWidget):
    def __init__(self, parent, tuple):
        super(FileRecordWidget, self).__init__(parent)
        self.files = parent.files
        self.filename = tuple[0]
        self.id = tuple[1]

        layout = QHBoxLayout()
        fileLabel = QLabel('File: ' + self.filename)
        removeBtn = QPushButton('-')
        removeBtn.clicked.connect(self.destroy)
        # button.setStyleSheet("background-color: grey")
        fileLabel.setFixedWidth(500)
        layout.addWidget(fileLabel)
        layout.addWidget(removeBtn)
        self.setLayout(layout)
        self.show()

    def destroy(self):
        delPos = [t[1] for t in self.files].index(self.id)
        print(self.files.pop(delPos))
        self.deleteLater()
        print("AFTER POP:", self.files)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
