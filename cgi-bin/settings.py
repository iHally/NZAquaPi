#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb
import time
import datetime
import os

# global variables
speriod=(15*60)-1
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
curs.execute("SELECT Status, Optimal_Level, Triggered_Drop, Max_Time, Sump_Min FROM ATO")
for row in curs:
        ATO_on = row[0]
        ATO_opt_level = row[1]
        ATO_drp = row[2]
        ATO_maxtime = row[3]
        ATO_min = row[4]
curs.execute("SELECT Status, Method, Remove_Amount, Remove_Time, Add_Time, Frequency, Frequency_Time, Email_Confirmation FROM AWC")
for row in curs:
        AWC_on = row[0]
        AWC_method = row[1]
        AWC_remove_amt = row[2]
        AWC_remove_time = row[3]
        AWC_add_time = row[4]
        AWC_freq = row[5]
        AWC_time = row[6]
        AWC_Email_Confirmation = row[7]
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

# main function
# This is where the program starts 
def main():

    ADMINIP1 = "192.168.1.3" #Wifi - Games PC
    ADMINIP2 = "192.168.1.4" #Wifi - Mobile Phone
    ADMINIP3 = "101.168.85.62" #3G - Mobile Phone
    IsAdmin = 0
    UserIP = 0
    UserIP = cgi.escape(os.environ["REMOTE_ADDR"])
    if UserIP == ADMINIP1: 
        IsAdmin = 1
    if UserIP == ADMINIP2: 
        IsAdmin = 1
    if UserIP == ADMINIP3:
        IsAdmin = 1
    
    cgitb.enable()

# print the HTTP header
    print "Content-type: text/html\n\n"

# start printing the page
    print "<html>"

# set background
    print "<head>"
    print "<style type=\"text/css\">"
    print "<!--"
    print "body"
    print "{"
    print "background-image:url(/images/background.jpg);"
    print "background-repeat:repeat-y;"
    print "background-position:center;"
    print "background-size:100% 5%;"
    print "}"
    print "-->"
    print "</style>"

# set main table properties
    print "<style type=\"text/css\">"
    print "<!--"
    print "table#main_table"
    print "{"
    print "    border: 0px solid black;"
    print "    table-layout: fixed;"
    print "    width: 70%;"
    print "    margin-left:15%;"
    print "    margin-right:15%;"
    print "}"
    print "th, td#main_table"
    print "{"
    print "    border: 0px solid white;"
    print "    overflow: hidden;"
    print "    width: 20%;"
    print "}"
    print "-->"
    print "</style>"
    
# set footer table properties
    print "<style type=\"text/css\">"
    print "<!--"
    print "table#footer_table"
    print "{"
    print "    border: 0px solid white;"
    print "    table-layout: fixed;"
    print "    width: 70%;"
    print "    margin-left:15%;"
    print "    margin-right:15%;"
    print "}"
    print "th, td#footer_table"
    print "{"
    print "    border: 0px solid black;"
    print "    overflow: hidden;"
    #print "width: 20%;"
    print "}"
    print "-->"
    print "</style>"
    print "</head>"

# print the page body
    print "<body>"
    print "<table id=\"main_table\">"
    print "<tr>"
    print "<th colspan=\"7\">"
    print "<br>"
    print "<img src=\"../images/banner.jpg\" id=\"banner\" width=\"85%\"/>"
    print "</th>"
    print "</tr>"
    print "<tr>"
    print "<th></th>"
    print "<th><a href=\"MAIN.py\"><img src=\"/images/button_home.jpg\" onmouseover=\"this.src='/images/button_home_hover.jpg'\" onmouseout=\"this.src='/images/button_home.jpg'\" id=\"button_home\" width=\"95%\"></a></th>"
    print "<th><a href=\"blog.py\"><img src=\"../images/button_info.jpg\" onmouseover=\"this.src='/images/button_info_hover.jpg'\" onmouseout=\"this.src='/images/button_info.jpg'\" id=\"button_info\" width=\"95%\"></a></th>"
    print "<th><a href=\"/phpBB3/\"><img src=\"../images/button_forum.jpg\" onmouseover=\"this.src='/images/button_forum_hover.jpg'\" onmouseout=\"this.src='/images/button_forum.jpg'\" id=\"button_forum\" width=\"95%\"></a></th>"
    print "<th><a href=\"sensor_log.py\"><img src=\"../images/button_logs.jpg\" onmouseover=\"this.src='/images/button_logs_hover.jpg'\" onmouseout=\"this.src='/images/button_logs.jpg'\" id=\"button_logs\" width=\"95%\"></a></th>"
    if IsAdmin == 1:
        print "<th><a href=\"settings.py\"><img src=\"../images/button_settings.jpg\" onmouseover=\"this.src='/images/button_settings_hover.jpg'\" onmouseout=\"this.src='/images/button_settings.jpg'\" id=\"button_settings\" width=\"95%\"></a></th>"
    else:
        print "<th><a href=\"not_created.py\"><img src=\"../images/button_about.jpg\" onmouseover=\"this.src='/images/button_about_hover.jpg'\" onmouseout=\"this.src='/images/button_about.jpg'\" id=\"button_settings\" width=\"95%\"></a></th>"
    print "<th></th>"
    print "</tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"

    if IsAdmin == 1:
        OutputSettings()
    else:
        print "<tr><td colspan=\"7\"><p>You do not have access to this page you cheeky bugger!</p></td></tr>"
    
def OutputSettings():   
    print "<tr>"
    print "<th></th>"
    print "<th></th>"
    print "<th><a href=\"settings.py\"><img src=\"../images/button_main.jpg\" onmouseover=\"this.src='/images/button_main_hover.jpg'\" onmouseout=\"this.src='/images/button_main.jpg'\" id=\"button_main\" width=\"95%\"></a></th>"
    print "<th><a href=\"mosfet_override.py\"><img src=\"../images/button_mosfets.jpg\" onmouseover=\"this.src='/images/button_mosfets_hover.jpg'\" onmouseout=\"this.src='/images/button_mosfets.jpg'\" id=\"button_mosfets\" width=\"95%\"></a></th>"
    print "<th><a href=\"blog_settings.py\"><img src=\"../images/button_blogs.jpg\" onmouseover=\"this.src='/images/button_blogs_hover.jpg'\" onmouseout=\"this.src='/images/button_blogs.jpg'\" id=\"button_blogs\" width=\"95%\"></a></th>"
    print "<th><a href=\"stats.py\"><img src=\"../images/button_stats.jpg\" onmouseover=\"this.src='/images/button_stats_hover.jpg'\" onmouseout=\"this.src='/images/button_stats.jpg'\" id=\"button_stats\" width=\"95%\"></a></th>"
    print "<th></th>"
    print "</tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
	
    print "<tr><td colspan=\"7\"><h3>NZAquaPi Settings Page</h3></td></tr>"
    print "<tr><td colspan=\"7\">"
    print "<p>Below you will find settings that can be modified to chance the behaviour of the NZAquaPi Aquarium Controller. ENJOY!</p>"
    print "<br>"
    print "<form action=\"/cgi-bin/settings_saved.py\" method=\"POST\">"
    
    print "<h3>Email Information</h3>"
    print("1. SMTP server: <input type=\"text\" value=\"{0}\" name =\"smtp_server\">".format(email_SMTP_serv))
    print "<br>"
    print("2. SMTP port: <input type=\"text\" value=\"{0}\" name =\"smtp_port\">".format(email_SMTP_port))
    print "<br>"
    print("3. Login email address: <input type=\"text\" value=\"{0}\" name =\"login_email\">".format(login_eml))
    print "<br>"
    print("4. Login password: <input type=\"text\" value=\"{0}\" name =\"login_pass\">".format(login_ps))
    print "<br>"
    print("5. Recipient email: <input type=\"text\" value=\"{0}\" name =\"recipient_email\">".format(recip_email))
    
    print "<h3>Auto-Top Off (ATO) & Auto Water Change Information:</h3>"
    
    print "1. ATO Enabled? <select name=\"ATO_enabled\" size=\"1\">"
    if ATO_on == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print "<option value=\"DISABLED\">Disabled</option></select>"
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select>"
    print "<br>"
    print "<blockquote>"
    
    print "a) Optimal Sump water level: <select name=\"ATO_optimal_level\" size=\"1\">"
    i = 250
    while i < 351:
        if i == ATO_opt_level:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 10
    if i == ATO_opt_level:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> mm".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> mm".format(i))
    print "<br>"
    
    print "b) Water level drop before enabled: <select name=\"ATO_drop\" size=\"1\">"
    i = 20
    while i < 71:
        if i == ATO_drp:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 20
    if i == ATO_drp:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> mm".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> mm".format(i))
    print "<br>"
    
    print "c) Max time before pump off (redundancy): <select name=\"ATO_maxtime_redund\" size=\"1\">"
    i = 15
    while i < 151:
        if i == ATO_maxtime:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 30
    if i == ATO_maxtime:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> sec".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> sec".format(i))
    print "<br>"
    
    print "d) Minimum Sump water level: <select name=\"ATO_min\" size=\"1\">"
    i = 140
    while i < 241:
        if i == ATO_min:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 10
    if i == ATO_min:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> mm".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> mm".format(i))
    print "</blockquote>"
    
    print "2. Auto Water-Change Enabled? <select name=\"waterchange_enabled\" size=\"1\">"
    if AWC_on == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print "<option value=\"DISABLED\">Disabled</option></select>"
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select>"
    print "<br>"
    print "<blockquote>"
    
    print "a) Method for water change: <select name=\"waterchange_method\" size=\"1\">"
    if AWC_method == "eTape":
        print "<option value=\"eTape\" selected=\"selected\">eTape Liquid Level Sensor</option>"
        print "<option value=\"Manual\">Manual Solenoid run times</option></select>"
    else:
        print "<option value=\"eTape\">eTape Liquid Level Sensor</option>"
        print "<option value=\"Manual\" selected=\"selected\">Manual Solenoid run times</option></select>"
    print "<br>"
    print "<blockquote>"
    
    print "i) eTape - Water level to remove <select name=\"waterchange_leveltoremove\" size=\"1\">"
    i = 30
    while i < 161:
        if i == AWC_remove_amt:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 10
    if i == AWC_remove_amt:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> mm".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> mm".format(i))
    print "<br>"
    
    print "ii) Manual Times - Remove water for <select name=\"waterchange_removetime\" size=\"1\">"
    i = 30
    while i < 590:
        if i == AWC_remove_time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 30
    if i == AWC_remove_time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> sec (NB: Removal via syphon)".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> sec (NB: Removal via syphon)".format(i))
    print "<br>"
    
    print "iii) Manual Times - Add water for <select name=\"waterchange_addtime\" size=\"1\">"
    i = 15
    while i < 166:
        if i == AWC_add_time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 15
    if i == AWC_add_time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> sec (NB: Addition under pressure from mains)".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> sec (NB: Addition under pressure from mains)".format(i))
    print "</blockquote>"
    
    print "b) Frequency of water change: <select name=\"waterchange_schedule\" size=\"1\">"
    i = 1
    while i < 10:
        if i == AWC_freq:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == AWC_freq:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<blockquote>"
    print "1. Once Daily<br>"
    print "2. Alt Daily<br>"
    print "3. Twice Weekly (Mon/Thurs)<br>"
    print "4. Monday<br>"
    print "5. Tuesday<br>"
    print "6. Wednesday<br>"
    print "7. Thursday<br>"
    print "8. Friday<br>"
    print "9. Saturday<br>"
    print "10. Sunday<br>"
    #print "11. Once Fortnightly (Sun)<br>"
    print "</blockquote>"
    
    print "c) Time of water change: <select name=\"waterchange_schedule_time\" size=\"1\">"
    if AWC_time == "0":
        print "<option value=\"0\" selected=\"selected\">0</option>"
    else:
        print "<option value=\"0\">0</option>"
    i = 1
    while i < 23:
        if i == AWC_time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == AWC_time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "d) Email confirmation upon completion of AWC? <select name=\"AWC_email\" size=\"1\">"
    if AWC_Email_Confirmation == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print "<option value=\"DISABLED\">Disabled</option></select>"
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select>"
    print "</blockquote>"
    
    print "<h3>Sensor Information:</h3><h4>Temperature Sensors:</h4>"
    print "1. Sump (Waterproof DB18B20) - <select name=\"temp1\" size=\"1\">"
    if Temp_Sump_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print("<option value=\"DISABLED\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name1\">".format(Temp_Sump_id))
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print("<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name1\">".format(Temp_Sump_id))
    print "<br>"
    print "<blockquote>"
    
    print "a) Alarm Minimum: <select name=\"sump_min\" size=\"1\">"
    i = 15
    while i < 30:
        if i == Temp_Sump_Min:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Min:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"sump_low_alarm\" size=\"1\">"
    if Temp_Sump_Low_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
    
    print "Alarm after (x) consecutive low readings: <select name=\"sump_low_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == Temp_Sump_Low_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Low_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "b) Alarm Maximum: <select name=\"sump_max\" size=\"1\">"
    i = 20
    while i < 35:
        if i == Temp_Sump_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"sump_high_alarm\" size=\"1\">"
    if Temp_Sump_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
    
    print "Alarm after (x) consecutive low readings: <select name=\"sump_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == Temp_Sump_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "c) Can turn heater on? <select name=\"sump_heater\" size=\"1\">"
    
    if Temp_Sump_Heater_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print " Temp on: <select name=\"sump_heater_on\" size=\"1\">"
    i = 15
    while i < 30:
        if i == Temp_Sump_Heater_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Heater_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Temp off: <select name=\"sump_heater_off\" size=\"1\">"
    i = 20
    while i < 35:
        if i == Temp_Sump_Heater_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Heater_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "<br>"
        
    print "d) Can turn cooling fans on? <select name=\"sump_fans\" size=\"1\">"
    if Temp_Sump_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "Temp on: <select name=\"sump_fans_on\" size=\"1\">"
    i = 20
    while i < 35:
        if i == Temp_Sump_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Temp off: <select name=\"sump_fans_off\" size=\"1\">"
    i = 15
    while i < 30:
        if i == Temp_Sump_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Sump_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "</blockquote>"
    
    
    # DISPLAY TEMP SENSOR
    print "2. Display (Waterproof DB18B20) - <select name=\"temp2\" size=\"1\">"
    if Temp_Display_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print("<option value=\"DISABLED\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name2\">".format(Temp_Display_id))
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print("<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name2\">".format(Temp_Display_id))
    print "<br>"
    print "<blockquote>"
    
    print "a) Alarm Minimum: <select name=\"display_min\" size=\"1\">"
    i = 15
    while i < 30:
        if i == Temp_Display_Min:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Min:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"display_low_alarm\" size=\"1\">"
    if Temp_Display_Low_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
    
    print "Alarm after (x) consecutive low readings: <select name=\"display_low_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == Temp_Display_Low_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Low_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "b) Alarm Maximum: <select name=\"display_max\" size=\"1\">"
    i = 20
    while i < 35:
        if i == Temp_Display_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"display_high_alarm\" size=\"1\">"
    if Temp_Display_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
    
    print "Alarm after (x) consecutive low readings: <select name=\"display_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == Temp_Display_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "c) Can turn heater on? <select name=\"display_heater\" size=\"1\">"
    if Temp_Display_Heater_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print " Temp on: <select name=\"display_heater_on\" size=\"1\">"
    i = 15
    while i < 30:
        if i == Temp_Display_Heater_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Heater_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Temp off: <select name=\"display_heater_off\" size=\"1\">"
    i = 20
    while i < 35:
        if i == Temp_Display_Heater_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Heater_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "<br>"
        
    print "d) Can turn cooling fans on? <select name=\"display_fans\" size=\"1\">"
    if Temp_Display_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "Temp on: <select name=\"display_fans_on\" size=\"1\">"
    i = 20
    while i < 35:
        if i == Temp_Display_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Temp off: <select name=\"display_fans_off\" size=\"1\">"
    i = 15
    while i < 30:
        if i == Temp_Display_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_Display_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "</blockquote>"
    

    #Sensor #3
    print "3. Left Dock (Waterproof DB18B20) - <select name=\"temp3\" size=\"1\">"
    if Temp_LDock_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print("<option value=\"DISABLED\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name3\">".format(Temp_LDock_id))
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print("<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name3\">".format(Temp_LDock_id))
    print "<br>"
    print "<blockquote>"
    
    print "a) Alarm Maximum: <select name=\"ldock_max\" size=\"1\">"
    i = 20
    while i < 45:
        if i == Temp_LDock_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_LDock_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"ldock_high_alarm\" size=\"1\">"
    if Temp_LDock_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
    
    print "Alarm after (x) consecutive low readings: <select name=\"ldock_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == Temp_LDock_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_LDock_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "b) Can turn cooling fans on? <select name=\"ldock_fans\" size=\"1\">"
    if Temp_LDock_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "Temp on: <select name=\"ldock_fans_on\" size=\"1\">"
    i = 20
    while i < 45:
        if i == Temp_LDock_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_LDock_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Temp off: <select name=\"ldock_fans_off\" size=\"1\">"
    i = 15
    while i < 40:
        if i == Temp_LDock_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_LDock_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "</blockquote>"
    
    
    # SENSOR #4
    print "4. Right Dock (Waterproof DB18B20) - <select name=\"temp4\" size=\"1\">"
    if Temp_RDock_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print("<option value=\"DISABLED\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name4\">".format(Temp_RDock_id))
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print("<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select> - Sensor ID: <input type=\"text\" value=\"{0}\" name =\"name4\">".format(Temp_RDock_id))
    print "<br>"
    print "<blockquote>"
    
    print "a) Alarm Maximum: <select name=\"rdock_max\" size=\"1\">"
    i = 20
    while i < 45:
        if i == Temp_RDock_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_RDock_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"rdock_high_alarm\" size=\"1\">"
    if Temp_RDock_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
    
    print "Alarm after (x) consecutive low readings: <select name=\"rdock_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == Temp_RDock_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_RDock_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "b) Can turn cooling fans on? <select name=\"rdock_fans\" size=\"1\">"
    if Temp_RDock_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "Temp on: <select name=\"rdock_fans_on\" size=\"1\">"
    i = 20
    while i < 45:
        if i == Temp_RDock_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_RDock_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Temp off: <select name=\"rdock_fans_off\" size=\"1\">"
    i = 15
    while i < 40:
        if i == Temp_RDock_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == Temp_RDock_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "</blockquote>"
    
    # HUMIDITY SENSORS 1 & 2
    print "<h4>Humidity Sensors (+ Temperature):</h4>"
    print "1. Cabinet (AM3032 / Wired DHT22) - <select name=\"rh1\" size=\"1\">"
    if RH_Cabinet_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print "<option value=\"DISABLED\">Disabled</option></select> (GPIO #23)"
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select> (GPIO #23)"
    print "<br>"
    print "<blockquote>"
    
    print "a) RH - Alarm Maximum: <select name=\"rh_cabinet_max\" size=\"1\">"
    i = 50
    while i < 96:
        if i == RH_Cabinet_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 5
    if i == RH_Cabinet_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> RH,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> RH,".format(i))
    
    print "Alarm enabled? <select name=\"rh_cabinet_high_alarm\" size=\"1\">"
    if RH_Cabinet_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
        
    print "Alarm after (x) consecutive low readings: <select name=\"rh_cabinet_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == RH_Cabinet_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Cabinet_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "b) RH - Can turn exhaust fans on? <select name=\"rh_cabinet_fans\" size=\"1\">"
    if RH_Cabinet_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "RH on: <select name=\"rh_cabinet_fans_on\" size=\"1\">"
    i = 50
    while i < 96:
        if i == RH_Cabinet_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 5
    if i == RH_Cabinet_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> RH,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> RH,".format(i))
    
    print "RH off: <select name=\"rh_cabinet_fans_off\" size=\"1\">"
    i = 30
    while i < 86:
        if i == RH_Cabinet_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 5
    if i == RH_Cabinet_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> RH".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> RH".format(i))
    print "<br>"
    
    print "c) Temp - Alarm Maximum: <select name=\"rhtemp_max\" size=\"1\">"
    i = 25
    while i < 50:
        if i == RH_Cabinet_Temp_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Cabinet_Temp_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"rhtemp_high_alarm\" size=\"1\">"
    if RH_Cabinet_Temp_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
        
    print "Alarm after (x) consecutive high readings: <select name=\"rhtemp_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == RH_Cabinet_Temp_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Cabinet_Temp_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "d) Temp - Can turn exhaust fans on? <select name=\"rhtemp_fans\" size=\"1\">"
    if RH_Cabinet_Temp_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "Temp on: <select name=\"rhtemp_fans_on\" size=\"1\">"
    i = 25
    while i < 50:
        if i == RH_Cabinet_Temp_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Cabinet_Temp_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
        
    print "Temp off: <select name=\"rhtemp_fans_off\" size=\"1\">"
    i = 25
    while i < 50:
        if i == RH_Cabinet_Temp_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Cabinet_Temp_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "</blockquote>"
    print "<br>"
    
    
    #Humidity Sensor #2
    print "2. Hood (AM3032 / Wired DHT22) - <select name=\"rh2\" size=\"1\">"
    if RH_Hood_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">Enabled</option>"
        print "<option value=\"DISABLED\">Disabled</option></select> (GPIO #24)"
    else:
        print "<option value=\"ENABLED\">Enabled</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">Disabled</option></select> (GPIO #24)"
    print "<br>"
    print "<blockquote>"
    
    print "a) RH - Alarm Maximum: <select name=\"rh_hood_max\" size=\"1\">"
    i = 50
    while i < 96:
        if i == RH_Hood_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 5
    if i == RH_Hood_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> RH,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> RH,".format(i))
    
    print "Alarm enabled? <select name=\"rh_hood_high_alarm\" size=\"1\">"
    if RH_Hood_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
        
    print "Alarm after (x) consecutive low readings: <select name=\"rh_hood_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == RH_Hood_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Hood_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "b) RH - Can turn exhaust fans on? <select name=\"rh_hood_fans\" size=\"1\">"
    if RH_Hood_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "RH on: <select name=\"rh_hood_fans_on\" size=\"1\">"
    i = 50
    while i < 96:
        if i == RH_Hood_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 5
    if i == RH_Hood_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> RH,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> RH,".format(i))
    
    print "RH off: <select name=\"rh_hood_fans_off\" size=\"1\">"
    i = 30
    while i < 86:
        if i == RH_Hood_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 5
    if i == RH_Hood_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> RH".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> RH".format(i))
    print "<br>"
    
    print "c) Temp - Alarm Maximum: <select name=\"rh2temp_max\" size=\"1\">"
    i = 25
    while i < 50:
        if i == RH_Hood_Temp_Max:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Hood_Temp_Max:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
    
    print "Alarm enabled? <select name=\"rh2temp_high_alarm\" size=\"1\">"
    if RH_Hood_Temp_High_Alarm == "ON":
        print "<option value=\"ON\" selected=\"selected\">ON</option>"
        print "<option value=\"OFF\">OFF</option></select>"
    else:
        print "<option value=\"ON\">ON</option>"
        print "<option value=\"OFF\" selected=\"selected\">OFF</option></select>"
        
    print "Alarm after (x) consecutive high readings: <select name=\"rh2temp_high_alarm_time\" size=\"1\">"
    i = 1
    while i < 5:
        if i == RH_Hood_Temp_High_Time:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Hood_Temp_High_Time:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select>".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select>".format(i))
    print "<br>"
    
    print "d) Temp - Can turn exhaust fans on? <select name=\"rh2temp_fans\" size=\"1\">"
    if RH_Hood_Temp_Fan_Status == "ENABLED":
        print "<option value=\"ENABLED\" selected=\"selected\">YES</option>"
        print "<option value=\"DISABLED\">NO</option></select>"
    else:
        print "<option value=\"ENABLED\">YES</option>"
        print "<option value=\"DISABLED\" selected=\"selected\">NO</option></select>"
        
    print "Temp on: <select name=\"rh2temp_fans_on\" size=\"1\">"
    i = 25
    while i < 50:
        if i == RH_Hood_Temp_Fan_ON:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Hood_Temp_Fan_ON:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c,".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c,".format(i))
        
    print "Temp off: <select name=\"rh2temp_fans_off\" size=\"1\">"
    i = 25
    while i < 50:
        if i == RH_Hood_Temp_Fan_OFF:
            print("<option value =\"{0}\" selected=\"selected\">{0}</option>".format(i))
        else:
            print("<option value =\"{0}\">{0}</option>".format(i))
        i = i + 1
    if i == RH_Hood_Temp_Fan_OFF:
        print("<option value =\"{0}\" selected=\"selected\">{0}</option></select> &deg;c".format(i))
    else:
        print("<option value =\"{0}\">{0}</option></select> &deg;c".format(i))
    print "</blockquote>"
    print "<br>"
    print '''
    

<h4>Light Sensors:</h4>
1. Left T5 Photocell - <select name="light1" size="1"> 
  <option>Disabled</option>
  <option>Enabled</option></select> Pre-determined "Low" level: <select name="light1_low" size="1">
          <option>300</option>
          <option>400</option>
          <option>500</option>
          <option>600</option>
          <option>700</option>
          <option>800</option>
          <option>900</option>
          <option>1000</option>
          <option>1100</option>
          <option>1200</option>
          <option>1300</option>
          <option>1400</option>
          <option>1500</option></select> (Analog Pin 0)
<br>
2. Right T5 Photocell - <select name="light2" size="1"> 
  <option>Disabled</option>
  <option>Enabled</option></select> Pre-determined "Low" level: <select name="light2_low" size="1">
          <option>300</option>
          <option>400</option>
          <option>500</option>
          <option>600</option>
          <option>700</option>
          <option>800</option>
          <option>900</option>
          <option>1000</option>
          <option>1100</option>
          <option>1200</option>
          <option>1300</option>
          <option>1400</option>
          <option>1500</option></select> (Analog Pin 1)
<blockquote>
a) Usual AM Lights ON: <select name="light_AM_on" size="1">
          <option>0400</option>
          <option>0430</option>
          <option>0500</option>
          <option>0530</option>
          <option>0600</option>
          <option>0630</option>
          <option>0700</option>
          <option>0730</option>
          <option>0800</option>
          <option>0830</option>
          <option>0900</option>
          <option>0930</option>
          <option>1000</option></select>
<br>
b) Usual Lunch Lights OFF: <select name="light_Lunch_off" size="1">
          <option>1000</option>
          <option>1030</option>
          <option>1100</option>
          <option>1130</option>
          <option>1200</option>
          <option>1230</option>
          <option>1300</option>
          <option>1330</option>
          <option>1400</option>
          <option>1430</option>
          <option>1500</option>
          <option>1530</option></select>
<br>
c) Usual Lunch Lights ON: <select name="light_Lunch_on" size="1">
          <option>1200</option>
          <option>1230</option>
          <option>1300</option>
          <option>1330</option>
          <option>1400</option>
          <option>1430</option>
          <option>1500</option>
          <option>1530</option>
          <option>1600</option>
          <option>1630</option>
          <option>1700</option>
          <option>1730</option></select>
<br>
d) Usual PM Lights OFF: <select name="light_PM_off" size="1">
          <option>1700</option>
          <option>1730</option>
          <option>1800</option>
          <option>1830</option>
          <option>1900</option>
          <option>1930</option>
          <option>2000</option>
          <option>2030</option>
          <option>2100</option>
          <option>2130</option>
          <option>2200</option>
          <option>2230</option></select>
<br>
e) Tolerance: <select name="light_tol" size="1">
          <option>15</option>
          <option>30</option>
          <option>45</option>
          <option>60</option>
          <option>75</option>
          <option>90</option>
          <option>105</option>
          <option>120</option></select> min
</blockquote>
<h4>Fluid Level Sensors:</h4>
1. Sump Fluid Level (12" eTape) - <select name="fluid1" size="1"> 
  <option>Disabled</option>
  <option>Enabled</option></select> (Analog Pin 2)

<br>
<br>
<input type="submit" value="Submit">
</form>
'''

    print "</td></tr></table>"


    print "</body>"
    print "</html>"

    sys.stdout.flush()
    
if __name__=="__main__":
    main()




