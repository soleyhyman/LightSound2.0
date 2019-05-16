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

# Define function to read logged LightSound 2.0 data
def LightSoundReaderV2Log(inputFilename):

	# make lists
	timezone = ''
	timestamp_list = []
	time_list = []
	lux_list = []
	gain_list = []
	integration_list = []

	# read in input file
	inputDataFile = open(inputFilename)
	lines = inputDataFile.readlines()

	# loop over lines
	for l in range(len(lines)):
		currentline = lines[l]
		if currentline.startswith("Timezone"):
			linesplit = currentline.split(None)
			timezone = linesplit[1]			
		if currentline.startswith("Time:"):
			linesplit = currentline.split(None)
			timestamp = linesplit[1] + ' ' + linesplit[2]
			timestamp_list.append(timestamp)
		elif currentline.startswith("["):
			linesplit = currentline.split(None)
			time_list.append(linesplit[1])
		elif currentline.startswith("Visible"):
			linesplit = currentline.split(None)
			lux_list.append(linesplit[2])
		elif currentline.startswith("Gain"):
			linesplit = currentline.split(None)
			gain = linesplit[1].strip('x')
			gain_list.append(gain)
		elif currentline.startswith("Integration"):
			linesplit = currentline.split(None)
			integration_list.append(linesplit[1])
		else:
			pass

	return 	timezone, timestamp_list, time_list, lux_list, gain_list, integration_list

##################################

# Read arguments from command line
serial_port = str(sys.argv[1])	# Can be found using 'mode' command (Windows), ls /dev/tty.* (should be /dev/tty.usbmodem* or /dev/tty.usbserial* for Mac; /dev/ttyUSB* or /dev/ttyACM* for Linux)
baud_rate = int(sys.argv[2])	# Should be 9600 for LightSound 2.0
timezone = str(sys.argv[3])		# Specify timezone of observations (e.g. CST, EST, ART, CLT, etc.)
file_prefix = str(sys.argv[4])		# Specify filename prefix for data files (NO extension)

# Create serial port
ser = serial.Serial(serial_port, baud_rate)

# Open logging file and begin logging data
with open(file_prefix + '_raw.log', 'w+') as f:
	print('Timezone:', timezone, '\n')
	f.writelines('Timezone: ' + timezone + '\r \n')
	while True:
		try:
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
		except KeyboardInterrupt:
			f.close()
			print('Logging terminated')
			break

############################

# Read logged data and save it as columns in tab separated file

# Read in logged data
v2_timezone, v2_timestamps, v2_times, v2_lux, v2_gains, v2_integrations = LightSoundReaderV2Log(file_prefix+'_raw.log')

# Group data by rows
with open(file_prefix+'_data.csv', 'w+') as col_file:
	col_file.writelines('Timezone: ' + timezone + '\n')
	col_file.writelines('Timestamp, Time (ms), Lux, Gain, Integration\n')

	for i in range(len(v2_timestamps)):
		data_row = [v2_timestamps[i], v2_times[i], v2_lux[i], v2_gains[i], v2_integrations[i]]
		col_file.writelines(','.join(data_row) + '\n')

print('Logged data saved in columns')
col_file.close()