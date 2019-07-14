'''
anlegen influx Datenbank abc
anlegen Tabelle xyz in abc
schreiben unterschiedlicher Variablen-Typen und Beispiel Anpassung Integer für "Wind Direction degree (integer)"
'''

from influxdb import InfluxDBClient
import logging

db_influx_name = "luftdaten"  # name of influxDB
db_influx_measurement = "weather"  # name of influxDB table/measurement (without calling this table, name of the table would be same us influxDB name)

def data_entry_influx(tup_db):
    """add data into a existing table"""
    #print("Tuple before influx entry: ", tup_db)
    logging.info('Tuple before influx entry: %s', tup_db)
    if tup_db[1] == '': return
    json_body = [{"measurement": db_influx_measurement,
        "fields": {
            "Temperature_outside_ws °C": tup_db[1],
            "Humidity_outside_ws %r.H.": tup_db[2],
            "Wind Direction": tup_db[3],
            "Wind Direction degree": str(tup_db[4]),
            "Wind Direction degree (int)": int(tup_db[4]),
            "Wind speed km/h": tup_db[5],
            "Wind Gust km/h": tup_db[6],
            "Rain mm": tup_db[7],
            "Battery Status": tup_db[8],
            "Temperature_inside_pi °C": tup_db[9],
            "Pressure_inside_pi hPa": tup_db[10],
            "Humidity_inside_pi %r.H.": tup_db[11]
        }
    }]    
   
    client = InfluxDBClient('192.168.178.60', 8086, 'admin', 'bart')
    client.create_database(db_influx_name)
    client.switch_database(db_influx_name)
    #print("vor write influx")
    client.write_points(json_body)
    #print("nach write influx")
    result = client.query('SELECT * FROM ' + db_influx_measurement + ' GROUP BY * ORDER BY DESC LIMIT 1;')
    #print("Result: {0}".format(result))
    logging.info('Read InfluxDB after entry: %s', result)
    
#tup = ('2019-04-22 14:30...', 22.5, 20, 'X', '90', 25.704, 28.125, 89.7, 'OK', 22.5, 959.5966, 27.14)
#data_entry_influx(tup)

# prüfen der Einträge in InfluxDB
# Console:
# influx -username admin -password bart
# show databases
# use abc
# show measurements
# show field keys from xyz
# prüfen ob fieldType passt wie gewünscht (string, float, integer)
# select * from xyz
# select * from xyz group by * order by desc limit 1