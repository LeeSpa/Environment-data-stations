'''Write into a SQLite DB and create tabel if needed.'''

import sqlite3
import logging

db_sqlite = "/home/pi/Weather/weather_station.db"

def create_table():
    """creat a table in a sqlite db if not exists"""
    logging.info('Function SQLite create_table entered')
    conn = sqlite3.connect(db_sqlite)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS weather ("
              "'Time' TEXT, "
              "'Temperature_outside_ws °C' REAL, "
              "'Humidity_outside_ws %r.H.' INTEGER, "
              "'Wind Direction' TEXT, "
              "'Wind Direction degree' INTEGER, "
              "'Wind speed km/h' REAL, "
              "'Wind Gust km/h' REAL, "
              "'Rain mm' REAL, "
              "'Battery Status' TEXT, "
              "'Temperature_inside_pi °C' REAL, "
              "'Pressure_inside_pi hPa' REAL, "
              "'Humidity_inside_pi %r.H.' REAL)")
    conn.commit()
    c.close()
    conn.close()
    logging.info('Function SQLite create_table left')

def data_entry(tup_db):
    """add date into a existing table by using variables"""
    logging.info('Function SQLite data_entry entered')
    conn = sqlite3.connect(db_sqlite)
    c = conn.cursor()
    c.execute("INSERT INTO weather ("
              "'Time', "
              "'Temperature_outside_ws °C', "
              "'Humidity_outside_ws %r.H.', "
              "'Wind Direction', "
              "'Wind Direction degree', "
              "'Wind speed km/h', "
              "'Wind Gust km/h', "
              "'Rain mm', "
              "'Battery Status', "
              "'Temperature_inside_pi °C', "
              "'Pressure_inside_pi hPa', "
              "'Humidity_inside_pi %r.H.') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tup_db)

    conn.commit()
    c.close()
    conn.close()
    logging.info('Function SQLite data_entry left')
