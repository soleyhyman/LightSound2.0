##############
## Data plotter for LightSound 2.0
## Code developed by Soley Hyman
## last updated: 14 May 2019 
## Python package requirements: datetime, matplotlib, numpy, sys
##############

# Import packages
import numpy as np
import matplotlib.dates as mdates
import sys
from datetime import datetime
from matplotlib import pyplot as plt

# Define function to read logged LightSound 2.0 data
def LightSoundReaderV2(inputFilename):

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
			timestamp_fmt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
			timestamp_list.append(timestamp_fmt)
		elif currentline.startswith("["):
			linesplit = currentline.split(None)
			time = float(linesplit[1])
			time_list.append(time)
		elif currentline.startswith("Visible"):
			linesplit = currentline.split(None)
			lux = float(linesplit[2])
			lux_list.append(lux)
		elif currentline.startswith("Gain"):
			linesplit = currentline.split(None)
			gain = int(linesplit[1].strip('x'))
			gain_list.append(gain)
		elif currentline.startswith("Integration"):
			linesplit = currentline.split(None)
			integration = int(linesplit[1])
			integration_list.append(integration)
		else:
			pass

	return 	timezone, timestamp_list, time_list, lux_list, gain_list, integration_list


# Read in arguments from command line
filename = str(sys.argv[1])		 # Specify filename of logged data, with extension
plot_lines = int(sys.argv[2])	 # Specify whether to also graph gain and integration times (0 = lux only, 1 = lux, gain, and integrations)
savename = str(sys.argv[3])		 # Specify savename (with extension, usually .png); use 'none' if no save desired

# Read in data
v2_timezone, v2_timestamps, v2_times, v2_lux, v2_gains, v2_integrations = LightSoundReaderV2(filename)

# Plot data
if plot_lines == 0: 
	plt.plot(v2_timestamps, v2_lux, color='blue', label='Lux')
elif plot_lines == 1:
	plt.plot(v2_timestamps, v2_lux, color='blue', label='Lux')
	plt.plot(v2_timestamps, v2_gains, color='red', label='Gain')
	plt.plot(v2_timestamps, v2_integrations, color='green', label='Integration')

# Format plot ticks
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)

# Format plot title and labels
plt.title(v2_timestamps[0].strftime('Observations on %Y %b %d at approx. %H:%M ') + v2_timezone)
plt.xlabel('Local time (%s)' % v2_timezone)
plt.ylabel('Intensity (Lux)')
if plot_lines != 0: plt.legend(loc='upper right')

# Save image and show plot
if savename != 'none':
	plt.savefig(savename, dpi=500, bbox_inches='tight')
	plt.show()
else:
	plt.show()