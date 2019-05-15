##############
## Serial logger for LightSound 2.0
## Code developed by Soley Hyman, with help from G M's code at: https://electronics.stackexchange.com/questions/54/saving-arduino-sensor-data-to-a-text-file */
## last updated: 14 May 2019 
## Python package requirements: pySerial (https://pyserial.readthedocs.io/en/latest/pyserial.html#installation), datetime, sys
##############

# Import packages
import serial
import sys
from datetime import datetime

# Read arguments from command line
serial_port = str(sys.argv[1])	# Can be found using 'mode' command (Windows), ls /dev/tty.* (should be /dev/tty.usbmodem* or /dev/tty.usbserial* for Mac; /dev/ttyUSB* or /dev/ttyACM* for Linux)
baud_rate = int(sys.argv[2])	# Should be 9600 for LightSound 2.0
timezone = str(sys.argv[3])		# Specify timezone of observations (e.g. CST, EST, ART, CLT, etc.)
filename = str(sys.argv[4])		# Specify filename for log file with extension (usually .txt)


# Create serial port
ser = serial.Serial(serial_port, baud_rate)

# Open logging file and begin logging data
with open(filename, 'w+') as f:
    print('Timezone:', timezone, '\n')
    f.writelines('Timezone: ' + timezone + '\r \n')
    while True:
        timeNow = datetime.now()
        line = ser.readline()
        line = line.decode("utf-8")
        if line.startswith('['):
            f.writelines('Time: ' + str(timeNow) + '\n')
            print('Time:', timeNow)
            f.writelines([line])
            print(line.strip('\n'))	
        else:
            f.writelines([line])
            print(line.strip('\n'))	