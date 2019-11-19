import serial 
import time

def serialTransmit(paramaters):
	list_serialOut = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22]
	for i in range (0: len(parameters)):
		if i == 0 or i ==1:
			parameters [i] = round(1/(paramaters [i]) * 60 *1000)
		list_serialOut[2+i] = paramaters [i]
		
	#index 0: always 1
	#index 1: 1 for transmit, 0 for receive
	#index 2 through 20: programmable parameters
	#index 21: always 22
	for i in list_serialOut:
		ser.write(bytes([i]))
	time.sleep(1)

ser = serial.Serial('COM5', baudrate=115200, timeout=1)
