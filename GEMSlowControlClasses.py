################################################################################
#   Definitions of GEM slow control classs.                                    #
# MotorControl class has been written by Fabian Muller.                        #
#                                                                              #
#                      - 27. Nov. 2017. Hoyong Jeong (hyjeong@hep.korea.ac.kr) #
################################################################################


import serial
import sys
import time
import datetime


################################################################################
#   Class definition of HVControl                                              #
################################################################################
class HVControl:
	#------------------------------------------------#
	#   Members                                      #
	#------------------------------------------------#
	# Commands
	__cmd_SetV     = 'VOLT';
	__cmd_GetV     = 'VOLT?';
	__cmd_SetI     = 'CURR';
	__cmd_GetI     = 'CURR?';
	__cmd_On       = 'OUTP ON';
	__cmd_Off      = 'OUTP OFF';
	__cmd_MeasureV = 'MEAS:VOLT?';
	__cmd_MeasureI = 'MEAS:CURR?';
	__cmd_GetVer   = 'VERS?';
	__cmd_GetSN    = '*IDN?';
	__cmd_Reset    = '*RST';
	# Parameters
	__minV         =     0;
	__maxV         =  6000; # in V
	__minI         =     0;
	__maxI         = 10000; # in uA
	__rampUp       =    50; # in V/s
	__rampDown     =    50; # in V/s
	# Etc
	__Is_Ready     = False;
	__serial       =     0;
	rate           =  9600;
	__port         =    '';

	#------------------------------------------------#
	#   Initialize when constructed                  #
	#------------------------------------------------#
	def __init__(self, port):
		self.__port = port;

	#------------------------------------------------#
	#   Get whether it is ready or not               #
	#------------------------------------------------#
	def IsReady(self):
		return self.__Is_Ready;

	#------------------------------------------------#
	#   Get connection                               #
	#------------------------------------------------#
	def Connect(self):
		if not self.__Is_Ready:
			try:
				self.__serial = serial.Serial(self.__port, baudrate=self.rate, timeout=0.5, interCharTimeout=0.005);
#				self.__serial = serial.Serial(self.__port, baudrate=self.rate);
				self.__Is_Ready = True;
			except:
				self.__Is_Ready = False;
				print(' Failed to connect with port', self.__port, '(', sys.exc_info()[0], ')');
				print(' 1. You may need sudo?');
				print(' 2. Or please check USB connection.');
				return False;
		else:
			print(' Connection is already on.');
		return True;

	#------------------------------------------------#
	#   Send command                                 #
	#------------------------------------------------#
	def __sendCommand(self, cmd, argument = ''):
		if self.__Is_Ready:
			self.__serial.write(cmd.encode('ascii'));
			if argument != '':
				self.__serial.write(' '.encode('ascii'));
				self.__serial.write(argument.encode('ascii'));
			self.__serial.write('\n'.encode('ascii'));
		else:
			print(' Not ready. Cannot send command', cmd, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return False;
		return True;

	#------------------------------------------------#
	#   Read answer                                  #
	#------------------------------------------------#
	def __readAns(self):
		if self.__Is_Ready:
			try:
				return self.__serial.read_all().decode()[:-1];
			except:
				print(' Error while reading from', self.__port, '(', sys.exc_info()[0], ')');
				self.__Is_Ready = False;
				return '';

	#------------------------------------------------#
	#   Set voltage                                  #
	#------------------------------------------------#
	def SetVoltage(self, vol):
		if self.__Is_Ready and int(vol) >= self.__minV and int(vol) <= self.__maxV:
			self.__sendCommand(self.__cmd_SetV, vol);

	#------------------------------------------------#
	#   Set current                                  #
	#------------------------------------------------#
	def SetCurrent(self, cur):
		if self.__Is_Ready and int(cur) >= self.__minI and int(cur) <= self.__maxI:
			self.__sendCommand(self.__cmd_SetI, cur);

	#------------------------------------------------#
	#   Get voltage                                  #
	#------------------------------------------------#
	def GetVoltage(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_GetV);
			time.sleep(0.1);
			return self.__readAns();
		else:
			print(' Not ready. Cannot send command', __cmd_GetV, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return '';

	#------------------------------------------------#
	#   Get current                                  #
	#------------------------------------------------#
	def GetCurrent(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_GetI);
			time.sleep(0.1);
			return self.__readAns();
		else:
			print(' Not ready. Cannot send command', __cmd_GetI, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return '';

	#------------------------------------------------#
	#   Measure voltage                              #
	#------------------------------------------------#
	def MeasureVoltage(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_MeasureV);
			time.sleep(0.3);
			return self.__readAns();
		else:
			print(' Not ready. Cannot send command', __cmd_MeasureV, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return '';

	#------------------------------------------------#
	#   Measure current                              #
	#------------------------------------------------#
	def MeasureCurrent(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_MeasureI);
			time.sleep(0.3);
			return self.__readAns();
		else:
			print(' Not ready. Cannot send command', __cmd_MeasureI, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return '';

	#------------------------------------------------#
	#   Set ramp-up                                  #
	#------------------------------------------------#
	def SetRampUp(self, value):
		self.__rampUp = int(value);

	#------------------------------------------------#
	#   Set ramp-down                                #
	#------------------------------------------------#
	def SetRampDown(self, value):
		self.__rampDown = int(value);

	#------------------------------------------------#
	#   Get ramp-up                                  #
	#------------------------------------------------#
	def GetRampUp(self):
		return self.__rampUp;

	#------------------------------------------------#
	#   Get ramp-down                                #
	#------------------------------------------------#
	def GetRampDown(self):
		return self.__rampDown;

	#------------------------------------------------#
	#   Activate output                              #
	#------------------------------------------------#
	def TurnOn(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_On);
#			goal = self.GetVoltage();
#			if goal == '.0':
#				goal = '0';
#			self.SetVoltage('0');
#			self.__sendCommand(self.__cmd_On);
#			now = self.__rampUp;
#			while float(now) < float(goal):
#				self.SetVoltage(str(now));
#				print(' Activating... V =', now);
#				now = now + self.__rampUp;
#				time.sleep(1);
#			self.SetVoltage(goal);
		else:
			print(' Not ready. Cannot send command', __cmd_On, 'to', self.__port, '(', sys.exc_info()[0], ')');

	#------------------------------------------------#
	#   Deactivate output                            #
	#------------------------------------------------#
	def TurnOff(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_Off);
		else:
			print(' Not ready. Cannot send command', __cmd_Off, 'to', self.__port, '(', sys.exc_info()[0], ')');

	#------------------------------------------------#
	#   Get version                                  #
	#------------------------------------------------#
	def GetVer(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_GetVer);
			time.sleep(0.1);
			return self.__readAns();
		else:
			print(' Not ready. Cannot send command', __cmd_GetVer, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return '';

	#------------------------------------------------#
	#   Get serial number                            #
	#------------------------------------------------#
	def GetSN(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_GetSN);
			time.sleep(0.1);
			return self.__readAns();
		else:
			print(' Not ready. Cannot send command', __cmd_GetSN, 'to', self.__port, '(', sys.exc_info()[0], ')');
			return '';

	#------------------------------------------------#
	#   Reset                                        #
	#------------------------------------------------#
	def Reset(self):
		if self.__Is_Ready:
			self.__sendCommand(self.__cmd_Reset);
		else:
			print(' Not ready. Cannot send command', __cmd_Reset, 'to', self.__port, '(', sys.exc_info()[0], ')');

	#------------------------------------------------#
	#   Print welcome                                #
	#------------------------------------------------#
	def PrintWelcome(self):
		print('\x1b[1;33m================================================================\x1b[0m');
		print('\x1b[1;32m Python script for...\x1b[0m');
		print();
		print('\x1b[1;32m H   H  V   V     CCC   OOO   N   N  TTTTT  RRRR    OOO   L      \x1b[0m');
		print('\x1b[1;32m H   H  V   V    C     O   O  NN  N    T    R   R  O   O  L      \x1b[0m');
		print('\x1b[1;32m HHHHH  V   V    C     O   O  N N N    T    RRRR   O   O  L      \x1b[0m');
		print('\x1b[1;32m H   H   V V     C     O   O  N  NN    T    R  R   O   O  L      \x1b[0m');
		print('\x1b[1;32m H   H    V       CCC   OOO   N   N    T    R   R   OOO   LLLLL  \x1b[0m');
		print('\x1b[1;33m================================================================\x1b[0m');
		print('\x1b[1;31m Author:        Hoyong Jeong (hyjeong.hep.korea.ac.kr)\x1b[0m');
		print('\x1b[1;31m Available for: Heinzinger Digital Interface II\x1b[0m');
		print('\x1b[1;31m Applied to:    PNC 6000 - 10 model\x1b[0m');
		print('\x1b[0m\x1b[1;33m================================================================\x1b[0m');
		print('\x1b[1;34m - This is a script to control HV supplier remotely.');
		print('\x1b[1;34m - Please choose number in menu.');
		print('\x1b[1;34m - Just hit enter to refresh.');
		print('\x1b[0m\x1b[1;33m================================================================\x1b[0m');

	#------------------------------------------------#
	#   Print status                                 #
	#------------------------------------------------#
	def PrintStatus(self):
		time.sleep(0.3);
		print(' ==============================================');
		print('  Machine status at', datetime.datetime.now());
		print(' ----------------------------------------------');
		print('  Ramp-up/down setting:\x1b[1;36m', self.GetRampUp(), 'V/s \x1b[0m / \x1b[1;36m', self.GetRampDown(), 'V/s\x1b[0m');
		print('  Output setting:      \x1b[1;36m', self.GetVoltage(), 'V \x1b[0m / \x1b[1;36m', self.GetCurrent(), 'uA\x1b[0m');
		print('  Measured real output:\x1b[1;36m', self.MeasureVoltage(), 'V \x1b[0m / \x1b[1;36m', self.MeasureCurrent(), 'uA\x1b[0m');
		print(' ==============================================');

	#------------------------------------------------#
	#   Print menu                                   #
	#------------------------------------------------#
	def PrintMenu(self):
		print(' +----------+---------------------------------+');
		print(' | Menu No. | Description                     |');
		print(' +==========+=================================+');
		print(' |     0    | Details                         |');
		print(' |     1    | Set voltage                     |');
		print(' |     2    | Set current                     |');
		print(' |     3    | Set ramp-up                     |');
		print(' |     4    | Set ramp-down                   |');
		print(' |     5    | Activate output                 |');
		print(' |     6    | Deactivate output               |');
		print(' |     7    | Check version of this interface |');
		print(' |     8    | Show S/N of this HV supply      |');
		print(' |     9    | Reset                           |');
		print(' |    10    | Exit                            |');
		print(' |    11    | Exit with reset                 |');
		print(' +----------+---------------------------------+');
		menu = input(' Choose: ');
		return menu;

	#------------------------------------------------#
	#   Print description                            #
	#------------------------------------------------#
	def PrintDescription(self):
		print('  0. Show this.');
		print('  1. Set voltage in V unit.');
		print('  2. Set current in uA unit.');
		print('  3. Set maximum high voltage increase rate.');
		print('  4. Set maximum high voltage decrease rate.');
		print('  5. Turn on output.');
		print('  6. Turn off output.');
		print('  7. Show the version of the digital interface.');
		print('     But it seems not working now...');
		print('  8. Show the S/N of the power supply.');
		print('  9. Reset of the digital interface.');
		print('     All setup will be initialized.');
		print(' 10. Quit this script. Setup and operation of');
		print('     this machine will be maintained.');
		print(' 11. Quit this script with reset. Every setup');
		print('     Will be initialized and power supply will');
		print('     be switched to the local mode.');


################################################################################
#   Class definition of MotorControl                                           #
################################################################################
class MotorControl:
	#------------------------------------------------#
	#   Members                                      #
	#------------------------------------------------#
	# Commands
	__cmd_Init        =  0xAA;
	__cmd_MoveTo      =  0xC0;
	__cmd_ReadError   =  0xB3;
	__cmd_GetPosition =  0xA7;
	__cmd_Stop        =  0xFF;
	# Parameters
	__minSteps        =   140;
	__maxSteps        =  3610;
	# Error dictionary
	__errorDict = { 2 : ( 2,    'No Power Connected'),
	                4 : ( 4,    'Motor Driver Error'),
	                8 : ( 8,         'Input Invalid'),
	               16 : (16,    'Input Disconnected'),
	               32 : (32, 'Feedback Disconnected'),
	               64 : (64,  'Max. Current Exeeded')};
	# Etc
	__Is_Ready        = False;
	__serial          =     0;
	__port            =    '';
	rate              =  9600;
	accuracy          =     4;

	#------------------------------------------------#
	#   Initialize when constructed                  #
	#------------------------------------------------#
	def __init__(self, port):
		self.__port = port;

	#------------------------------------------------#
	#   Get whether it is ready or not               #
	#------------------------------------------------#
	def IsReady(self):
		return self.__Is_Ready;

	#------------------------------------------------#
	#   Get connection                               #
	#------------------------------------------------#
	def Connect(self):
		if not self.__Is_Ready:
			try:
				self.__serial = serial.Serial(self.__port, baudrate=self.rate, timeout=0.5, interCharTimeout=0.005);
				#init connection sending 0xAA
				self.__serial.write(serial.to_bytes([self.__cmd_Init]));
				self.__Is_Ready = True;
			except:
				self.__Is_Ready = False;
				print( 'Failed to Init PololuJRK on', self.__port, '(', sys.exc_info()[0] , ')');
				return (False, 'E0');
		return (True, '');

	#------------------------------------------------#
	#   Send command                                 #
	#------------------------------------------------#
	def __sendCommand(self, cmd, argument = []):
		if self.__Is_Ready:
			try:
				# Send command byte
				self.__serial.write(serial.to_bytes([cmd]));
				# If arguments, attach them
				for byte in argument:
					self.__serial.write(serial.to_bytes([byte]));
			except:
				self.__Is_Ready = False;
				print( 'error sending command:', hex(cmd), 'to', self.__port, '(', sys.exc_info()[0] , ')');
				return (False, 'E1');
		return (True, '');

	#------------------------------------------------#
	#   Read answer                                  #
	#------------------------------------------------#
	def __readAns(self, nBytes):
		# Read nBytes from serial port
		if self.__Is_Ready:
			try:
				ans = self.__serial.read(nBytes);
				return (True, ans);
			except:
				print( 'error reading from', self.__port, '(', sys.exc_info()[0] , ')');
				self.__Is_Ready = False;
				return (False, 'E1');

	#------------------------------------------------#
	#   Stop motor                                   #
	#------------------------------------------------#
	def MotorStop(self):
		if self.__Is_Ready:
			return self.__sendCommand(self.__cmd_Stop);

	#------------------------------------------------#
	#   move position to input value                 #
	#------------------------------------------------#
	def MoveTo(self, pos):
		if self.__Is_Ready and pos >= self.__minSteps and pos <=  self.__maxSteps:
			# the lower 5 bits are attached to the command byte
			cmd = self.__cmd_MoveTo + (pos & 0x1F);
			# the upper 7 bits are sent as the argument
			arg = [(pos >> 5) & 0x7F];
			ans = self.__sendCommand(cmd, arg);
		if not ans[0]: # error
			return ans;
		while True:
			time.sleep(1);
			currentPos = self.GetPosition();
			#print( currentPos);
			if not currentPos[0]: # error
				return currentPos;
			if currentPos[0] and abs(pos - currentPos[1]) <= self.accuracy:
				break;
		return self.MotorStop();

	#------------------------------------------------#
	#   Get current position                         #
	#------------------------------------------------#
	def GetPosition(self):
		if self.__Is_Ready:
			#request position
			self.__sendCommand(self.__cmd_GetPosition);
		#read answer
		ans = self.__readAns(2);
		# convert answer
		if ans[0]:
			#print( 'raw:', ans[1][0], ans[1][1] );
			if len(ans[1]):
				step = (ans[1][0] & 0xff) + ((ans[1][1] & 0xff) << 8);
#				return (True, (ans[1][0] & 0xff) +  ((ans[1][1] & 0xff) << 8));
				return (True, step, self.LinearCal(step));
			else:
				return (False, 'E4'); # connection lost?
		else:
			return (False, ans[1]);

	#------------------------------------------------#
	#   Let's go home                                #
	#------------------------------------------------#
	def GoHome(self):
		return self.MoveTo(self.__minSteps);

	#------------------------------------------------#
	#   Get status                                   #
	#------------------------------------------------#
	def Status(self):
		if self.__Is_Ready:
			#request status
			self.__sendCommand(self.__cmd_ReadError);
		# read answer
		ans = self.__readAns(2);
		if ( ans[0] ):
			#print( 'raw:', ans[1][0], ans[1][1]);
			statusMsg = (ans[1][0] & 0xff) +  ((ans[1][1] & 0xff) << 8);
			if ( statusMsg < 2 ):
				return(True, (0, 'Ready'));
			else:
				if statusMsg in self.__errorDict.keys():
					return (False, self.__errorDict[statusMsg]);
				else:
					return (False, (128, 'Serial Comunication Error'));
		else:
			return (False, (255, 'Serial Comunication Error'));

	#------------------------------------------------#
	#   Linear calibration                           #
	#------------------------------------------------#
	#   This method depends on calibration by real measurement.
	# According to my measurement...
	#   @  140 -> 349 mm + 191.5 mm + 493 mm + 275 mm = 1308.5 mm
	#   @ 3610 -> 480 mm + 191.5 mm + 493 mm + 275 mm = 1439.5 mm
	def LinearCal(self, step):
		pos = (1439.5-1308.5)/(3610.0-140.0)*(float(step)-140.0) + 1308.5;
		pos = round(pos, 1);
		return str(pos) + ' mm';

	#------------------------------------------------#
	#   Print welcome                                #
	#------------------------------------------------#
	def PrintWelcome(self):
		print('\x1b[1;33m================================================================\x1b[0m');
		print('\x1b[1;32m Python script for...\x1b[0m');
		print();
		print('\x1b[1;32m M   M  OOO  TTTTT  OOO  RRRR \x1b[0m');
		print('\x1b[1;32m MM MM O   O   T   O   O R   R\x1b[0m');
		print('\x1b[1;32m M M M O   O   T   O   O RRRR \x1b[0m');
		print('\x1b[1;32m M   M O   O   T   O   O R  R \x1b[0m');
		print('\x1b[1;32m M   M  OOO    T    OOO  R   R\x1b[0m');
		print();
		print('\x1b[1;32m                  CCC   OOO   N   N  TTTTT  RRRR    OOO   L      \x1b[0m');
		print('\x1b[1;32m                 C     O   O  NN  N    T    R   R  O   O  L      \x1b[0m');
		print('\x1b[1;32m                 C     O   O  N N N    T    RRRR   O   O  L      \x1b[0m');
		print('\x1b[1;32m                 C     O   O  N  NN    T    R  R   O   O  L      \x1b[0m');
		print('\x1b[1;32m                  CCC   OOO   N   N    T    R   R   OOO   LLLLL  \x1b[0m');
		print('\x1b[1;33m================================================================\x1b[0m');
		print('\x1b[1;31m Author:        Hoyong Jeong (hyjeong.hep.korea.ac.kr)\x1b[0m');
		print('\x1b[1;31m Available for: Pololu Jrk 21v3 USB Motor Controller\x1b[0m');
		print('\x1b[1;31m Applied to:    Concentric LACT6P-12V-20 Linear Actuator\x1b[0m');
		print('\x1b[0m\x1b[1;33m================================================================\x1b[0m');
		print('\x1b[1;34m - This is a script to control motor remotely.');
		print('\x1b[1;34m - It has been modified from the original version Fabian wrote.');
		print('\x1b[1;34m - Please choose number in menu.');
		print('\x1b[1;34m - Just hit enter to refresh.');
		print('\x1b[0m\x1b[1;33m================================================================\x1b[0m');

	#------------------------------------------------#
	#   Print status                                 #
	#------------------------------------------------#
	def PrintStatus(self):
		time.sleep(0.3);
		print(' ==============================================');
		print('  Machine status at', datetime.datetime.now());
		print(' ----------------------------------------------');
		print('  Motor status:    \x1b[1;36m', self.Status(), '\x1b[0m');
		print('  Current position:\x1b[1;36m', self.GetPosition(), '\x1b[0m');
		print(' ==============================================');

	#------------------------------------------------#
	#   Print menu                                   #
	#------------------------------------------------#
	def PrintMenu(self):
		print(' +----------+---------------------------------+');
		print(' | Menu No. | Description                     |');
		print(' +==========+=================================+');
		print(' |     0    | Details                         |');
		print(' |     1    | Move to                         |');
		print(' |     2    | Exit                            |');
		print(' |     3    | Exit with reset                 |');
		print(' +----------+---------------------------------+');
		menu = input(' Choose: ');
		return menu;

	#------------------------------------------------#
	#   Print description                            #
	#------------------------------------------------#
	def PrintDescription(self):
		print(' 0. Show this.');
		print(' 1. Set position to go as unit of step.');
		print('    Minimum: 140, Maximum: 3610');
		print('    Note: 26.5 step/mm');
		print(' 2. Quit this script. Current position will be');
		print('    maintained.');
		print(' 3. Quit this script with reset. Motor will be')
		print('    set to home position before quit.');
