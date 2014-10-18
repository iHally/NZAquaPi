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
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">Contents</h3><br><br>"
    print "1. Cabinet Design<br>"
    print "2. Hood Design<br>"
    print "3. Plumbing<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Display <-> Sump Plumbing<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Additional Sump Plumbing<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c) Still to do...<br>"
    print "4. Electricals and DIY Controller<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Lighting<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) DIY Controller<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) Introduction<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii) Parts List<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iii) Sensors<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iv) Solenoids<br>&nbsp;&nbsp;&nbsp;&nbsp;v) eTape<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vi) Fans<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vii) Webcam<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;viii) Software<br>"
    print "5. Background<br>"
    print "6. Finished Product / Final thoughts<br>"
    print "<br>"
    print "Change Log:"
    print "<br>18.02.2014 6:30PM - Initial info copied from old forums to here. NOT YET FORMATTED, PICS AND LINKS NOT WORKING. INFO NEEDS UPDATING AS WELL...<br>"
    print "<br>16.03.2014 9:25AM - Fixed links to pictures and external sites<br>"
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">1. Cabinet Design</h3><br><br>"
    print "<br><br>TBA.<br><br>"
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">2. Hood Design</h3><br><br>"
    print "<br><br>TBA.<br><br>"
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">3. Plumbing</h3><br><br>"
    
    print "<b>Plumbing:</b><br><br>"
    print "Firstly, I must give credit where credit is due. The basis for by Display->Sump plumbing has been borrowed from Brett and Lee's 8 foot build which they were kind enough to document in a <a href=\"http://www.australianfreshwaterturtles.com.au/forum/showthread.php?9904-8ft-Tank-Build/page5\">very informative thread</a>.<br><br>"
    print "Initial talk on the design of my plumbing was done with Brett and others in <a href=\"http://www.australianfreshwaterturtles.com.au/forum/showthread.php?11107-Our-next-tank-6x2x2-(-sump)\">this thread</a> (a while ago, it has taken me a LONG time to complete the design!)<br><br>"
    
    print "<b>Sump plumbing:</b><br><br>"
    print "Because I wanted to design a system that would allow for automatic water changes and ATO (Auto Top-off), a bit of extra plumbing was required. After a lot of thought and a few redesigns, I have finished with the following:<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/empty_sump_front.JPG\" width=\"80%\"/></p><br>"
    print "This pic shows the general flow of water from the display, through the sump then back to the display again. Section 1 is mechanical filtration, section 2 is biological filtration utilizing DIY containers that sit on top of each other all holding ceramic noodles. Section 3 is reserved from the return pump, electronics for measure water level, heaters and a bit of purogen.<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/empty_sump_side.JPG\" width=\"50%\"/></p><br>"
    print "The floor of the cabinet is kitchen whiteboard. I then cut another sheet of the whiteboard that the sump sits on, and then attached door handles. This allows me to remove the plumbing from the sump and slide the sump out of the cabinet for easy installation / cleaning etc. Whiteboard on whiteboard is surprisingly low friction and it slides easily when the sump is empty. It is unlikely you will be able to slide it if the sump is full, which is why I designed a water drain function (detailed below) which would be done before attempting to move the sump.<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/pipes1.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/pipes2.JPG\" width=\"80%\"/></p><br>"
    print "I will use the numbers in the 2 pictures above to try to explain what each bit is and why it is necessary:<br><br>"
    print "<b>1, 2 + 4.</b> barrel unions. Lets me remove sections of the plumbing when needed. I undo (1) and the sump bulkheads (6) allowing me to push the inner part of the sump bulkhead out behind the sump so I can slide the sump out.<br><br>"
    print "<b>3.</b> <a href=\"http://www.adafruit.com/products/997\">12V Plastic Solenoid</a>. Will be connected to the Raspberry Pi. Applying power to it opens the valve, allowing the siphon to begin removing water from the tank (detailed below).<br><br>"
    print "<b>5.</b> I just realised that I did not put in a number 5. My bad!<br><br>"
    print "<b>6.</b> Bulkheads. These have 90 degree angles attached to the inside pointing upwards. If the water level in the sump gets dangerously high, it drains into the 90 degree angles and through the plumbing behind the cabinet, coming back into the cabinet at (1). Before people ask 'But why did you bring the plumbing back inside the cabinet before going through the floor? Why not have all that plumbing behind the cabinet?' - I would have liked to do this, in fact this was the original plan, however right where the cabinet is to go in that space between the cabinet and the wall, there is a dirty great structural steel beam underneath the floor, and buggered if I was going to try to drill through that. My options were to either move the cabinet another 20-30cms out from the wall (yuck!!) or bring the plumbing back inside the cabinet and drill down through the cabinet floor, through the timber floor below and out that way... problem solved!<br><br>"
    print "<b>7.</b> Ball valve (usually closed) that can be turned on to allow almost complete drainage of sump compartments 1 and 2 before removing the sump.<br><br>"
    print "<b>9.</b> As above, another ball value (usually closed) allowing almost complete drainage of sump compartment 3.<br><br>"
    print "<b>10.</b> Ball valve (usually open) that will drain only to the minimum sump level (so that the pump won't suck air / run dry). This is just added redundancy, the aim is to never drain to this level as we don't want to break the siphon.<br><br>"
    print "<b>8.</b> Screw cap, very important!! Allows me to remove all air from the plumbing so that it will siphon when the 12V solenoid is opened. To prime the system (assuming the sump is already full of water) do the following:<br>"
    print "- 1 - Open all 3 valves - this removes any air below the valves (NB: all valves sit below standard sump water level).<br>"
    print "- 2 - Close all 3 valves<br>"
    print "- 3 - Open screw cap and poor water into the piping until piping completely full of water (can give it a bit of a shake to remove trapped bubbles if needed) NB: positioning of this was designed to be above the sump so any water splilled doesn't matter :)<br>"
    print "- 4 - Close system by screwing back on cap<br>"
    print "- 5 - Open ball valve (10)<br><br>"
    print "There is now water in all the plumbing and the syphon will start draining water from the pipe below (10) when the solenoid is switched on.<br><br>"
    print "To drain the sump completely, open valves (7) and (9) and close (10), then turn on solenoid. The solenoid is positioned slightly lower than the bottom of the pipes below the open valves, so the siphon will still drain.<br><br>" 
    print "To remove water from the plumbing system before removing the sump, simply open all 3 valves, unscrew the cap (8) and then turn on the solenoid and the remaining water will drain out... No mess!!<br><br>"
    
    print "<b>Display <-> Sump plumbing:</b><br><br>"
    print "Once I was finally ready to move the display tank into position (Very heavy, had to ensure would only need to move it once... Once in position there would be no moving of the cabinet due to the weight) it was time to start filling the system with water. Over the course of 2 weeks (On the advice of a structural engineer) we slowly filled the tank, measuring whether the floor was sagging below (Which it didn't... thanks goodness!!). I then added some feeder fish to start the cycling process and did frequent water changes, as the ceramic noodles drove the pH up to very unsafe levels during the first 2 weeks (Up around 10 initially, gradually reducing as more water changes were being done).<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/maintank.JPG\" width=\"80%\"/></p><br>"
    print "The above picture shows the completed plumbing system in its entirety. The three outlets on the left of the display tank draw the water into the sump, then the pump moves the water back into the display tank on the right hand side. This picture was taken mid-cycle when I was still doing daily / alt-daily water changes to combat high Nitrite levels. The orange fish you can see are not the feeders that we bought but are actually rosy barbs. Extremely hardy and handled the deranged water parameters perfectly!<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/outlets1.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/outlets2.JPG\" width=\"80%\"/></p><br>"
    print "The above two pictures show the three outlets. From left to right, there is the left hand side (LHS), middle (MID) and right hand side (RHS) outlets:<br><br>"
    print "<b>LHS:</b> Draws water from lower down the tank (important for messy turtles) via a tuned siphon. There are 2 holes below the water level and enclosed in the fine blank flyscreen that break the siphon if the water level drops below these holes. This prevents a huge amount of water draining out of the display in the event of a power failure (stopping the return pump from working). Although if these holes weren't there it wouldn't ever actually flood the house due to the sump overflow detailed above, when the power came back on there wouldn't be enough water in the sump to restart the siphon and the pump would run dry, wrecking it! The black flyscreen mesh is there to stop snails / plants (i.e. DUCKWEED!) from clogging the holes, which would prevent them from doing their job in a blackout. There is also a gang valve behind the tank, which is used to tune the flow of the siphon. The aim of this is to remove a fraction LESS water being drained into the sump then what the return pump is pushing back into the display. This results in the water level in the display slowly rising until it gets to MID, which acts as a surface skimmer. This ensures the water level in the display remains constant, allowing me to place the turtle docks in certain positions and not worry about water levels changing :)<br><br>"
    print "<b>MID:</b> Acts as the display overflow, handling the extra water being pumped back into the display that LHS can't remove. I wanted to have floating plants in my tank, which posed an obvious problem with an overflow, as they would all quickly end up in the sump!. I overcame this by cementing a larger piece of PVC around the overflow. You can see that water can still flow through the space between them, but it comes from below the surface about 20mm, so duckweed doesn't get sucked in! It's a bit hard to explain, I could take a quick video if needed to better explain it...<br><br>"
    print "<b>RHS:</b> This is an emergency overflow, and is not normally used. It is positioned slightly higher than MID and in the event that either LHS or MID become partially/completely blocked, the water level will rise then begin draining through RHS. I was pondering the idea of installing a flow meter on this drain and wire it to the Raspberry Pi to alert me if it registers flow through it, but the only flow meters I could find for cheap were from Adafruit and were only 1/2 inch, meaning it would constrict flow to much if it were used, defeating the purpose of it.<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/outlets4.JPG\" width=\"80%\"/></p><br>"
    print "Here the water from the display arrives in the sump. It's pretty busy looking but functions well. I have an interim filter sock set up to handle mechanical filtration. I will probably work out a more suitable system once the turtles get moved in, but this suffices for now.<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/pump.JPG\" width=\"80%\"/></p><br>"
    print "An important decision was always going to be the return pump. I needed something that was quiet, had a relatively small footprint and turned over the required amount of water. I wanted a relatively high flow system, mainly aimed to maximise mechanical filtration and removing as much of the turtle waste as possible. The display tank had about 440L of water and the sump around 140L and I decided I wanted to turn over the water about 4 times per hour. The pump I ended up getting was a shitty asian no-name brand that pushes about approx 2000L per hour which is around what was needed. Seeing the system working but I am now thinking of forking out the extra dosh and upgrading to a Eheim pump that will do around 3000L per hour. This is because the pump I bought is not as quiet as I was led to believe, and that the plumbing can handle a LOT more flow (and the siphon will restart a lot easier with a greater flow rate). I will however wait until the background is finished and in position to see how the water flows around. If all OK will upgrade and keep the cheap asian pump as a spare. Behind the sump you can also see the second solenoid that is connected directly into the house water supply. This is connected to the Raspberry Pi and allows for water to be pumped into the sump during a water change or to top off water lost due to evaporation. The AWC and ATO work perfectly, but I am yet to receive my peristaltic pump from eBay so have to dose Prime manually at the moment which is a bit of a pain!<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/inlet.JPG\" width=\"50%\"/></p><br>"
    print "This shows the inlet returning the water from the sump to the display. On the inside of the tank there is a piece of PVC that extends down just below the waterline. This ensures there is no noise from the large volume of water returning to the tank, and in the event of a power failure will only reverse siphon a small amount before the siphon breaks.<br><br>"
    print "Any questions, let me know, and I will update this information if it is ambiguous :)<br><br>"
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">4. Electricals and DIY Controller</h3><br><br>"
    print "<b>Electricals and DIY Controller:</b><br><br><b>Lighting:</b><br><br>"
    print "<a href=\"http://www.guppysaquariumproducts.com.au/lights-t5-ho/t5-florescent-light-fittings-supreme-aqua/t5-aquarium-overhead-lighting-3x54w-hi-output-1200/prod_260.html\">Supreme Aqua 3x54w T5HO</a><br><br>"
    print "Beautiful looking fixtures, the 4 foot ones I am using are $99.20 each. Remember to remove the plastic splash sheet if you are going to use a UV T5 tube in one of these. They get quite hot for a fluoro, I recommend keeping these away from splashes if possible to avoid broken glass... Having said that, I've never seen one break before...<br><br>"
    print "T5 really are the new norm in my opinion, T8s are outdated. Brighter lights, stronger UV and energy efficient (ref?) I am using 2 of these triple housings, each with 1x UV tube and 2x regular globes (they come with standard fluoros in them). I managed to get my LFS to order me in some Zoo Med ReptiSun 10.0 UVB tubes for $60 each, but if you are stuck you can get them from <a href=\"http://www.amazingamazon.com.au/reptisun-t5-uvb-light.html\">Amazing Amazon</a> as well for $69.95, but expect to pay postage on top of that. You can get them in all the various sizes and although $60 is still quite expensive, they last for a year when compared to 6 months for the T8 UVBs.<br><br>"
    print "I will also have a simple small fluoro mounted on the ceiling inside the cabinet to help me see if it is a tad dark in there. Something from Bunnings would do the job.<br><br>"
    print "<b>DIY Controller: (WIP)</b><br><br>"
    print "The brains of the controller is a RaspberryPi. This is effectively a cheap (~$75) mini computer that you can mod to the wazoo to do pretty much anything. A couple of basics you will need:<br>"
    print " - <a href=\"http://www.buyraspberrypi.com.au/\">http://www.buyraspberrypi.com.au/</a><br>"
    print "----- RaspberryPi Model B in case - $54.95<br>"
    print "----- Power Supply for Pi - $19.95<br>"
    print "----- AusPi Wireless-n Adapter - $29.95<br>"
    print "- Compatible SD card - This is used as the hard-drive. There are many flavours of Linux you can use to get the job done<br><br>"
    print "Other things I have bought so far (list not yet complete) - I have a doco saved of all items I have used so far, places purchased from and costs if anyone is interested.<br>"
    print " - Half sized breadboard<br>"
    print "  - Adafruit assembled Pi Cobbler<br>"
    print "  - Waterproof DS19B20 1-wire temperature sensors<br>"
    print "  - AM2032 (wired DHT22) humidity/temperature sensors<br>"
    print "  - Triple Output LEDs and 5mm LEDs<br>"
    print "  - USB 2.0 multi all-in-one care reader (my desktop didn't have one, and I hate using my laptop...)<br>"
    print "  - 4.7k resistors, 10k resistors<br>"
    print "  - 3-Terminal solderless breadboard modules<br>"
    print "  - 2 pin 12V 2A power supply<br>"
    print "  - 12V Plastic water solenoid valves x2<br>"
    print "  - eTape liquid level sensor<br>"
    print "  - 2.1mm DC barrel jack x2<br>"
    print "  - MOSFET logic level n-channel x6<br>"
    print "  - 1N4001 diodes<br>"
    print "  - 12V PC fans<br><br>"
    print "My ultimate controller will do the following:"
    print "- SENSORS:<br>"
    print "      ----- <b>{Completed}</b> Measure temperatures of sump water, display water, left dock and right dock<br>"
    print "     ----- <b>{Completed}</b> Measure relative humidity inside cabinet (where sump is) and hood (above display tank)<br>"
    print "      ----- <b>{Completed}</b> Measure luminosity of both light banks to report if a globe dies<br>"
    print "      ----- <b>{In progress}</b> Measure sump water level using 12 inch eTape liquid level sensor<br>"
    print "      ----- Measure pH of water - <b>No longer doing this</b>. The probes are too expensive and require continual calibration to remain accurate. For turtle tanks not required. Will stick to manual tests.<br><br>"
    print " - SOFTWARE:<br>"
    print "      ----- <b>{Completed}</b> Record temperatures and humidity in a database<br>"
    print "      ----- <b>{Completed}</b> Act as a web server to display all logged information in graphical form<br>"
    print "      ----- Be able to make changes to hardware settings through the web server<br>"
    print "      ----- Make secure (username/password etc.)<br>"
    print "      ----- Connect and control webcam (see below)<br>"
    print "      ----- Add other functionality such as auto-feeding, manual water changes etc.<br><br>"
    print " - AUTOMATION:<br>"
    print "      ----- Auto top off (ATO) - Will utilise readings from eTape liquid level sensor, will then switch on power to one of the 12V solenoid valves which will add water from the house water supply. Will also add water conditioner using a peristaltic pump at the same time<br>"
    print "      ----- <b>{Completed}</b> Auto water change - Will switch power to a second 12V solenoid valve which will siphon water out of the sump until it hits a desired level (built in redundancy needed). Will then refill by same method as above in ATO<br>"
    print "      ----- <b>{Completed}</b> Lower water temp - will switch on fans that blow air on to water surface when water temp rises above pre-determined level. Could use a chiller if you wanted to get fancy. Could also increase water temp using controller if you wanted but I feel it is safer to use a thermostatically controlled heater since they are dirt cheap anyway...<br>"
    print "      ----- <b>{Completed}</b> Lower humidity - similar as above, will switch on exhaust fans in either the cabinet of hood to remove humid air when needed. This will help protect the cabinet from mould formation and will help ventilate the hood<br>"
    print "      ----- Auto fish feed - undecided on this at this stage.<br><br>"
    print " - WEBCAM - pan / tilt / zoom webcam mounted to ceiling to allow user to control to get a view of the little buggers over the net (useful for when on holidays, or if you are particularly *clingy* to your turtle friends.<br><br>"
    print "<b>The majority of the automation tasks are still very much a WIP (Work In Progress) as I am still waiting on several components to be able to hook up the fans, connect the solenoid valves etc. Will keep you posted.</b><br><br>"
    print "I will post a link to my SD card image when completed which will have all the python scripts etc. so you can use whatever bits of it you like to mod your own. It would be too difficult to document each individual part of the code as I have taken bits and pieces from over 1 dozen sources (so far...) I won't bore you guys with code :) I will also link to various resources for the hardware side of things for wiring of components etc, but will do this when it is a tad more complete. Adafruit has great tutorials which for the most part I have either used or been able to use them as a starting point."
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    
    
    print "<tr>"
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">5. Background</h3><br><br>"
    print "Creating the background was a rather involved process. It firstly involved a lot of research, looking at the pros and cons of the various different types of backgrounds. The majority of the DIY backgrounds use a styrofoam base, then concrete over the top to seal it with colour either added over the top of that or in the concrete mix. Very strong, but very heavy, and plays havok with pH due to all the stuff that leaches out of the concrete. I instead decided to create a styrofoam base, then fibreglass over the top of it. The end result is still very strong, and is much lighter than its concrete counterpart.<br><br>"
    print "There were several things I learned along the way which were extremely important to know if anyone decides to create their own fibreglass background, as follows:<br>"
    print "   - Use only EPOXY resin - Standard polyester resin that you get from Bunnings (called 'Fibreglass Resin') will MELT styrofoam on contact!<br>"
    print "   - Ensure that the epoxy resin used is mainly SOLIDS and contains little to no SOLVENTS - These can leach out of the cured epoxy, potentially polluting your aquarium water<br>"
    print "   - Use a UV protective epoxy - Only relevent if you have a UV globe (i.e. for Turtles) - A lot of types of epoxy will degrade under UV light<br>"
    print "   - Use a colour pigment rather than a seperate colour coat over the top - Much easier, no problems with aforementioned UV degradability<br><br>"
    print "A bit of general knowledge on mixing epoxy is also handy - there are many useful how-to's on the internet...<br><br>"
    print "<b>Material List:</b><br><br>"
    print "   - Sheets of styrofoam - Can get these in differing thicknesses, I got standard white styrofoam from 'Clark foam and rubber' and it worked fine<br>"
    print "   - Aquarium safe silicon - Needed to glue the bits of styrofoam together<br>"
    print "   - Various cutting tools - A used stanley knives, scalpels and a hacksaw blade dependent on what I needed to do<br>"
    print "   - Heat gun - Used to gently melt the styrofoam after it is shaped as needed<br>"
    print "   - Epoxy resin - Do the research to make sure you get the right stuff! - I got BOTE-COTE from a place in Logan, QLD. Has been used on aquarium backgrounds, UV protection, no solvents etc.<br>"
    print "   - Fibreglass - Get a fine mesh fibreglass so you can easily push it into all the shaped bits of styrofoam. I got mine along with the resin<br>"
    print "   - Colour pigments - I went for black, white and green. Used black and white for a grey coloured base, then bits of green over the top to look like moss (kind of...)<br>"
    print "   - Thinner - used to clean up brushes etc. after using epoxy, not essential but cuts down on the number of brushes etc. you have to throw away - Highly recommended<br>"
    print "   - Assorted brushes, rollers, mixing containers, gloves (standard supermarket yellow ones are fine) and face masks for when sanding - All from Bunnings<br>" 
    print "   - Sandpaper - Relatively course, needed to sand back the bits of resin and excess fibreglass used before each subsequent coat<br><br>"
    print "<b>How I did it...</b><br><br>"
    print "<b>1.</b> First step is to measure out the dimensions of the background and silicon them together, forming one giant piece of styrofoam. The depth of this will be the maximum depth of the background.<br><br>"
    print "<b>2.</b> After this is done, cut and shape the background to what you desire. I included a large cave in the middle down the bottom, a waterfall at the top in the middle, 2x docks for either side both with different shapes and 5 seperate little holes in the bottom for crayfish to hide in... Use your imagination!<br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background18.JPG\" width=\"50%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background19.JPG\" width=\"50%\"/></p><br>"	
    print "<p style=\"text-align:center\"><img src=\"../images/big/background1.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background2.JPG\" width=\"80%\"/></p><br>"	
    print "<b>3.</b> Now, assuming your tank already has the cross brackets at the top, you are going to need to cut your background into several pieces to fit it in... I cut mine into 7 pieces, then did some reshaping to make the cuts look a bit more natural. After this is done, fit it all into the tank! Make sure you allow for all your bulkheads, and desisions need to be made if you want to still have access to the bulkheads after it is created. I designed mine so that only the top left piece and top right piece were not siliconed to the back glass wall. This allows me to access the bulkheads (as well as a small 12V pump that will pump the water for the waterfall) if needed while still fitting snuggly in so there is no movement or chance they could be displaced<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background3.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background4.JPG\" width=\"80%\"/></p><br>"
    print "<b>4.</b> Next you need to hit all of the shaped bits with the heat gun. Do this on a low heat (practice on a small bit first so you can see what effect it has on the styrofoam). The aim is to melt the individual styrofoam balls together without deforming the carefully crafted design that's been created.<br><br>"
    print "<b>5.</b> Time to fibreglass!! I did this over a month or so, with each piece getting one layer of fibreglass on any surface that would come into contact with turtles (i.e. mainly the front surface that has been shaped). So resin on the styrofoam, then layer the pre-cut piece of fibreglass, then more resin on top and patted down into each little carved out bit. I gave all the sides of each piece and the back of each piece at least 2 resin coats (without fibreglass) to improve the strength of the pieces. For all the base coats I also used the black and white pigments to make a grey colour which I think looks quite natural(ish). Between each coat there was lots of sanding to remove the excess bits of fibreglass and any resin drips that weren't wanted.<br><br>"
    print "<b>6.</b> Add the colour! After the base coats I mixed up some more epoxy and added the green pigment, then used some cloth and sponges to dab on bits of green all over the background, creating an effect of moss... kind of... I'm not really that artistic but meh, looks good enough for me...<br><br>"
    print "<b>7.</b> I finally added a clear coat of resin to the top of both docks and sprinkled some fine river sand over the top to make the surface more abrasive and easier for the turtles to climb on to - The fibreglass and resin are very smooth and although it would have been quite amusing to watch them try to climb onto the slippery docks, it's not really very practical!<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background5.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background6.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background7.JPG\" width=\"80%\"/></p><br>"
    print "<b>8.</b> After refitting it all back into the tank and making sure it was all fitting nice and snugly with proper access to the bulkheads etc. it was time to silicon all the pieces (excluding the small pieces top left and right) into the tank. I started from one side then moved piece by piece over to the other side, siliconing each piece to the back piece of glass as well as sides and bottom. I had pre-cut a bunch of pieces of wood and propped these up against the front piece of glass (using kitchen scrubbers between the wood and glass) to make sure the pieces of background were pushed hard up against the glass. I used a bit over 2 tubes of silicon for this, and was high as a kite for the majority of it thanks to silicon fumes...<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background17.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background16.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background13.JPG\" width=\"80%\"/></p><br>"
    print "<b>9.</b> After this had cured, I did the same with the left and right docks, once again using pre-cut bits of wood and a few weights on top of the docks to help keep them in the correct place. It is worth noting that before I drained the tank to do all this I stuck a few bits of tape to the glass to mark the waterline... VERY important to make sure the docks are at the right height. Thanks to the aforementioned plumbing I knew the water level would always be the exact same level! score!<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background14.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background15.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background8.JPG\" width=\"80%\"/></p><br>"
    print "<b>10.</b> One final line of silicone along the bottom and sides of the background and around the tops of the docks, then after cured I removed the top left and right pieces (not siliconed) and filled the tank up to give the background a good rinse off and to confirm it wasn't going to detach and start floating around - something that was always a worrying possibility due to the massive amount of buoyancy that each piece of styrofoam had... all good but.<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background9.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background10.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background11.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background12.JPG\" width=\"80%\"/></p><br>"
    print "<b>11.</b> I finally gave the 3 inlets on the left 2 coats of resin and a bit of green to make them blend in with the background. While I was waiting for this to cure I added a bunch of fine white sand I had prewashed thoroughly (Still waiting for the cal-grit to arrive), added an awesome piece of driftwood we picked up, then the moment of truth... CHUCKED THE TURTLES IN! - We couldn't wait to introduce the little guys to their new home, even though the tank currently had a fair bit less water than usual meaning they couldn't get onto the docks, and no filtration as the sump wasn't running... We figured one night without filtration wouldn't hurt and it meant I could clean their old tank out and stick the fish that were being temporarily housed in the sump into the old tank. The next day the water was noticeably brown from the tannins being released, but the turtles didn't seem to mind, they were too busy chasing the crayfish I had also added the day before ;).<br><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background20.JPG\" width=\"50%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background21.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background22.JPG\" width=\"80%\"/></p><br>"
    print "<p style=\"text-align:center\"><img src=\"../images/big/background23.JPG\" width=\"80%\"/></p><br>"
	

    
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "<tr>"
    print "<td colspan=\"7\">"
    print "<h3 class=\"inline\" style=\"margin: 0px;\">6. Finished Product / Final thoughts</h3><br><br>"
    print "<br><br>TBA.<br><br>"
    print "</td></tr>"
    print "<tr><th colspan=\"7\"><hr></th></tr>"
    
    print "</table>"
    print "</body>"
    print "</html>"
        
    sys.stdout.flush()

if __name__=="__main__":
    main()




