# Importere library til at forbinde til adafruit.io
import umqtt_robust2
from machine import Pin, ADC
import GPSfunk
from hydrering import jord
from fugtighed import humidity
from temperatur import temperature
import LED2
import neopixel
import dht
from time import sleep_ms, sleep, ticks_ms
lib = umqtt_robust2
# ATGM336H-5N <--> ESP32 
# GPS til ESP32 kredsløb
# GPS VCC --> ESP32 3v3
# GPS GND --> ESP32 GND
# GPS TX  --> ESP32 GPIO 16

sensor = dht.DHT11(Pin(14))
sens = ADC(Pin(36))

tempfeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'tempfeed/csv'), 'utf-8')
airhumfeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'airhumfeed/csv'), 'utf-8')
humfeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'humfeed/csv'), 'utf-8')
# opret en ny feed kaldet map_gps indo på io.adafruit
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'mapfeed/csv'), 'utf-8')
# opret en ny feed kaldet speed_gps indo på io.adafruit
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'DannyLy', b'speedfeed/csv'), 'utf-8')

prev_time = 0
#jord_interval = 5000
#hum_interval = 5500
#temp_interval = 6000
interval = 5000
state = 0


#timerSet = False
LED_interval = 5000
#timer = 0

while True:
    sleep_ms(500)
    besked = lib.besked
    # haandtere fejl i forbindelsen og hvor ofte den skal forbinde igen
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        current_time = ticks_ms()
        """lib.c.publish(topic=mapFeed, msg=GPSfunk.main())
        speed = GPSfunk.main()
        speed = speed[:4]
        print("speed: ",speed)
        lib.c.publish(topic=speedFeed, msg=speed)
        sleep(10)"""
        if (current_time - prev_time > interval):
            lib.c.publish(topic=humfeed, msg=str(jord()))
            prev_time = ticks_ms()
        if (current_time - prev_time > interval): #nonblocking delay
            lib.c.publish(topic=airhumfeed, msg=str(humidity()))
            prev_time = ticks_ms
        if (current_time - prev_time > interval): #nonblocking delay
            lib.c.publish(topic=tempfeed, msg=str(temperature()))
            prev_time = ticks_ms()
        
        """current_time = ticks_ms()
        if jord() > 0.5:
            if not timerSet: 
                timer = current_time
                timerSet = True 
                print("timerSet")             
        if jord() < 0.5: # sætter timeren til currentTime når værdien fra jord er over 0.5V
            timer = current_time
            if timerSet:
                timerSet = False
                print("timerstop") # Stopper timeren når værdien fra jord er under 0.5V
        if (current_time - timer > LED_interval):#eksekvere koden hvis (currentTime - timeren) der er blevet opdateret til er større end (intervallet) vi har sat
            while True:
                for i in range(0, 11):
                    LED2.set_color(255, 0, 0)
                    sleep_ms(500)
                    LED2.set_color(0, 0, 0)
                    sleep_ms(500)
                    i = i+1"""
                    
            
         # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.client.disconnect()
        lib.sys.exit()
    except OSError as e:
        print('Failed to read sensor.')
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages
lib.c.disconnect()


