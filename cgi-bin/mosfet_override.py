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
curs.execute("SELECT MOSFET1_Status, MOSFET1_Override, MOSFET1_Override_Time, MOSFET2_Status, MOSFET2_Override, MOSFET2_Override_Time, MOSFET3_Status, MOSFET3_Override, MOSFET3_Override_Time, MOSFET4_Status, MOSFET4_Override, MOSFET4_Override_Time, MOSFET5_Status, MOSFET5_Override, MOSFET5_Override_Time, MOSFET6_Status, MOSFET6_Override, MOSFET6_Override_Time, MOSFET7_Status, MOSFET7_Override, MOSFET7_Override_Time, Override_State FROM MOSFET_Status")
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
        Override_State = row[21]
conn.close

if MOSFET1_Status == 0:
    MOSFET1_Status = "OFF"
else:
    MOSFET1_Status = "ON"
if MOSFET2_Status == 0:
    MOSFET2_Status = "OFF"
else:
    MOSFET2_Status = "ON"
if MOSFET3_Status == 0:
    MOSFET3_Status = "OFF"
else:
    MOSFET3_Status = "ON"
if MOSFET4_Status == 0:
    MOSFET4_Status = "OFF"
else:
    MOSFET4_Status = "ON"
if MOSFET5_Status == 0:
    MOSFET5_Status = "OFF"
else:
    MOSFET5_Status = "ON"
if MOSFET6_Status == 0:
    MOSFET6_Status = "OFF"
else:
    MOSFET6_Status = "ON"
if MOSFET7_Status == 0:
    MOSFET7_Status = "OFF"
else:
    MOSFET7_Status = "ON"

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
        OutputMOSFETS()
    else:
        print "<tr><td colspan=\"7\"><p>You do not have access to this page you cheeky bugger!</p></td></tr>"

def OutputMOSFETS():
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
	
    print "<tr><td colspan=\"7\"><h3>NZAquaPi - Manual MOSFET Override</h3></td></tr>"
    print "<tr><td colspan=\"7\">"
    print "<p>This page can be used for testing the MOSFETS (12V switches). From here you can manually turn on/off the fans, as well as drain/add water to the sump with the solenoids. USE WITH CARE!!</p>"
    print "<p>Initially shows current state of MOSFETS.</p><br>"
    print "<p>Setting Override to \"YES\" will toggle the state of the MOSFET, i.e. If MOSFET is ON will turn OFF and vise versa...</p><br>"
    print "<br>"
        
    print "<form action=\"/cgi-bin/mosfet_override.py\" method=\"POST\">"

    form=cgi.FieldStorage()
    if "mosfet1_override" in form:
        print "<p>DATA SAVED, will be executed in < 15 seconds. Return to main page via link above...</p>"
        curs.execute("UPDATE MOSFET_Status SET MOSFET1_Override=?, MOSFET1_Override_Time=?, MOSFET2_Override=?, MOSFET2_Override_Time=?, MOSFET3_Override=?, MOSFET3_Override_Time=?, MOSFET4_Override=?, MOSFET4_Override_Time=?, MOSFET5_Override=?, MOSFET5_Override_Time=?, MOSFET6_Override=?, MOSFET6_Override_Time=?, MOSFET7_Override=?, MOSFET7_Override_Time=?, Override_State=?", (form["mosfet1_override"].value, form["mosfet1_time"].value, form["mosfet2_override"].value, form["mosfet2_time"].value, form["mosfet3_override"].value, form["mosfet3_time"].value, form["mosfet4_override"].value, form["mosfet4_time"].value, form["mosfet5_override"].value, form["mosfet5_time"].value, form["mosfet6_override"].value, form["mosfet6_time"].value, form["mosfet7_override"].value, form["mosfet7_time"].value, 1))
        conn.commit()
        conn.close
    else:
        if Override_State == 1:
            print "<p>At least one of the MOSFET overrides is already switched on... Please wait for the override daemon to process this first!</p>"
        else:
            print "<form action=\"/cgi-bin/mosfet_override.py\" method=\"POST\">"
            print "<h3>Fan MOSFETS:</h3>"
            print("1. MOSFET #1: SUMP FAN (GPIO Pin 12) - Fan is currently {0}. Override: <select name=\"mosfet1_override\" size=\"1\">".format(MOSFET1_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet1_time\" size=\"1\">"    
            i = 0
            while i < 299:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 15
            print "<option value =\"300\">300</option></select> seconds. (NB: \"0\" switches indefinately)"
            print "<br>"
            print "<br>"
        
            print("2. MOSFET #2: HOOD EXHAUST FANS (GPIO Pin 13) - Fans are currently {0}. Override: <select name=\"mosfet2_override\" size=\"1\">".format(MOSFET2_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet2_time\" size=\"1\">"    
            i = 0
            while i < 299:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 15
            print "<option value =\"300\">300</option></select> seconds. (NB: \"0\" switches indefinately)"
            print "<br>"
            print "<br>"
        
            print("3. MOSFET #3: HOOD COOLING FANS (GPIO Pin 15) - Fans are currently {0}. Override: <select name=\"mosfet3_override\" size=\"1\">".format(MOSFET3_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet3_time\" size=\"1\">"    
            i = 0
            while i < 299:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 15
            print "<option value =\"300\">300</option></select> seconds. (NB: \"0\" switches indefinately)"
            print "<br>"
            print "<br>"
        
            print("4. MOSFET #4: CABINET EXHAUST FANS (GPIO Pin 16) - Fans are currently {0}. Override: <select name=\"mosfet4_override\" size=\"1\">".format(MOSFET4_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet4_time\" size=\"1\">"    
            i = 0
            while i < 299:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 15
            print "<option value =\"300\">300</option></select> seconds. (NB: \"0\" switches indefinately)"
            print "<br>"
            print "<br>"
        
            print "<h3>12V Liquid Solenoid MOSFETS:</h3>"
            print("1. MOSFET #5: WASTE SIPHON (GPIO Pin 18) - Solenoid is currently {0}. Override: <select name=\"mosfet5_override\" size=\"1\">".format(MOSFET5_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet5_time\" size=\"1\">"    
            i = 0
            while i < 299:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 15
            print "<option value =\"300\">300</option></select> seconds. (NB: \"0\" switches indefinately)"
            print "<br>"
            print "<br>"
  
            print("2. MOSFET #6: MAINS RESUPPLY (GPIO Pin 22) - Solenoid is currently {0}. Override: <select name=\"mosfet6_override\" size=\"1\">".format(MOSFET6_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet6_time\" size=\"1\">"    
            i = 15
            while i < 59:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 15
            print "<option value =\"60\">60</option></select> seconds. (NB: \"0\" switches indefinately - DISABLED)"
            print "<br>"
            print "<br>"
            
            print "<h3>Peristaltic Pump MOSFET:</h3>"
            print("MOSFET #7: Prime Doser (GPIO Pin 11) - Solenoid is currently {0}. Override: <select name=\"mosfet7_override\" size=\"1\">".format(MOSFET7_Status))
            print "<option value=\"OFF\" selected=\"selected\">OFF</option>"
            print "<option value=\"ON\">ON</option></select>"
            print "<select name=\"mosfet7_time\" size=\"1\">"    
            i = 0.5
            while i < 4.5:
                print("<option value =\"{0}\">{0}</option>".format(i))
                i = i + 0.5
            print "<option value =\"5\">5</option></select> seconds. (NB: \"0\" switches indefinately - DISABLED)"
            print "<br>"
            print "<br>"
            
            print "<input type=\"submit\" value=\"Submit\">"
            print "</form>"
    print "<br>"
    
    print "</td></tr></table>"
    
    print "</body>"
    print "</html>"

    sys.stdout.flush()


if __name__=="__main__":
    main()




