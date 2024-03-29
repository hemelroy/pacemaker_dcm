from serial import Serial
import time
import sys
import matplotlib.pyplot as plt

#ser = Serial('COM7', baudrate=115200, timeout=1)


def serialTransmit(parameters, mode):
	tx_list = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29]

	tx_list[2] = mode + 1

	#print (parameters[2],type(parameters[2]))
	for i in range(0, len(parameters)):
		if i == 0 or i == 1 or i == 12:
			parameters [i] = round(1/(int(parameters [i])) * 60 *1000)
		if i == 2 or i == 4:
			parameters [i] = (round(float(parameters [i]),2) / 5.0) * 100
		if i == 10 or i == 11:
			parameters [i] = round(((parameters[0]-parameters[1])/parameters[i])/10)

	#print (tx_list)
	print ('Parameters:', parameters)
	#index 0: always 1
	#index 1: 1 for transmit, 0 for receive
	#index 2 through 23: programmable parameters
	#index 28: always 29
	

	tx_list[4] = int(int(parameters[0]) / 256)
	tx_list[3] = int(int(parameters[0])) - (tx_list[4] * 256)

	vpaceamp = 70
	tx_list[6] = int(int(parameters[2]) / 256)
	tx_list[5] = int(parameters[2]) - (tx_list[6] * 256)

	vpacewidth = 10
	tx_list[8] = int(int(parameters[3]) / 256)
	tx_list[7] = int(parameters[3]) - (tx_list[8] * 256)

	vrp = 320
	tx_list[10] = int(int(parameters[6]) / 256)
	tx_list[9] = int(int(parameters[6])) - (tx_list[10] * 256)

	apaceamp=40
	tx_list[12] = int(int(parameters[4]) / 256)
	tx_list[11] = int(parameters[4]) - (tx_list[12] * 256)

	apacewidth=70
	tx_list[14] = int(int(parameters[5]) / 256)
	tx_list[13] = int(parameters[5]) - (tx_list[14] * 256)

	arp=250
	tx_list[16] = int(int(parameters[7]) / 256)
	tx_list[15] = int(int(parameters[7])) - (tx_list[16] * 256)

	avDelay=100
	tx_list[18] = int(int(parameters[8]) / 256)
	tx_list[17] = int(int(parameters[8])) - (tx_list[18] * 256)
	
	#aThreshold=2
	#tx_list[20] = int(int(parameters[9]) / 256)
	#tx_list[19] = int(int(parameters[9])) - (tx_list[20] * 256)	
	tx_list[19] = int (parameters[9])
	
	#reactionTime = 7
	tx_list[22] = int(int(parameters[10]) / 256)
	tx_list[21] = int(int(parameters[10])) - (tx_list[22] * 256)
	
	#recoveryTime = 7
	tx_list[24] = int(int(parameters[11]) / 256)
	tx_list[23] = int(int(parameters[11])) - (tx_list[24] * 256)
	
	#uppRateInterval = 180
	tx_list[26] = int(int(parameters[1]) / 256)
	tx_list[25] = int(int(parameters[1])) - (tx_list[26] * 256)
	
	#msr = 180
	tx_list[28] = int(int(parameters[12]) / 256)
	tx_list[27] = int(int(parameters[12])) - (tx_list[28] * 256)
	
	print('Send:',tx_list)

	ser = Serial('COM7', baudrate=115200, timeout=1)
	for i in tx_list:
		ser.write(bytes([i]))
	time.sleep(2)
	ser.close()

def serialReceive():
	ser = Serial('COM7', baudrate=115200, timeout=1)
	vEgram = []
	aEgram = []
	for x in range(10):  # Looping 10 times to obtain 10 distinct Data Points for E-GRAM Plots
		list_serialIn = []
		arr = []

		arr.append(b'\x01')
		arr.append(b'\x00')
		for i in range(19):
			arr.append(b'\x01')
		arr.append(b'\x16')

		# Requesting E-GRAM data values serially
		for j in arr:
			ser.write(j)

		i = 1
		while i:  # Reading Vent. and Atr. serial data

			s = ser.read()
			s = int.from_bytes(s, byteorder=sys.byteorder)
			list_serialIn.append(s)

			i += 1
			if i > 22:
				i = 0
		time.sleep(0.5)

		# Storing converting and storing Serial Data into appropriate arrays
		vEgram.append((list_serialIn[15] + (list_serialIn[16] * 256)))
		aEgram.append((list_serialIn[17] + (list_serialIn[18] * 256)))

	
	# Ploting Ventricle and Atrium Array Data Points
	plt.figure(1)
	plt.subplot(211)
	plt.ylabel("Vent. Egram")
	plt.plot(vEgram)

	plt.subplot(212)
	plt.ylabel("Atr. Egram")
	plt.plot(aEgram)
	plt.show()
	time.sleep(2)

def serialTest():
	ser = Serial('COM7', baudrate=115200, timeout=1)