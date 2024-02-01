# main.py

import machine
import time
import socket
import network as n
from machine import I2C
from machine import Pin
from machine import sleep
import mpu6050
import lsm303
import cred

port = 31111 #Server Port

wlan=None
s=None
i2c_1 = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
i2c_2 = I2C(scl=Pin(0), sda=Pin(2))       #initializing the I2C method for ESP8266
mpu1= mpu6050.accel(i2c_1)
mpu2= lsm303.accel(i2c_2)
arr=None
print("BEGIN INIT")


def connectWifi(ssid,passwd):
	global wlan
	print("CREATE WLAN")
	wlan=n.WLAN(n.STA_IF)
	print("WLAN ACTIVE")
	wlan.active(True)
	#Close the connection, make sure there is no connection, so as not to fail
	# wlan.disconnect()
	print("WLAN CONNECT")
	wlan.connect(ssid,passwd)
	while(wlan.ifconfig()[0]=='0.0.0.0'):
		time.sleep(1)
	return True

try:
	if(connectWifi(cred.SSID, cred.PASSWORD) == True):
		print("WLAN CONNECT DONE")
    	#Establish Socket connection
		s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	#Socket attributes
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    	#Get IP address
		ip=wlan.ifconfig()[0]
		print("UDP SERVER IP:", ip, ":", port)
		s.settimeout(None)
    	#Binding IP address
		s.bind((ip,port))

	print('Waiting...')
	while True:
		
		# arr = mpu.get_values()
		# s.send(arr)
		# time.sleep(1)
	
		data,addr=s.recvfrom(1024)
		print("rec data:",data," len:",len(data))
		#data[device id,command]
		if len(data) >= 2:
			# print(data[0]," ",b"1")
			if chr(data[0])=="1":
				if chr(data[1]) == "0":
					arr = mpu1.get_values()
					
					print("len",len(arr)," ",arr)
					s.sendto(arr,addr)
				else:
					print(mpu1.type)
					s.sendto(bytes(mpu1.type,'utf-8'),addr)	
			if chr(data[0])=="2":
				if chr(data[1]) == "0":
					# arr = mpu2.get_values()
					arr = mpu2.get_sfcp_message()
					print("len",len(arr)," ",arr)
					s.sendto(bytes(arr),addr)
				else:
					print(mpu2.type)
					s.sendto(bytes(mpu2.type,'utf-8'),addr)	
		# print('Received:',data,'From',addr)
		else:
			s.sendto(bytes('ERROR ','utf-8'),addr)#As is sent back
except Exception as ex:		
	print("EXCEPTION ", ex)
	if (s):
		s.close()
		wlan.disconnect()
		wlan.active(False)


