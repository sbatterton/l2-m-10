# libraries used for sending and reading data over think-speak 
import urllib.parse
import requests
import http.client
import json
import time
# libraries used for sensors for RPi 
import RPi.GPIO as GPIO
import threading
from hx711 import HX711
from hcsr04 import HCSR04

GPIO.setwarnings(False)
hx = HX711(5, 6) # GPIO pins from RPI used for the load-cell sensor
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(95.20) # calibrating load cell 
hx.reset()
hx.tare()

hc = HCSR04(18, 24) # GPIO pins from RPI used for the ultra-sonic sensor 

# allows data to be read over groups think-speak channel
def readData():
    URl='https://api.thingspeak.com/channels/1173908/feeds.json?api_key=6G647UFZ4V0F7XL2&results=2'
    KEY='6G647UFZ4V0F7XL2'
    HEADER='&results=1'
    NEW_URL = URl+KEY+HEADER
    #print(NEW_URL)
    
    get_data=requests.get(NEW_URL).json()
    #print(get_data)
    
    channel_id=get_data['channel']['id']
    
    field1 = get_data['feeds'][0]
    #print(field1)
    
    return (field1)     

    

keySend = "AB2DLL1XSNYHIU2O" # key to think-speak channel  
# allows weight and distance data from load cell and ultra sonic sensor ... 
# ... to be sent over think speak channel 
def sendData(dist,wt): 
    while True:
        params = urllib.parse.urlencode({'field1': dist, 'field2': wt, 'key': keySend })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            data = response.read()
            conn.close()
            break
        except:
            print ("connection failed")
            break
# function from HX711 library to get weight readings from load cell 
def getWeight(): 
    wt = max(0, int(hx.get_weight(5)))
    return wt
# function from HCSR04 library to get distance readings from ultra sonic sensor 
def getDistance():
    ht = hc.distance()
    return ht
# code that occurs when water storage and bowl status needs to be updated 
currentID = readData()['entry_id']
while True: 
    field = readData()
    if field['entry_id'] == (currentID+1):
        currentID += 1
        if field['field1'] == '3':
            grams = getWeight()
            time.sleep(0.1)
            distance = getDistance()
            sendData(distance, grams)
            time.sleep(1)
            print("Distance and Weight sent")
            print(field['field2'])
            continue
