#!/usr/bin/env python

import sys
import cgi
import cgitb
import os
import sqlite3
import smtplib

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
    
    print "h4.inline {"
    print "display: inline; }"
    print "h3.inline {"
    print "display: inline; }"
    
    
    print "</style>"

# add javascript email checker
    print "<script type=\"text/javascript\">"
    print "function validateForm() {"
    print "    var x=document.forms[\"subscribe_to_blog\"][\"email\"].value;"
    print "    var atpos=x.indexOf(\"@\");"
    print "    var dotpos=x.lastIndexOf(\".\");"
    print "    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length) {"
    print "        alert(\"Not a valid e-mail address\");"
    print "        return false;"
    print "    };"   
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
    print "<tr>"
    print "<th></th>"
    print "<th></th>"
    print "<th><a href=\"blog.py\"><img src=\"../images/button_blog.jpg\" onmouseover=\"this.src='/images/button_blog_hover.jpg'\" onmouseout=\"this.src='/images/button_blog.jpg'\" id=\"button_blog\" width=\"95%\"></a></th>"
    print "<th><a href=\"making_of.py\"><img src=\"../images/button_makingof.jpg\" onmouseover=\"this.src='/images/button_makingof_hover.jpg'\" onmouseout=\"this.src='/images/button_makingof.jpg'\" id=\"button_makingof\" width=\"95%\"></a></th>"
    print "<th><a href=\"fauna.py\"><img src=\"../images/button_fauna.jpg\" onmouseover=\"this.src='/images/button_fauna_hover.jpg'\" onmouseout=\"this.src='/images/button_fauna.jpg'\" id=\"button_fauna\" width=\"95%\"></a></th>"
    print "<th><a href=\"flora.py\"><img src=\"../images/button_flora.jpg\" onmouseover=\"this.src='/images/button_flora_hover.jpg'\" onmouseout=\"this.src='/images/button_flora.jpg'\" id=\"button_flora\" width=\"95%\"></a></th>"
    print "<th></th>"
    print "</tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    form=cgi.FieldStorage()
    if "subscribe" in form:
        print "<tr><td colspan=\"7\" style=\"text-align: center;\">Your email has been added to the email list. Please check your email for a confirmation... (to make sure it went to the right place!) Cheers!</td></tr>"
        print "<tr><td colspan=\"7\"><hr></td></tr>"
        #add email to database
        dbname='/var/www/NZAquaPi_blog.db'
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("INSERT INTO mailing_list VALUES(?, ?, strftime('%d-%m-%Y, %H:%M', 'now', 'localtime'))", (form["email"].value, "1"))
        conn.commit()
        conn.close()
        #send verification email
        dbname='/var/www/NZAquaPi.db'
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("SELECT smtp_server, smtp_port, login_email_address, password_hash FROM Email")
        for row in curs:
			email_SMTP_serv = row[0]
			email_SMTP_port = row[1]
			login_eml = row[2]
			login_ps = row[3]
        recip_email = form["email"].value
        subject = 'NZAquaPi - Email Subscription Notification'
        body = "Greetings!<br><br>This is a notification email to let you know that you are now subscribed to my mailing list. You will now receive an email whenever a new blog is posted! GOOD JOB!<br><br>Cheers,<br><br>Nathan<br><br><br><br><br><br>(To unsubscribe, just send an email to admin@nzaquapi.com and i'll remove you from the list.)<br>"
        session = smtplib.SMTP(str(email_SMTP_serv), str(email_SMTP_port))
        session.ehlo()
        session.starttls()
        session.login(login_eml, login_ps)
        login_eml = "admin@nzaquapi.com"
        headers = ["from: " + login_eml, "subject: " + subject, "to: " + recip_email, "mime-version: 1.0", "content-type: text/html"]
        headers = "\r\n".join(headers)
        session.sendmail(login_eml, recip_email, headers + "\r\n\r\n" + body)
        session.quit()
    else:
        print "<form name =\"subscribe_to_blog\" action=\"/cgi-bin/blog.py\" onsubmit=\"return validateForm();\" method=\"POST\">"
        print "<tr><td colspan=\"7\" style=\"text-align: center;\">Subscribe to mailing list: <input type=\"text\" name =\"email\"><input type=\"submit\" name=\"subscribe\" value=\"Submit\"></td></tr>"
        print "</form>"
        print "<tr><td colspan=\"7\"><hr></td></tr>"

    dbname='/var/www/NZAquaPi_blog.db'
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT * FROM blog ORDER BY id DESC")
    rows=curs.fetchall()
    for row in rows:
        print("<tr><td colspan=\"6\"><h2 align=left>{0}</h2></td><td><h4>{1}</h4></td></tr><tr><td colspan=\"7\">{2}</td></tr><tr><td colspan=\"7\"><hr></td></tr>".format(str(row[1]), str(row[2]), str(row[3])))
    conn.close()
  
    print "</table>"
    print "</body>"
    print "</html>"
        
    sys.stdout.flush()

if __name__=="__main__":
    main()




