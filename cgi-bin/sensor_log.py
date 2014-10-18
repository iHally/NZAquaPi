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
newest_time = 0
temp_display = 0
temp_sump = 0
temp_rdock = 0
temp_ldock = 0
rhtemp_hood = 0
rhtemp_cabinet = 0
rh_hood = 0
rh_cabinet = 0
PhotoCell = 0
eTape = 0

cgitb.enable()

# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"

# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table1, table2, table3, table4):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    print_graph_script(table1, table2, table3, table4)
    print "</head>"


# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    if option == 1:
        curs.execute("SELECT * FROM Sensors_Log WHERE time>datetime('now', 'localtime' ,'-%s hours')" % 24)
    elif option == 2:
        curs.execute("SELECT * FROM Sensors_Log WHERE time>datetime('now', 'localtime' ,'-%s days')" % 7)
    elif option == 3:
        curs.execute("SELECT * FROM Sensors_Log WHERE time>datetime('now', 'localtime' ,'-%s days')" % 30)
    elif option == 4:
        curs.execute("SELECT * FROM Sensors_Log WHERE time>datetime('now', 'localtime' ,'-%s days')" % 365)
    elif option == 5:
        curs.execute("SELECT * FROM Sensors_Log")
    rows=curs.fetchall()
    conn.close()
    return rows

# get most recent values and store in global variables
def grab_newest_data(rows):
    row=rows[-1]
    global newest_time, temp_display, temp_sump, temp_ldock, temp_rdock, rhtemp_hood, rhtemp_cabinet, rh_hood, rh_cabinet, PhotoCell, eTape
    newest_time = row[0]
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
    
# convert rows from database into a javascript table - FOR TEMPERATURES
def create_temp_table(rows):
    chart_table=""
    for row in rows[:-1]:
        properdate=time.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        dateinrow="new Date({0},{1},{2},{3},{4},{5})".format(properdate.tm_year, properdate.tm_mon - 1, properdate.tm_mday, properdate.tm_hour, properdate.tm_min, properdate.tm_sec)
        rowstr="[{0}, {1}, {2}, {3}, {4}, {5}, {6}],\n".format(dateinrow,str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[6]),str(row[8]))
        chart_table+=rowstr
    row=rows[-1]
    rowstr="[{0}, {1},  {2}, {3}, {4}, {5}, {6}]\n".format(dateinrow,str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[6]),str(row[8]))
    chart_table+=rowstr
    return chart_table
    
# convert rows from database into a javascript table - FOR RELATIVE HUMIDITY
def create_RH_table(rows):
    chart_table=""
    for row in rows[:-1]:
        properdate=time.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        dateinrow="new Date({0}, {1}, {2}, {3}, {4}, {5})".format(properdate.tm_year, properdate.tm_mon - 1, properdate.tm_mday, properdate.tm_hour, properdate.tm_min, properdate.tm_sec)
        rowstr="[{0}, {1}, {2}],\n".format(dateinrow,str(row[5]),str(row[7]))
        chart_table+=rowstr
    row=rows[-1]
    rowstr="[{0}, {1}, {2}]\n".format(dateinrow,str(row[5]),str(row[7]))
    chart_table+=rowstr
    return chart_table  

# convert rows from database into a javascript table - FOR PHOTOCELL
def create_PhotoCell_table(rows):
    chart_table=""
    for row in rows[:-1]:
        properdate=time.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        dateinrow="new Date({0}, {1}, {2}, {3}, {4}, {5})".format(properdate.tm_year, properdate.tm_mon - 1, properdate.tm_mday, properdate.tm_hour, properdate.tm_min, properdate.tm_sec)
        rowstr="[{0}, {1}],\n".format(dateinrow,str(row[9]))
        chart_table+=rowstr
    row=rows[-1]
    rowstr="[{0}, {1}]\n".format(dateinrow,str(row[9]))
    chart_table+=rowstr
    return chart_table  
    
# convert rows from database into a javascript table - FOR ETAPE
def create_eTape_table(rows):
    chart_table=""
    for row in rows[:-1]:
        properdate=time.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
        dateinrow="new Date({0}, {1}, {2}, {3}, {4}, {5})".format(properdate.tm_year, properdate.tm_mon - 1, properdate.tm_mday, properdate.tm_hour, properdate.tm_min, properdate.tm_sec)
        rowstr="[{0}, {1}],\n".format(dateinrow,str(row[10]))
        chart_table+=rowstr
    row=rows[-1]
    rowstr="[{0}, {1}]\n".format(dateinrow,str(row[10]))
    chart_table+=rowstr
    return chart_table  

# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table1, table2, table3, table4):

    # google chart snippet
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawALL);
      function drawChart1() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime','Date');
        data.addColumn('number','Display');
        data.addColumn('number','Sump');
        data.addColumn('number','LDock');
        data.addColumn('number','RDock');
        data.addColumn('number','Cabinet');
        data.addColumn('number','Hood');
        data.addRows([
          %s
        ]);
        var options = {title: 'Temperature', curveType: 'function', hAxis: {format: 'MMM d, y - a'}, chartArea: {height: '500'}};
        var chart = new google.visualization.LineChart(document.getElementById('chart1_div'));
        chart.draw(data, options);
      }
      function drawChart2() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime','Date');
        data.addColumn('number','Cabinet');
        data.addColumn('number','Hood');
        data.addRows([
          %s
        ]);
        var options = {title: 'Relative Humidity', curveType: 'function', hAxis: {format: 'MMM d, y - a'}, chartArea: {height: '500'}};
        var chart = new google.visualization.LineChart(document.getElementById('chart2_div'));
        chart.draw(data, options);
      }
      function drawChart3() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime','Date');
        data.addColumn('number','Photocell');
        data.addRows([
          %s
        ]);
        var options = {title: 'Photocell', curveType: 'function', hAxis: {format: 'MMM d, y - a'}, chartArea: {height: '500'}};
        var chart = new google.visualization.LineChart(document.getElementById('chart3_div'));
        chart.draw(data, options);
      }
      function drawChart4() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime','Date');
        data.addColumn('number','eTape');
        data.addRows([
          %s
        ]);
        var options = {title: 'eTape', curveType: 'function', hAxis: {format: 'MMM d, y - a'}, chartArea: {height: '500'}};
        var chart = new google.visualization.LineChart(document.getElementById('chart4_div'));
        chart.draw(data, options);
      }
      function drawALL() {
        drawChart1();
        drawChart2();
        drawChart3();
        drawChart4();
      }
    </script>"""
    
    print chart_code % (table1, table2, table3, table4)

# print the div that contains the graph
def show_graph():
    print '<div id="chart1_div" style="width: 80%; height: 600px; margin:0 auto;"></div>'
    print '<p></p>'
    print '<div id="chart2_div" style="width: 80%; height: 600px; margin:0 auto;"></div>'
    print '<p></p>'
    print '<div id="chart3_div" style="width: 80%; height: 600px; margin:0 auto;"></div>'
    print '<p></p>'
    print '<div id="chart4_div" style="width: 80%; height: 600px; margin:0 auto;"></div>'
    print '<p></p>'

# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None:
        option = str(24)

    curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestamp>datetime('now','-%s hour')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmax[0]),str(rowmax[1]))

    curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('now','-%s hour')" % option)
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('now','-%s hour')" % option)
    rowavg=curs.fetchone()


    print "<hr>"


    print "<h2>Minumum temperature&nbsp</h2>"
    print rowstrmin
    print "<h2>Maximum temperature</h2>"
    print rowstrmax
    print "<h2>Average temperature</h2>"
    print "%.2f" % rowavg+"C"

    print "<hr>"

    print "<h2>In the last hour:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>"

    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-1 hour')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td></tr>".format(str(row[0]),str(row[1]))
        print rowstr
    print "</table>"

    print "<hr>"

    conn.close()

def print_time_selector(option):

    print """<form action="/cgi-bin/sensor_log.py" method="POST">
        Show the temperature logs for  
        <select name="timeinterval">"""


    if option is not None:

        if option == "1":
            print "<option value=\"1\" selected=\"selected\">the last 24 hours</option>"
        else:
            print "<option value=\"1\">the last 24 hours</option>"

        if option == "2":
            print "<option value=\"2\" selected=\"selected\">the last 7 days</option>"
        else:
            print "<option value=\"2\">the last 7 days</option>"

        if option == "3":
            print "<option value=\"3\" selected=\"selected\">the last month (30 Days)</option>"
        else:
            print "<option value=\"3\">the last month (30 Days)</option>"
            
        if option == "4":
            print "<option value=\"4\" selected=\"selected\">the last year</option>"
        else:
            print "<option value=\"4\">the last year</option>"
            
        if option == "5":
            print "<option value=\"5\" selected=\"selected\">all data</option>"
        else:
            print "<option value=\"5\">all data</option>"    

    else:
        print """<option value="1">the last 24 hours</option>
            <option value="2">the last 7 days</option>
            <option value="3">the last month (30 Days)</option>
            <option value="4">the last year</option>
            <option value="5" selected="selected">all data</option>"""
            

    print """        </select>
        <input type="submit" value="Display">
    </form>"""

#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        return form["timeinterval"].value
    else:
        return 1

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

    # get options that may have been passed to this script
    option=get_option()

    # get data from the database
    records=get_data(option)

    # print the HTTP header
    printHTTPheader()

    if len(records) != 0:
        # convert the data into a table
        grab_newest_data(records)
        table1=create_temp_table(records)
        table2=create_RH_table(records)
        table3=create_PhotoCell_table(records)
        table4=create_eTape_table(records)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    
    #printHTMLHead("Nathan's AquaPi", table1, table2, table3)

    print "<head>"
    #print "<title>"
    #print title
    #print "</title>"

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
    #print "width: 20%;"
    print "}"
    print "-->"
    print "</style>"
    print_graph_script(table1, table2, table3, table4)
    
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

    OutputSensorLogs(option)

def OutputSensorLogs(option):
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
	
    print "<tr><td colspan=\"7\"><h3>AquaPi Graphical Logs</h3></td></tr>"
    print "<tr><td colspan=\"7\">"

    print_time_selector(option)
    print "<br />"
    print "<br />"
    print "</td></tr></table>"
    
    #print "<h3>Historical Data:</h3>"
    show_graph()
    
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()




