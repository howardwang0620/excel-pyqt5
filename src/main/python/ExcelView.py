import sys
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Widgets.ExcelViewWidgets import *
from Model import ExcelModel


class ExcelWindow(QMainWindow):

    returnMenuSignal = pyqtSignal()
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.model.buildDF()
        self.title = "Excel Stuff Here BABY"
        self.width = 1400
        self.height = 900
        self.typingTimer = QTimer()
        self.typingTimer.setSingleShot(True)
        self.typingTimer.timeout.connect(self.onAddressTextChange)
        self.initUI()

    def initUI(self):
        container = QWidget()
        mainLayout = QVBoxLayout()

        sp = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        sp.setHorizontalStretch(3);
        self.state = StateWidget()
        self.state.setSizePolicy(sp)
        self.state.stateBox.currentTextChanged.connect(self.onStateBoxChange)

        sp.setHorizontalStretch(5);
        self.city = CityWidget()
        self.city.setSizePolicy(sp)
        self.city.cityBox.model().itemChanged.connect(self.onCityBoxCheck)
        self.city.cityBox.view().pressed.connect(self.onCityBoxSelect)
        self.city.cityBox.completer.activated.connect(self.onCompleterActivated)

        self.address = AddressWidget()
        sp.setHorizontalStretch(6);
        self.address.setSizePolicy(sp)
        self.address.input.textChanged.connect(self.startTypingTimer)

        inputContainer = QHBoxLayout()
        inputContainer.addWidget(self.state)
        inputContainer.addWidget(self.city)
        inputContainer.addWidget(self.address)

        # place layout in qframe for borders
        inputFrame = QFrame()
        inputFrame.setFrameStyle(QFrame.Panel)
        inputFrame.setLayout(inputContainer)


        excelContainer = QHBoxLayout()

        inputExcelContainer = QVBoxLayout()
        inputExcelLabel = QLabel("Input Excel Rows")
        inputExcelLabel.setAlignment(Qt.AlignCenter)
        inputExcelLabel.setStyleSheet("font-weight: bold;");
        self.addRecordBtn = QPushButton('Add')
        self.inputExcelTable = ExcelTableWidget(self.addRecordBtn)
        self.addRecordBtn.setMinimumHeight(40)
        self.addRecordBtn.clicked.connect(self.onAddRecordClick)
        inputExcelContainer.addWidget(inputExcelLabel)
        inputExcelContainer.addWidget(self.inputExcelTable)
        inputExcelContainer.addWidget(self.addRecordBtn)

        outputExcelContainer = QVBoxLayout()
        outputExcelLabel = QLabel("Output Excel Rows")
        outputExcelLabel.setAlignment(Qt.AlignCenter)
        outputExcelLabel.setStyleSheet("font-weight: bold;");
        self.removeRecordBtn = QPushButton('Remove')
        self.outputExcelTable = ExcelTableWidget(self.removeRecordBtn)
        self.removeRecordBtn.setMinimumHeight(40)
        self.removeRecordBtn.clicked.connect(self.onRemoveRecordClick)
        outputExcelContainer.addWidget(outputExcelLabel)
        outputExcelContainer.addWidget(self.outputExcelTable)
        outputExcelContainer.addWidget(self.removeRecordBtn)

        excelContainer.addLayout(inputExcelContainer)
        excelContainer.addLayout(outputExcelContainer)

        excelFrame = QFrame()
        excelFrame.setLayout(excelContainer)
        excelFrame.setFrameStyle(QFrame.Panel)


        mainActionsContainer = QHBoxLayout()
        self.quitBtn = StyledPushButton('Quit')
        # self.quitBtn.clicked.connect(self.close)
        self.quitBtn.clicked.connect(lambda: self.showWarningDialog(self.close))
        self.mainMenuBtn = StyledPushButton('Menu')
        self.mainMenuBtn.clicked.connect(lambda: self.showWarningDialog(self.returnMenuSignal.emit))
        self.saveBtn = StyledPushButton('Save')
        self.saveBtn.clicked.connect(self.saveSlot)
        mainActionsContainer.addStretch(1)
        mainActionsContainer.addWidget(self.quitBtn)
        mainActionsContainer.addWidget(self.mainMenuBtn)
        mainActionsContainer.addWidget(self.saveBtn)

        mainActionsFrame = QFrame()
        mainActionsFrame.setLayout(mainActionsContainer)
        # mainActionsFrame.setFrameStyle(QFrame.Panel)

        mainLayout.addWidget(inputFrame)
        mainLayout.addWidget(excelFrame)
        mainLayout.addWidget(mainActionsFrame)

        container.setLayout(mainLayout)

        self.resize(self.width, self.height)
        self.setCentralWidget(container)
        self.setWindowTitle(self.title)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()   # geometry of the main window
        cp = QDesktopWidget().availableGeometry().center()      # center point of screen
        qr.moveCenter(cp)           # move rectangle's center point to screen's center point
        self.move(qr.topLeft())     # top left of rectangle becomes top left of window centering it


    ### EVENT ACTIONS ###

    # on state combobox select event
    def onStateBoxChange(self, state):
        self.model.setState(state)
        cities = self.model.getAllCities()

        # reset and update cities
        self.city.fillCityBox(cities)

        # disable address input
        self.address.disable()

        # empty table
        self.inputExcelTable.empty()

    # on selection of an item from the completer, select the corresponding item from combobox
    def onCompleterActivated(self, text):
        if text:
            index = self.city.cityBox.findText(str(text))
            self.onCityBoxSelect(self.city.cityBox.model().index(index, 0))

    # checks city combo box on mouse click
    def onCityBoxSelect(self, index):
        item = self.city.cityBox.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    # adds city to model filter on combo box check change
    def onCityBoxCheck(self, item):
        if item.checkState() == Qt.Checked:
            self.model.addCityToFilter(item.text())
            self.city.cityBox.setInput(item.text())
        else:
            self.model.removeCityFromFilter(item.text())
            self.city.cityBox.clearInput()

        if self.model.selectedCities:
            self.address.enable()
        else:
            self.address.disable()

        self.inputExcelTable.updateData(self.model.currentFrame())

    def onCityBoxSelectAll(self, item):
        print("select all")

    # helper timer for address input text change
    def startTypingTimer(self):
        self.typingTimer.start(250)

    # on text change for address
    def onAddressTextChange(self):
        self.model.setAddress(self.address.getText())
        self.inputExcelTable.updateData(self.model.currentFrame())

    # on add record button click
    def onAddRecordClick(self):
        ix = self.inputExcelTable.selectionModel().selectedRows()
        cols = self.inputExcelTable.columnCount()
        ids = []
        for i in ix:
            row = i.row()
            item = self.inputExcelTable.item(row, cols - 1)
            ids.append(item.text())
        self.model.addToOutputList(ids)
        self.inputExcelTable.updateData(self.model.currentFrame())
        self.outputExcelTable.updateData(self.model.outputFrame())

    # on remove record button click
    def onRemoveRecordClick(self):
        ix = self.outputExcelTable.selectionModel().selectedRows()
        cols = self.outputExcelTable.columnCount()
        ids = []
        for i in ix:
            row = i.row()
            item = self.outputExcelTable.item(row, cols - 1)
            ids.append(item.text())
        self.model.removeFromOutputList(ids)
        self.outputExcelTable.updateData(self.model.outputFrame())
        self.inputExcelTable.updateData(self.model.currentFrame())


    def showWarningDialog(self, callback):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Do you want to continue?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        ret = msg.exec()
        if(ret == QMessageBox.Yes):
            callback()

    def saveSlot(self):
        timestamp = "output_" + datetime.today().strftime("%m-%d-%YT%H.%M.%S%z")
        fileName, selectedFilter = QFileDialog.getSaveFileName(self, 'Save File', timestamp, "Excel Workbook (*.xlsx);;Excel 5.0/95 Workbook (*.xls)")
        self.model.finish(fileName)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Successfully saved {}!".format(fileName))
        msg.setStyleSheet("QLabel{min-width: 250px; min-height: 150px;}");
        msg.exec()
        self.returnMenuSignal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    files = ['/Users/howardwang/Desktop/excel-application/excel-files/8.7.2020 nj pm.xls.xlsx', \
             '/Users/howardwang/Desktop/excel-application/excel-files/8.10.2020 nj am.xls.xlsx']
    # files = ['/Users/howardwang/Desktop/excel-application/test-files/append-test1.xlsx', \
    #          '/Users/howardwang/Desktop/excel-application/test-files/append-test2.xlsx']
    model = ExcelModel(files)
    ex = ExcelWindow(model)
    sys.exit(app.exec_())
