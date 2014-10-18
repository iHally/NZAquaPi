#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb
import time
import datetime


# global variables
speriod=(15*60)-1
dbname='/var/www/NZAquaPi.db'

# main function
# This is where the program starts 
def main():

    cgitb.enable()

    # print the HTTP header
    print "Content-type: text/html\n\n"

    # start printing the page
    print "<html>"

    # print the page body
    print "<body>"
    print "<h2>NZAquaPi Settings Page</h2><br>"
    print "<p>Settings Saved...</p>"
    print "<br>"
    print "<p>Return to main page: <a href=\"MAIN.py\">HERE</a></p>"
    print "<br><br>"
    
    form=cgi.FieldStorage()
    
    print "<h3>Details:</h4>"
    print("<p>SMTP Server: {0}</p>".format(form["smtp_server"].value))
    print("<p>SMTP Port: {0}</p>".format(form["smtp_port"].value))
    print("<p>Login Email: {0}</p>".format(form["login_email"].value))
    print("<p>Login Password: {0}</p>".format(form["login_pass"].value))
    print("<p>Recipient Email: {0}</p>".format(form["recipient_email"].value))
    print "<p>---------------------</p>"
    print("<p>ATO Enabled: {0}</p>".format(form["ATO_enabled"].value))
    print("<p>ATO Optimal level: {0}</p>".format(form["ATO_optimal_level"].value))
    print("<p>ATO Drop: {0}</p>".format(form["ATO_drop"].value))
    print("<p>ATO Maxtime (Redundancy): {0}</p>".format(form["ATO_maxtime_redund"].value))
    print("<p>ATO Min: {0}</p>".format(form["ATO_min"].value))
    print("<p>AWC Enabled: {0}</p>".format(form["waterchange_enabled"].value))
    print("<p>AWC Method: {0}</p>".format(form["waterchange_method"].value))
    print("<p>AWC Level to Remove: {0}</p>".format(form["waterchange_leveltoremove"].value))
    print("<p>AWC Remove Time: {0}</p>".format(form["waterchange_removetime"].value))
    print("<p>AWC Add Time: {0}</p>".format(form["waterchange_addtime"].value))
    print("<p>AWC Schedule: {0}</p>".format(form["waterchange_schedule"].value))
    print("<p>AWC Schedule Time: {0}</p>".format(form["waterchange_schedule_time"].value))
    print("<p>AWC Email Confirmation: {0}</p>".format(form["AWC_email"].value))
    print "<p>---------------------</p>"
    print("<p>Sump Temp Sensor: {0}</p>".format(form["temp1"].value))
    print("<p>Sump Temp Sensor Name: {0}</p>".format(form["name1"].value))
    print("<p>Sump Min Alarm: {0}</p>".format(form["sump_min"].value))
    print("<p>Sump Min Alarm Temp: {0}</p>".format(form["sump_low_alarm"].value))
    print("<p>Sump Min Alarm Temp Ticks: {0}</p>".format(form["sump_low_alarm_time"].value))
    print("<p>Sump Max Alarm: {0}</p>".format(form["sump_max"].value))
    print("<p>Sump Max Alarm Temp: {0}</p>".format(form["sump_high_alarm"].value))
    print("<p>Sump Max Alarm Temp Ticks: {0}</p>".format(form["sump_high_alarm_time"].value))
    print("<p>Sump Heater: {0}</p>".format(form["sump_heater"].value))
    print("<p>Sump Heater On: {0}</p>".format(form["sump_heater_on"].value))
    print("<p>Sump Heater Off: {0}</p>".format(form["sump_heater_off"].value))
    print("<p>Sump Fans: {0}</p>".format(form["sump_fans"].value))
    print("<p>Sump Fans On: {0}</p>".format(form["sump_fans_on"].value))
    print("<p>Sump Fans Off: {0}</p>".format(form["sump_fans_off"].value))
    print("<p>Display Temp Sensor: {0}</p>".format(form["temp2"].value))
    print("<p>Display Temp Sensor Name: {0}</p>".format(form["name2"].value))
    print("<p>Display Min Alarm: {0}</p>".format(form["display_min"].value))
    print("<p>Display Min Alarm Temp: {0}</p>".format(form["display_low_alarm"].value))
    print("<p>Display Min Alarm Temp Ticks: {0}</p>".format(form["display_low_alarm_time"].value))
    print("<p>Display Max Alarm: {0}</p>".format(form["display_max"].value))
    print("<p>Display Max Alarm Temp: {0}</p>".format(form["display_high_alarm"].value))
    print("<p>Display Max Alarm Temp Ticks: {0}</p>".format(form["display_high_alarm_time"].value))
    print("<p>Display Heater: {0}</p>".format(form["display_heater"].value))
    print("<p>Display Heater On: {0}</p>".format(form["display_heater_on"].value))
    print("<p>Display Heater Off: {0}</p>".format(form["display_heater_off"].value))
    print("<p>Display Fans: {0}</p>".format(form["display_fans"].value))
    print("<p>Display Fans On: {0}</p>".format(form["display_fans_on"].value))
    print("<p>Display Fans Off: {0}</p>".format(form["display_fans_off"].value))
    print("<p>LDock Temp Sensor: {0}</p>".format(form["temp3"].value))
    print("<p>LDock Temp Sensor Name: {0}</p>".format(form["name3"].value))
    print("<p>LDock Max Alarm: {0}</p>".format(form["ldock_max"].value))
    print("<p>LDock Max Alarm Temp: {0}</p>".format(form["ldock_high_alarm"].value))
    print("<p>LDock Max Alarm Temp Ticks: {0}</p>".format(form["ldock_high_alarm_time"].value))
    print("<p>LDock Fans: {0}</p>".format(form["ldock_fans"].value))
    print("<p>LDock Fans On: {0}</p>".format(form["ldock_fans_on"].value))
    print("<p>LDock Fans Off: {0}</p>".format(form["ldock_fans_off"].value))
    print("<p>RDock Temp Sensor: {0}</p>".format(form["temp4"].value))
    print("<p>RDock Temp Sensor Name: {0}</p>".format(form["name4"].value))
    print("<p>RDock Max Alarm: {0}</p>".format(form["rdock_max"].value))
    print("<p>RDock Max Alarm Temp: {0}</p>".format(form["rdock_high_alarm"].value))
    print("<p>RDock Max Alarm Temp Ticks: {0}</p>".format(form["rdock_high_alarm_time"].value))
    print("<p>RDock Fans: {0}</p>".format(form["rdock_fans"].value))
    print("<p>RDock Fans On: {0}</p>".format(form["rdock_fans_on"].value))
    print("<p>RDock Fans Off: {0}</p>".format(form["rdock_fans_off"].value))
    print "<p>---------------------</p>"
    print("<p>RH Cabinet Sensor: {0}</p>".format(form["rh1"].value))
    print("<p>RH Cabinet Max Alarm: {0}</p>".format(form["rh_cabinet_max"].value))
    print("<p>RH Cabinet Max Alarm Temp: {0}</p>".format(form["rh_cabinet_high_alarm"].value))
    print("<p>RH Cabinet Max Alarm Temp Ticks {0}</p>".format(form["rh_cabinet_high_alarm_time"].value))
    print("<p>RH Cabinet Fans: {0}</p>".format(form["rh_cabinet_fans"].value))
    print("<p>RH Cabinet Fans On: {0}</p>".format(form["rh_cabinet_fans_on"].value))
    print("<p>RH Cabinet Fans Off: {0}</p>".format(form["rh_cabinet_fans_off"].value))
    print("<p>RHTemp Cabinet Max Alarm: {0}</p>".format(form["rhtemp_max"].value))
    print("<p>RHTemp Cabinet Max Alarm Temp: {0}</p>".format(form["rhtemp_high_alarm"].value))
    print("<p>RHTemp Cabinet Max Alarm Temp Ticks {0}</p>".format(form["rhtemp_high_alarm_time"].value))
    print("<p>RHTemp Cabinet Fans: {0}</p>".format(form["rhtemp_fans"].value))
    print("<p>RHTemp Cabinet Fans On: {0}</p>".format(form["rhtemp_fans_on"].value))
    print("<p>RHTemp Cabinet Fans Off: {0}</p>".format(form["rhtemp_fans_off"].value))
    print("<p>RH Hood Sensor: {0}</p>".format(form["rh2"].value))
    print("<p>RH Hood Max Alarm: {0}</p>".format(form["rh_hood_max"].value))
    print("<p>RH Hood Max Alarm Temp: {0}</p>".format(form["rh_hood_high_alarm"].value))
    print("<p>RH Hood Max Alarm Temp Ticks {0}</p>".format(form["rh_hood_high_alarm_time"].value))
    print("<p>RH Hood Fans: {0}</p>".format(form["rh_hood_fans"].value))
    print("<p>RH Hood Fans On: {0}</p>".format(form["rh_hood_fans_on"].value))
    print("<p>RH Hood Fans Off: {0}</p>".format(form["rh_hood_fans_off"].value))
    print("<p>RHTemp Hood Max Alarm: {0}</p>".format(form["rh2temp_max"].value))
    print("<p>RHTemp Hood Max Alarm Temp: {0}</p>".format(form["rh2temp_high_alarm"].value))
    print("<p>RHTemp Hood Max Alarm Temp Ticks {0}</p>".format(form["rh2temp_high_alarm_time"].value))
    print("<p>RHTemp Hood Fans: {0}</p>".format(form["rh2temp_fans"].value))
    print("<p>RHTemp Hood Fans On: {0}</p>".format(form["rh2temp_fans_on"].value))
    print("<p>RHTemp Hood Fans Off: {0}</p>".format(form["rh2temp_fans_off"].value))
    print "<p>---------------------</p>"
    print("<p>Photosensor 1: {0}</p>".format(form["light1"].value))
    print("<p>Photosensor 1 Low Level: {0}</p>".format(form["light1_low"].value))
    print("<p>Photosensor 2: {0}</p>".format(form["light2"].value))
    print("<p>Photosensor 2 Low Level: {0}</p>".format(form["light2_low"].value))
    print("<p>Light AM On: {0}</p>".format(form["light_AM_on"].value))
    print("<p>Light Lunch Off: {0}</p>".format(form["light_Lunch_off"].value))
    print("<p>Light Lunch On: {0}</p>".format(form["light_Lunch_on"].value))
    print("<p>Light PM Off: {0}</p>".format(form["light_PM_off"].value))
    print("<p>Light Tolerence: {0}</p>".format(form["light_tol"].value))
    print "<p>---------------------</p>"
    print("<p>Fluid Level Sensor: {0}</p>".format(form["fluid1"].value))

    print "<br>"
    print "<br>"
    print "</body>"
    print "</html>"
    
    AWC_Next_Day = 0
    CurrentHr = int(time.strftime("%H"))
    CurrentDay = int(time.strftime("%u"))
    if int(form["waterchange_schedule"].value) == 1:
        if int(form["waterchange_schedule_time"].value) > CurrentHr: # daily
            AWC_Next_Day = CurrentDay
        else:
            if CurrentDay == 7:
                AWC_Next_Day = 1
            else:
                AWC_Next_Day = CurrentDay + 1
    elif int(form["waterchange_schedule"].value) == 2: # alt daily
        if int(form["waterchange_schedule_time"].value) > CurrentHr:
            AWC_Next_Day = CurrentDay
        else:
            if CurrentDay > 5:
                AWC_Next_Day = CurrentDay - 5
            else:
                AWC_Next_Day = CurrentDay + 2
    if AWC_Next_Day == 1:
        AWC_Next_Day = "Monday"
    elif AWC_Next_Day == 2:
		AWC_Next_Day = "Tuesday"
    elif int(AWC_Next_Day) == 3:
		AWC_Next_Day = "Wednesday"
    elif AWC_Next_Day == 4:
		AWC_Next_Day = "Thursday"
    elif AWC_Next_Day == 5:
		AWC_Next_Day = "Friday"
    elif AWC_Next_Day == 6:
		AWC_Next_Day = "Saturday"
    elif AWC_Next_Day == 7:
		AWC_Next_Day = "Sunday"
    if int(form["waterchange_schedule"].value) == 3: # twice weekly - monday and thursday
        if CurrentDay == 1:
            if int(form["waterchange_schedule_time"]).value < CurrentHr:
                AWC_Next_Day = "Monday"
            else:
                AWC_Next_Day = "Thursday"
        elif CurrentDay == 2 or CurrentDay == 3:
            AWC_Next_Day = "Thursday"
        elif CurrentDay == 4:
            if int(form["waterchange_schedule_time"].value) < CurrentHr:
                AWC_Next_Day = "Thursday"
            else:
                AWC_Next_Day = "Monday"
        elif CurrentDay == 5 or CurrentDay == 6 or CurrentDay == 7:
            AWC_Next_Day = "Monday"
    elif int(form["waterchange_schedule"].value) == 4:
        AWC_Next_Day = "Monday"
    elif int(form["waterchange_schedule"].value) == 5:
        AWC_Next_Day = "Tuesday"
    elif int(form["waterchange_schedule"].value) == 6:
        AWC_Next_Day = "Wednesday"
    elif int(form["waterchange_schedule"].value) == 7:
        AWC_Next_Day = "Thursday"
    elif int(form["waterchange_schedule"].value) == 8:
        AWC_Next_Day = "Friday"
    elif int(form["waterchange_schedule"].value) == 9:
        AWC_Next_Day = "Saturday"
    elif int(form["waterchange_schedule"].value) == 10:
        AWC_Next_Day = "Sunday"
        
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()    
    curs.execute("UPDATE Email SET smtp_server=?, smtp_port=?, login_email_address=?, password_hash=?, recipient=?", (form["smtp_server"].value, form["smtp_port"].value, form["login_email"].value, form["login_pass"].value, form["recipient_email"].value))
    conn.commit()
    curs.execute("UPDATE ATO SET Status=?, Optimal_Level=?, Triggered_Drop=?, Max_Time=?, Sump_Min=?", (form["ATO_enabled"].value, form["ATO_optimal_level"].value, form["ATO_drop"].value, form["ATO_maxtime_redund"].value, form["ATO_min"].value))
    conn.commit()
    curs.execute("UPDATE AWC SET Status=?, Method=?, Remove_Amount=?, Remove_Time=?, Add_Time=?, Frequency=?, Frequency_Time=?, Frequency_Next_Day=?, Email_Confirmation=?", (form["waterchange_enabled"].value, form["waterchange_method"].value, form["waterchange_leveltoremove"].value, form["waterchange_removetime"].value, form["waterchange_addtime"].value, form["waterchange_schedule"].value, form["waterchange_schedule_time"].value, AWC_Next_Day, form["AWC_email"].value))
    conn.commit()
    curs.execute("UPDATE Temp_Display SET id=?, Min=?, Max=?, Heater_ON=?, Heater_OFF=?, Fan_ON=?, Fan_OFF=?, Status=?, Low_Alarm=?, Low_Time=?, High_Alarm=?, High_Time=?, Heater_Status=?, Fan_Status=?", (form["name2"].value, form["display_min"].value, form["display_max"].value, form["display_heater_on"].value, form["display_heater_off"].value, form["display_fans_on"].value, form["display_fans_off"].value, form["temp2"].value, form["display_low_alarm"].value, form["display_low_alarm_time"].value, form["display_high_alarm"].value, form["display_high_alarm_time"].value, form["display_heater"].value, form["display_fans"].value))
    conn.commit()
    curs.execute("UPDATE Temp_Sump SET id=?, Min=?, Max=?, Heater_ON=?, Heater_OFF=?, Fan_ON=?, Fan_OFF=?, Status=?, Low_Alarm=?, Low_Time=?, High_Alarm=?, High_Time=?, Heater_Status=?, Fan_Status=?", (form["name1"].value, form["sump_min"].value, form["sump_max"].value, form["sump_heater_on"].value, form["sump_heater_off"].value, form["sump_fans_on"].value, form["sump_fans_off"].value, form["temp1"].value, form["sump_low_alarm"].value, form["sump_low_alarm_time"].value, form["sump_high_alarm"].value, form["sump_high_alarm_time"].value, form["sump_heater"].value, form["sump_fans"].value))
    conn.commit()
    curs.execute("UPDATE Temp_LDock SET id=?, Max=?, Fan_ON=?, Fan_OFF=?, Status=?, High_Alarm=?, High_Time=?, Fan_Status=?", (form["name3"].value, form["ldock_max"].value, form["ldock_fans_on"].value, form["ldock_fans_off"].value, form["temp3"].value, form["ldock_high_alarm"].value, form["ldock_high_alarm_time"].value, form["ldock_fans"].value))
    conn.commit()
    curs.execute("UPDATE Temp_RDock SET id=?, Max=?, Fan_ON=?, Fan_OFF=?, Status=?, High_Alarm=?, High_Time=?, Fan_Status=?", (form["name4"].value, form["rdock_max"].value, form["rdock_fans_on"].value, form["rdock_fans_off"].value, form["temp4"].value, form["rdock_high_alarm"].value, form["rdock_high_alarm_time"].value, form["rdock_fans"].value))
    conn.commit()
    curs.execute("UPDATE RH_Cabinet SET Max=?, Fan_ON=?, Fan_OFF=?, Status=?, High_Alarm=?, High_Time=?, Temp_Max=?, Temp_Fan_ON=?, Temp_Fan_OFF=?, Temp_High_Alarm=?, Temp_High_Time=?, Fan_Status=?, Temp_Fan_Status=?", (form["rh_cabinet_max"].value, form["rh_cabinet_fans_on"].value, form["rh_cabinet_fans_off"].value, form["rh1"].value, form["rh_cabinet_high_alarm"].value, form["rh_cabinet_high_alarm_time"].value, form["rhtemp_max"].value, form["rhtemp_fans_on"].value, form["rhtemp_fans_off"].value, form["rhtemp_high_alarm"].value, form["rhtemp_high_alarm_time"].value, form["rh_cabinet_fans"].value, form["rhtemp_fans"].value))
    conn.commit()
    curs.execute("UPDATE RH_Hood SET Max=?, Fan_ON=?, Fan_OFF=?, Status=?, High_Alarm=?, High_Time=?, Temp_Max=?, Temp_Fan_ON=?, Temp_Fan_OFF=?, Temp_High_Alarm=?, Temp_High_Time=?, Fan_Status=?, Temp_Fan_Status=?", (form["rh_hood_max"].value, form["rh_hood_fans_on"].value, form["rh_hood_fans_off"].value, form["rh2"].value, form["rh_hood_high_alarm"].value, form["rh_hood_high_alarm_time"].value, form["rh2temp_max"].value, form["rh2temp_fans_on"].value, form["rh2temp_fans_off"].value, form["rh2temp_high_alarm"].value, form["rh2temp_high_alarm_time"].value, form["rh_hood_fans"].value, form["rh2temp_fans"].value))
    conn.commit()
    
    conn.close()
    
    sys.stdout.flush()

if __name__=="__main__":
    main()




