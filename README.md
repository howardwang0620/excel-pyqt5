# excel-pyqt5
PyQt5 UI for modifying Excel Files (Upwork Project)

## Requirements:
1. Make sure you have [Git](https://git-scm.com/downloads) installed
2. Install [Python3.6](https://www.python.org/downloads/release/python-360/) if not installed (**Must use Python 3.6**)
3. Make sure you have [pip](https://pip.pypa.io/en/stable/installing/) installed
4. Install virtualenv if not installed by running:
    - `pip install virtualenv`


## Setup

1. Clone this repo onto your machine using:
    - `git clone https://github.com/howardwang0620/excel-pyqt5.git`
2. CD into directory with:
    - `cd excel-pyqt5`
3. Create a virtualenv running Python3.6:
    - `virtualenv -p {path\to\python3.6\executable} myenv`
    - {path\to\python3.6\executable} designates the location where python3.6 was installed (**don't include the brackets**):
        - eg:  `C:\Users\{user}\AppData\Local\Programs\Python\Python36\python.exe`
4. Activate virtualenv by running (**must do this everytime you want to interact with app through command line**):
    - `myenv\scripts\activate.bat`
5. Install pip dependencies:
    - `pip install -r requirements.txt`
6. Run the application using:
    - `fbs run`

## Create Application
**:warning: Must have virtualenv activated (Setup -> Step 2)**

* #### Freeze into Desktop Application
    1. run `fbs freeze`
        * If error occurs with FileNotFound - missing api-ms-win-crt-*:
            1. Check if the directory exists by going to:`C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64`
                - If you don't have it, download it [here](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)
            2. Add directory to PATH environment variable:
                * `This PC->Properties->Advanced System Settings`
                * Under System Variables, **select Path and Edit**. Add a new path by **selecting New**, then paste in location of 64-bit DLL (the directory above) and **apply changes**
            3. Restart your computer and run `fbs freeze` again


* #### Create Distributable Installer :
    1. Run and install NSIS ([download here](https://sourceforge.net/projects/nsis/files/NSIS%203/3.06.1/nsis-3.06.1-setup.exe/download?use_mirror=iweb&download=))
    2. Add NSIS directory to PATH environment variable:
        * `This PC->Properties->Advanced System Settings`
        * Under System Variables, **select Path and Edit**. Add a new path by **selecting New**, then paste in location of NSIS and **apply changes**
    3. Restart your computer
    3. Run `fbs installer`
