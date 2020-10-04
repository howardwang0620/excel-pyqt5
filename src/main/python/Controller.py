import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Model import ExcelModel
from UploaderView import UploadWindow
from ExcelView import ExcelWindow

class Controller(ApplicationContext):
    def __init__(self):
        super().__init__()

        self.model = ExcelModel()
        self.view = UploadWindow(self.model)
        self.initController()

    # init controller buttons based on type, eg: upload, save, back
    def initController(self):
        # connect uploadFiles signal
        self.initView("yes")

    def initView(self, type):
        # self.view.fileList.addFileSignal.connect(self.addFileToModel)
        # self.view.fileList.removeFileSignal.connect(self.removeFileFromModel)
        self.view.uploadSignal.connect(self.filesUploaded)

    # @pyqtSlot(str)
    # def addFileToModel(self, file):
    #     self.model.addFile(file)
    #
    # @pyqtSlot(str)
    # def removeFileFromModel(self, file):
    #     self.model.removeFile(file)
    #
    # @pyqtSlot()
    def filesUploaded(self):
        self.view.close()
        self.view = ExcelWindow(self.model)

    def run(self):
        self.view.show()
        return self.app.exec_()

if __name__ == '__main__':
    c = Controller()                      # 4. Instantiate the subclass
    exit_code = c.run()                   # 5. Invoke run()
    sys.exit(exit_code)
