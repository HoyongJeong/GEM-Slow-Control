#!/usr/bin/python3


################################################################################
#   Script to control motor                                                    #
# Original was written by Fabian Muller.                                       #
#                                                                              #
#                      - 27. Nov. 2017. Hoyong Jeong (hyjeong@hep.korea.ac.kr) #
################################################################################


from GEMSlowControlClasses import MotorControl


################################################################################
#   Main function                                                              #
################################################################################
if __name__ == '__main__':

	Motor = MotorControl('/dev/ttyACM1');
	Motor.PrintWelcome();
	Motor.Connect();

	while Motor.IsReady:
		Motor.PrintStatus();
		menu = Motor.PrintMenu();
		if menu == '0':
			Motor.PrintDescription();
		if menu == '1':
			pos = input(' Move to: ');
			pos = int(pos);
			Motor.MoveTo(pos);
		if menu == '2':
			print('Bye bye :)');
			break;
		if menu == '3':
			Motor.GoHome();
			print('Bye bye :)');
			break;
		else:
			print();
			continue;
