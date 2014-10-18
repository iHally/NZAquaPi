#!/usr/bin/env python

import sqlite3
import os
import time
import datetime
import glob
import sys
import decimal
import smtplib
import spidev
import RPi.GPIO as GPIO
import logging
import dhtreader

spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT) #LED 1
GPIO.setup(12, GPIO.OUT) #MOSFET 1
GPIO.setup(13, GPIO.OUT) #MOSFET 2
GPIO.setup(15, GPIO.OUT) #MOSFET 3
GPIO.setup(16, GPIO.OUT) #MOSFET 4
GPIO.setup(18, GPIO.OUT) #MOSFET 5
GPIO.setup(22, GPIO.OUT) #MOSFET 6
GPIO.setup(11, GPIO.OUT) #MOSFET 7

# global variables
speriod=(15*60)-1
dbname='/var/www/NZAquaPi.db'
AWC_completed = 0 
OldHr = 69
etape_channel = 1
SleepTime_ATO_AWC = 900
SleepTime_Sensors = 3600
SleepTime_MOSFET_Override = 15
eTapeReadTime = 5.0

#TEMPVAR
DoubleRunning = 1

#ATO DETAILS:
ATO_FIRST = 1000
#360mm - 1040
ATO_0 = 1067
#350mm - 1095 - MAX
ATO_1 = 1135
#340mm - 1175
ATO_2 = 1203
#330mm - 1230
ATO_3 = 1250
#320mm - 1270
ATO_4 = 1295
#310mm - 1320
ATO_5 = 1350
#300mm - 1380
ATO_6 = 1410
#290mm - 1440
ATO_7 = 1463
#280mm - 1487
ATO_8 = 1510
#270mm - 1535
ATO_9 = 1565
#260mm - 1595
ATO_10 = 1625
#250mm - 1653
ATO_11 = 1675
#240mm - 1695
ATO_12 = 1717
#230mm - 1740
ATO_13 = 1767
#220mm - 1795
ATO_14 = 1823
#210mm - 1850
ATO_15 = 1867
#200mm - 1883
ATO_16 = 1910
#190mm - 1937 - MIN
ATO_LAST = 2000

"""
FREQUENCY OPTIONS:

1. Once Daily
2. Alt Daily
3. Twice Weekly (Mon/Thurs)
4. Monday
5. Tuesday
6. Wednesday
7. Thursday
8. Friday
9. Saturday
10. Sunday

TIME OPTIONS ARE IN 24HR TIME, ON THE HOUR
"""

#setup logging
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/tmp/nzaquapi.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
logger.info("Daemon Loaded")

def Read_eTape(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def eTape_read_loop():
	count = 0
	temp_level = 0
	while count <= eTapeReadTime:
		etape_level = Read_eTape(etape_channel)
		etape_level = (1023.0 / etape_level) - 1
		etape_level = 560.0 / etape_level
		count = count + 1
		if count == eTapeReadTime:
			etape_level = round((etape_level + temp_level) / eTapeReadTime, 2)
			return etape_level
		else:
			temp_level = temp_level + etape_level
		time.sleep(1)

def Convert_Ohms(Ohms):
	if Ohms < ATO_FIRST:
		mm = 600
	elif Ohms >= ATO_FIRST and Ohms < ATO_0:
		mm = 360
	elif Ohms >= ATO_0 and Ohms < ATO_1:
		mm = 350
	elif Ohms >= ATO_1 and Ohms < ATO_2:
		mm = 340
	elif Ohms >= ATO_2 and Ohms < ATO_3:
		mm = 330
	elif Ohms >= ATO_3 and Ohms < ATO_4:
		mm = 320
	elif Ohms >= ATO_4 and Ohms < ATO_5:
		mm = 310
	elif Ohms >= ATO_5 and Ohms < ATO_6:
		mm = 300
	elif Ohms >= ATO_6 and Ohms < ATO_7:
		mm = 290
	elif Ohms >= ATO_7 and Ohms < ATO_8:
		mm = 280
	elif Ohms >= ATO_8 and Ohms < ATO_9:
		mm = 270
	elif Ohms >= ATO_9 and Ohms < ATO_10:
		mm = 260
	elif Ohms >= ATO_10 and Ohms < ATO_11:
		mm = 250
	elif Ohms >= ATO_11 and Ohms < ATO_12:
		mm = 240
	elif Ohms >= ATO_12 and Ohms < ATO_13:
		mm = 230	
	elif Ohms >= ATO_13 and Ohms < ATO_14:
		mm = 220	
	elif Ohms >= ATO_14 and Ohms < ATO_15:
		mm = 210	
	elif Ohms >= ATO_15 and Ohms < ATO_16:
		mm = 200	
	elif Ohms >= ATO_16 and Ohms < ATO_LAST:
		mm = 190
	else:
		mm = 1
	return mm

# Will read temp sensors now
def read_temp_sensors():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    # search for the number of device files that starts with 28
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if devicelist=='':
        return None
        logger.error("Haven't found any temp sensors???")
        print "Haven't found any???"
    else:
        TempSensorsFound = 0
        TempSensorsFound = len(devicelist)
        TempsActive = 0
        if Temp_Display_Status == "ENABLED":
            TempsActive = TempsActive + 1
        if Temp_Sump_Status == "ENABLED":
            TempsActive = TempsActive + 1
        if Temp_LDock_Status == "ENABLED":
            TempsActive = TempsActive + 1
        if Temp_RDock_Status == "ENABLED":
            TempsActive = TempsActive + 1
        if TempsActive > TempSensorsFound:
            logger.error("At least one temp sensor has not been found, check your connections...")
            print "At least one temp sensor has not been found, check your connections..."
        else:
            if Temp_Display_Status == "ENABLED":
                w1devicefile = '/sys/bus/w1/devices/' + Temp_Display_id + '/w1_slave'
                i = 1
                while i <= 5:
                    temperature = get_temp(w1devicefile)
                    if temperature != None:
                        print "Display Temperature = " + str(round(temperature, 2)) + "*c"
                        i = 6
                    else:
                        # Sometimes reads fail on the first attempt
                        # so we need to retry
                        time.sleep(1)
                        i = i + 1
                        if i == 6:
                            logger.error("Could not read Temp_Display sensor after 5 attempts")
                global temp_display
                temp_display = round(temperature,2)
            if Temp_Sump_Status == "ENABLED":
                w1devicefile = '/sys/bus/w1/devices/' + Temp_Sump_id + '/w1_slave'
                i = 1
                while i <= 5:
                    temperature = get_temp(w1devicefile)
                    if temperature != None:
                        print "Sump Temperature = " + str(round(temperature, 2)) + "*c"
                        i = 6
                    else:
                        # Sometimes reads fail on the first attempt
                        # so we need to retry
                        time.sleep(1)
                        i = i + 1
                        if i == 6:
                            logger.error("Could not read Temp_Sump sensor after 5 attempts")
                global temp_sump
                temp_sump = round(temperature,2)
            if Temp_LDock_Status == "ENABLED":
                w1devicefile = '/sys/bus/w1/devices/' + Temp_LDock_id + '/w1_slave'
                i = 1
                while i <= 5:
                    temperature = get_temp(w1devicefile)
                    if temperature != None:
                        print "Left Dock Temperature = " + str(round(temperature, 2)) + "*c"
                        i = 6
                    else:
                        # Sometimes reads fail on the first attempt
                        # so we need to retry
                        time.sleep(1)
                        i = i + 1
                        if i == 6:
                            logger.error("Could not read Temp_LDock sensor after 5 attempts")
                global temp_ldock
                temp_ldock = round(temperature,2)
            if Temp_RDock_Status == "ENABLED":
                w1devicefile = '/sys/bus/w1/devices/' + Temp_RDock_id + '/w1_slave'
                i = 1
                while i <= 5:
                    temperature = get_temp(w1devicefile)
                    if temperature != None:
                        print "Right Dock Temperature = " + str(round(temperature, 2)) + "*c"
                        i = 6
                    else:
                        # Sometimes reads fail on the first attempt
                        # so we need to retry
                        time.sleep(1)
                        i = i + 1
                        if i == 6:
                            logger.error("Could not read Temp_RDock sensor after 5 attempts")
                global temp_rdock
                temp_rdock = round(temperature,2)
       
# gets temerature values - used in read_temp_sensors module
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1 
    status = lines[0][-4:-1]

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        return tempvalue
    else:
        return None
       
# Will read humidity sensors now
def read_humidity_sensors():
    dhtreader.init()
    Attempts = 0
    while True:
        try:
            t, h = dhtreader.read(22, 2)
            break
        except TypeError:
            print "Failed to read from sensor on pin 3 (GPIO 2), trying again..."
            time.sleep(3)
            Attempts = Attempts + 1
            if Attempts > 5:
                logger.error("Could not read Hood Humidity sensor after 5 attempts")
                break
    if t and h:
        print("Hood Temp = {0}*c, Hood RH = {1}%".format(round(t, 2), round(h, 2)))
        global rhtemp_hood, rh_hood
        rhtemp_hood = round(t,2)
        rh_hood = round(h,2)
    else:
        print("Failed to read from sensor.")
    
    Attempts = 0
    while True:
        try:
            t, h = dhtreader.read(22, 3)
            break
        except TypeError:
            print "Failed to read from sensor on pin 5 (GPIO 3), trying again..."
            time.sleep(3)
            Attempts = Attempts + 1
            if Attempts > 5:
                logger.error("Could not read Cabinet Humidity sensor after 5 attempts")
                break
    if t and h:
        print("Cabinet Temp = {0}*c, Cabinet RH = {1}%".format(round(t, 2), round(h, 2)))
        time.sleep(2)
        global rhtemp_cabinet, rh_cabinet
        rhtemp_cabinet = round(t,2)
        rh_cabinet = round(h,2)
    else:
        print("Failed to read from sensor.")    

# Read light sensor
def read_analogs():
    spi = spidev.SpiDev()
    spi.open(0,0)
    
    ReadTime_PhotoCell = 10.0
    ReadTime_eTape = eTapeReadTime
    
    # set channel for light sensor and read channel
    print("Measuring light levels for {} seconds for an accurate reading...".format(ReadTime_PhotoCell))
    channel = 0 
    count = 0
    global PhotoCell
    PhotoCell = 0
    while count <= ReadTime_PhotoCell:
        count = count + 1
        adc = spi.xfer2([1,(8+channel)<<4,0])
        PhotoCell_temp = ((adc[1]&3) << 8) + adc[2]
        if count == ReadTime_PhotoCell:
            PhotoCell = (PhotoCell + PhotoCell_temp) / ReadTime_PhotoCell
            print("PhotoCell: {}".format(PhotoCell))
            count = ReadTime_PhotoCell + 1
        else:
            PhotoCell = PhotoCell + PhotoCell_temp
            time.sleep(1)
        
    # set channel for etape and read channel
    print("Measuring eTape levels for {} seconds for an accurate reading...".format(ReadTime_eTape))
    global sump_level
    channel = 1 
    count = 0
    temp_level = 0
    while count <= ReadTime_eTape:
        adc = spi.xfer2([1,(8+channel)<<4,0])
        etape_level = ((adc[1]&3) << 8) + adc[2]
        etape_level = (1023.0 / etape_level) - 1
        etape_level = 560.0 / etape_level
        count = count + 1
        if count == ReadTime_eTape:
            etape_level = round((etape_level + temp_level) / ReadTime_eTape, 2)
            sump_level = Convert_Ohms(etape_level)
            print("Sump Level: {}mm".format(sump_level))
            count = ReadTime_eTape + 1
        else:
            temp_level = temp_level + etape_level
        time.sleep(1)

# Check the temperatures to ensure they are in correct ranges, activates/deactivates fans/heaters/alarms as needed
def check_temps():
    
    WaterFans = 2 #for if not changed to either 0 or 1
    #HoodWaterFan = 2 #for if not changed to either 0 or 1
    HoodExhaustFan = 2 #for if not changed to either 0 or 1
    CabinetFans = 2 #for if not changed to either 0 or 1
    LHoodWaterFan = 2 #for if not changed to either 0 or 1
    RHoodWaterFan = 2 #for if not changed to either 0 or 1
    RHHoodWaterFan = 2 #for if not changed to either 0 or 1
    TEMP_HoodExhaustFan = 2
    
    OkToTurnOff = 0
    if Temp_Display_Status == "ENABLED":
        if temp_display >= Temp_Display_Fan_ON and Temp_Display_Fan_Status == "ENABLED":
            WaterFans = 1
        if temp_display >= Temp_Display_Max and Temp_Display_High_Alarm == "ON":
            # work out if alarm already been sent somehow, if not send alarm
            print("ALARM - DISPLAY TEMP HIGH (Recorded Temp: {0}, High Alarm Set: {1})".format(temp_display, Temp_Display_Max))
        if temp_display < Temp_Display_Fan_OFF and Temp_Display_Fan_Status == "ENABLED":
            WaterFans = 0
            OkToTurnOff = 1
        if temp_display < Temp_Display_Min and Temp_Display_Low_Alarm == "ON":
            # work out if alarm already been sent somehow, if not send alarm
            print("ALARM - DISPLAY TEMP LOW (Recorded Temp: {0}, Low Alarm Set: {1})".format(temp_display, Temp_Display_Min))
            
    if Temp_Sump_Status == "ENABLED":
        if temp_sump >= Temp_Sump_Fan_ON and Temp_Sump_Fan_Status == "ENABLED":
            WaterFans = 1
        if temp_sump >= Temp_Sump_Max and Temp_Sump_High_Alarm == "ON":
            print("ALARM - SUMP TEMP HIGH (Recorded Temp: {0}, High Alarm Set: {1})".format(temp_sump, Temp_Sump_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if temp_sump < Temp_Sump_Fan_OFF and Temp_Sump_Fan_Status == "ENABLED" and OkToTurnOff == 1:
            WaterFans = 0
        if temp_sump < Temp_Sump_Min and Temp_Sump_Low_Alarm == "ON":
            print("ALARM - DISPLAY TEMP LOW (Recorded Temp: {0}, Low Alarm Set: {1})".format(sump_display, Temp_Sump_Min))
            # work out if alarm already been sent somehow, if not send alarm
            
    if Temp_LDock_Status == "ENABLED":
        if temp_ldock >= Temp_LDock_Fan_ON and Temp_LDock_Fan_Status == "ENABLED":
            #LHoodWaterFan = 1
            HoodExhaustFan = 1
        if temp_ldock >= Temp_LDock_Max and Temp_LDock_High_Alarm == "ON":
            print("ALARM - LEFT DOCK TEMP HIGH (Recorded Temp: {0}, High Alarm Set: {1})".format(temp_ldock, Temp_LDock_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if temp_ldock < Temp_LDock_Fan_OFF and Temp_LDock_Fan_Status == "ENABLED":
            LHoodWaterFan = 0
            
    if Temp_RDock_Status == "ENABLED":
        if temp_rdock >= Temp_RDock_Fan_ON and Temp_RDock_Fan_Status == "ENABLED":
            #RHoodWaterFan = 1
            HoodExhaustFan = 1
        if temp_rdock >= Temp_LDock_Max and Temp_LDock_High_Alarm == "ON":
            print("ALARM - RIGHT DOCK TEMP HIGH (Recorded Temp: {0}, High Alarm Set: {1})".format(temp_rdock, Temp_RDock_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if temp_rdock < Temp_RDock_Fan_OFF and Temp_RDock_Fan_Status == "ENABLED":
            RHoodWaterFan = 0

    if RH_Hood_Status == "ENABLED":
        if rhtemp_hood >= RH_Hood_Temp_Fan_ON and RH_Hood_Temp_Fan_Status == "ENABLED":
            #RHHoodWaterFan = 1
            HoodExhaustFan = 1
        if rhtemp_hood >= RH_Hood_Temp_Max and RH_Hood_High_Alarm == "ON":
            print("ALARM - HOOD TEMP HIGH (Recorded Temp: {0}, High Alarm Set: {1})".format(rhtemp_hood, RH_Hood_Temp_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if rhtemp_hood < RH_Hood_Temp_Fan_OFF and RH_Hood_Temp_Fan_Status == "ENABLED":
            RHHoodWaterFan = 0
        if rh_hood >= RH_Hood_Fan_ON and RH_Hood_Fan_Status == "ENABLED":
            HoodExhaustFan = 1
        if rh_hood >= RH_Hood_Max and RH_Hood_High_Alarm == "ON":
            print("ALARM - HOOD RELATIVE HUMIDITY HIGH (Recorded RH: {0}, High Alarm Set: {1})".format(rh_hood, RH_Hood_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if rh_hood < RH_Hood_Fan_OFF and RH_Hood_Fan_Status == "ENABLED":
            TEMP_HoodExhaustFan = 0
            
    #if LHoodWaterFan == 1 or RHoodWaterFan == 1 or RHHoodWaterFan == 1:
    #    HoodWaterFan = 1
    #elif LHoodWaterFan == 0 and RHoodWaterFan == 0 and RHHoodWaterFan == 0:
    if LHoodWaterFan == 0 and RHoodWaterFan == 0 and RHHoodWaterFan == 0 and TEMP_HoodExhaustFan == 0:
        #HoodWaterFan = 0
        HoodExhaustFan = 0
        
    OkToTurnCabFanOff = 1
    if RH_Cabinet_Status == "ENABLED":
        if rhtemp_cabinet >= RH_Cabinet_Temp_Fan_ON and RH_Cabinet_Temp_Fan_Status == "ENABLED":
            CabinetFans = 1
            OkToTurnCabFanOff = 0
        if rhtemp_cabinet >= RH_Cabinet_Temp_Max and RH_Cabinet_High_Alarm == "ON":
            print("ALARM - CABINET TEMP HIGH (Recorded Temp: {0}, High Alarm Set: {1})".format(rhtemp_cabinet, RH_Cabinet_Temp_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if rhtemp_cabinet < RH_Cabinet_Temp_Fan_OFF and RH_Cabinet_Temp_Fan_Status == "ENABLED":
            CabinetFans = 0
        if rh_cabinet >= RH_Cabinet_Fan_ON and RH_Cabinet_Fan_Status == "ENABLED":
            CabinetFans = 1
        if rh_cabinet >= RH_Cabinet_Max and RH_Cabinet_High_Alarm == "ON":
            print("ALARM - CABINET RELATIVE HUMIDITY HIGH (Recorded RH: {0}, High Alarm Set: {1})".format(rh_cabinet, RH_Cabinet_Max))
            # work out if alarm already been sent somehow, if not send alarm
        if rh_cabinet < RH_Cabinet_Fan_OFF and RH_Cabinet_Fan_Status == "ENABLED" and OkToTurnCabFanOff == 1:
            CabinetFans = 0

    #time.sleep(2)
    
    #OLD CONFIG:    
    #MOSFET 1 (GPIO Pin 12) = hood fans
    #MOSFET 2 (GPIO Pin 13) = hood exhaust fans
    #MOSFET 3 (GPIO Pin 15) = cabinet exhaust fans
    #MOSFET 4 (GPIO Pin 16) = sump fan
    
    #NEW CONFIG:
    #MOSFET 1 (GPIO Pin 12) = sump fan
    #MOSFET 2 (GPIO Pin 13) = hood exhaust fans
    #MOSFET 3 (GPIO Pin 15) = hood fans
    #MOSFET 4 (GPIO Pin 16) = cabinet exhaust fans
    
    if WaterFans == 1:
        #turn on mosfet 1, 2 and 3
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.HIGH)
        os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet1_status.jpg")
        os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet2_status.jpg")
        os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet3_status.jpg")
    elif WaterFans == 0:
        #turn off mosfet 1
        GPIO.output(12, GPIO.LOW)
        os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet1_status.jpg")
        #if HoodWaterFan == 1:
            #turn on mosfet 2, 3
            #GPIO.output(13, GPIO.HIGH)
            #GPIO.output(15, GPIO.HIGH)
            #os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet2_status.jpg")
            #os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet3_status.jpg")
        #elif HoodWaterFan == 0:
        
        #turn off mosfet 3
        GPIO.output(15, GPIO.LOW)
        os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet3_status.jpg")	
        
    if HoodExhaustFan == 1:
        #turn on mosfet 2
        GPIO.output(13, GPIO.HIGH)
        os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet2_status.jpg")
    elif HoodExhaustFan == 0:
		print "should now see this...."
		#turn off mosfet 2
		GPIO.output(13, GPIO.LOW)
		os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet2_status.jpg")
    
    if CabinetFans == 1:
        #turn on mosfet 4
        GPIO.output(16, GPIO.HIGH)
        os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet4_status.jpg")
    elif CabinetFans == 0:
        #turn off mosfet 4
        GPIO.output(16, GPIO.LOW)
        os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet4_status.jpg")
    
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()    
    Attempts = 0
    while True:
        try:
            curs.execute("UPDATE MOSFET_Status SET MOSFET1_Status=?, MOSFET2_Status=?, MOSFET3_Status=?, MOSFET4_Status=?", (GPIO.input(12), GPIO.input(13), GPIO.input(15), GPIO.input(16)))
            conn.commit()
            break 
        except:
            Attempts = Attempts + 1
            time.sleep(2)  
            if Attempts == 5:
                logger.error("Could not write to database after 5 attempts")
                break
    conn.close

    print "  "
    print "Fan MIN/MAX Settings:"
    print("Display Fan On: {0}, Display Fan Off: {1}".format(Temp_Display_Fan_ON, Temp_Display_Fan_OFF))
    print("Sump Fan On: {0}, Sump Fan Off: {1}".format(Temp_Sump_Fan_ON, Temp_Sump_Fan_OFF))
    print("LDock Fan On: {0}, LDock Fan Off: {1}".format(Temp_LDock_Fan_ON, Temp_LDock_Fan_OFF))
    print("RDock Fan On: {0}, RDock Fan Off: {1}".format(Temp_RDock_Fan_ON, Temp_RDock_Fan_OFF))
    print("RH Cabinet Fan On: {0}, RH Cabinet Fan Off: {1}".format(RH_Cabinet_Fan_ON, RH_Cabinet_Fan_OFF))
    print("RH Cabinet Temp Fan On: {0}, RH Cabinet Temp Fan Off: {1}".format(RH_Cabinet_Temp_Fan_ON, RH_Cabinet_Temp_Fan_OFF))
    print("RH Hood Fan On: {0}, RH Hood Fan Off: {1}".format(RH_Hood_Fan_ON, RH_Hood_Fan_OFF))
    print("RH Hood Temp Fan On: {0}, RH Hood Temp Fan Off: {1}".format(RH_Hood_Temp_Fan_ON, RH_Hood_Temp_Fan_OFF))

    print " "
    print "Variable Values: (0 = OFF, 1 = ON, 2 = NO CHANGE)"
    print "WaterFans: " + str(WaterFans) 
    #print "HoodWaterFan: " + str(HoodWaterFan)
    print "HoodExhaustFan: " + str(HoodExhaustFan)
    print "CabinetFans: " + str(CabinetFans)

    print "   "
    print "Fan Status:"
    status = GPIO.input(12)
    print "SUMP FANS (GPIO Pin 12): " + str(status)
    status = GPIO.input(13)
    print "HOOD EXHAUST FANS (GPIO Pin 13): " + str(status)
    status = GPIO.input(15)
    print "HOOD FANS (GPIO Pin 15): " + str(status)
    status = GPIO.input(16)
    print "CABINET EXHAUST FANS (GPIO Pin 16): " + str(status)
    
# store the temperatures in the database
def log_data():

    print "Writing data into DB..."

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    Attempts = 0
    CurrentDateTime = datetime.datetime.now()
    while True:
        try:
            #curs.execute("INSERT INTO Sensors_Log VALUES(strftime('%d-%m-%Y, %H:%M', 'now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (temp_display, temp_sump, temp_ldock, temp_rdock, rh_hood, rhtemp_hood, rh_cabinet, rhtemp_cabinet, PhotoCell, sump_level))
            curs.execute("INSERT INTO Sensors_Log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (CurrentDateTime, temp_display, temp_sump, temp_ldock, temp_rdock, rh_hood, rhtemp_hood, rh_cabinet, rhtemp_cabinet, PhotoCell, sump_level))
            conn.commit()
            break 
        except:
            Attempts = Attempts + 1
            time.sleep(2)  
            if Attempts == 5:
                logger.error("Could not write to database after 5 attempts")
                break
    conn.close
    print "Data logged into DB"

def load_DB_ATO_AWC():
	global ATO_on, ATO_opt_level, ATO_drp, ATO_maxtime, ATO_min, AWC_on, AWC_method, AWC_remove_amt, AWC_remove_time, AWC_add_time, AWC_freq, AWC_time, Send_Email, AWC_Next_Day
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT Status, Optimal_Level, Triggered_Drop, Max_Time, Sump_Min FROM ATO")
	for row in curs:
		ATO_on = row[0]
		ATO_opt_level = row[1]
		ATO_drp = row[2]
		ATO_maxtime = row[3]
		ATO_min = row[4]
	curs.execute("SELECT Status, Method, Remove_Amount, Remove_Time, Add_Time, Frequency, Frequency_Time, Email_Confirmation, Frequency_Next_Day FROM AWC")
	for row in curs:
		AWC_on = row[0]
		AWC_method = row[1]
		AWC_remove_amt = row[2]
		AWC_remove_time = row[3]
		AWC_add_time = row[4]
		AWC_freq = row[5]
		AWC_time = row[6]
		Send_Email = row[7]
		AWC_Next_Day = row[8]
	conn.close

def load_DB_Override_State():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT Override_State FROM MOSFET_Status")
	for row in curs:
		Override_State = row[0]
	conn.close
	return Override_State

def load_DB_Sensors():
# import DB settings
	global Temp_Display_id, Temp_Display_Min, Temp_Display_Max, Temp_Display_Heater_ON, Temp_Display_Heater_OFF, Temp_Display_Fan_ON, Temp_Display_Fan_OFF, Temp_Display_Status, Temp_Display_Low_Alarm, Temp_Display_Low_Time, Temp_Display_High_Alarm, Temp_Display_High_Time, Temp_Display_Heater_Status, Temp_Display_Fan_Status
	global Temp_Sump_id, Temp_Sump_Min, Temp_Sump_Max, Temp_Sump_Heater_ON, Temp_Sump_Heater_OFF, Temp_Sump_Fan_ON, Temp_Sump_Fan_OFF, Temp_Sump_Status, Temp_Sump_Low_Alarm, Temp_Sump_Low_Time, Temp_Sump_High_Alarm, Temp_Sump_High_Time, Temp_Sump_Heater_Status, Temp_Sump_Fan_Status
	global Temp_LDock_id, Temp_LDock_Max, Temp_LDock_Fan_ON, Temp_LDock_Fan_OFF, Temp_LDock_Status, Temp_LDock_High_Alarm, Temp_LDock_High_Time, Temp_LDock_Fan_Status
	global Temp_RDock_id, Temp_RDock_Max, Temp_RDock_Fan_ON, Temp_RDock_Fan_OFF, Temp_RDock_Status, Temp_RDock_High_Alarm, Temp_RDock_High_Time, Temp_RDock_Fan_Status
	global RH_Hood_id, RH_Hood_Max, RH_Hood_Fan_ON, RH_Hood_Fan_OFF, RH_Hood_Status, RH_Hood_High_Alarm, RH_Hood_High_Time, RH_Hood_Temp_Max, RH_Hood_Temp_Fan_ON, RH_Hood_Temp_Fan_OFF, RH_Hood_Temp_High_Alarm, RH_Hood_Temp_High_Time, RH_Hood_Fan_Status, RH_Hood_Temp_Fan_Status
	global RH_Cabinet_id, RH_Cabinet_Max, RH_Cabinet_Fan_ON, RH_Cabinet_Fan_OFF, RH_Cabinet_Status, RH_Cabinet_High_Alarm, RH_Cabinet_High_Time, RH_Cabinet_Temp_Max, RH_Cabinet_Temp_Fan_ON, RH_Cabinet_Temp_Fan_OFF, RH_Cabinet_Temp_High_Alarm, RH_Cabinet_Temp_High_Time, RH_Cabinet_Fan_Status, RH_Cabinet_Temp_Fan_Status
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT id, Min, Max, Heater_ON, Heater_OFF, Fan_ON, Fan_OFF, Status, Low_Alarm, Low_Time, High_Alarm, High_Time, Heater_Status, Fan_Status FROM Temp_Display")
	for row in curs:
		Temp_Display_id = row[0]
		Temp_Display_Min = row[1]
		Temp_Display_Max = row[2]
		Temp_Display_Heater_ON = row[3]
		Temp_Display_Heater_OFF = row[4]
		Temp_Display_Fan_ON = row[5]
		Temp_Display_Fan_OFF = row[6]
		Temp_Display_Status = row[7]
		Temp_Display_Low_Alarm = row[8]
		Temp_Display_Low_Time = row[9]
		Temp_Display_High_Alarm = row[10]
		Temp_Display_High_Time = row[11]
		Temp_Display_Heater_Status = row[12]
		Temp_Display_Fan_Status = row[13]
	curs.execute("SELECT id, Min, Max, Heater_ON, Heater_OFF, Fan_ON, Fan_OFF, Status, Low_Alarm, Low_Time, High_Alarm, High_Time, Heater_Status, Fan_Status FROM Temp_Sump")
	for row in curs:
		Temp_Sump_id = row[0]
		Temp_Sump_Min = row[1]
		Temp_Sump_Max = row[2]
		Temp_Sump_Heater_ON = row[3]
		Temp_Sump_Heater_OFF = row[4]
		Temp_Sump_Fan_ON = row[5]
		Temp_Sump_Fan_OFF = row[6]
		Temp_Sump_Status = row[7]
		Temp_Sump_Low_Alarm = row[8]
		Temp_Sump_Low_Time = row[9]
		Temp_Sump_High_Alarm = row[10]
		Temp_Sump_High_Time = row[11]
		Temp_Sump_Heater_Status = row[12]
		Temp_Sump_Fan_Status = row[13]
	curs.execute("SELECT id, Max, Fan_ON, Fan_OFF, Status, High_Alarm, High_Time, Fan_Status FROM Temp_LDock")
	for row in curs:
		Temp_LDock_id = row[0]
		Temp_LDock_Max = row[1]
		Temp_LDock_Fan_ON = row[2]
		Temp_LDock_Fan_OFF = row[3]
		Temp_LDock_Status = row[4]
		Temp_LDock_High_Alarm = row[5]
		Temp_LDock_High_Time = row[6] 
		Temp_LDock_Fan_Status = row[7]   
	curs.execute("SELECT id, Max, Fan_ON, Fan_OFF, Status, High_Alarm, High_Time, Fan_Status FROM Temp_RDock")
	for row in curs:
		Temp_RDock_id = row[0]
		Temp_RDock_Max = row[1]
		Temp_RDock_Fan_ON = row[2]
		Temp_RDock_Fan_OFF = row[3]
		Temp_RDock_Status = row[4]
		Temp_RDock_High_Alarm = row[5]
		Temp_RDock_High_Time = row[6]   
		Temp_RDock_Fan_Status = row[7]  
	curs.execute("SELECT id, Max, Fan_ON, Fan_OFF, Status, High_Alarm, High_Time, Temp_Max, Temp_Fan_ON, Temp_Fan_OFF, Temp_High_Alarm, Temp_High_Time, Fan_Status, Temp_Fan_Status FROM RH_Hood")
	for row in curs:
		RH_Hood_id = row[0]
		RH_Hood_Max = row[1]
		RH_Hood_Fan_ON = row[2]
		RH_Hood_Fan_OFF = row[3]
		RH_Hood_Status = row[4]
		RH_Hood_High_Alarm = row[5]
		RH_Hood_High_Time = row[6]
		RH_Hood_Temp_Max = row[7]
		RH_Hood_Temp_Fan_ON = row[8]
		RH_Hood_Temp_Fan_OFF = row[9]
		RH_Hood_Temp_High_Alarm = row[10]
		RH_Hood_Temp_High_Time = row[11]
		RH_Hood_Fan_Status = row[12]
		RH_Hood_Temp_Fan_Status = row[13]
	curs.execute("SELECT id, Max, Fan_ON, Fan_OFF, Status, High_Alarm, High_Time, Temp_Max, Temp_Fan_ON, Temp_Fan_OFF, Temp_High_Alarm, Temp_High_Time, Fan_Status, Temp_Fan_Status FROM RH_Cabinet")
	for row in curs:
		RH_Cabinet_id = row[0]
		RH_Cabinet_Max = row[1]
		RH_Cabinet_Fan_ON = row[2]
		RH_Cabinet_Fan_OFF = row[3]
		RH_Cabinet_Status = row[4]
		RH_Cabinet_High_Alarm = row[5]
		RH_Cabinet_High_Time = row[6]
		RH_Cabinet_Temp_Max = row[7]
		RH_Cabinet_Temp_Fan_ON = row[8]
		RH_Cabinet_Temp_Fan_OFF = row[9]
		RH_Cabinet_Temp_High_Alarm = row[10]
		RH_Cabinet_Temp_High_Time = row[11]
		RH_Cabinet_Fan_Status = row[12]
		RH_Cabinet_Temp_Fan_Status = row[13]
	conn.close

def ATO_MAIN():
	while True:
		try:
			print ""
			print "ATO Activated..."
			print ""
			load_DB_ATO_AWC()
			print("Calculating sump level (averaging readings over {} seconds)...".format(eTapeReadTime))
			etape_level = eTape_read_loop()
			sump_level = Convert_Ohms(etape_level)
			if sump_level < ATO_min:
				print "ALARM: SUMP WATER LEVEL LOWER THAN MINIMUM!"
				print "Sending email alert of alarm..."
				subject = 'NZAquaPi - ATO - ALARM!'
				body = "HELP!<br><br>This is an email alarm: SUMP WATER LEVEL LOWER THAN MINIMUM!<br><br>Nathan"
				Send_Email_Note(subject, body)
				print "Email sent!"
				logger.info("ALARM: - ATO - SUMP LEVEL LOWER THAN MINIMUM. Should get email confirmation of this")
				break
			elif sump_level == 600:
				print "ALARM: SUMP WATER LEVEL HIGHER THAN MAXIMUM!"
				print "Sending email alert of alarm..."
				subject = 'NZAquaPi - ATO - ALARM!'
				body = "HELP!<br><br>This is an email alarm: SUMP WATER LEVEL HIGHER THAN MAXIMUM!<br><br>Nathan"
				Send_Email_Note(subject, body)
				print "Email sent!"
				logger.info("ALARM: - ATO - SUMP LEVEL HIGHER THAN MAXIMUM. Should get email confirmation of this")
				break
			elif sump_level <= (ATO_opt_level - ATO_drp):
				#15 seconds of pump in = ~20mm (30secs = 45mm)
				time_to_run_pump = 15.0 * (ATO_drp / 20)
				time_to_add_prime = time_to_run_pump / 15.0 * 0.5 #every 15 seconds the pump runs add prime for 0.5 seconds
				print("eTape: {}ohms --> {}mm".format(etape_level, sump_level))
				print ""
				print("Optimal sump water level: {}mm".format(ATO_opt_level))
				print("Water level drop before enabled: {}mm".format(ATO_drp))
				print ""
				if time_to_add_prime < 0.5:
					print("Calculated time to run peristaltic pump for is less than the minimum allowed value (Calculated value: {0}seconds)... SKIPPING PRIME".format(time_to_add_prime))
					print "Sending email notification..."
					#send email alert
					subject = 'NZAquaPi - ATO Notification'
					body = ("Greetings!<br><br>This is a notification to let you know that Prime was not added to the soon to be completed ATO as the amount to add was less than the minimum allowed value (Calculated value: {}seconds).<br><br>Nathan".format(time_to_add_prime))
					Send_Email_Note(subject, body)
					print "Email sent!"
					print ""
					logger.info("NOTIFICATION: - ATO - Peristaltic pump not run")
				else:
					print("Turning Solenoid 7 ON for {0} seconds...".format(time_to_add_prime))
					GPIO.output(11, GPIO.HIGH)
					time.sleep(time_to_add_prime)
					GPIO.output(11, GPIO.LOW)
					print "Turning Solenoid 7 OFF..."
					time.sleep(0.5)
				
				print("Turning Solenoid 6 ON for {0} seconds...".format(time_to_run_pump))
				os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet6_status.jpg")
				ATO_Begin_Level = sump_level
				ATO_Pump_On = datetime.datetime.now()
				GPIO.output(22, GPIO.HIGH)
				time.sleep(time_to_run_pump)
				print "Turning Solenoid 6 OFF..."
				GPIO.output(22, GPIO.LOW)
				ATO_Pump_Off = datetime.datetime.now()
				os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet6_status.jpg")

				etape_level = eTape_read_loop()
				sump_level = Convert_Ohms(etape_level)
				ATO_End_Level = sump_level
				# send email if enabled
				if Send_Email == "ENABLED":
					print "Email enabled, sending email notification now..."
					subject = 'NZAquaPi - ATO Notification'
					body = "Greetings!<br><br>This is a notification email to let you know that the Auto-Top Off feature of the NZAquaPi has just been completed.<br><br>Optimal Level: " + str(ATO_opt_level) + "<br>Actual Level: " + str(ATO_Begin_Level) + "<br>Required drop before activating: " + str(ATO_drp) + "<br>Time Commenced: " + str(ATO_Pump_On) + "<br>Time Finished: " + str(ATO_Pump_Off) + "<br>Final Sump Level: " + str(ATO_End_Level) + "<br><br>Cheers,<br><br>Nathan"
					Send_Email_Note(subject, body)
					Emailed = "YES"
					print "Email sent!"
				else:
					print "Email disabled, skipping..."
					Emailed = "NO"
				
				# write log of events...
				conn=sqlite3.connect(dbname)
				curs=conn.cursor()
				curs.execute("SELECT COUNT(*) from ATO_Log")
				result=curs.fetchone()
				conn.close()
				number_of_rows=result[0]
				ID_to_use = number_of_rows + 1
				print "Writing log into Database... (Id is #" + str(ID_to_use) + ")"
				conn=sqlite3.connect(dbname)
				curs=conn.cursor()
				curs.execute("INSERT INTO ATO_Log VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (ID_to_use, ATO_opt_level, ATO_Begin_Level, ATO_drp, ATO_Pump_On, ATO_Pump_Off, ATO_End_Level, Emailed))
				conn.commit()
				conn.close()
				logger.info("ATO Completed. Should get email confirmation of this")
				print "Log Written"
				print ""
				print "ATO Completed!"
			else:
				print "Sump level OK. Will recheck in 15minutes."
			break
		except:
			logger.error("FATAL: ATO process error occured")
			break

def AWC_MAIN():
	while True:
		try:
			load_DB_ATO_AWC()
			if len(str(AWC_time)) == 1:
				string_AWC_time = "0" + str(AWC_time)
			else:
				string_AWC_time = str(AWC_time)
			CurrentDay = time.strftime("%A")
			CurrentHr = time.strftime("%H")
			
			global OldHr, AWC_completed, DoubleRunning
			
			if CurrentHr <> OldHr:
				print ""
				print "AWC Activating..."
				print ""
				CurrDateTime = datetime.datetime.now()
				print("Current AWC Method = {}".format(AWC_method))
				print "Current DateTime: " + str(CurrDateTime)
				print "Current Day: " + CurrentDay
				print "Current Hour: " + CurrentHr
				print "AWC_freq: " + str(AWC_freq)
				print "AWC_next_day: " + AWC_Next_Day
				print "AWC_time: " + string_AWC_time 
				print ""
				OldHr = CurrentHr
				#logger.info("AWC: Current Day = {0}, Current Day = {1}, AWC_Freq = {2}, AWC_next_day = {3}, AWC_time = {4}".format(CurrentDay, CurrentHr, AWC_freq, AWC_Next_Day, string_AWC_time))
			
			if (CurrentDay == AWC_Next_Day and CurrentHr == string_AWC_time) or DoubleRunning == 2:
				if AWC_completed == 0:
					if AWC_method == "eTape":
						print "Current Day = designated WC day & current hour = designated WC hour."
						print "Commencing eTape controlled water change..."
						print ""
						print "Calculating sump level (averaging readings over 2 minutes)..."
						print ""
						etape_level = eTape_read_loop()
						sump_level = Convert_Ohms(etape_level)
						if (sump_level - AWC_remove_amt) < ATO_min:
							print("Cannot complete AWC, removing {} from sump when current sump level is {} will drop sump level below minimum of {} (Specified as ATO_min in settings...)".format(AWC_remove_amt, sump_level, ATO_min))
							print "Please adjust settings... Perhaps lower the value of water to remove with each WC?"
							print "                          Perhaps increase the sump optimal level and ensure ATO is enabled?"
							print "Sending email alert of notification..."
							subject = 'NZAquaPi - AWC - Notification!'
							body = "Greetings!<br><br>Cannot complete eTape AWC, removing " + str(AWC_remove_amt) + " from sump when current sump level is " + str(sump_level) + " will drop sump level below minimum of " + str(ATO_min) + " (Specified as ATO_min in settings...)<br><br>Please adjust settings... Perhaps lower the value of water to remove with each WC? Perhaps increase the sump optimal level and ensure ATO is enabled?<br><br>Nathan"
							Send_Email_Note(subject, body)
							print "Email sent!"
							logger.info("AWC: Cannot complete as not enough H20 in sump. Should get email confirmation of this")
							break
						else:
							print "Current sump level: " + str(sump_level)
							print "Amount of water to remove: " + str(AWC_remove_amt)
							Log_Drain_On = datetime.datetime.now()
							i = 1
							while i <= 30:
								if i == 1 and AWC_remove_amt >= 30:
									RemoveFor = 400
								elif i > 1 and (AWC_remove_amt - (sump_level - new_sump_level)) >= 30:
									RemoveFor = 400
								else:
									RemoveFor = 200
								print("Removing water...({})".format(i))
								print("   Turning Solenoid 5 ON for {} seconds... (should remove ~{}mm water)".format(RemoveFor, (RemoveFor / 20)))
								os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet5_status.jpg")
								GPIO.output(18, GPIO.HIGH)
								time.sleep(RemoveFor)
								
								print "   Turning Solenoid 5 OFF..."
								GPIO.output(18, GPIO.LOW)
								os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet5_status.jpg")

								print "   Re-testing sump level..."
								etape_level = eTape_read_loop()
								new_sump_level = Convert_Ohms(etape_level)
								print "   New sump level: " + str(new_sump_level)
								print("   Required sump level: {}".format(sump_level - AWC_remove_amt))
								
								if (sump_level - AWC_remove_amt) == new_sump_level:
									print "Required sump level achieved, beginning sump refill..."
									Log_Drain_Off = datetime.datetime.now()
									Number_Of_Cycles = i
									i = 31
								elif (sump_level - AWC_remove_amt) > new_sump_level:
									print "   Have possibly removed too much water, re-resting sump level to confirm..."
									etape_level = eTape_read_loop()
									new_sump_level = Convert_Ohms(etape_level)
									if (sump_level - AWC_remove_amt) > new_sump_level:
										print("   Yep, new sump level (re-checked) is {}. Beginning sump refill anyway... hopefully haven't broken drain syphon (or damaged return pump!)".format(new_sump_level))
									else:
										print("   Nope, all good! re-checked level is {}. Beginning sump refill...".format(new_sump_level))
									Log_Drain_Off = datetime.datetime.now()
									Number_Of_Cycles = i
									i = 31
								elif (sump_level - AWC_remove_amt) < new_sump_level and i == 30:
									print("ALARM: Either MOSFET5 not working or Syphon broken. {} cycles have been completed and still haven't drained {}mm...".format(i, AWC_remove_amt))
									print "Check MOSFET5 and Syphon."
									print "Sending email alert of alarm..."
									subject = 'NZAquaPi - AWC - ALARM!'
									body = "HELP!<br><br>This is an email alarm: Either MOSFET5 not working or Syphon broken. " + str(i) + "cycles have been completed and still haven't drained " + str(AWC_remove_amt) + "mm...<br><br>Nathan"
									Send_Email_Note(subject, body)
									print "Email sent!"
									logger.info("AWC: Either MOSFET5 not working of Syphon broken. Should get email confirmation of this")
									i = 32
									break
								elif (sump_level - AWC_remove_amt) < new_sump_level:
									print "   Not enough water removed yet, will remove more now..."
									i = i + 1
							if i == 32:
								break
							
							#13 seconds of pump in = ~20mm (30secs = 45mm)
							time_to_run_pump = 13 * (AWC_remove_amt / 20)
							time_to_add_prime = time_to_run_pump / 15.0 * 0.5 #every 15 seconds the pump runs add prime for 0.5 seconds
							if time_to_add_prime < 0.5:
								print("Calculated time to run peristaltic pump for is less than the minimum allowed value (Calculated value: {0}seconds)... SKIPPING PRIME".format(time_to_add_prime))
								print "Sending email notification..."
								subject = 'NZAquaPi - AWC Notification'
								body = ("Greetings!<br><br>This is a notification to let you know that Prime was not added to the soon to be completed AWC as the amount to add was less than the minimum allowed value (Calculated value: {}seconds).<br><br>Nathan".format(time_to_add_prime))
								Send_Email_Note(subject, body)
								print "Email sent!"
								logger.info("AWC: No Prime added. Should get email confirmation of this")
							else:
								print "Adding Prime..."
								print("   Turning Solenoid 7 ON for {0} seconds...".format(time_to_add_prime))
								GPIO.output(11, GPIO.HIGH)
								time.sleep(time_to_add_prime)
								GPIO.output(11, GPIO.LOW)
								print "   Turning Solenoid 7 OFF..."
								time.sleep(0.5)
							print "Adding water..."
							
							print("   Turning Solenoid 6 ON for {} seconds... (should add ~20mm water per 13 seconds)".format(time_to_run_pump))
							os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet6_status.jpg")
							Log_Inlet_On = datetime.datetime.now()
							GPIO.output(22, GPIO.HIGH)
							time.sleep(time_to_run_pump)
							
							print "   Turning Solenoid 6 OFF..."
							GPIO.output(22, GPIO.LOW)
							Log_Inlet_Off = datetime.datetime.now()
							os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet6_status.jpg")

							print "   Re-testing sump level..."
							etape_level = eTape_read_loop()
							final_sump_level = Convert_Ohms(etape_level)
							print "   Final sump level: " + str(final_sump_level)
							print ""
							print "------"
							print "eTape AWC Summary:"
							print "   Amount removed: " + str(sump_level - new_sump_level)
							print "   Amount added: " + str(final_sump_level - new_sump_level)
							if (sump_level + new_sump_level) < (final_sump_level - new_sump_level):
								print "    NB: Amount added less than amount removed. No biggie, ensure ATO is turned on and will top it back up anyway! :)"
							elif (sump_level + new_sump_level) > (final_sump_level - new_sump_level):
								print "    NB: Amount added more than amount removed. No biggie, evaporation will fix it eventually! :)"
							print "------"
							logger.info("AWC: (eTape) AWC Completed")
					
					elif AWC_method == "Manual":
						print "Current Day = designated WC day & current hour = designated WC hour."
						print "Commencing manual water change..."
						print ""
						
						print("Turning Solenoid 5 ON for {0} seconds...".format(AWC_remove_time))
						os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet5_status.jpg")
						Log_Drain_On = datetime.datetime.now()
						GPIO.output(18, GPIO.HIGH)
						time.sleep(AWC_remove_time)
						
						print "Turning Solenoid 5 OFF..."
						GPIO.output(18, GPIO.LOW)
						Log_Drain_Off = datetime.datetime.now()
						os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet5_status.jpg")
						time.sleep(0.5)
						
						time_to_add_prime = AWC_add_time / 15.0 * 0.5 #every 15 seconds the pump runs add prime for 0.5 seconds
						if time_to_add_prime < 0.5:
							print("Calculated time to run peristaltic pump for is less than the minimum allowed value (Calculated value: {0}seconds)... SKIPPING PRIME".format(time_to_add_prime))
							print "Sending email notification..."
							subject = 'NZAquaPi - AWC Notification'
							body = ("Greetings!<br><br>This is a notification to let you know that Prime was not added to the soon to be completed AWC as the amount to add was less than the minimum allowed value (Calculated value: {}seconds).<br><br>Nathan".format(time_to_add_prime))
							Send_Email_Note(subject, body)
							print "Email sent!"
						else:
							print "Adding Prime..."
							print("Turning Solenoid 7 ON for {0} seconds...".format(time_to_add_prime))
							GPIO.output(11, GPIO.HIGH)
							time.sleep(time_to_add_prime)
							print "Turning Solenoid 7 OFF..."
							GPIO.output(11, GPIO.LOW)
							time.sleep(0.5)
						
						print("Turning Solenoid 6 ON for {0} seconds...".format(AWC_add_time))
						os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet6_status.jpg")
						Log_Inlet_On = datetime.datetime.now()
						GPIO.output(22, GPIO.HIGH)
						time.sleep(AWC_add_time)
						
						print "Turning Solenoid 6 OFF..."
						print ""
						GPIO.output(22, GPIO.LOW)
						Log_Inlet_Off = datetime.datetime.now()
						os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet6_status.jpg")
						
					# send email if enabled
					if Send_Email == "ENABLED":
						print "Email enabled, sending email notification now..."
						if AWC_method == "eTape":
							subject = 'NZAquaPi - AWC Notification (eTape Method)'
							body = "Greetings!<br><br>This is a notification email to let you know that a pre-schedule eTape AWC has been completed.<br><br>Starting sump level: " + str(sump_level) + "mm<br>Amount to remove: " + str(AWC_remove_amt) + "mm<br><br>Time drain began: " + str(Log_Drain_On) + "<br>Time drain finished: " + str(Log_Drain_Off) + "<br>New sump level: " + str(new_sump_level) + "mm (Amount removed: " + str(sump_level - new_sump_level) + "mm)<br>Cycles required to achieve new level: " + str(Number_Of_Cycles) + "<br><br>Time inlet opened to refill: " + str(Log_Inlet_On) + "<br>Time inlet closed (i.e. AWC Completed): " + str(Log_Inlet_Off) + "<br>Final sump level: " + str(final_sump_level) + "mm (Amount added: " + str(final_sump_level - new_sump_level) + "mm)<br><br>Cheers,<br><br>Nathan"
						else:
							subject = 'NZAquaPi - AWC Notification (Manual Method)'
							body = "Greetings!<br><br>This is a notification email to let you know that a pre-schedule Manual AWC has been completed.<br><br>Time AWC commenced: " + str(Log_Drain_On) + "<br>Time AWC completed: " + str(Log_Inlet_Off) + "<br><br>Cheers,<br><br>Nathan"
						Send_Email_Note(subject, body)
						Emailed = "YES"
						print "Email sent!"
					else:
						print "Email disabled, skipping..."
						Emailed = "NO"
					print ""
					
					# write log of events...
					conn=sqlite3.connect(dbname)
					curs=conn.cursor()
					curs.execute("SELECT COUNT(*) from AWC_Log")
					result=curs.fetchone()
					conn.close
					number_of_rows=result[0]
					ID_to_use = number_of_rows + 1
					print "Writing log into Database... (Id is #" + str(ID_to_use) + ")"
					conn=sqlite3.connect(dbname)
					curs=conn.cursor()
					if AWC_method == "eTape":
						curs.execute("INSERT INTO AWC_Log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ID_to_use, AWC_method, Log_Drain_On, Log_Drain_Off, Log_Inlet_On, Log_Inlet_Off, sump_level, new_sump_level, final_sump_level, AWC_remove_amt, Number_Of_Cycles, (sump_level - new_sump_level), (final_sump_level - new_sump_level), Emailed))
					else:
						curs.execute("INSERT INTO AWC_Log VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ID_to_use, AWC_method, Log_Drain_On, Log_Drain_Off, Log_Inlet_On, Log_Inlet_Off, "", "", "", "", "", "", "", Emailed))
					conn.commit()
					conn.close()
					print "Log written into DB."
					print ""
					
					# mark next day to run
					if DoubleRunning == 2:
						DoubleRunning = 3
					
					if DoubleRunning == 1:
						DoubleRunning = 2
					elif DoubleRunning == 3:
						DoubleRunning = 1
						if AWC_freq == 1:
							if AWC_Next_Day == "Monday":
								NextD = "Tuesday"
							elif AWC_Next_Day == "Tuesday":
								NextD = "Wednesday"
							elif AWC_Next_Day == "Wednesday":
								NextD = "Thursday"
							elif AWC_Next_Day == "Thursday":
								NextD = "Friday"
							elif AWC_Next_Day == "Friday":
								NextD = "Saturday"
							elif AWC_Next_Day == "Saturday":
								NextD = "Sunday"
							elif AWC_Next_Day == "Sunday":
								NextD = "Monday"
						elif AWC_freq == 2:
							if AWC_Next_Day == "Monday":
								NextD = "Wednesday"
							elif AWC_Next_Day == "Tuesday":
								NextD = "Thursday"
							elif AWC_Next_Day == "Wednesday":
								NextD = "Friday"
							elif AWC_Next_Day == "Thursday":
								NextD = "Saturday"
							elif AWC_Next_Day == "Friday":
								NextD = "Sunday"
							elif AWC_Next_Day == "Saturday":
								NextD = "Monday"
							elif AWC_Next_Day == "Sunday":
								NextD = "Tuesday"
						elif AWC_freq == 3:
							if AWC_Next_Day == "Monday":
								NextD = "Thursday"
							else:
								NextD = "Monday"
						conn=sqlite3.connect(dbname)
						curs=conn.cursor()
						curs.execute("UPDATE AWC SET Frequency_Next_Day=?", (NextD,))
						conn.commit()
						conn.close
						AWC_completed = 1
					else:
						if AWC_freq == 1:
							if AWC_Next_Day == "Monday":
								NextD = "Tuesday"
							elif AWC_Next_Day == "Tuesday":
								NextD = "Wednesday"
							elif AWC_Next_Day == "Wednesday":
								NextD = "Thursday"
							elif AWC_Next_Day == "Thursday":
								NextD = "Friday"
							elif AWC_Next_Day == "Friday":
								NextD = "Saturday"
							elif AWC_Next_Day == "Saturday":
								NextD = "Sunday"
							elif AWC_Next_Day == "Sunday":
								NextD = "Monday"
						elif AWC_freq == 2:
							if AWC_Next_Day == "Monday":
								NextD = "Wednesday"
							elif AWC_Next_Day == "Tuesday":
								NextD = "Thursday"
							elif AWC_Next_Day == "Wednesday":
								NextD = "Friday"
							elif AWC_Next_Day == "Thursday":
								NextD = "Saturday"
							elif AWC_Next_Day == "Friday":
								NextD = "Sunday"
							elif AWC_Next_Day == "Saturday":
								NextD = "Monday"
							elif AWC_Next_Day == "Sunday":
								NextD = "Tuesday"
						elif AWC_freq == 3:
							if AWC_Next_Day == "Monday":
								NextD = "Thursday"
							else:
								NextD = "Monday"
						conn=sqlite3.connect(dbname)
						curs=conn.cursor()
						curs.execute("UPDATE AWC SET Frequency_Next_Day=?", (NextD,))
						conn.commit()
						conn.close
						AWC_completed = 1
			else:
				AWC_completed = 0
			break
		except:
			logger.error("FATAL: AWC process error occured")
			break

def Send_Email_Note(subject, body):
#send email notification
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT smtp_server, smtp_port, login_email_address, password_hash, recipient FROM Email")
	for row in curs:
		email_SMTP_serv = row[0]
		email_SMTP_port = row[1]
		login_eml = row[2]
		login_ps = row[3]
		recip_email = row[4]
	conn.close
	session = smtplib.SMTP(str(email_SMTP_serv), str(email_SMTP_port))
	session.ehlo()
	session.starttls()
	session.login(login_eml, login_ps)
	headers = ["from: " + login_eml, "subject: " + subject, "to: " + recip_email, "mime-version: 1.0", "content-type: text/html"]
	headers = "\r\n".join(headers)
	session.sendmail(login_eml, recip_email, headers + "\r\n\r\n" + body)
	session.quit()

def MOSFET_OVERRIDE_MAIN():
	shutdown_MOSFETS = 0
	Override_State = load_DB_Override_State()
	while True:
		try:
			#print ""
			#print "MOSFET Override check occuring..."
			if Override_State == 1:
				print ""
				print "Override_State TRIGGERED!..."
				print ""
				conn=sqlite3.connect(dbname)
				curs=conn.cursor()
				curs.execute("SELECT MOSFET1_Status, MOSFET1_Override, MOSFET1_Override_Time, MOSFET2_Status, MOSFET2_Override, MOSFET2_Override_Time, MOSFET3_Status, MOSFET3_Override, MOSFET3_Override_Time, MOSFET4_Status, MOSFET4_Override, MOSFET4_Override_Time, MOSFET5_Status, MOSFET5_Override, MOSFET5_Override_Time, MOSFET6_Status, MOSFET6_Override, MOSFET6_Override_Time, MOSFET7_Status, MOSFET7_Override, MOSFET7_Override_Time FROM MOSFET_Status")
				for row in curs:
					MOSFET1_Status = row[0]
					MOSFET1_Override = row[1]
					MOSFET1_Override_Time = row[2]
					MOSFET2_Status = row[3]
					MOSFET2_Override = row[4]
					MOSFET2_Override_Time = row[5]
					MOSFET3_Status = row[6]
					MOSFET3_Override = row[7]
					MOSFET3_Override_Time = row[8]
					MOSFET4_Status = row[9]
					MOSFET4_Override = row[10]
					MOSFET4_Override_Time = row[11]
					MOSFET5_Status = row[12]
					MOSFET5_Override = row[13]
					MOSFET5_Override_Time = row[14]
					MOSFET6_Status = row[15]
					MOSFET6_Override = row[16]
					MOSFET6_Override_Time = row[17]
					MOSFET7_Status = row[18]
					MOSFET7_Override = row[19]
					MOSFET7_Override_Time = row[20]
				conn.close
				
				if MOSFET1_Override == "ON":
					print "MOSFET1 Override: " + MOSFET1_Override + " (for " + str(MOSFET1_Override_Time) + " seconds)"
				else:
					print "MOSFET1 Override: " + MOSFET1_Override
				if MOSFET2_Override == "ON":
					print "MOSFET2 Override: " + MOSFET2_Override + " (for " + str(MOSFET2_Override_Time) + " seconds)"
				else:
					print "MOSFET2 Override: " + MOSFET2_Override
				if MOSFET3_Override == "ON":
					print "MOSFET3 Override: " + MOSFET3_Override + " (for " + str(MOSFET3_Override_Time) + " seconds)"
				else:
					print "MOSFET3 Override: " + MOSFET3_Override
				if MOSFET4_Override == "ON":
					print "MOSFET4 Override: " + MOSFET4_Override + " (for " + str(MOSFET4_Override_Time) + " seconds)"
				else:
					print "MOSFET4 Override: " + MOSFET4_Override
				if MOSFET5_Override == "ON":
					print "MOSFET5 Override: " + MOSFET5_Override + " (for " + str(MOSFET5_Override_Time) + " seconds)"
				else:
					print "MOSFET5 Override: " + MOSFET5_Override
				if MOSFET6_Override == "ON":
					print "MOSFET6 Override: " + MOSFET6_Override + " (for " + str(MOSFET6_Override_Time) + " seconds)"
				else:
					print "MOSFET6 Override: " + MOSFET6_Override	
				if MOSFET7_Override == "ON":
					print "MOSFET7 Override: " + MOSFET7_Override + " (for " + str(MOSFET7_Override_Time) + " seconds)"
				else:
					print "MOSFET7 Override: " + MOSFET7_Override	
				print ""
				
				#turn on/off solenoids that need to be
				if MOSFET1_Override == "ON":
					if MOSFET1_Status == 1 and GPIO.input(12) == 1:
						GPIO.output(12, GPIO.LOW)
						print "MOSFET1 is now OFF"
						os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet1_status.jpg")
					elif MOSFET1_Status == 0 and GPIO.input(12) == 0:
						GPIO.output(12, GPIO.HIGH)
						print "MOSFET1 is now ON"
						os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet1_status.jpg")
					else:
						logger.error("ERROR: MOSFET1_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET1_Status and actual GPIO status NOT MATCHING!"
						shutdown_MOSFETS = 1
						break
				if MOSFET2_Override == "ON":
					if MOSFET2_Status == 1 and GPIO.input(13) == 1:
						GPIO.output(13, GPIO.LOW)
						print "MOSFET2 is now OFF"
						os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet2_status.jpg")
					elif MOSFET2_Status == 0 and GPIO.input(13) == 0:
						GPIO.output(13, GPIO.HIGH)
						print "MOSFET2 is now ON"
						os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet2_status.jpg")
					else:
						logger.error("ERROR: MOSFET2_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET2_Status and actual GPIO status NOT MATCHING"
						shutdown_MOSFETS = 1
						break
				if MOSFET3_Override == "ON":
					if MOSFET3_Status == 1 and GPIO.input(15) == 1:
						GPIO.output(15, GPIO.LOW)
						print "MOSFET3 is now OFF"
						os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet3_status.jpg")
					elif MOSFET3_Status == 0 and GPIO.input(15) == 0:
						GPIO.output(15, GPIO.HIGH)
						print "MOSFET3 is now ON"
						os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet3_status.jpg")
					else:
						logger.error("ERROR: MOSFET3_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET3_Status and actual GPIO status NOT MATCHING"
						shutdown_MOSFETS = 1
						break
				if MOSFET4_Override == "ON":
					if MOSFET4_Status == 1 and GPIO.input(16) == 1:
						GPIO.output(16, GPIO.LOW)
						print "MOSFET4 is now OFF"
						os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet4_status.jpg")
					elif MOSFET4_Status == 0 and GPIO.input(16) == 0:
						GPIO.output(16, GPIO.HIGH)
						print "MOSFET4 is now ON"
						os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet4_status.jpg")
					else:
						logger.error("ERROR: MOSFET4_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET4_Status and actual GPIO status NOT MATCHING"
						shutdown_MOSFETS = 1
						break
				if MOSFET5_Override == "ON":
					if MOSFET5_Status == 1 and GPIO.input(18) == 1:
						GPIO.output(18, GPIO.LOW)
						print "MOSFET5 is now OFF"
						os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet5_status.jpg")
					elif MOSFET5_Status == 0 and GPIO.input(18) == 0:
						GPIO.output(18, GPIO.HIGH)
						print "MOSFET5 is now ON"
						os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet5_status.jpg")
					else:
						logger.error("ERROR: MOSFET5_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET5_Status and actual GPIO status NOT MATCHING"
						shutdown_MOSFETS = 1
						break
				if MOSFET6_Override == "ON":
					if MOSFET6_Status == 1 and GPIO.input(22) == 1:
						GPIO.output(22, GPIO.LOW)
						print "MOSFET6 is now OFF"
						os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet6_status.jpg")
					elif MOSFET6_Status == 0 and GPIO.input(22) == 0:
						GPIO.output(22, GPIO.HIGH)
						print "MOSFET6 is now ON"
						os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet6_status.jpg")
					else:
						logger.error("ERROR: MOSFET6_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET6_Status and actual GPIO status NOT MATCHING"
						shutdown_MOSFETS = 1
						break
				if MOSFET7_Override == "ON":
					if MOSFET7_Status == 1 and GPIO.input(11) == 1:
						GPIO.output(11, GPIO.LOW)
						print "MOSFET7 is now OFF"
					elif MOSFET7_Status == 0 and GPIO.input(11) == 0:
						GPIO.output(11, GPIO.HIGH)
						print "MOSFET7 is now ON"
					else:
						logger.error("ERROR: MOSFET7_Status and actual GPIO status NOT MATCHING")
						print "ERROR: MOSFET7_Status and actual GPIO status NOT MATCHING"
						shutdown_MOSFETS = 1
						break
				print ""
				
				found = 0
				oldsleep = 0
				MOSFET1_SWITCH = "FALSE"
				MOSFET2_SWITCH = "FALSE"
				MOSFET3_SWITCH = "FALSE"
				MOSFET4_SWITCH = "FALSE"
				MOSFET5_SWITCH = "FALSE"
				MOSFET6_SWITCH = "FALSE"
				MOSFET7_SWITCH = "FALSE"

				i = 0.5
				while i <= 300:
					if MOSFET1_Override_Time == i and MOSFET1_Override == "ON":
						found = 1
						MOSFET1_SWITCH = "TRUE"
					if MOSFET2_Override_Time == i and MOSFET2_Override == "ON":
						found = 1
						MOSFET2_SWITCH = "TRUE"
					if MOSFET3_Override_Time == i and MOSFET3_Override == "ON":
						found = 1
						MOSFET3_SWITCH = "TRUE"
					if MOSFET4_Override_Time == i and MOSFET4_Override == "ON":
						found = 1
						MOSFET4_SWITCH = "TRUE"
					if MOSFET5_Override_Time == i and MOSFET5_Override == "ON":
						found = 1
						MOSFET5_SWITCH = "TRUE"
					if MOSFET6_Override_Time == i and MOSFET6_Override == "ON":
						found = 1
						MOSFET6_SWITCH = "TRUE"
					if MOSFET7_Override_Time == i and MOSFET7_Override == "ON":
						found = 1
						MOSFET7_SWITCH = "TRUE"
					if found == 1:
						print("Sleeping for {0} seconds ({1} - {2})...".format(i - oldsleep, i, oldsleep))
						time.sleep(i - oldsleep)
						if MOSFET1_SWITCH == "TRUE":
							MOSFET1_SWITCH = "FALSE"
							if GPIO.input(12) == 1:
								GPIO.output(12, GPIO.LOW)
								print "MOSFET1 is now OFF"
								os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet1_status.jpg")
							elif GPIO.input(12) == 0:
								GPIO.output(12, GPIO.HIGH)
								print "MOSFET1 is now ON"
								os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet1_status.jpg")
						if MOSFET2_SWITCH == "TRUE":
							MOSFET2_SWITCH = "FALSE"
							if GPIO.input(13) == 1:
								GPIO.output(13, GPIO.LOW)
								print "MOSFET2 is now OFF"
								os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet2_status.jpg")
							elif GPIO.input(13) == 0:
								GPIO.output(13, GPIO.HIGH)
								print "MOSFET2 is now ON"
								os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet2_status.jpg")
						if MOSFET3_SWITCH == "TRUE":
							MOSFET3_SWITCH = "FALSE"
							if GPIO.input(15) == 1:
								GPIO.output(15, GPIO.LOW)
								print "MOSFET3 is now OFF"
								os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet3_status.jpg")
							elif GPIO.input(15) == 0:
								GPIO.output(15, GPIO.HIGH)
								print "MOSFET3 is now ON"
								os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet3_status.jpg")
						if MOSFET4_SWITCH == "TRUE":
							MOSFET4_SWITCH = "FALSE"
							if GPIO.input(16) == 1:
								GPIO.output(16, GPIO.LOW)
								print "MOSFET4 is now OFF"
								os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet4_status.jpg")
							elif GPIO.input(16) == 0:
								GPIO.output(16, GPIO.HIGH)
								print "MOSFET4 is now ON"
								os.system("cp /var/www/images/blue_on.jpg /var/www/images/mosfet4_status.jpg")
						if MOSFET5_SWITCH == "TRUE":
							MOSFET5_SWITCH = "FALSE"
							if GPIO.input(18) == 1:
								GPIO.output(18, GPIO.LOW)
								print "MOSFET5 is now OFF"
								os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet5_status.jpg")
							elif GPIO.input(18) == 0:
								GPIO.output(18, GPIO.HIGH)
								print "MOSFET5 is now ON"
								os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet5_status.jpg")
						if MOSFET6_SWITCH == "TRUE":
							MOSFET6_SWITCH = "FALSE"
							if GPIO.input(22) == 1:
								GPIO.output(22, GPIO.LOW)
								print "MOSFET6 is now OFF"
								os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet6_status.jpg")
							elif GPIO.input(22) == 0:
								GPIO.output(22, GPIO.HIGH)
								print "MOSFET6 is now ON"
								os.system("cp /var/www/images/red_on.jpg /var/www/images/mosfet6_status.jpg")
						if MOSFET7_SWITCH == "TRUE":
							MOSFET7_SWITCH = "FALSE"
							if GPIO.input(11) == 1:
								GPIO.output(11, GPIO.LOW)
								print "MOSFET7 is now OFF"
							elif GPIO.input(11) == 0:
								GPIO.output(11, GPIO.HIGH)
								print "MOSFET7 is now ON"
						oldsleep = i
						found = 0
					i = i + 0.5
				print ""
				print "Updating database with new MOSFET status, and removing manual triggers..."
				conn=sqlite3.connect(dbname)
				curs=conn.cursor()
				curs.execute("UPDATE MOSFET_Status SET MOSFET1_Status=?, MOSFET1_Override=?, MOSFET1_Override_Time=?, MOSFET2_Status=?, MOSFET2_Override=?, MOSFET2_Override_Time=?, MOSFET3_Status=?, MOSFET3_Override=?, MOSFET3_Override_Time=?, MOSFET4_Status=?, MOSFET4_Override=?, MOSFET4_Override_Time=?, MOSFET5_Status=?, MOSFET5_Override=?, MOSFET5_Override_Time=?, MOSFET6_Status=?, MOSFET6_Override=?, MOSFET6_Override_Time=?, MOSFET7_Status=?, MOSFET7_Override=?, MOSFET7_Override_Time=?, Override_State=?", (GPIO.input(12), "OFF", 0, GPIO.input(13), "OFF", 0, GPIO.input(15), "OFF", 0, GPIO.input(16), "OFF", 0, GPIO.input(18), "OFF", 0, GPIO.input(22), "OFF", 15, GPIO.input(11), "OFF", 0.5, 0))
				conn.commit()
				conn.close
				print "Database updated"
				print ""
				print "Manual Override complete!"
			break
		except:
			logger.error("FATAL: MOSFET process error occured")
			break
			
	if shutdown_MOSFETS == 1:
		GPIO.output(11, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(22, GPIO.LOW)
		logger.error("ERROR: Something BAD has happened and triggered the MOSFETS to shutdown")
		
def SENSORS_MAIN():
	while True:
		try:
			print ""
			print "Sensor Output:"
			load_DB_Sensors()
			read_temp_sensors()
			read_humidity_sensors()
			read_analogs()
			print ""
			print "Alarms Triggered:"
			check_temps()
			log_data()
			break
		except:
			logger.error("FATAL: SENSORS process error occured")
			break

#MAIN LOOP START#
FirstRun = 1
while True:
	try:
		if FirstRun == 1:
			print "Starting NZAquaPi Daemon..."
			MOSFET_OVERRIDE_MAIN()
			MOSFET_OVERRIDE_finished = datetime.datetime.now()
			ATO_MAIN()
			ATO_finished = datetime.datetime.now()
			AWC_MAIN()
			if DoubleRunning == 2:
				AWC_MAIN()
			AWC_finished = datetime.datetime.now()
			SENSORS_MAIN()
			SENSORS_finished = datetime.datetime.now()
			FirstRun = 0
		else:
			FirstCurrentTime = datetime.datetime.now()
			if FirstCurrentTime >= MOSFET_OVERRIDE_finished + datetime.timedelta(seconds=SleepTime_MOSFET_Override):
				MOSFET_OVERRIDE_MAIN()
				MOSFET_OVERRIDE_finished = datetime.datetime.now()
			CurrentTime = datetime.datetime.now()
			if CurrentTime >= ATO_finished + datetime.timedelta(seconds=SleepTime_ATO_AWC):
				ATO_MAIN()
				ATO_finished = datetime.datetime.now()
			CurrentTime = datetime.datetime.now()
			if CurrentTime >= AWC_finished + datetime.timedelta(seconds=SleepTime_ATO_AWC):
				AWC_MAIN()
				if DoubleRunning == 2:
					AWC_MAIN()
				AWC_finished = datetime.datetime.now()
			CurrentTime = datetime.datetime.now()
			if CurrentTime >= SENSORS_finished + datetime.timedelta(seconds=SleepTime_Sensors):
				SENSORS_MAIN()
				SENSORS_finished = datetime.datetime.now()
			CurrentTime = datetime.datetime.now()
			if datetime.timedelta(seconds=SleepTime_MOSFET_Override) > CurrentTime - FirstCurrentTime:
				time.sleep(SleepTime_MOSFET_Override)
		GPIO.output(8, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(8, GPIO.LOW)
		
	except:
		logger.error("SYSTEM FATAL: Main process error has occured")
		subject = 'NZAquaPi - FATAL PROCESS ERROR!'
		body = "HELP!<br><br>There has been a fatal process error. The NZAquaPi daemon has been terminated! RaspberryPi must be restarted ASAP. <br><br>Nathan"
		Send_Email_Note(subject, body)
		break

