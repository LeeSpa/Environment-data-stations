#!/usr/bin/python3.5
"""That would be a script to gather data from a weather station
and from the BME280 at Raspberry Pi
and writing data to SQLite and InfluxDB"""

import os
import sys 
import time, timeit, datetime
import logging

import send_email
import read_rtl_sdr
import read_bme280
import write_db_sqlite
import write_db_influx

#logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
#logging.basicConfig(filename='/home/pi/Weather/weather_station.log', format='%(asctime)s %(message)s', level=logging.INFO)
logging.basicConfig(filename='/home/pi/Weather/weather_station.log', format='%(asctime)s %(message)s', level=logging.WARNING)
#logging.basicConfig(filename='/home/pi/Weather/weather_station.log', format='%(asctime)s %(message)s', level=logging.ERROR)

#send_email.send_email_home("Start Weather Station", "Python has started weather_station.py")  # message
logging.info('')
logging.info('Python has started weather_station.py at %s', datetime.datetime.now())
logging.info('------------------------------------------------------------------------')

def sound_1000():
    """Play sound 1 second with 1000 Hz"""
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 1000))

def read_ws():
    '''Read all data from weather station'''
    start_time = time.time()
    tup_wst = read_rtl_sdr.read_rtl_sdr()
    dif_time = time.time() - start_time
    print("Wait time since start listening ==========> {t:2.1f} Seconds".format(t=dif_time))
    #print("Values from weather station: ", tup_wst)
    logging.info('Values from weather station: %s', tup_wst)
    return tup_wst

def read_bme():
    '''Read all data from Bosch sensor'''
    temp, press, humid = read_bme280.read_bme280()
    tup_bme280 = (temp, press, humid)
    #print("Values from BME280: ", tup_bme280)
    logging.info('Values from BME280: %s', tup_bme280)
    return tup_bme280

def write_sqlite(tup_db):
    '''Write all data to SQLite-DB'''
    logging.info('create table if needed')
    write_db_sqlite.create_table()
    write_db_sqlite.data_entry(tup_db)
    logging.info('put data to SQLite-DB: %s', tup_db)

def write_influx(tup_db):
    '''Write all data to Influx-DB'''
    write_db_influx.data_entry_influx(tup_db)
    logging.info('put data to Influx-DB: %s', tup_db)

def restart():
    """Restarts the current program."""
    #send_email.send_email_home("Restart file weather_station.py", "")
    print("Restart file weather_station.py")
    sound_1000()
    logging.warning('Restart file weather_station.py at %s', datetime.datetime.now())
    python = sys.executable
    os.execl(python, python, * sys.argv)

while True:
    try:
        tup_ws = read_ws()  # call weather station
        logging.info('read weather station: %s', tup_ws)
        tup_bme = read_bme()  # call Raspberry Pi values
        logging.info('read raspberry pi pressure sensor: %s', tup_bme)
        tup = tup_ws + tup_bme
        #print("All before writing in both DB: ", tup)
        #print(tup)
        write_sqlite(tup)  # write all data to SQLite-DB
        #print("nach sqlite")
        write_influx(tup)  # write all data to Influx-DB
        #print("nach influx")
        logging.info('Loop has finished at =============> %s', datetime.datetime.now())
        logging.info('------------------------------------------------------------------------')
    except: 
        restart()  # Restart "weather_station.py"
        