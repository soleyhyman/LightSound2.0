# LightSound Computer Interface

The LightSound Computer Interface is the updated program for connecting your LightSound to your computer and log or liveplot data, as well as to plot pre-existing LightSound data. It features a more intuitive graphical user interface (GUI) to be more accessible for a wide range of users. The capabilities of the program for each operating system are described under [Details for Supported Operating Systems](#details-for-supported-operating-systems) below.

## Details for Supported Operating Systems
### Windows Users
The LightSound Computer Interface is available as both a stand-alone program (.exe file) and a Python script. It is screenreader accessible. To download the...
- **Standalone program**: Click [**here**](https://github.com/soleyhyman/LightSound2.0/raw/main/LightSound-Computer-Interface/LightSound-Interface-Windows/LightSound-Interface-Windows.zip?download=) to download the ZIP folder of the standalone Windows program. If you're unfamiliar with ZIP files, you can follow the directions at [this link](https://support.microsoft.com/en-us/windows/zip-and-unzip-files-8d28fa72-f2f9-712f-67df-f80cf89fd4e5) to extract the program.
- **Python program**: Download the Python script file at this [link](https://github.com/soleyhyman/LightSound2.0/blob/main/LightSound-Computer-Interface/LightSound-Interface-Windows/LightSound-Interface-Windows.py) via the download symbol icon. See [Python Setup Information](#python-setup-information) for instructions on how to setup the Python environment.

### Mac/OSX Users
- **Standalone program**: Click [**here**](https://github.com/soleyhyman/LightSound2.0/raw/main/LightSound-Computer-Interface/LightSound-Interface-Mac-OSX/LightSound-Interface-OSX.zip?download=) to download the ZIP folder of the standalone Mac OSX program. You can uncompress/unzip the folder by double-clicking on it.
- **Python program**: Download the Python script file [here](https://github.com/soleyhyman/LightSound2.0/blob/main/LightSound-Computer-Interface/LightSound-Interface-Mac-OSX/LightSound-Interface-OSX.py). See [Python Setup Information](#python-setup-information) for instructions on how to setup the Python environment.

### UNIX System Users (e.g., Linux, Ubuntu, Debian)
Currently, there is no standalone application being developed. You can use the same Python program for Mac/OSX users, which can be downloaded [here](https://github.com/soleyhyman/LightSound2.0/blob/main/LightSound-Computer-Interface/LightSound-Interface-Mac-OSX/LightSound-Interface-OSX.py). See [Python Setup Information](#python-setup-information) for instructions on how to setup the Python environment.

## Python Setup Information
**Note:** If you already use Python regularly, we recommend you set up a virtual environment to separate this installation from your other installations. If you use an Anaconda distribution, you can find instructions at [this link](https://www.geeksforgeeks.org/set-up-virtual-environment-for-python-using-anaconda/). If you do not use Anaconda, you can follow the directions [here](https://docs.python.org/3/tutorial/venv.html).

For detailed instructions on how to set up Python, see the [Python-Setup-Instructions-for-LightSound-Interface](https://github.com/soleyhyman/LightSound2.0/blob/main/LightSound-Computer-Interface/Python-Setup-Instructions-for-LightSound-Interface.pdf) document.

If you are already familiar with Python, you can follow the below steps:
1. Install the necessary packages via the following commands:
    ```
    pip install numpy
    pip install matplotlib
    pip install pyserial
    pip install wxpython
    ```
    You can skip the first two lines if you already have `numpy` and `matplotlib` installed.
2. If you want, move the LightSound Interface Python code to to wherever you can easily find it (e.g., Desktop, Documents).
3. In your terminal or file window, navigate to where you have saved the Python script and make a new folder called `LightSoundData`.
4. To run the code:
    - Windows: 
        ```
        python LightSound-Interface-Windows.py
        ```
    - Mac/Linux:
        ```
        python LightSound-Interface-OSX.py
        ```