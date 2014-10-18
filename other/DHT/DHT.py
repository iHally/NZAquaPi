#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import dhtreader
import time

dhtreader.init()

Attempts = 0
while True:
    try:
        t, h = dhtreader.read(22, 23)
        break
    except TypeError:
        print("Failed to read from sensor on GPIO 23, trying again...")
        time.sleep(3)
        Attempts = Attempts + 1
        if Attempts >= 5:
            break
if t and h:
    print("AM2032 on GPIO 23: Temp = {0}*C, Hum = {1}%".format(t, h))
else:
    print("Failed to read from sensor.")
    
Attempts = 0
while True:
    try:
        t, h = dhtreader.read(22, 24)
        break
    except TypeError:
        print("Failed to read from sensor on GPIO 24, trying again...")
        time.sleep(3)
        Attempts = Attempts + 1
        if Attempts >= 5:
            break
if t and h:
    print("AM2032 on GPIO 24: Temp = {0}*C, Hum = {1}%".format(t, h))
else:
    print("Failed to read from sensor.")        


