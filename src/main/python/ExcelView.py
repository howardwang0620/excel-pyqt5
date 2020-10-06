import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Widgets.ExcelViewWidgets import *
from Model import ExcelModel

class ExcelWindow(QMainWindow):


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
        self.inputExcelTable = ExcelTableWidget()
        self.addRecordBtn = QPushButton('Add')
        self.addRecordBtn.clicked.connect(self.onAddRecordClick)
        inputExcelContainer.addWidget(self.inputExcelTable)
        inputExcelContainer.addWidget(self.addRecordBtn)

        outputExcelContainer = QVBoxLayout()
        self.outputExcelTable = ExcelTableWidget()
        self.removeRecordBtn = QPushButton('Remove')
        outputExcelContainer.addWidget(self.outputExcelTable)
        outputExcelContainer.addWidget(self.removeRecordBtn)

        excelContainer.addLayout(inputExcelContainer)
        excelContainer.addLayout(outputExcelContainer)

        excelFrame = QFrame()
        excelFrame.setLayout(excelContainer)
        excelFrame.setFrameStyle(QFrame.Panel)


        mainActionsContainer = QHBoxLayout()
        self.mainMenuBtn = QPushButton('Menu')
        self.mainMenuBtn.setMinimumWidth(100)
        self.mainMenuBtn.setMinimumHeight(50)
        self.saveBtn = QPushButton('Save')
        self.saveBtn.setMinimumWidth(100)
        self.saveBtn.setMinimumHeight(50)
        mainActionsContainer.addStretch(1)
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

    def onStateBoxChange(self, state):
        self.model.setState(state)
        cities = self.model.getAllCities()

        # reset and update cities
        self.city.fillCityBox(cities)

        # disable address input
        self.address.disable()

        # reset and update table
        self.inputExcelTable.resetData()

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

    def startTypingTimer(self):
        self.typingTimer.start(250)

    def onAddressTextChange(self):
        self.model.setAddress(self.address.getText())
        self.inputExcelTable.updateData(self.model.currentFrame())

    def onAddRecordClick(self):
        ix = self.inputExcelTable.selectionModel().selectedRows()
        for i in sorted(ix):
            print(i.row())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    files = ['/Users/howardwang/Desktop/excel-application/excel-files/8.7.2020 nj pm.xls.xlsx', \
             '/Users/howardwang/Desktop/excel-application/excel-files/8.10.2020 nj am.xls.xlsx']
    # files = ['/Users/howardwang/Desktop/excel-application/test-files/append-test1.xlsx', \
    #          '/Users/howardwang/Desktop/excel-application/test-files/append-test2.xlsx']
    model = ExcelModel(files)
    ex = ExcelWindow(model)
    sys.exit(app.exec_())
