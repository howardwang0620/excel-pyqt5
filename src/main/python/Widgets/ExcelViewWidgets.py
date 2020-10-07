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

    def fillCityBox(self, data):
        self.enable()
        # data = ['SELECT ALL'] + data
        self.cityBox.addItems(data)

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
            self.completer = QCompleter( self )

            # add a filter model to filter matching items
            self.pFilterModel = QSortFilterProxyModel(self)
            self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
            self.pFilterModel.setSourceModel(self.model())

            # add a completer, which uses the filter model
            self.completer = QCompleter(self.pFilterModel, self)
            # always show all (filtered) completions
            self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            # self.completer.setCompletionMode(QCompleter.PopupCompletion)

            self.setCompleter(self.completer)
            self.lineEdit().textEdited.connect(self.filter)

        # connect signal to text edited
        def filter(self, text):
            self.pFilterModel.setFilterFixedString(str(text))


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
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.actionButton = button
        self.actionButton.setEnabled(False)

    def updateData(self, df):
        self.hScrollPos = self.horizontalScrollBar().value()
        self.clear()
        self.data = df
        # if self.data is not None:
            # print("DF:", self.data)
        if self.data is not None and not self.data.empty:
            self.actionButton.setEnabled(True)
            self.renderData()
        else:
            self.actionButton.setEnabled(False)

    # clear values from table
    def clear(self):
        self.clearSelection()
        self.clearContents()
        self.setRowCount(0)

    # really clears tables
    def empty(self):
        self.clear()
        self.setColumnCount(0)

    def renderData(self):
        df = self.data
        headers = list(df)
        headers.extend(['id'])
        self.setRowCount(df.shape[0])
        self.setColumnCount(df.shape[1] + 1)
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


class StyledPushButton(QPushButton):
    def __init__(self, parent=None):
        super(StyledPushButton, self).__init__(parent)
        self.setMinimumWidth(100)
        self.setMinimumHeight(50)
