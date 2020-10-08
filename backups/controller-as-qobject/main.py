import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from Controller import Controller

if __name__ == '__main__':
    appctxt = ApplicationContext()
    controller = Controller(sys.argv)
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
