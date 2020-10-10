# excel-pyqt5
PyQt5 UI for modifying Excel Files (Upwork Project)

## Installation:
1. Clone this repo to your directory using [Git](https://git-scm.com/downloads)
    - `git clone https://github.com/howardwang0620/excel-pyqt5.git`


2. Install [Python3.6](https://www.python.org/downloads/release/python-360/) if not installed (**Must use Python 3.6**)


3. [Install pip](https://pip.pypa.io/en/stable/installing/) if not installed


4. Install virtualenv if not already installed by running:
    - `pip install virtualenv`


## Setup
1. CD into directory with:
    - `cd excel-pyqt5`


2. Create a virtualenv running Python3.6:
    - `virtualenv -p {path\to\python3.6\executable} myenv`
    - {path\to\python3.6\executable} designates the location where python3.6 was installed (**don't include the brackets**):
        - eg:  `C:\Users\{user}\AppData\Local\Programs\Python\Python36\python.exe`


3. Activate virtualenv by running (**must do this everytime you want to interact with app through command line**):
    - `myenv\scripts\activate.bat`


4. Install dependencies:
    - `pip install -r requirements.txt`


5. Run the application using:
    - `fbs run`

## Create Application
**:warning: Must have virtualenv activated (Setup -> Step 2)**

* #### Freeze into Desktop Application
    1. run `fbs freeze`
        * If error occurs with FileNotFound - missing api-ms-win-crt-*:
            1. Check if the directory exists by going to:`C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64`
                - If you don't have it, download it [here](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)
            2. Add to PATH environment variable:
                * `This PC->Properties->Advanced System Settings`
                * Under System Variables, **select Path and Edit**. Add a new path by **selecting New**, then paste in location of 64-bit DLL (the directory above) and **apply changes**
            3. Restart your computer


* #### Create Distributable Installer :
    1. Run and install NSIS ([download here](https://sourceforge.net/projects/nsis/files/NSIS%203/3.06.1/nsis-3.06.1-setup.exe/download?use_mirror=iweb&download=))
    2. Add NSIS directory to PATH environment variable:
        * `This PC->Properties->Advanced System Settings`
        * Under System Variables, **select Path and Edit**. Add a new path by **selecting New**, then paste in location of NSIS and **apply changes**
    3. Restart your computer
    3. Run `fbs installer`
