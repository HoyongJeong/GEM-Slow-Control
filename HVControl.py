#!/usr/bin/python3


################################################################################
#   Script for communication with Heiniozinger(R) Digital Interface II         #
# This interface controls HV supplier whose model is 'PNC 6000 - 10'.          #
#                                                                              #
#                      - 24. Nov. 2017. Hoyong Jeong (hyjeong@hep.korea.ac.kr) #
################################################################################


from GEMSlowControlClasses import HVControl


################################################################################
#   Main function                                                              #
################################################################################
if __name__ == '__main__':

	HV = HVControl('/dev/ttyUSB0');
	HV.PrintWelcome();
	HV.Connect();

	while HV.IsReady():
		HV.PrintStatus();
		menu = HV.PrintMenu();
		if menu == '0':
			HV.PrintDescription();
			print();
		if menu == '1':
			command = input(' -> Voltage? (in V): ');
			HV.SetVoltage(command);
			print();
		if menu == '2':
			command = input(' -> Current? (in uA): ');
			HV.SetCurrent(command);
			print();
		if menu == '3':
			command = input(' -> Ramp-up? (in V/s): ');
			HV.SetRampUp(command);
			print();
		if menu == '4':
			command = input(' -> Ramp-down? (in V/s): ');
			HV.SetRampDown(command);
			print();
		if menu == '5':
			HV.TurnOn();
			print();
		if menu == '6':
			HV.TurnOff();
			print();
		if menu == '7':
			print(' Version of interface:', HV.GetVer());
			print();
		if menu == '8':
			print(' S/N of the power supply:', HV.GetSN());
		if menu == '9':
			HV.Reset();
			print();
		if menu == '10':
			print('Bye bye :)');
			break;
		if menu == '11':
			HV.Reset();
			print('Bye bye :)');
			break;
		else:
			print();
			continue;
