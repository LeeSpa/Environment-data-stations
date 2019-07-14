# Environment-data-stations
gathering data for displaying on dashboard


Sensor station 1:
particulate matter sensor 
https://luftdaten.info/en/home-en/ 

ESP8266 sends data via wifi to mosquitto server on raspberry pi 3


Sensor station 2:
PCE-FWS-20 weather station (outside sensors only) 
https://www.pce-instruments.com/deutsch/messtechnik/messgeraete-fuer-alle-parameter/umweltmessgeraet-pce-instruments-umweltmessgeraet-pce-fws-20-det_18527.htm?_list=qr.art&_listpos=56
(cheaper one on aliexpress)

SDR Receiver 
DVB-T + DAB + FM + RTL2832U USB 2.0 
https://www.amazon.de/gp/product/B013Q94CT6/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1

rtl-433
https://github.com/merbanan/rtl_433


Base station:
raspberry pi 3 with mosquitto, sqlite, influxdb, grafana


Project status: 
all components working well, but still on progress
comming up issues from time to time
need to debug 
