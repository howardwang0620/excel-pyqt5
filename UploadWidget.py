import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Excel File Upload'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        # self.files = ["File: ASCACDASCADSCASCASDCADCAS","File: ASCACDASCADSCASCASDCADCAS","File: ASCACDASCADSCASCASDCADCAS"]
        self.initUI()

    def initUI(self):

        container = QHBoxLayout()

        fileContainer = QVBoxLayout()
        # self.fileList = QListWidget()
        self.fileList = DragAndDropListWidget(self)
        fileContainer.addWidget(self.fileList)

        self.initFileList()

        btnContainer = QVBoxLayout()
        addBtn = QPushButton('Add File')
        addBtn.clicked.connect(self.promptFileDialog)

        removeBtn = QPushButton('Remove File')
        removeBtn.clicked.connect(self.removeWidgetItem)

        submitBtn = QPushButton('Submit')
        submitBtn.clicked.connect(self.submitAction)

        quitBtn = QPushButton('Quit')
        quitBtn.clicked.connect(self.quitAction)

        btnContainer.addWidget(addBtn)
        btnContainer.addWidget(removeBtn)
        btnContainer.addWidget(submitBtn)
        btnContainer.addWidget(quitBtn)

        fileList = QListWidget()
        container.addLayout(fileContainer)
        container.addLayout(btnContainer)

        self.setLayout(container)
        self.resize(self.width, self.height)

        # center widget to screen
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

        self.setWindowTitle(self.title)
        self.show()

    def initFileList(self):
        print("init function todo for back button")
        # for i, filename in enumerate(self.files):
        #     self.addWidgetItem(filename)

    def promptFileDialog(self):
        home_dir = str(Path.home())
        filter = "CSV files (*.csv)|*.csv|Excel Files|*.xls;*.xlsx"
        filenames = QFileDialog.getOpenFileNames(self, 'Open file', home_dir, filter)[0]
        for i in range(len(filenames)):
            self.addWidgetItem(filenames[i])

    def addWidgetItem(self, filename):
        item = QListWidgetItem(filename)
        item.setSizeHint(QSize(100, 30))
        self.fileList.addItem(item)

    def removeWidgetItem(self):
        selectedItems = self.fileList.selectedItems()
        if not selectedItems: return
        for item in selectedItems:
           self.fileList.takeItem(self.fileList.row(item))

    def submitAction(self):
        print("submit")


    def quitAction(self):
        self.close()

class DragAndDropListWidget(QListWidget):
    def __init__(self, type, parent=None):
        super(DragAndDropListWidget, self).__init__(parent)

        # accept element drops
        self.setAcceptDrops(True)

        # accept multiple selection on elements
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                filename = str(url.toLocalFile())
                item = QListWidgetItem(filename)
                item.setSizeHint(QSize(100, 30))
                self.addItem(item)
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
