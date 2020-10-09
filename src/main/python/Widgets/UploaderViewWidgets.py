from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# IMPLEMENT ONLY ALLOW .CSV, .XLS, .XLSX


class DragAndDropListWidget(QListWidget):

    addFileSignal = pyqtSignal(str)
    removeFileSignal = pyqtSignal(str)

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
                if filename.endswith(('.xls', '.xlsx')):
                    self.addWidgetItem(filename)
                else:
                    event.ignore()
        else:
            event.ignore()

    # file dialog prompt
    def promptFileDialog(self):
        home_dir = str(Path.home())
        filter = "Excel Files|*.xls;*.xlsx"
        fileNames, selectedFilter = QFileDialog.getOpenFileNames(
            self, 'Open file', home_dir, filter)
        for i in range(len(fileNames)):
            self.addWidgetItem(fileNames[i])

    # Adds file to widgetlist, then to model thru signal
    def addWidgetItem(self, filename):

        # Checks if file exists in qlistwidget, then sends signal to controller for add to model
        if filename not in self.toList():
            # print("Adding:", filename, "to model then list")

            # add file to model
            # self.model.addFile(filename)
            self.addFileSignal.emit(filename)

            # add file to QListWidget
            item = QListWidgetItem(filename)
            item.setSizeHint(QSize(100, 30))
            self.addItem(item)
        else:
            print(filename, "is already in there")

    # Removes selected files from widgetlist and model
    def removeWidgetItem(self):

        # For now, will directly communnicate with model (view->model instead of view->controller->model)
        selectedItems = self.selectedItems()
        if not selectedItems:
            return
        for item in selectedItems:
            if item.text() in self.toList():
                # print(item.text(), "removed!:", self.model.getFiles())

                # emit filename to signal for removal from model
                # self.removeFileSignal.emit(item.text())
                # self.model.removeFile(filename)
                self.removeFileSignal.emit(item.text())

                # remove file from list
                self.takeItem(self.row(item))
            else:
                print(item.text(), "not in model, cant be removed")

    # returns this listwidget as a list of files
    def toList(self):
        return [self.item(i).text() for i in range(self.count())]
