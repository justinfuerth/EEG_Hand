#EEGApp.py - Modified from EEGLogger.py
#Created by: Emotiv Sytems
#Modified by: Josh Chan, Justin Fuerth, Matthew Snell
#Last Modified: April 2nd, 2014
# python version >= 2.5
import ctypes
import sys
import os
import serial
import numpy as np
from ctypes import *
from numpy import *
import time
from ctypes.util import find_library
print ctypes.util.find_library('edk.dll')
print os.path.exists('.\\edk.dll')

libEDK = cdll.LoadLibrary(".\\edk.dll")

#refencing each channel by its integer value
ED_COUNTER = 0
ED_INTERPOLATED=1
ED_RAW_CQ=2
ED_AF3=3
ED_F7=4
ED_F3=5
ED_FC5=6
ED_T7=7
ED_P7=8
ED_O1=9
ED_O2=10
ED_P8=11
ED_T8=12
ED_FC6=13
ED_F4=14
ED_F8=15
ED_AF4=16
ED_GYROX=17
ED_GYROY=18
ED_TIMESTAMP=19
ED_ES_TIMESTAMP=20
ED_FUNC_ID=21
ED_FUNC_VALUE=22
ED_MARKER=23
ED_SYNC_SIGNAL=24

# IN DLL(edk.dll)
# typedef enum EE_DataChannels_enum {
# ED_COUNTER = 0, ED_INTERPOLATED, ED_RAW_CQ,
# ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,
# ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,
# ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX,
# ED_GYROY, ED_TIMESTAMP, ED_ES_TIMESTAMP,
# ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL
# } EE_DataChannel_t;

targetChannelList = [ED_COUNTER,ED_AF3, ED_F7, ED_F3,
ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2,
ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4,
ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID,
ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]

#header used to write to a .csv file
header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7',
'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8',
'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID',
'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
write = sys.stdout.write
eEvent = libEDK.EE_EmoEngineEventCreate()
eState = libEDK.EE_EmoStateCreate()
userID = c_uint(0)
nSamples = c_uint(0)
nSam = c_uint(0)
nSamplesTaken = pointer(nSamples)
da = zeros(128,double)
data = pointer(c_double(0))
user = pointer(userID)
composerPort = c_uint(1726)
secs = c_float(1)
datarate = c_uint(0)
readytocollect = False
option = c_int(0)
state = c_int(0)


#Code starts here
#Prompt User to press 1 to start the real-time application
input=''
print "===================================================="
print "Press '1' to start and connect to the EEGApp "
print ">> "
#------------------------------------------------------------
option = int(raw_input())
#defining channels as Lists. These act as the real-time windows for the EEG data
P8List = []
F7List = []
F8List = []
F4List = []
AF3List = []
#filling each list with start values of 0

for i in range(500):
	P8List.append(0)
	F7List.append(0)
	F8List.append(0)
	F4List.append(0)
	AF3List.append(0)
# Connecting to the Emotiv Headset
if option == 1:
	print libEDK.EE_EngineConnect("Emotiv Systems-5")
if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
	print "Emotiv Engine start up failed."
else :
	print "option = ?"

#Creates a data structure for the incomming EEG data and a buffer for the data to be stored temporarily
hData = libEDK.EE_DataCreate()
libEDK.EE_DataSetBufferSizeInSec(secs)

#Connecting to the Arduino
connected = False
ser = serial.Serial("COM4", 9600)

## loop until the arduino tells us it is ready
while not connected:
	serin = ser.read()
connected = True
print "Connected to arduino"

# This section loops infinitely until the user presses Ctrl+C to interrupt the program

while (1):
	#state is a one time variable that will pair the headset with the USB dongle for wireless communication
	state = libEDK.EE_EngineGetNextEvent(eEvent)
	
	#if state is 0, connect the headset to the USB Port and signal that data is ready to be collected
	if state == 0:
		eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
	libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
	if eventType == 16: #libEDK.EE_Event_enum.EE_UserAdded:
		print "User added"
		libEDK.EE_DataAcquisitionEnable(userID,True)
		readytocollect = True

	# Data collection happens here
	if readytocollect==True:

	#Update the data structure and see how many samples are on the buffer ready to be read in
	libEDK.EE_DataUpdateHandle(0, hData)
	libEDK.EE_DataGetNumberOfSample(hData,nSamplesTaken)

	#if there are samples on the buffer
	if nSamplesTaken[0] != 0:
		nSam=nSamplesTaken[0]
		
		#creates an array the size of the number of samples to be read for each channel
		arr=(ctypes.c_double*nSamplesTaken[0])()
		arr2=(ctypes.c_double*nSamplesTaken[0])()
		arr3=(ctypes.c_double*nSamplesTaken[0])()
		arr4=(ctypes.c_double*nSamplesTaken[0])()
		arr5=(ctypes.c_double*nSamplesTaken[0])()

	#iterates x times, where x is the number of samples to be read
	for sampleIdx in range(nSamplesTaken[0]):

	#reads the data from the buffer into the arrays, for each sample in each channel
		libEDK.EE_DataGet(hData,targetChannelList[9],byref(arr), nSam)
		libEDK.EE_DataGet(hData,targetChannelList[2],byref(arr2), nSam)
		libEDK.EE_DataGet(hData,targetChannelList[13],byref(arr3), nSam)
		libEDK.EE_DataGet(hData,targetChannelList[12],byref(arr4), nSam)
		libEDK.EE_DataGet(hData,targetChannelList[1],byref(arr5), nSam)

#for loop to throw out the oldest samples and add in the newest ones
		for i in range(len(arr)):
			P8List.pop(0)
			F7List.pop(0)
			F8List.pop(0)
			F4List.pop(0)
			AF3List.pop(0)
			P8List.append(arr[i])
			F7List.append(arr2[i])
			F8List.append(arr3[i])
			F4List.append(arr4[i])
			AF3List.append(arr5[i])
# calls the filter_signal function, defined at the bottom of this code
# the function takes the windows as an argument and returns the filtered data
# as an array
	signal = filter_signal(P8List)
	signal2 = filter_signal(F7List)
	signal3 = filter_signal(F8List)
	signal4 = filter_signal(F4List)
	signal5 = filter_signal(AF3List)

#for each sample in the window, check if the AF3 and F7 channels go above the threshold and
#if the P8 channel stays below the threshold
	for i in range(len(signal)):
		if signal2[i] > 100 and signal5[i] > 100 and signal[i] < 100:
	
			#if these conditions passed, count it as a blink
			print signal3[i]
			print "you blinked!"
			#if there is a message on the buffer, the arduino is currently in the ready state
			#and we can send an actuation command to the arduino
		if (ser.inWaiting() > 0):
			print ser.read(size=1)
			ser.write('1')
#if there is nothing in the serial buffer, the arduino is currently actuating the hand
#this means that this threshold value has already been counted and we do not need to send another
#actuation command
		else:
			print "Arduino is busy!"

	time.sleep(0.2)

#free the data structures from memory
libEDK.EE_DataFree(hData)

#exiting the program cleanly
libEDK.EE_EngineDisconnect()
libEDK.EE_EmoStateFree(eState)
libEDK.EE_EmoEngineEventFree(eEvent)

#------------------------------------------------------------------------------------------------------------------------------
#function: filter_signal
#
#preconditions: takes in a List as an argument.Assumes that the list is full of floating point numbers
#postconditions: returns an array filled with floating point numbers
#
#description: converts a window into the frequency domain, and cuts off any samples that have a frequency
#of 0.15 Hz or lower. Then converts this cut signal back into time domain and returns it to the calling
#function. This effectively removes the DC bias from the samples and gives a true 0 to the window.

def filter_signal(mylist):
	signal = np.asarray(mylist)
	W = fftfreq(signal.size, 0.0078)
	f_signal = rfft(signal)
	cut_f_signal = f_signal.copy()
	cut_f_signal[(W<0.16)] = 0
	#cut_f_signal[(W>30)] = 0
	cut_signal = irfft(cut_f_signal)
return cut_signal