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

    # Initializes controller and activates UploaderView
    def initController(self):
        self.initUploadView()

    # This function inits UploaderView and connects the filesUploaded() function to UploaderView's uploadSignal
    # When the uploadSignal is emitted, the filesUploaded() function begins executing
    def initUploadView(self, files=None):
        self.model = ExcelModel(files)
        self.view = UploadWindow(self.model)
        self.view.uploadSignal.connect(self.filesUploaded)
        self.view.show()

    # Initiates the Excel View window and connects the returnMenuSignal to returnToUpload()
    def initExcelView(self):
        self.view = ExcelWindow(self.model)
        self.view.returnMenuSignal.connect(self.returnToUpload)
        self.view.show()

    # Executes when UploaderView.uploadSignal is emitted (user has uploaded and submitted files)
    # This will close the active UploaderView, and initialize the ExcelView for processing data
    def filesUploaded(self):
        response = self.model.buildDF()
        if response['status_code']:
            self.view.close()
            self.initExcelView()
        else:
            CustomQMessageBox('Warning', response['message'])

    # Function occurs when exiting ExcelView, either through 1. Saving a file or 2. Pressing Main Menu
    def returnToUpload(self):
        self.view.close()
        self.initUploadView(self.model.files)

    def run(self):
        return self.app.exec_()


if __name__ == '__main__':
    c = Controller()
    exit_code = c.run()
    sys.exit(exit_code)
