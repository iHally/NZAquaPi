#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sqlite3
import os
import datetime
import smtplib

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

dbname='/var/www/NZAquaPi.db'

# import DB settings
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

def rename_for_output(function, pin):
    found = 0
    if function == 0:
        status = GPIO.input(pin)
        function = "OUT (" + str(status) + ")"
        found = 1
    if function == 1:
        function = "IN"
        found = 1
    if function == 40:
        function = "I2C"
        found = 1
    if function == 41:
        function = "SPI"
        found = 1
    if function == 42:
        function = "SERIAL"
        found = 1
    if found == 0:
        function = "UNKNOWN/OTHER (" + str(function) + ")"
    return function

def MAIN():
    print ""
    print "---------------------------"
    print "CURRENT GPIO STATUS:"
    print "---------------------------"
    print "Pin 1: 3.3V" 
    print "Pin 2: 5V" 
    function = GPIO.gpio_function(3)
    function = rename_for_output(function, 3)
    print "Pin 3: " + str(function)
    print "Pin 4: 5V" 
    function = GPIO.gpio_function(5)
    function = rename_for_output(function, 5)
    print "Pin 5: " + str(function)
    print "Pin 6: Gnd" 
    function = GPIO.gpio_function(7)
    function = rename_for_output(function, 7)
    print "Pin 7: " + str(function)
    function = GPIO.gpio_function(8)
    function = rename_for_output(function, 8)
    print "Pin 8: " + str(function)
    print "Pin 9: Gnd" 
    function = GPIO.gpio_function(10)
    function = rename_for_output(function, 10)
    print "Pin 10: " + str(function)
    function = GPIO.gpio_function(11)
    function = rename_for_output(function, 11)
    print "Pin 11: " + str(function)
    function = GPIO.gpio_function(12)
    function = rename_for_output(function, 12)
    print "Pin 12: " + str(function)
    function = GPIO.gpio_function(13)
    function = rename_for_output(function, 13)
    print "Pin 13: " + str(function)
    print "Pin 14: Gnd" 
    function = GPIO.gpio_function(15)
    function = rename_for_output(function, 15)
    print "Pin 15: " + str(function)
    function = GPIO.gpio_function(16)
    function = rename_for_output(function, 16)
    print "Pin 16: " + str(function)
    print "Pin 17: 3.3V" 
    function = GPIO.gpio_function(18)
    function = rename_for_output(function, 18)
    print "Pin 18: " + str(function)
    function = GPIO.gpio_function(19)
    function = rename_for_output(function, 19)
    print "Pin 19: " + str(function)
    print "Pin 20: Gnd" 
    function = GPIO.gpio_function(21)
    function = rename_for_output(function, 21)
    print "Pin 21: " + str(function)
    function = GPIO.gpio_function(22)
    function = rename_for_output(function, 22)
    print "Pin 22: " + str(function)
    function = GPIO.gpio_function(23)
    function = rename_for_output(function, 23)
    print "Pin 23: " + str(function)
    function = GPIO.gpio_function(24)
    function = rename_for_output(function, 24)
    print "Pin 24: " + str(function)
    print "Pin 25: Gnd" 
    function = GPIO.gpio_function(26)
    function = rename_for_output(function, 26)
    print "Pin 26: " + str(function)

def proper_config():
    GPIO.setup(3, GPIO.IN) #AM3023 (Hood) - Default is Serial
    GPIO.setup(5, GPIO.IN) #AM3023 (Cabinet) - Default is Serial
    GPIO.setup(8, GPIO.OUT, initial = 0)  #LED 1 - Default is I2C (Out HIGH)
    GPIO.setup(11, GPIO.OUT, initial = 0) #MOSFET 7 (Peristaltic Pump)
    GPIO.setup(12, GPIO.OUT, initial = 0) #MOSFET 1
    GPIO.setup(13, GPIO.OUT, initial = 0) #MOSFET 2
    GPIO.setup(15, GPIO.OUT, initial = 0) #MOSFET 3
    GPIO.setup(16, GPIO.OUT, initial = 0) #MOSFET 4
    GPIO.setup(18, GPIO.OUT, initial = 0) #MOSFET 5 (Solenoid)
    GPIO.setup(22, GPIO.OUT, initial = 0) #MOSFET 6 (Solenoid)
    GPIO.setup(26, GPIO.OUT, initial = 0) #LED 3 - Default is SPI (Out HIGH)

def startup_test():
    time.sleep(10)
    GPIO.output(8, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(8, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(8, GPIO.HIGH)  
    time.sleep(0.5)
    GPIO.output(8, GPIO.LOW)
    GPIO.output(26, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(11, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(8, GPIO.HIGH)  
    GPIO.output(11, GPIO.HIGH)  
    GPIO.output(26, GPIO.HIGH)  
    time.sleep(1)
    GPIO.output(8, GPIO.LOW)  
    GPIO.output(11, GPIO.LOW)  
    GPIO.output(26, GPIO.LOW) 
  
proper_config()    
MAIN()
print "------"
print ""

print "------"
print "Updating mosfet icons for webpage and default database values..."
os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet1_status.jpg")
os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet2_status.jpg")
os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet3_status.jpg")
os.system("cp /var/www/images/blue_off.jpg /var/www/images/mosfet4_status.jpg")
os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet5_status.jpg")
os.system("cp /var/www/images/red_off.jpg /var/www/images/mosfet6_status.jpg")
conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("UPDATE MOSFET_Status SET MOSFET1_Status=?, MOSFET1_Override=?, MOSFET1_Override_Time=?, MOSFET2_Status=?, MOSFET2_Override=?, MOSFET2_Override_Time=?, MOSFET3_Status=?, MOSFET3_Override=?, MOSFET3_Override_Time=?, MOSFET4_Status=?, MOSFET4_Override=?, MOSFET4_Override_Time=?, MOSFET5_Status=?, MOSFET5_Override=?, MOSFET5_Override_Time=?, MOSFET6_Status=?, MOSFET6_Override=?, MOSFET6_Override_Time=?, MOSFET7_Status=?, MOSFET7_Override=?, MOSFET7_Override_Time=?, Override_State=?", (GPIO.input(12), "OFF", 0, GPIO.input(13), "OFF", 0, GPIO.input(15), "OFF", 0, GPIO.input(16), "OFF", 0, GPIO.input(18), "OFF", 0, GPIO.input(22), "OFF", 15, GPIO.input(11), "OFF", 0.5, 0))
conn.commit()
print "Completed."
print "------"
print ""

print "------"
print "Sending email notification of system restart now..."
subject = 'NZAquaPi - System Notification'
body = "Greetings!<br><br>This is a notification email to let you know that the NZAquaPi has just restarted.<br><br>Cheers,<br><br>Nathan"
session = smtplib.SMTP(str(email_SMTP_serv), str(email_SMTP_port))
session.ehlo()
session.starttls()
session.login(login_eml, login_ps)
headers = ["from: " + login_eml, "subject: " + subject, "to: " + recip_email, "mime-version: 1.0", "content-type: text/html"]
headers = "\r\n".join(headers)
session.sendmail(login_eml, recip_email, headers + "\r\n\r\n" + body)
session.quit()
print "Email sent!"
print "------"
print ""

# write log of events...
print "------"
curs.execute("SELECT COUNT(*) from System_Log")
result=curs.fetchone()
number_of_rows=result[0]
ID_to_use = number_of_rows + 1
print "Writing log into Database... (Id is #" + str(ID_to_use) + ")"
curs.execute("INSERT INTO System_Log VALUES(?, ?)", (ID_to_use, datetime.datetime.now()))
conn.commit()
conn.close()
print "Log written into DB."
print "------"
print ""

#startup_test()
