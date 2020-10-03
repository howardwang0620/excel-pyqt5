from fbs_runtime.application_context.PyQt5 import ApplicationContext
from MainView import Window

import sys

class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        self.setup_upload_window()
        return self.app.exec_()                 # 3. End run() with this line

    def setup_upload_window(self):
        self.uploader = Window()

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
