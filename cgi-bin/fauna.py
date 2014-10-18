#!/usr/bin/env python

import sys
import cgi
import cgitb
import os

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

    print "<tr>"
    print "<td colspan=\"3\" style=\"vertical-align: top;\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">Rosy barb</h3><br><h4 class=\"inline\"><i>(Pethia conchonius)</i></h4><br><br>Max Size: 14cm<br>Lifespan: 5 years<br>"
    print "pH: 6-8<br>Hardness: 5-19dH<br>Temperature: 12-22<br>"
    print "<br>Diet: Omnivorours<br>Nature: Active, generally peacefull"
    print "<br><br>Details: The rosy barb is a subtropical freshwater cyprinid fish found in southern Asia from Afghanistan to Bangladesh."
    print "<br><br>Notes: We originally bought these fish as feeders for the turtles. The turtles however befriended them and they soon became life-long pals! Although the aquarium temperature is not optimal, they are very hardy and have adapted well to conditions."
    print "<br><br>External link: <a href=\"http://en.wikipedia.org/wiki/Rosy_barb\">http://en.wikipedia.org/wiki/Rosy_barb</a>"
    print "</td>"
    print "<td></td>"
    print "<td colspan=\"3\"\"><img src=\"/images/fish_rosybarb.jpg\" valign=\"top\" width=\"100%\"/></td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"3\" style=\"vertical-align: top;\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">Golden sucking loach (a.k.a. Bob)</h3><br><h4 class=\"inline\"><i>(Gyrinocheilus aymonieri)</i></h4><br><br>Max Size: 28cm<br>Lifespan: 8-10 years<br>"
    print "pH: 6-8<br>Hardness: 36-357ppm<br>Temperature: 22-26<br>"
    print "<br>Diet: Algae<br>Nature: Agressive, particularly to yellow / orange fish"
    print "<br><br>Details: Golden sucking catfish are a freshwater fish that is native to large parts of southeast Asia. They are most often seen in large rivers, occasionally entering flooded fields. They spend most of their time on flat surfaces, such as rocks, in flowing water, using its unusually formed inferior mouth to attach itself to rocks in stronger flows."
    print "<br><br>Notes: Bob is awesome. Bob was one of the first fish we bought. He has always been a bit of a character, and loves harrassing similar coloured fish. Now that he is bigger he has taken quite a liking to hitching a ride on the turtles shells and helps keep them clean of algae. We know he is a male due to the red pimples (breeding tubercles) on his nose."
    print "<br><br>External link: <a href=\"http://en.wikipedia.org/wiki/Gyrinocheilus_aymonieri\">http://en.wikipedia.org/wiki/Gyrinocheilus_aymonieri</a>"
    print "</td>"
    print "<td></td>"
    print "<td colspan=\"3\"\"><img src=\"/images/fish_bob.jpg\" valign=\"top\" width=\"100%\"/></td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"3\" style=\"vertical-align: top;\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">Red-tailed black shark (a.k.a. Ebony)</h3><br><h4 class=\"inline\"><i>(Epalzeorhynchos bicolor)</i></h4><br><br>Size: 15cm<br>Lifespan: 8 years<br>"
    print "pH: 6.8-7.5<br>Hardness: 5-15dH<br>Temperature: 22-26<br>"
    print "<br>Diet: Scavengers<br>Nature: Agressive chasers, but will rarely bite or harm other fish"
    print "<br><br>Details: The red-tailed black shark is a species of freshwater fish in the carp family, Cyprinidae. It is native to Thailand, and is currently critically endangered in the wild, but common in aquaria. There is no evidence that collection for the aquarium trade is responsible for the species' decline, and it is more likely that construction of dams and draining of swamps that took place during the 1970s was to blame."
    print "<br><br>Notes: Ebony generally keeps to herself and likes hiding under rocks and in hollowed out logs. "
    print "<br><br>External link: <a href=\"http://en.wikipedia.org/wiki/Red-tailed_black_shark\">http://en.wikipedia.org/wiki/Red-tailed_black_shark</a>"
    print "</td>"
    print "<td></td>"
    print "<td colspan=\"3\"\"><img src=\"/images/fish_ebony.jpg\" valign=\"top\" width=\"100%\"/></td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"3\" style=\"vertical-align: top;\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">Pearl Gourami (a.k.a. Boris, RIP Vladimir & Jemima)</h3><br><h4 class=\"inline\"><i>(Trichopodus leerii)</i></h4><br><br>Size: 12cm<br>Lifespan: 5-7 years<br>"
    print "pH: 7<br>Hardness: <br>Temperature: 22-28<br>"
    print "<br>Diet: Omnivorours<br>Nature: Very peaceful"
    print "<br><br>Details: The pearl gourami originates from Thailand, Malaysia, Sumatra, and Borneo. It occurs in lowland swamps with acidic water. This fish prefers the top and middle levels of the water."
    print "<br><br>Notes: These were some of the first fish we ever bought. Very chilled out fish. Unfortunately we lost our smallest one, Jemima in 2012 and Vladimir died just recently after continually getting pestered by the turtles. Vladimir was the first of the original fish friends that the turtles have eaten - bloodthirsty buggers... "
    print "<br><br>External link: <a href=\"http://en.wikipedia.org/wiki/Pearl_gourami\">http://en.wikipedia.org/wiki/Pearl_gourami</a>"
    print "</td>"
    print "<td></td>"
    print "<td colspan=\"3\"\"><img src=\"/images/fish_gourami.jpg\" valign=\"top\" width=\"100%\"/></td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "</table>"
    print "</body>"
    print "</html>"
        
    sys.stdout.flush()

if __name__=="__main__":
    main()




