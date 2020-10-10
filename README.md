# excel-pyqt5
PyQt5 UI for modifying Excel Files (Upwork Project)

## Installation:
1. Clone this repo to your directory using Git (install [git here](https://git-scm.com/downloads)):


2. CD into directory by using:
    - `cd excel-pyqt5`


3. [Install Python3.6](https://www.python.org/downloads/release/python-360/) if not installed (**Must use Python 3.6**):


4. [Install pip](https://pip.pypa.io/en/stable/installing/) if not installed:


5. Install virtualenv if not already installed by running:
    - `pip install virtualenv`


## Setup
1. Run python3.6 in a virtualenv by running:
    - `virtualenv -p {path\to\python\executable} myenv`
    - {path\to\python\executable} designates the location where python3.6 was installed (**don't include the brackets**):
        - eg:  `C:\Users\{user}\AppData\Local\Programs\Python\Python36\python.exe`


2. Activate virtualenv by running (**must do this everytime you want to interact with app through command line**):
    - `myenv\scripts\activate.bat`


3. Run to install dependencies:
    - `pip install -r requirements.txt`


4. Run the application using:
    - `fbs run`

## Create Application
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
