import urllib.parse
import requests
import http.client
import json
import time


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

    
    
keySend = "AB2DLL1XSNYHIU2O"
def sendData(wt,dist):
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


currentID = readData()['entry_id']
while True:
    field = readData()
    if field['entry_id'] == (currentID+1):
        currentID += 1
        if field['field1'] == '2':
            grams = 300
            distance = 20
            sendData(distance, grams)
            time.sleep(1)
            print("Distance and Weight sent")
            continue

#if __name__ == "__main__":
    #grams = 300
    #readData()
    #sendData(grams)