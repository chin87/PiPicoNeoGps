from machine import UART, Pin, SPI
from time import sleep
from micropyGPS import MicropyGPS
from ST7735 import TFT
from sysfont import sysfont

import time
import math

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

latitude = ""
longitude = ""
satellites = ""
date = ""
time = ""
altitude = ""
speed = ""

# Instantiate the micropyGPS object
my_gps = MicropyGPS()

# Define the UART pins and create a UART object
gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

tft.fill(TFT.BLACK);

def printGPSData():
    v = 10
    tft.text((0, v), "----GPS----", TFT.BLUE, sysfont, 2 )
    v += sysfont["Height"] * 3
    tft.text((0, v), " Speed:"+speed, TFT.CYAN, sysfont, 1, nowrap=True)
    v += sysfont["Height"] * 2
    tft.text((0, v), " Date:"+date, TFT.WHITE, sysfont, 1, nowrap=False)
    v += sysfont["Height"]
    tft.text((0, v), " Time:"+time, TFT.WHITE, sysfont, 1, nowrap=False)
    v += sysfont["Height"] * 2
    tft.text((0, v), " Lat "+latitude, TFT.GREEN, sysfont, 1, nowrap=False)
    v += sysfont["Height"]
    tft.text((0, v), " Long "+longitude, TFT.GREEN, sysfont, 1, nowrap=False)
    v += sysfont["Height"]
    tft.text((0, v), " Alt "+str(altitude), TFT.GREEN, sysfont, 1, nowrap=False)
    v += sysfont["Height"]
    tft.text((0, v), " Sat:" +str(satellites), TFT.GREEN, sysfont, 1, nowrap=False)
    
while True:
    try:
        while gps_serial.any():
            data = gps_serial.read()
            for byte in data:
                stat = my_gps.update(chr(byte))
                if stat is not None:
                    latitude = my_gps.latitude_string()
                    longitude = my_gps.longitude_string()
                    satellites = my_gps.satellites_in_use
                    date = my_gps.date_string('s_dmy')
                    time = "UTC:"+':'.join(map(str, my_gps.timestamp))
                    altitude = my_gps.altitude
                    speed = my_gps.speed_string()
                    # Print parsed GPS data
                    print('UTC Timestamp:', my_gps.timestamp)
                    print('Date:', date, ' Time:', time)
                    print('Latitude:', latitude)
                    print('Longitude:', longitude)
                    print('Altitude:', altitude)
                    print('Satellites in use:', satellites)
                    print('Horizontal Dilution of Precision:', my_gps.hdop)
                    printGPSData()
                    sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
                    
 

