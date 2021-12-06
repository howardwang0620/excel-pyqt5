from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StateWidget(QWidget):
    def __init__(self, stateList):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Select State')
        layout.addWidget(label)

        self.stateBox = QComboBox()
        for state in stateList:
            self.stateBox.addItem(state)

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
            self.completer.setCompletionMode(
                QCompleter.UnfilteredPopupCompletion)
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
            item = self.model().item(self.count() - 1, 0)
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


class InvoiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Invoice No.')
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
    def __init__(self, actionButton, selectAllBtn=None):
        super().__init__()
        self.data = None
        self.actionButton = actionButton
        self.actionButton.setEnabled(False)
        self.selectAllBtn = selectAllBtn
        self.mousePressValid = False
        self.lastSelectedRow = None
        self.enterKeyPressed = False
        if self.selectAllBtn is not None:
            self.selectAllBtn.setEnabled(False)
            self.selectAllBtn.clicked.connect(self.toggleSelectAll)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setStyleSheet("QTableView::item{padding: 0 5px 0 5px;}")
        self.itemSelectionChanged.connect(self.toggleButton)

    def mousePressEvent(self, event):
        self.mousePressValid = False
        if not (event.modifiers() & Qt.ShiftModifier):
            self.clearSelection()
        if self.itemAt(event.pos()) is None:
            self.lastSelectedRow = None
        else:
            self.mousePressValid = True
        super(ExcelTableWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        row = self.row(self.itemAt(event.pos()))
        if row == -1 and self.mousePressValid:
            yPos = event.y()
            if(yPos < 0):
                self.lastSelectedRow = 0
            else:
                self.lastSelectedRow = self.rowCount() - 1
        elif row != -1:
            self.lastSelectedRow = row

        super(ExcelTableWidget, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.clearSelection()
            self.handleRowChangedOnKeyUp()

            # don't de-select selected rows
            if not self.isRowSelected(self.lastSelectedRow):
                self.selectRow(self.lastSelectedRow)

        elif event.key() == Qt.Key_Down:
            self.clearSelection()
            self.handleRowChangedOnKeyDown()

            # don't de-select selected rows
            if not self.isRowSelected(self.lastSelectedRow):
                self.selectRow(self.lastSelectedRow)

        elif event.key() == Qt.Key_Return:
            if len(self.selectionModel().selectedRows()) > 0:
                self.enterKeyPressed = True
                self.actionButton.click()

        super(ExcelTableWidget, self).keyPressEvent(event)

    def isRowSelected(self, row):
        return self.lastSelectedRow in map(lambda x: x.row(), self.selectionModel().selectedRows())

    def handleRowChangedOnKeyUp(self):
        # select new row, if enter key was last pressed, maintain lastselectedrow value
        if self.lastSelectedRow is not None:
            if not self.enterKeyPressed:
                self.lastSelectedRow = max(0, self.lastSelectedRow - 1)
            else:
                self.lastSelectedRow = min(
                    self.lastSelectedRow, self.rowCount() - 1)
        else:
            self.lastSelectedRow = 0
        self.enterKeyPressed = False

    def handleRowChangedOnKeyDown(self):
        if self.lastSelectedRow is not None:
            if not self.enterKeyPressed:
                self.lastSelectedRow = min(
                    self.lastSelectedRow + 1, self.rowCount() - 1)
            else:
                self.lastSelectedRow = min(
                    self.lastSelectedRow, self.rowCount() - 1)
        else:
            self.lastSelectedRow = 0
        self.enterKeyPressed = False

    # render table elements
    def render(self, data):
        self.hScrollPos = self.horizontalScrollBar().value()
        self.clear()
        if data is not None:
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
        rows = df.shape[0]
        cols = df.shape[1] + 1
        self.setRowCount(rows)
        self.setColumnCount(cols)
        headers = list(data)
        headers.extend(['id'])
        self.setHorizontalHeaderLabels(headers)

        # getting data from df is computationally costly so convert it to array first
        df_indexes = df.index.values
        df_values = df.values
        self.blockSignals(True)
        for row in range(rows):
            for col in range(cols):
                if col < cols - 1:
                    item = QTableWidgetItem(str(df_values[row, col]))
                else:
                    item = QTableWidgetItem(str(df_indexes[row]))
                self.setItem(row, col, item)
        self.blockSignals(False)
        self.reformatTable()
        if self.selectAllBtn is not None:
            self.selectAllBtn.setEnabled(self.rowCount() > 0)

    def reformatTable(self):
        self.hideColumn(6)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.horizontalScrollBar().setValue(self.hScrollPos)

    # toggle connected action button on/off depending if items are selected

    @ pyqtSlot()
    def toggleButton(self):
        self.actionButton.setEnabled(len(self.selectedItems()) > 0)

    @ pyqtSlot()
    def toggleSelectAll(self):
        if len(self.selectionModel().selectedRows()) < self.rowCount():
            self.lastSelectedRow = self.rowCount()
            self.selectAll()
        else:
            self.lastSelectedRow = 0
            self.clearSelection()

class DateFormatDropdownWidget(QWidget):
    def __init__(self, dateFormats):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Output Date Format')
        layout.addWidget(label)

        self.formatBox = QComboBox()
        for format in dateFormats:
            self.formatBox.addItem(format)

        self.formatBox.setCurrentIndex(0)
        layout.addWidget(self.formatBox)

        self.setLayout(layout)
