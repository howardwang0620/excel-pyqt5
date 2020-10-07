import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class UploadWindow(QMainWindow):

    # signals for button events
    uploadSignal = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.title = "App"
        self.width = 800
        self.height = 400

        self.model = model
        self.initUI()

    def initUI(self):

        window = QWidget()
        container = QHBoxLayout()

        fileContainer = QVBoxLayout()
        # self.fileList = QListWidget()
        self.fileList = DragAndDropListWidget(self.model)
        fileContainer.addWidget(self.fileList)

        self.initFileList()

        btnContainer = QVBoxLayout()
        addBtn = QPushButton('Add File')
        addBtn.clicked.connect(self.fileList.promptFileDialog)

        removeBtn = QPushButton('Remove File')
        removeBtn.clicked.connect(self.fileList.removeWidgetItem)

        self.state = StateWidget()
        self.state.setFixedHeight(75)

        submitBtn = QPushButton('Submit')
        # submitBtn.clicked.connect(self.uploadFiles)
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
        self.show()

    # inits model into itemlistwidget
    def initFileList(self):
        if self.model.getFiles():
            for file in self.model.getFiles():
                self.fileList.addWidgetItem(file)

    def uploadFiles(self):
        if self.fileList.toList():
            self.uploadSignal.emit()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No files selected!")
            msg.setStyleSheet("QLabel{min-width: 150px; min-height: 50px;}");
            msg.exec()

## IMPLEMENT ONLY ALLOW .CSV, .XLS, .XLSX
class DragAndDropListWidget(QListWidget):
    def __init__(self, model, parent=None):
        super(DragAndDropListWidget, self).__init__(parent)

        # set model for update during add/drop event
        self.model = model

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
                # For now, will directly communnicate with model (view->model instead of view->controller->model)
                self.addWidgetItem(filename)
        else:
            event.ignore()

    # file dialog prompt
    def promptFileDialog(self):
        home_dir = str(Path.home())
        filter = "Excel Files|*.xls;*.xlsx"
        fileNames, selectedFilter = QFileDialog.getOpenFileNames(self, 'Open file', home_dir, filter)
        for i in range(len(fileNames)):
            self.addWidgetItem(fileNames[i])

    # Adds file to widgetlist, then to model thru signal
    # (?) Bundle adds into a list for only one signal action?
    def addWidgetItem(self, filename):

        # Checks if file exists in qlistwidget, then sends signal to controller for add to model
        if filename not in self.toList():
            # print("Adding:", filename, "to model then list")

            # add file to model
            self.model.addFile(filename)

            # add file to QListWidget
            item = QListWidgetItem(filename)
            item.setSizeHint(QSize(100, 30))
            self.addItem(item)
        else:
            print(filename, "is already in there")

    # Removes selected files from widgetlist and model
    # (?) Bundle removes into a list for only one signal action?
    def removeWidgetItem(self):

        # For now, will directly communnicate with model (view->model instead of view->controller->model)
        selectedItems = self.selectedItems()
        if not selectedItems: return
        for item in selectedItems:
            if item.text() in self.toList():
                # print(item.text(), "removed!:", self.model.getFiles())

                # emit filename to signal for removal from model
                # self.removeFileSignal.emit(item.text())
                self.model.removeFile(filename)

                # remove file from list
                self.takeItem(self.row(item))
            else:
                print(item.text(), "not in model, cant be removed")

    # returns this listwidget as a list of files
    def toList(self):
        return [self.item(i).text() for i in range(self.count())]

class StateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Select State')
        self.stateBox = QComboBox()
        self.stateBox.addItem("NY")
        self.stateBox.addItem("NJ")
        layout.addWidget(label)
        layout.addWidget(self.stateBox)
        self.setLayout(layout)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=UploadWindow()
    sys.exit(app.exec_())
