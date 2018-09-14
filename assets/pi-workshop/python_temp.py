#!/usr/bin/python

# Import modules
import os
import time
import glob

# Make sure our 1-Wire kernel modules are loaded
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Using glob to match wildcard devices
source = glob.glob("/sys/bus/w1/devices/28-*/w1_slave")

# Only pick the first device
for dir in source:
    temp_sensor = source[0]

# Get the raw data from the sensor
def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Turn the raw data into readable data
def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines = temp_raw()

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        # Convert the data to a float and add the decimal
        temp_c = float(temp_string) / 1000.0
        # Convert C to F
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        # Round to 2 decimal places
        temp_c = "{0:.2f}".format(temp_c)
        temp_f = "{0:.2f}".format(temp_f)
        # Convert the float to a string
        values = str(temp_c + " C " + temp_f + " F")
        return values

while True:
    # Run the read_temp() function and print its output
    print read_temp()
    time.sleep(1)