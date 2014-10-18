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
dbname='/var/www/NZAquaPi_stats.db'


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
        Stats()
    else:
        print "<tr><td colspan=\"7\"><p>You do not have access to this page you cheeky bugger!</p></td></tr>"

def Stats():
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
	
    print "<tr><td colspan=\"7\"><h3>User Stats...</h3></td></tr>"
    print "<tr><td colspan=\"7\">"
    
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT * FROM stats")
    rows=curs.fetchall()
    for row in rows:
        print("<p>Date: {0},   IP: {1},   Mac Address: {2}</p>".format(str(row[0]), str(row[1]), str(row[2])))
    conn.close()
        
    print "</td></tr></table>"
    print "</body>"
    print "</html>"

    sys.stdout.flush()
   
if __name__=="__main__":
    main()




