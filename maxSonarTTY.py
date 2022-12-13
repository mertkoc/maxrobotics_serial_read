#!/usr/bin/python3
# Filename: maxSonarTTY.py

# Reads serial data from Maxbotix ultrasonic rangefinders
# Gracefully handles most common serial data glitches
# Use as an importable module with "import MaxSonarTTY"
# Returns an integer value representing distance to target in millimeters

from time import time
from time import sleep
from serial import Serial, SerialException
import os
# import pexpect.fdpexpect

# serialDevice = "/dev/ttyAMA0" # default for RaspberryPi
MAXWAIT = 2 # seconds to try for a good reading before quitting
# ser = Serial(serialDevice, 9600, 8, 'N', 1, timeout=1)

def measure(ser):

    # ser = Serial(portName, 9600, 8, 'N', 1, timeout=1)
    timeStart = time()
    valueCount = 0

    while time() < timeStart + MAXWAIT:
        if ser.inWaiting():
            bytesToRead = ser.inWaiting()
            valueCount += 1
            if valueCount < 2: # 1st reading may be partial number; throw it out
                continue
            testData = ser.read(bytesToRead)
            if not testData.startswith(b'R'):
                # data received did not start with R
                continue
            try:
                sensorData = testData.decode('utf-8').lstrip('R')
            except UnicodeDecodeError:
                # data received could not be decoded properly
                continue
            try:
                mm = int(sensorData)
            except ValueError:
                # value is not a number
                continue
            # ser.close()
            return(mm)

    # ser.close()
    raise RuntimeError("Expected serial data not received")

if __name__ == '__main__':
    # ser= Serial()
    port_name = "COM3"
    ser = Serial(port_name, 9600, 8, 'N', 1, timeout=1)
    # ser.baudrate = 9600
    # ser.port = "COM3"
    # ser.open()
    # for ns in range(4): 
    #     try:
    #         # ser = serial.Serial(0)  # open first serial port
    #         # print (ser.portstr)       # check which port was really used
    #         # ser.write("hello")      # write a string
    #         # ser.close()  
    #         ser.port=f"COM{ns}"
    #         ser.open()
    #         print (f"COM {ns+1} available")
    #         ser.close()
    #         measurement = measure(ser)
    #         print(measurement * 2.54)
    #         sleep(0.2)

    #     except SerialException:
    #         print (f"COM {ns+1} NOT available")


    while True:
        measurement = measure(ser)
        print(measurement * 2.54)
        sleep(0.2)