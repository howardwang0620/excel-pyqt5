import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Model import ExcelModel
from UploaderView import UploadWindow
from ExcelView import ExcelWindow

class Controller(QApplication):
    def __init__(self, sys_argv):
        super(Controller, self).__init__(sys_argv)
        self.initController()

    # init controller buttons based on type, eg: upload, save, back
    def initController(self):
        # connect uploadFiles signal
        self.initUploadView()

    def initUploadView(self, files=None):
        self.model = ExcelModel(files)
        self.view = UploadWindow(self.model)
        self.view.uploadSignal.connect(self.filesUploaded)
        self.view.show()

    def initExcelView(self):
        self.view = ExcelWindow(self.model)
        self.view.returnMenuSignal.connect(self.returnToUpload)
        self.view.show()

    @pyqtSlot()
    def filesUploaded(self):
        self.view.close()
        self.model.buildDF()
        self.initExcelView()

    @pyqtSlot()
    def returnToUpload(self):
        self.view.close()
        self.initUploadView(self.model.files)

    def run(self):
        return self.exec_()

if __name__ == '__main__':
    app = Controller(sys.argv)
    sys.exit(app.exec())