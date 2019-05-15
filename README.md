# LightSound2.0
Python data logger, plotter, and Arduino code for LightSound 2.0 devices

### About LightSound
LightSound is an Arduino-based device that converts light intensity to sound via a light sensor and MIDI board so that blind and visually impaired (BVI) individuals may experience events like solar and lunar eclipses. The original version (LightSound 1.0) was designed and used during the total solar eclipse on August 21, 2017. In preparation for the upcoming North and South American total solar eclipses (2019, 2020, and 2024), LightSound has been redesigned with higher sensitivities and an improved sound library. The project has received funding from IAU100 to build and distribute 20 LightSound 2.0 to schools in Chile and Argentina in the path of the 2019 and 2020 solar eclipses so that BVI students may experience the event. More information and instructions for LightSound 2.0 can be found at: http://astrolab.fas.harvard.edu/accessibility.html

### Instructions for logging data
Runs on Python 3.x

Package requirements: `datetime`, `sys`, and [`pySerial`](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)
1. Ensure that the serial logger program (LightSound2_data_logger.py) is located in the folder where you will save your data
2. Connect the LightSound 2.0 to the computer with a micro-USB B cord (must be able to transfer data)
3. Determine the appropriate serial port of the LightSound 2.0
    -	Windows: type `mode` into command line, port should have the form `COM*`
    - Mac: type `ls /dev/tty.*` into terminal, port should have the form `/dev/tty.usbmodem*` or `/dev/tty.usbserial*` 
    - Linux: type `ls/dev/tty.*` into terminal, port should have the form `/dev/ttyUSB*` or `/dev/ttyACM*`
4. In the terminal (Mac/Linux) or command line (Windows), navigate to data folder and type: `python LightSound2_data_logger.py port 9600 timezone filename.txt`
    - `port` is the port name determined in Step 3
    - `9600` is the baud rate for reading the LightSound 2.0 data
    -	`timezone` is the timezone of observations (e.g. CST, EST, ART, CLT, etc.)
    -	`filename` is the prefix of the name of the log file for the data
5. To stop data logging, press `Ctrl + C` in terminal/command line

### Instructions for plotting data
Runs on Python 3.x

Package requirements: `datetime`, `matplotlib`, `numpy`, `sys`
1. Ensure that the serial logger program (LightSound2_data_plotter.py) is located in the folder where you will save your data
2. In the terminal (Mac/Linux) or command line (Windows), navigate to data folder and type: `python LightSound2_data_parser.py filename.txt plot_lines savename.png`
    - `filename` is the prefix of the name of the log file for the data (extension should be the same as used for the data logging)
    - `plot_lines` determines whether the plot will include whether the gain and integration times (0 = lux only, 1 = lux, gain, and integrations)
    - `savename` is the prefix of the image name the plot will save to; use none if you do not want to save the image (extension typically is .png)
