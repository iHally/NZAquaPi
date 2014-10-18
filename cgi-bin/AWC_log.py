#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb
import os

# global variables
speriod=(15*60)-1
dbname='/var/www/NZAquaPi.db'

# main function
# This is where the program starts 
def main():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT Status, Method, Remove_Amount, Remove_Time, Add_Time, Frequency, Frequency_Time, Email_Confirmation, Frequency_Next_Day FROM AWC")
    for row in curs:
        AWC_on = row[0]
        AWC_method = row[1]
        AWC_remove_amt = row[2]
        AWC_remove_time = row[3]
        AWC_add_time = row[4]
        AWC_freq = row[5]
        AWC_time = row[6]
        AWC_Email_Confirmation = row[7]
        AWC_Next_Day = row[8]
    conn.close

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

    print "<head>"

    # set background
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
    print "}"
    print "-->"
    print "</style>"
    print "</head>"

#start printing page body
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

    print "<tr>"
    print "<th></th>"
    print "<th></th>"
    print "<th><a href=\"sensor_log.py\"><img src=\"../images/button_sensors.jpg\" onmouseover=\"this.src='/images/button_sensors_hover.jpg'\" onmouseout=\"this.src='/images/button_sensors.jpg'\" id=\"button_sensors\" width=\"95%\"></a></th>"
    print "<th><a href=\"AWC_log.py\"><img src=\"../images/button_AWC.jpg\" onmouseover=\"this.src='/images/button_AWC_hover.jpg'\" onmouseout=\"this.src='/images/button_AWC.jpg'\" id=\"button_AWC\" width=\"95%\"></a></th>"
    print "<th><a href=\"not_created.py\"><img src=\"../images/button_ATO.jpg\" onmouseover=\"this.src='/images/button_ATO_hover.jpg'\" onmouseout=\"this.src='/images/button_ATO.jpg'\" id=\"button_ATO\" width=\"95%\"></a></th>"
    print "<th></th>"
    print "<th></th>"
    print "</tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
	
    print "<tr><td colspan=\"7\"><h3>NZAquaPi AWC (Automatic Water Change) Log</h3></td></tr>"
    print "<tr><td colspan=\"7\">"

    print "<br><br>"
    
    print "<h3>Current Settings:</h4>"
    print "<br>"
    print("<p>AWC Status: {0}</p>".format(AWC_on))
    print("<p>AWC Method: {0}</p>".format(AWC_method))
    print "<br>"
    
    print("<p>Remove Amount (eTape Method only): {0}</p>".format(AWC_remove_amt))
    print("<p>Remove Time: {0}</p>".format(AWC_remove_time))
    print("<p>Add Time: {0}</p>".format(AWC_add_time))
    print("<p>Frequency: {0}</p>".format(AWC_freq))
    print("<p>Frequency Next Day: {0}</p>".format(AWC_Next_Day))
    print("<p>Frequency Time: {0}</p>".format(AWC_time))
    print "<br>"
    
    curs.execute("SELECT * FROM AWC_Log")
    rows=curs.fetchall()
    for row in rows:
        print("<p>ID: {0}, Siphon began: {1}, Siphon finished: {2}, Intake opened: {3}, Intake closed: {4}, Email Sent: {5}</p>".format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])))
    conn.close()
    
    print "</td></tr></table>"
    print "</body>"
    print "</html>"
        
    sys.stdout.flush()

if __name__=="__main__":
    main()




