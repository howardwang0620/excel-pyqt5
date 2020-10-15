from sys import platform
from os import path, system
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Widgets.ExcelViewWidgets import *
from Widgets.Widgets import *


class ExcelWindow(QMainWindow):

    returnMenuSignal = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.title = "Excel View"
        self.width = 1400
        self.height = 900
        self.initUI()

    def initUI(self):

        container = QWidget()
        mainLayout = QVBoxLayout()

        sp = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        sp.setHorizontalStretch(2)
        self.state = StateWidget()
        self.state.setSizePolicy(sp)
        self.state.stateBox.currentTextChanged.connect(self.onStateBoxChange)
        sp.setHorizontalStretch(4)
        self.city = CityWidget()
        self.city.setSizePolicy(sp)
        self.city.cityBox.model().itemChanged.connect(self.onCityBoxCheck)

        self.invoice = InvoiceWidget()
        sp.setHorizontalStretch(4)
        self.invoice.setSizePolicy(sp)
        # no timeout, signal emitted whenever input value changes
        self.invoice.input.textChanged.connect(self.onInvoiceTextChange)

        self.address = AddressWidget()
        sp.setHorizontalStretch(6)
        self.address.setSizePolicy(sp)
        # no timeout, signal emitted whenever input value changes
        self.address.input.textChanged.connect(self.onAddressTextChange)

        # below code times out user input so signal emitted x mseconds after typing
        # self.typingTimer = QTimer()
        # self.typingTimer.setSingleShot(True)
        # self.typingTimer.timeout.connect(self.onAddressTextChange)
        # self.address.input.textChanged.connect(self.startTypingTimer)

        inputContainer = QHBoxLayout()
        inputContainer.addWidget(self.state)
        inputContainer.addWidget(self.city)
        inputContainer.addWidget(self.invoice)
        inputContainer.addWidget(self.address)

        # place layout in qframe for borders
        inputFrame = QFrame()
        inputFrame.setFrameStyle(QFrame.Panel)
        inputFrame.setLayout(inputContainer)

        excelContainer = QHBoxLayout()

        inputExcelContainer = QVBoxLayout()
        inputExcelLabel = QLabel("Input Excel Rows")
        inputExcelLabel.setAlignment(Qt.AlignCenter)
        inputExcelLabel.setStyleSheet("font-weight: bold;")

        inputExcelContainerButtons = QHBoxLayout()
        self.selectAllRecordBtn = QPushButton('Select All')
        self.selectAllRecordBtn.setMinimumHeight(40)
        self.addRecordBtn = QPushButton('Add')
        self.addRecordBtn.setMinimumHeight(40)
        self.addRecordBtn.clicked.connect(self.onAddRecordClick)
        self.inputExcelTable = ExcelTableWidget(
            self.addRecordBtn, self.selectAllRecordBtn)

        inputExcelContainerButtons.addWidget(self.selectAllRecordBtn)
        inputExcelContainerButtons.addWidget(self.addRecordBtn)
        inputExcelContainer.addWidget(inputExcelLabel)
        inputExcelContainer.addWidget(self.inputExcelTable)
        inputExcelContainer.addLayout(inputExcelContainerButtons)

        outputExcelContainer = QVBoxLayout()
        outputExcelLabel = QLabel("Output Excel Rows")
        outputExcelLabel.setAlignment(Qt.AlignCenter)
        outputExcelLabel.setStyleSheet("font-weight: bold;")
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
        self.quitBtn.clicked.connect(
            lambda: self.showWarningDialog(self.close))
        self.mainMenuBtn = StyledPushButton('Menu')
        self.mainMenuBtn.clicked.connect(
            lambda: self.showWarningDialog(self.returnMenuSignal.emit))
        self.saveBtn = StyledPushButton('Save')
        self.saveBtn.clicked.connect(self.saveCheck)
        mainActionsContainer.addStretch(1)
        mainActionsContainer.addWidget(self.quitBtn)
        mainActionsContainer.addWidget(self.mainMenuBtn)
        mainActionsContainer.addWidget(self.saveBtn)

        mainActionsFrame = QFrame()
        mainActionsFrame.setLayout(mainActionsContainer)

        mainLayout.addWidget(inputFrame)
        mainLayout.addWidget(excelFrame)
        mainLayout.addWidget(mainActionsFrame)

        container.setLayout(mainLayout)

        self.resize(self.width, self.height)
        self.setCentralWidget(container)
        self.setWindowTitle(self.title)
        self.center()

    def center(self):
        qr = self.frameGeometry()   # geometry of the main window
        cp = QDesktopWidget().availableGeometry().center()      # center point of screen
        qr.moveCenter(cp)   # move rectangle's center to screen's center point
        self.move(qr.topLeft())  # move rect top left to window top left

    ### EVENT ACTIONS ###
    # on state combobox select event
    @pyqtSlot(str)
    def onStateBoxChange(self, state):
        self.model.setState(state)
        cities = self.model.getAllCities()
        self.city.initCityBox(cities)   # initialize city combobox

        self.invoice.disable()  # disable invoice input
        self.address.disable()  # disable address input
        self.inputExcelTable.clear()    # empty table
        self.inputExcelTable.render(self.model.currentFrame())

    # adds city to model filter on combo box check change
    @pyqtSlot('QStandardItem*')
    def onCityBoxCheck(self, item):
        if item.checkState() == Qt.Checked:
            self.model.addCity(item.text())
            self.city.cityBox.setInput(item.text())
        else:
            self.model.removeCity(item.text())
            self.city.cityBox.clearInput()

        # model has cities to filter, render table and enable invoice + address search
        if self.model.selectedCities:
            self.invoice.enable()
            self.address.enable()
            self.inputExcelTable.render(self.model.currentFrame())

        # model has no cities to filter, empty table and disable invoice + address search
        else:
            self.invoice.disable()
            self.address.disable()
            self.inputExcelTable.empty()

    # # helper timer for input text change
    # @pyqtSlot(str)
    # def startTypingTimer(self, text):
    #     self.typingTimer.start(200)
    #
    # # on text change for address
    # # begins when typing timer times out
    # def onAddressTextChange(self):
    #     self.model.setAddress(self.address.getText())
    #     self.inputExcelTable.render(self.model.currentFrame())

    @pyqtSlot(str)
    def onInvoiceTextChange(self, text):
        self.model.setInvoice(text)
        self.inputExcelTable.render(self.model.currentFrame())

    @pyqtSlot(str)
    def onAddressTextChange(self, text):
        self.model.setAddress(text)
        self.inputExcelTable.render(self.model.currentFrame())

    # on add record button click
    @pyqtSlot()
    def onAddRecordClick(self):
        ix = self.inputExcelTable.selectionModel().selectedRows()
        cols = self.inputExcelTable.columnCount()
        ids = []

        for i in ix:
            row = i.row()
            item = self.inputExcelTable.item(row, cols - 1)
            item_data = item.text().split("_")
            ids.append(item.text())

        self.model.addToOutputList(ids)
        self.inputExcelTable.render(self.model.currentFrame())
        if self.inputExcelTable.rowCount() == 0:
            self.selectAllRecordBtn.setEnabled(False)
            self.inputExcelTable.empty()
        else:
            self.selectAllRecordBtn.setEnabled(True)

        self.outputExcelTable.render(self.model.outputFrame())

    @pyqtSlot()
    def onRemoveRecordClick(self):
        ix = self.outputExcelTable.selectionModel().selectedRows()
        cols = self.outputExcelTable.columnCount()
        ids = []
        for i in ix:
            row = i.row()
            item = self.outputExcelTable.item(row, cols - 1)
            item_data = item.text().split("_")
            ids.append(item.text())

        self.model.removeFromOutputList(ids)
        self.outputExcelTable.render(self.model.outputFrame())
        if self.outputExcelTable.rowCount() == 0:
            self.outputExcelTable.empty()
        self.inputExcelTable.render(self.model.currentFrame())

    @pyqtSlot()
    def showWarningDialog(self, callback):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Do you want to continue?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        ret = msg.exec()
        if(ret == QMessageBox.Yes):
            callback()

    def saveCheck(self):
        if self.outputExcelTable.rowCount() == 0:
            CustomQMessageBox('Warning', "No changes detected")
        else:
            self.saveSlot()

    def saveSlot(self):
        timestamp = "{}_output".format(
            datetime.today().strftime("%m-%d-%YT%H.%M.%S%z"))
        fileName = self.promptSaveFileDialog(timestamp)
        if fileName:
            response = self.model.finish(fileName, timestamp)
            if response['status_code']:
                CustomQMessageBox(
                    'Information', "Successfully saved {}!".format(response['output_file']))

                # OPEN OUTPUT FILE HERE
                if platform == 'darwin':
                    system(
                        'open -a "Microsoft Excel.app" "{}"'.format(response['output_file']))
                elif platform == 'win32':
                    system('start "EXCEL.EXE" "{}"'.format(
                        response['output_file']))

                self.returnMenuSignal.emit()
            else:
                CustomQMessageBox('Critical', response['message'])

    def promptSaveFileDialog(self, fileName):
        fileName, selectedFilter = QFileDialog.getSaveFileName(
            self, 'Save File', fileName, "Excel Workbook (*.xlsx);;Excel 5.0/95 Workbook (*.xls)")
        if not fileName:
            return ''

        name = path.basename(fileName)
        if len(name) < 32:
            return fileName

        CustomQMessageBox(
            'Information', "File name too long\n Please set to <=31 characters")
        return self.promptSaveFileDialog(name)
