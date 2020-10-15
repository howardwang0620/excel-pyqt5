import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Model import ExcelModel
from UploaderView import UploadWindow
from ExcelView import ExcelWindow
from Widgets.Widgets import CustomQMessageBox


class Controller(ApplicationContext):
    def __init__(self):
        super().__init__()
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

    def filesUploaded(self):
        response = self.model.buildDF()
        if response['status_code']:
            self.view.close()
            self.initExcelView()
        else:
            CustomQMessageBox('Warning', response['message'])

    def returnToUpload(self):
        self.view.close()
        self.initUploadView(self.model.files)

    def run(self):
        return self.app.exec_()


if __name__ == '__main__':
    c = Controller()
    exit_code = c.run()
    sys.exit(exit_code)
