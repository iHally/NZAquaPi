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
dbname='/var/www/NZAquaPi_blog.db'

# import DB settings
conn=sqlite3.connect(dbname)
curs=conn.cursor()
curs.execute("SELECT * FROM blog ORDER BY id DESC")
rows=curs.fetchall()
conn.close()

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
        OutputBlogs()
    else:
        print "<tr><td colspan=\"7\"><p>You do not have access to this page you cheeky bugger!</p></td></tr>"

def OutputBlogs():
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
	
    print "<tr><td colspan=\"7\"><h3>Blog Settings</h3></td></tr>"
    print "<tr><td colspan=\"7\">"
    print "<p>This page is used for creating / editing / removing blog entries... fairly self explanatory stuff!!</p>"
    print "<br>"
        
    print "<form action=\"/cgi-bin/blog_settings.py\" method=\"POST\">"

    form=cgi.FieldStorage()
    
    if "load" in form:
        if form["blog_select"].value == "NEW":
            print "Create a new blog entry or load an old one?: <select name=\"blog_select\" size=\"1\">"
            print "<option value=\"NEW\" selected=\"selected\">NEW</option>"
            for row in rows:
                print("<option value=\"{0}\">{0}</option>".format(str(row[0])))
            print "</select>"
            print "<input type=\"submit\" name=\"load\" value=\"Load\">"
            print "<br>"
            print "Title: <input type=\"text\" value=\"\" name =\"title\" style=\"width: 50%;\">"
            print "Date: <input type=\"text\" value=\"\" name =\"main_date\">"
            print "<br>"
            print "<input type=\"text\" value=\"\" name =\"main_text\" style=\"width: 100%; height: 400px;\">"
            print "<br>"
            print "<input type=\"submit\" name=\"cancel\" value=\"Cancel\">"
            print "<input type=\"submit\" name=\"delete\" value=\"Delete\">"
            print "<input type=\"submit\" name=\"save\" value=\"Save\">"
        else:
            for row in rows:
                if str(row[0]) == form["blog_select"].value:
                    print "Create a new blog entry or load an old one?: <select name=\"blog_select\" size=\"1\">"
                    print "<option value=\"NEW\">NEW</option>"
                    for row2 in rows:
                        if str(row2[0]) == form["blog_select"].value:
                            print("<option value=\"{0}\" selected=\"selected\">{0}</option>".format(str(row2[0])))
                        else:
                            print("<option value=\"{0}\">{0}</option>".format(str(row2[0])))
                    print "</select>"
                    print "<input type=\"submit\" name=\"load\" value=\"Load\">"
                    print "<br>"
                    print("Title: <input type=\"text\" value=\"{0}\" name =\"title\" style=\"width: 50%;\">".format(str(row[1])))
                    print("Date: <input type=\"text\" value=\"{0}\" name =\"main_date\">".format(str(row[2])))
                    print "<br>"
                    print("<input type=\"text\" value=\"{0}\" name =\"main_text\" style=\"width: 100%; height: 400px;\">".format(str(row[3])))
                    print "<br>"
                    print "<input type=\"submit\" name=\"cancel\" value=\"Cancel\">"
                    print "<input type=\"submit\" name=\"delete\" value=\"Delete\">"
                    print "<input type=\"submit\" name=\"save\" value=\"Save\">"
    elif "cancel" in form:
        print "Blog entry cancelled"
    elif "delete" in form:
        if form["blog_select"].value == "NEW":
            print "You tried to 'DELETE' a 'NEW' entry you muppet...."
        else:
            print("id {0} titled \"{1}\" has been deleted.".format(form["blog_select"].value, form["title"].value))
            #run sql query to delete row
            conn=sqlite3.connect(dbname)
            curs=conn.cursor()    
            curs.execute("DELETE FROM blog WHERE id=?", (form["blog_select"].value))
            conn.commit()
            conn.close()
    elif "save" in form:
        if form["blog_select"].value == "NEW":
            if str(rows) == "[]":
                NEW_INDEX = 1
            else:       
                row=rows[0]     
                NEW_INDEX = int(row[0]) + 1
            #add new entry into sql
            conn=sqlite3.connect(dbname)
            curs=conn.cursor()    
            curs.execute("INSERT INTO blog VALUES(?, ?, ?, ?)", (NEW_INDEX, form["title"].value, form["main_date"].value, form["main_text"].value))
            conn.commit()
            conn.close()
            print("New blog entry titled \"{0}\" (index id: {1}) has been saved.".format(form["title"].value, NEW_INDEX))
        else: 
            print("Blog id {0} saved.".format(form["blog_select"].value))
            #update entry in sql
            conn=sqlite3.connect(dbname)
            curs=conn.cursor()    
            curs.execute("UPDATE blog SET title=?, date=?, html=? WHERE id=?", (form["title"].value, form["main_date"].value, form["main_text"].value, form["blog_select"].value))
            conn.commit()
            conn.close()
    else:
        print "Create a new blog entry or load an old one?: <select name=\"blog_select\" size=\"1\">"
        print "<option value=\"NEW\" selected=\"selected\">NEW</option>"
        for row in rows:
            print("<option value=\"{0}\">{0}</option>".format(str(row[0])))
        print "</select>"
        print "<input type=\"submit\" name=\"load\" value=\"Load\">"
        print "<br>"
        print "Title: <input type=\"text\" value=\"\" name =\"title\" style=\"width: 50%;\">"
        print "Date: <input type=\"text\" value=\"\" name =\"main_date\">"
        print "<br>"
        print "<input type=\"text\" value=\"\" name =\"main_text\" style=\"width: 100%; height: 400px;\">"
        print "<br>"
        print "<input type=\"submit\" name=\"cancel\" value=\"Cancel\">"
        print "<input type=\"submit\" name=\"delete\" value=\"Delete\">"
        print "<input type=\"submit\" name=\"save\" value=\"Save\">"
        
    print "</form>"
    print "<br>"
    print "</td></tr></table>"
    print "</body>"
    print "</html>"

    sys.stdout.flush()
   
if __name__=="__main__":
    main()




