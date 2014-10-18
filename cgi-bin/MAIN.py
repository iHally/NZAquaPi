#!/usr/bin/env python

import sys
import cgi
import cgitb
import os
import sqlite3
import datetime

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
    from uuid import getnode as get_mac
    #MAC = get_mac()
    #dbname='/var/www/NZAquaPi.db'
    #conn=sqlite3.connect(dbname)
    #curs=conn.cursor()
    #curs.execute("INSERT INTO stats VALUES(strftime('%d-%m-%Y, %H:%M', 'now', 'localtime'), ?, ?)", (UserIP, MAC))
    #conn.commit()
    #conn.close()
    
    dbname='/var/www/NZAquaPi.db'
    
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

    print "<script>"
    print "(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){"
    print "(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),"
    print "m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)"
    print "})(window,document,'script','//www.google-analytics.com/analytics.js','ga');"
    print "ga('create', 'UA-48217871-1', 'nzaquapi.com');"
    print "ga('send', 'pageview');"
    print "</script>"

    print "<script type=\"text/javascript\">"
    print "var CheckForChanges = function() {"
    print "    document.getElementById(\"image1\").src=\"../images/mosfet1_status.jpg?rand=\" + Math.random();"
    print "    document.getElementById(\"image2\").src=\"../images/mosfet2_status.jpg?rand=\" + Math.random();"
    print "    document.getElementById(\"image3\").src=\"../images/mosfet3_status.jpg?rand=\" + Math.random();"
    print "    document.getElementById(\"image4\").src=\"../images/mosfet4_status.jpg?rand=\" + Math.random();"
    print "    document.getElementById(\"image5\").src=\"../images/mosfet5_status.jpg?rand=\" + Math.random();"
    print "    document.getElementById(\"image6\").src=\"../images/mosfet6_status.jpg?rand=\" + Math.random();"
    print "};"   
    print "window.onload = function() {"
    print "    setInterval(CheckForChanges, 1000);"
    print "};"
    print "</script>"
    
    
    
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
    
    # set mosfet table properties
    print "<style type=\"text/css\">"
    print "<!--"
    print "table#mosfet_table"
    print "{"
    print "    border: 2px solid blue;"
    print "    table-layout: fixed;"
    print "    width: 80%;"
    print "    margin-left:10%;"
    print "    margin-right:10%;"
    print "}"
    print "th, td#mosfet_table"
    print "{"
    print "    border: 0px solid white;"
    print "    overflow: hidden;"
    #print "width: 20%;"
    print "}"
    print "-->"
    print "</style>"
    
    print "</head>"
    
    # set sensor table properties
    print "<style type=\"text/css\">"
    print "<!--"
    print "table#sensor_table"
    print "{"
    print "    border: 2px solid blue;"
    print "    table-layout: fixed;"
    print "    width: 80%;"
    print "    margin-left:10%;"
    print "    margin-right:10%;"
    print "}"
    print "th, td#sensor_table"
    print "{"
    print "    border: 0px solid white;"
    print "    overflow: hidden;"
    #print "width: 20%;"
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
    #print "<table align=\"center\" width=\"80%\" border=\"1\">"
    #print "<table align=\"center\" width=\"70%\">"
    print "<tr>"
    print "<th colspan=\"7\">"
    print "<br>"
    print "<img src=\"../images/banner.jpg\" id=\"banner\" width=\"85%\"/>"
    print "</th>"
    print "</tr>"
    #print "<tr><th colspan=\"7\"><hr></th></tr>"
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
    
    print "<tr><th colspan=\"7\">Welcome to my website, NZAquaPi. First let me explain the name... my initials are NZ, I am not from New Zealand. The name 'AquaPi' has been used by several who"
    print "have created DIY aquarium controllers using a Raspberry Pi. I have built upon several ideas to design my own controller that I will be using to control my 6 foot (+ sump) freshwater aquarium."
    print "This aquarium is being designed as an upgrade from our current 4 foot tank and is home to our 2 maclaey river turtles, Bruce and Lucy." 
    print "<br><br>This site has been designed for 2 purposes. Firstly, to allow me to visually display and remotely control many of the tanks automated functions, such as water and air temperature control, "
    print "humidity control, automated water changes and automated top off after water evaporation. The second purpose is to share with you my design and implemenation throughout this project, "
    print "hopefully inspiring you to create your own DIY masterpiece. Although I purchased the tank and sump ready made (with bulkheads drilled), all of the cabinet/hood making, plumbing and electrical/electronic work I have done myself over the last 6 months."
    print "I am slowly getting there, but have a ways to go.<br><br>Please have a browse of this site, subscribe to the emailing list and even post your comments/suggestings in the forum.<br><br>Thanks for stopping by, Nathan</th></tr>"
    
    
    print "<tr>"
    print "<th rowspan=\"8\" colspan=\"3\"><br><img src=\"../images/camera.jpg\" id=\"camera\" width=\"80%\"/><br><br></th>"
    
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT * FROM Sensors_Log ORDER BY Time")
    #SELECT * FROM TABLE ORDER BY ID DESC LIMIT 1
    rows=curs.fetchall()
    conn.close()
    row=rows[-1]
    newest_time = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
    temp_display = row[1]
    temp_sump = row[2]
    temp_ldock = row[3]
    temp_rdock = row[4]
    rh_hood = row[5]
    rhtemp_hood = row[6]
    rh_cabinet = row[7]
    rhtemp_cabinet = row[8]
    PhotoCell = row[9]
    eTape = row[10]
    
    print "<th rowspan=\"8\" colspan=\"2\">"
    print "<table id=\"sensor_table\">"
    print "<tr>"
    print "<th colspan=\"3\"><p style=\"color:black\">Sensors:</p></th>"
    print "</tr>"
    print "<tr><th colspan=\"3\"><hr></th></tr>"
    print("<tr><th colspan=\"3\">(Time Taken: {0})</th></tr>".format(datetime.datetime.strftime(newest_time, '%d-%m-%Y, %H:%M',)))
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Ambient Temp</p></th>"
    print "<th><p style=\"color:black\">N/A</p></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Ambient RH</p></th>"
    print "<th><p style=\"color:black\">N/A</p></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Cabinet Temp</p></th>"
    print("<th><p style=\"color:black\">{0}&deg;c</p></th>".format(rhtemp_cabinet))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Cabinet RH</p></th>"
    print("<th><p style=\"color:black\">{0}%</p></th>".format(rh_cabinet))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Sump Temp</p></th>"
    print("<th><p style=\"color:black\">{0}&deg;c</p></th>".format(temp_sump))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Display Temp</p></th>"
    print("<th><p style=\"color:black\">{0}&deg;c</p></th>".format(temp_display))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">LDock Temp</p></th>"
    print("<th><p style=\"color:black\">{0}&deg;c</p></th>".format(temp_ldock))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">RDock Temp</p></th>"
    print("<th><p style=\"color:black\">{0}&deg;c</p></th>".format(temp_rdock))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Hood Temp</p></th>"
    print("<th><p style=\"color:black\">{0}&deg;c</p></th>".format(rhtemp_hood))
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Hood RH</p></th>"
    print("<th><p style=\"color:black\">{0}%</p></th>".format(rh_hood))
    print "</tr>"
    print "</table>"
    print "</th>"
    
    print "<th rowspan=\"8\" colspan=\"2\">"
    print "<table id=\"mosfet_table\">"
    print "<tr>"
    print "<th colspan=\"3\"><p style=\"color:black\">Mosfet Status:</p></th>"
    print "</tr>"
    print "<tr><th colspan=\"3\"><hr></th></tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Sump fan</p></th>"
    print "<th><img src=\"../images/mosfet1_status.jpg\" id=\"image1\" width=\"40px\" height=\"40px\"/></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Hood exhaust fans</p></th>"
    print "<th><img src=\"../images/mosfet2_status.jpg\" id=\"image2\" width=\"40px\" height=\"40px\"/></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Hood fans</p></th>"
    print "<th><img src=\"../images/mosfet3_status.jpg\" id=\"image3\" width=\"40px\" height=\"40px\"/></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Cabinet exhaust fans</p></th>"
    print "<th><img src=\"../images/mosfet4_status.jpg\" id=\"image4\" width=\"40px\" height=\"40px\"/></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Waste solenoid</p></th>"
    print "<th><img src=\"../images/mosfet5_status.jpg\" id=\"image5\" width=\"40px\" height=\"40px\"/></th>"
    print "</tr>"
    print "<tr>"
    print "<th colspan =\"2\"><p style=\"color:black\">Inlet solenoid</p></th>"
    print "<th><img src=\"../images/mosfet6_status.jpg\" id=\"image6\" width=\"40px\" height=\"40px\"/></th>"
    print "</tr>"
    print "</table>"
    print "</th>"
    print "</tr>"
    
    #print "<tr><th colspan=\"7\"><hr></th></tr>"
    #print "<tr><th colspan=\"7\">Site created by Nathan Zipf. Hosted on my Raspberry Pi. Coded in Python, HTML/CSS and Javascript and utilising a Sqlite3 database.</th></tr>"
    print "</table>"
    print "<table id=\"footer_table\">"
    print "<tr>"
    print "<th>"
    print "<p style=\"font-size:10px\">Site created by Nathan Zipf. Hosted on my Raspberry Pi. Coded in Python, HTML/CSS and Javascript and utilising a Sqlite3 database.</p>"
    print "</th>"
    print "</tr>"
    print "</table>"
   
    
    print "</body>"
    print "</html>"
        
    sys.stdout.flush()

if __name__=="__main__":
    main()




