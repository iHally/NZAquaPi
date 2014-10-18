NZAquaPi
========

A RaspberryPi based aquarium controller

----------
Hardware needed:
----------

- Raspberry Pi Model B
   - Power supply
   - USB Wifi adapter
   - SD card (must be compatible)

- Breadboards + jumper cables + resistors (mainly 4.7k and 10k, but others as well)
- Several 1N4001 diodes
- Several MOSFETs (Logic Level N-Channel) (I used 60V, 21A - overkill i know)
- 12V power supply(s) (I use 2x 2A supplys)
- 2.1mm DC barrel jacks for power supplys into breadboards
- 1x MCP3008 8-channel 10-bit ADC (SPI interface) - to read analog eTape and photocell
- Assorted screw terminals
- Assorted LEDs
- Assembled Pi Cobbler (optional)

- 4x waterproof DS18B20 1-wire temperature sensors
- 2x AM2302 humidity sensors (Or DHT22s)
- 1x eTape liquid level sensor
- 1x Photocell (cheap and nasty)
- 6x 12V PC fans - can use as few or many as you like - code is for 4 separate groups of fans
- 2x 12V plastic water solenoid valves
- 1x cheap 12V ebay perastaltic dosing pump

Useful guides:

- DS18B20 - https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
- AM2302 - http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=15755
- AM2302 - https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview
- eTape - http://www.adafruit.com/product/464
- MCP3008 - http://www.geeklee.co.uk/rpi-mcp3008-tmp36-sqlite-lighttpd/

After all connected, the GPIO will have connected to it:
- 4x DS18B20s (1-wire, using only 1x pin for all)
- 2x AM2302s (uses 2x pins)
- MCP3008 (uses 4 of the SPI pins - MOSI, MISO, SCLK and CE0)
- 6x PC fans via 4x MOSFETs (uses 4x pins)
- 2x liquid solendoids via 2x MOSFETS (uses 2x pins)
- 1x peristaltic pump via 1x MOSFET (uses 1x pin)
- 2x status LEDs (left over pins, only 1 is considered 'needed' as a status LED)

----------
SD card preparation:
----------

- Raspbian (Debian Wheezy) - http://downloads.raspberrypi.org/raspbian_latest.torrent
- enable 1-wire, spi, security etc. 

You will also need a few 3rd party apps to run this properly...

1. SqLite3 - to use the DB
2. smtplib - to send emails
3. rpi.GPIO - to control the GPIO
4. DHTreader - to read AM2302s
5. cgitb - to allow error traceback for python scripts
6. apache server - for web front end
7. phpBB (optional) - for forum portion of web front end



GOOD LUCK!
----------------------------
Nathan.
