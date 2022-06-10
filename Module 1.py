#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Module 1 - Libraries and Functions

import time 
import sys 
import pubnub
import RPi.GPIO as GPIO 
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback,PNStatusCategory 
from pubnub.pnconfiguration import PNConfiguration 
from pubnub.exceptions import PubNubException 

pnconf = PNConfiguration()                                          
pnconf.publish_key = 'pub-c-47de1ea1-b0ba-462c-ba6a-1c4fa5371251'
pnconf.subscribe_key = 'sub-c-d5e026e5-08a6-401d-9651-a1ba89559278'
pnconf.uuid = 'Project'  
pubnub = PubNub(pnconf)                                             
 
channel='Project'                                             
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 20
GPIO_ECHO = 26

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

my_listener = SubscribeListener()                          
pubnub.add_listener(my_listener)                          
pubnub.subscribe().channels(channel).execute()             
my_listener.wait_for_connect()  


# In[ ]:


# Module 1

import drivers
from time import sleep
dis = distance()
display = drivers.Lcd()

try:
    while True:
        display.lcd_display_string("Entering Private Property", 1)
        display.lcd_display_string("Stay on Trail", 2)
        sleep(2)
        display.lcd_clear()
        display.lcd_display_string("WARNING!!!", 1)  
        sleep(2)                                          
        display.lcd_clear()                                
        sleep(2)
        
        if dis < 30:
            data = "Unidentified Object"
            pubnub.publish().channel(channel).message(data).sync()
            
            for i in range(120):
                display.lcd_display_string("Unidentified Object", 1)
                display.lcd_display_string("is Detected !!!", 2)
                sleep(1)
                display.lcd_clear()
            
        while True:
            display.lcd_display_string("NOT ALLOWED !!!", 1)
            display.lcd_display_string("GAURDS ONTHEWAY", 2)
            sleep(1)
            display.lcd_clear()
                    
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()

GPIO.cleanup()
sys.exit()

