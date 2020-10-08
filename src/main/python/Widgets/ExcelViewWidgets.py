from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class StateWidget(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Select State')
        layout.addWidget(label)

        self.stateBox = QComboBox()
        self.stateBox.addItem("NY")
        self.stateBox.addItem("NJ")
        self.stateBox.setCurrentIndex(-1)
        layout.addWidget(self.stateBox)

        self.setLayout(layout)


class CityWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Select City')
        layout.addWidget(label)

        self.cityBox = self.CheckedComboBox()
        layout.addWidget(self.cityBox)

        self.setLayout(layout)
        self.disable()

    def initCityBox(self, data):
        self.enable()
        # data = ['SELECT ALL'] + data
        self.cityBox.addItems(data)
        self.cityBox.clearInput()

    def disable(self):
        self.cityBox.clear()
        self.cityBox.clearInput()
        self.setEnabled(False)

    def enable(self):
        self.setEnabled(True)
        self.cityBox.clear()


    class CheckedComboBox(QComboBox):
        def __init__(self, parent=None):
            super(CityWidget.CheckedComboBox, self).__init__(parent)
            self.setEditable(True)
            self.setMaxVisibleItems(15)
            self.setInsertPolicy(QComboBox.NoInsert)


            # add a filter model to filter matching items
            self.pFilterModel = QSortFilterProxyModel(self)
            self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
            self.pFilterModel.setSourceModel(self.model())

            # add a completer, which uses the filter model
            self.completer = QCompleter(self.pFilterModel, self)
            # always show all (filtered) completions
            self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            self.setCompleter(self.completer)

            # connect signals
            self.lineEdit().textEdited.connect(self.filter)
            self.completer.activated.connect(self.onCompleterActivated)
            self.view().pressed.connect(self.onCityBoxSelect)

        # on selection of an item from the completer, select the corresponding item from combobox
        @pyqtSlot('QString')
        def onCompleterActivated(self, text):
            if text:
                index = self.findText(str(text))
                self.onCityBoxSelect(self.model().index(index, 0))
                # super(CityWidget.CheckedComboBox, self).showPopup()

        # connect signal to text edited
        @pyqtSlot('QString')
        def filter(self, text):
            self.pFilterModel.setFilterFixedString(str(text))

        # checks city combo box on mouse click
        @pyqtSlot('QModelIndex')
        def onCityBoxSelect(self, index):
            item = self.model().itemFromIndex(index)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)

        def addItem(self, item):
            super().addItem(item)
            item = self.model().item(self.count()-1,0)
            item.model().blockSignals(True)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            item.model().blockSignals(False)

        def addItems(self, items):
            for item in items:
                self.addItem(item)

        def setInput(self, text):
            self.setCurrentText(text)

        def clearInput(self):
            self.clearEditText()


class AddressWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Input Address')
        layout.addWidget(label)

        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.setLayout(layout)
        self.disable()


    def getText(self):
        return self.input.text()

    def disable(self):
        self.input.clear()
        self.input.setEnabled(False)

    def enable(self):
        self.input.clear()
        self.input.setEnabled(True)


class ExcelTableWidget(QTableWidget):
    def __init__(self, button):
        super().__init__()
        self.data = None
        self.actionButton = button
        self.actionButton.setEnabled(False)

        # self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.itemSelectionChanged.connect(self.toggleButton)

    # toggle connected action button on/off depending if items are selected
    @pyqtSlot()
    def toggleButton(self):
        if(len(self.selectedItems()) > 0):
            self.actionButton.setEnabled(True)
        else:
            self.actionButton.setEnabled(False)

    # render table elements
    def render(self, data):
        self.hScrollPos = self.horizontalScrollBar().value()
        self.clear()
        if data is not None :
            self.buildTable(data)

    # empty only values from table
    def clear(self):
        self.clearSelection()
        self.clearContents()
        self.setRowCount(0)

    # empty header and values from table
    def empty(self):
        self.clear()
        self.setColumnCount(0)

    # add dataframe elements into table
    def buildTable(self, data):
        df = data
        self.setRowCount(df.shape[0])
        self.setColumnCount(df.shape[1] + 1)
        headers = list(data)
        headers.extend(['id'])
        self.setHorizontalHeaderLabels(headers)

        # getting data from df is computationally costly so convert it to array first
        df_indexes = df.index.values
        df_values = df.values
        rows = df.shape[0]
        cols = df.shape[1] + 1
        self.blockSignals(True)
        for row in range(rows):
            for col in range(cols):
                if col < cols - 1:
                    item = QTableWidgetItem(str(df_values[row, col]))
                else:
                    item = QTableWidgetItem(str(df_indexes[row]))
                self.setItem(row, col, item)
        self.blockSignals(False)
        self.resizeColumnsToContents()
        self.horizontalScrollBar().setValue(self.hScrollPos)

# 100x50 fixed size QPushButton
class StyledPushButton(QPushButton):
    def __init__(self, parent=None):
        super(StyledPushButton, self).__init__(parent)
        self.setMinimumWidth(100)
        self.setMinimumHeight(50)
