from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class StateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Select State')
        layout.addWidget(label)

        # subLayout = QHBoxLayout()
        self.stateBox = QComboBox()
        self.stateBox.addItem("NY")
        self.stateBox.addItem("NJ")
        self.stateBox.setCurrentIndex(-1)
        # subLayout.addWidget(self.stateBox)
        layout.addWidget(self.stateBox)
        # layout.addLayout(subLayout)

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
        # completer = QCompleter(self.cityBox.model())
        # self.cityBox.setCompleter(completer)
        # self.cityBox.completer().setCompletionMode(QCompleter.PopupCompletion)
        # self.cityBox.completer().setCaseSensitivity(Qt.CaseInsensitive)

    def fillCityBox(self, data):
        self.cityBox.clear()
        self.cityBox.addItems(data)
        # self.cityBox.setEditable(True)
        self.cityBox.setEditable(False)
        self.cityBox.clearInput()

    class CheckedComboBox(QComboBox):
        def __init__(self):
            super().__init__()
            self.setEditable(False)
            # self.completer().setCompletionMode(QCompleter.PopupCompletion)

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
            self.setEditable(True)
            self.setCurrentText(text)
            self.setEditable(False)

        def clearInput(self):
            self.setEditable(True)
            self.clearEditText()
            self.setEditable(False)



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
    def __init__(self):
        super().__init__()
        self.data = None
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.cellChanged.connect(self.onCellCheck)
        # self.itemSelectionChanged.connect(self.onRowSelect)

    def updateData(self, df):
        self.resetData()
        self.data = df
        if self.data is not None:
            self.renderData()

    def resetData(self):
        self.clearSelection()
        # self.disconnect()
        self.clearContents()
        self.setRowCount(0)
        self.setColumnCount(0)

    def renderData(self):
        df = self.data
        # headers = ['Select']
        # headers.extend(list(df))
        headers = list(df)
        # print(headers)
        # print(len(headers))
        # print(df.shape[1])
        self.setRowCount(df.shape[0])
        # self.setColumnCount(df.shape[1] + 1)
        self.setColumnCount(df.shape[1])
        self.setHorizontalHeaderLabels(headers)

        self.blockSignals(True)
        # getting data from df is computationally costly so convert it to array first
        df_array = df.values
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                # if col == 0:
                #     item = QTableWidgetItem()
                #     item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                #     item.setCheckState(Qt.Unchecked)
                # else:
                #     item = QTableWidgetItem(str(df_array[row,col-1]))

                item = QTableWidgetItem(str(df_array[row,col]))
                self.setItem(row, col, item)
        self.blockSignals(False)
        self.resizeColumnsToContents()

    # def onCellCheck(self, row):
    #     if self.item(row, 0).checkState() == Qt.Checked:
    #         self.selectRow(row)
    #         print("cell is checked")
    #     else:
    #         print(row)
    #         # self.selectionModel().select(row, QItemSelectionModel.Deselect)
    #         print("cell is not checked")
    #
    # def onRowSelect(self):
    #     print("selected row")

class MainActionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.mainMenuBtn = QPushButton('Menu')
        # self.mainMenuBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.saveBtn = QPushButton('Save')
        layout.addWidget(self.mainMenuBtn)
        layout.addWidget(self.saveBtn)
        self.setLayout(layout)


# class ExcelTableView(QTableView):
#     def __init__(self, data=None):
#         super().__init__()
#
#     def updateData(self, data):
#         self.tableModel = PandasModel(data)
#         self.setModel(self.tableModel)
#
# class PandasModel(QAbstractTableModel):
#     def __init__(self, data, parent=None):
#         QAbstractTableModel.__init__(self, parent)
#         self._data = data
#
#     def rowCount(self, parent=None):
#         return self._data.shape[0]
#
#     def columnCount(self, parent=None):
#         return self._data.shape[1]
#
#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 return str(self._data.iloc[index.row(), index.column()])
#         return None
#
#     def headerData(self, col, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return self._data.columns[col]
#         if orientation == Qt.Vertical and role == Qt.DisplayRole:
#             return self._data.index[col]
#         return None
