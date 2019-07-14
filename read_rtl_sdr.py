"""Returns data from weather station as described below"""

import os
import reset_usb
import logging

logging.basicConfig(filename='/home/pi/Weather/weather_station.log',level=logging.DEBUG)

def sound_1000():
    """ play sound 1 second with 1000 Hz for debug reason"""
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 1000))


def read_rtl_sdr():
    """"read the current weather data from weather station type PCE-FWS-20
        Station send data after each 48 seconds
        around each full hour, time synchronisation is active (msg type 1), no other data will be sent while active"""
    logging.info('reading rtl_433 started')
    # sound_1000()
    # rtl_433 - script
    # -f 868311000 - frequency to scan
    # -R 32 - use driver for weather station type PCE-FWS-20 only, no other transmitter will be received
    # -q - print minimum information - but is default and deprecated (veraltet) see -v to increase verbosity
    # -v - verbose - detaillierte Ausgabe
    # -I 2 - receive only known stations -- vealtet
    # -F json - output as JSON format (it is not a real dictionary!!!!)
    # -E - finish scan after successful receive
    # -T 60 - finish scan after 60 seconds
    # -- help -  for more information
    # ist alles auch über config Datein rtl_433.conf einzustellen
    progress = os.popen('rtl_433 -f 868311000 -R 32 -F json -E')
    #progress = os.popen('rtl_433')
    data_str = progress.read()
        
    # USB Reset if connection failed
    if not data_str:
        reset_usb.reset_usb()
        logging.warning("Restart USB port on Raspberry Pi")
        print("Restart USB port on Raspberry Pi")
        sound_1000()
    
    logging.info('reading rtl_433 finished')
    logging.debug('data_str: %s', data_str)
    pos = data_str.find("}") + 1  # if received more than one string of data, find end of first string
    logging.info('pos: %s', pos)
    data_str = data_str[:pos]  # cat off everything after first string
    logging.info('data_str: %s', data_str)
    data_dic = eval(data_str)  # convert json str to dic
    #print(data_dic)
    logging.info('data_dic: %s', data_dic)
    progress.close()
     
    
    # extract values out of dictionary and put these into a tuple
    time, model, msg_type, id, temp, humidity, direction_str, direction_deg, speed, gust, rain, battery \
        = "", "", "", "", "", "", "", "", "", "", "", ""
    if "time" in data_dic:
        time = data_dic["time"]
    if "model" in data_dic:
        model = data_dic["model"]
    if "msg_type" in data_dic:
        msg_type = data_dic["msg_type"]
    if "id" in data_dic:
        id = data_dic["id"]
    if "temperature_C" in data_dic:
        temp = data_dic["temperature_C"]
    if "humidity" in data_dic:
        humidity = data_dic["humidity"]
    #if "direction_str" in data_dic:
        #direction_str = data_dic["direction_str"]
    direction_str = "X"
    if "direction_deg" in data_dic:
        direction_deg = data_dic["direction_deg"]
    #if "speed" in data_dic:
    if "wind_avg_km_h" in data_dic:
        #speed = data_dic["speed"]
        speed = data_dic["wind_avg_km_h"]
    #if "gust" in data_dic:
    if "wind_max_km_h" in data_dic:
        #gust = data_dic["gust"]
        gust = data_dic["wind_max_km_h"]
    #if "rain" in data_dic:
    if "rain_mm" in data_dic:
        #rain = data_dic["rain"]
        rain = data_dic["rain_mm"]
    #if "battery" in data_dic:
    if "battery_ok" in data_dic:
        #battery = data_dic["battery"]
        battery1 = data_dic["battery_ok"]
        if battery1 == 1:
            battery = "batt ok"
        else:
            battery = "batt low"      
    data_tup = (time, temp, humidity, direction_str, direction_deg, speed, gust, rain, battery)
    #print("Tuple: ", data_tup)
    logging.info('data_tup: %s', data_tup)
    return data_tup

#read_rtl_sdr()
