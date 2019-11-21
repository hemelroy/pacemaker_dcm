import serial 
import time
import sys
import matplotlib.pyplot as plt

ser = serial.Serial('COM5', baudrate=115200, timeout=1)


list_serialOut = [1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22]
#index 0: always 1
#index 1: 1 for transmit, 0 for receive
#index 2 through 20: programmable parameters
#index 21: always 22

#For direct testing
#apacewidth = 10, vpacewidth = 10, lowrateinterval = 1000, VRP = 320, ARP = 250, vcmpamp = 40, acmpamp = 40, apaceamp = 70, vpaceamp=70, 


lowrateinterval = 1000
list_serialOut[4] = int(lowrateinterval / 256)
list_serialOut[3] = int(lowrateinterval) - (list_serialOut[4] * 256)

vpaceamp = 70
list_serialOut[6] = int(vpaceamp / 256)
list_serialOut[5] = int(vpaceamp) - (list_serialOut[6] * 256)

vpacewidth = 10
list_serialOut[8] = int(vpacewidth / 256)
list_serialOut[7] = int(vpacewidth) - (list_serialOut[8] * 256)

vrp = 320
list_serialOut[10] = int(vrp / 256)
list_serialOut[9] = int(vrp) - (list_serialOut[10] * 256)

apaceamp=40
list_serialOut[12] = int(apaceamp / 256)
list_serialOut[11] = int(apaceamp) - (list_serialOut[12] * 256)

apacewidth=70
list_serialOut[14] = int(apacewidth / 256)
list_serialOut[13] = int(apacewidth) - (list_serialOut[14] * 256)

arp=250
list_serialOut[16] = int(arp / 256)
list_serialOut[15] = int(arp) - (list_serialOut[16] * 256)

for i in list_serialOut:
    ser.write(bytes([i]))
time.sleep(1)

ser.close()


# #EVEYTHING BELOW THIS IS EGRAM
# vEgram = []
# aEgram = []
# for x in range(10):  # Looping 10 times to obtain 10 distinct Data Points for E-GRAM Plots
#     list_serialIn = []
#     arr = []

#     arr.append(b'\x01')
#     arr.append(b'\x00')
#     for i in range(19):
#         arr.append(b'\x01')
#     arr.append(b'\x16')

#     # Requesting E-GRAM data values serially
#     for j in arr:
#         ser.write(j)

#     i = 1
#     while i:  # Reading Vent. and Atr. serial data

#         s = ser.read()
#         s = int.from_bytes(s, byteorder=sys.byteorder)
#         list_serialIn.append(s)

#         i += 1
#         if i > 22:
#             i = 0
#     time.sleep(0.5)

#     # Storing converting and storing Serial Data into appropriate arrays
#     vEgram.append((list_serialIn[17] + (list_serialIn[18] * 256)))
#     aEgram.append((list_serialIn[19] + (list_serialIn[20] * 256)))

# # Ploting Ventricle and Atrium Array Data Points
# plt.figure(1)
# plt.subplot(211)
# plt.ylabel("Vent. Egram")
# plt.plot(vEgram)

# plt.subplot(212)
# plt.ylabel("Atr. Egram")
# plt.plot(aEgram)
# plt.show()