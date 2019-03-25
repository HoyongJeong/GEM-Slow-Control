#!/usr/bin/python3


from GEMSlowControlClasses import HVControl
import time


################################################################################
#   Main function                                                              #
################################################################################
if __name__ == '__main__':

	HV = HVControl('/dev/ttyUSB0');
	HV.Connect();

	timestamp = int(time.time());
	vol = HV.MeasureVoltage();
	cur = HV.MeasureCurrent();

#	print('Time =', timestamp, ', Voltage =', vol, ', Current =', cur);
	print(timestamp, vol, cur);
