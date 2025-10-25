'''
=============================================================
T 2 5  1 0   D i n g D o n g   C P y
=============================================================
https://github.com/infrapale/T2510_DingDong_CPy.git

https://docs.circuitpython.org/en/stable/docs/index.html
https://github.com/adafruit/awesome-circuitpython/blob/main/cheatsheet/CircuitPython_Cheatsheet.md
https://learn.adafruit.com/mp3-playback-rp2040/pico-i2s-mp3 

https://github.com/adafruit/circuitpython/issues/851
https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/convert-files
https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3
https://learn.adafruit.com/wave-shield-talking-clock/stuff
https://docs.circuitpython.org/en/8.2.x/README.html
https://learn.adafruit.com/adafruit-audio-bff/circuitpython
https://learn.adafruit.com/circuitpython-display-support-using-displayio
https://bigsoundbank.com/categories.html
https://learn.adafruit.com/microcontroller-compatible-audio-file-conversion


'''
import os
import sys
import audiocore
#from audiocore import RawSample
#from audiocore import WaveFile
#import audiopwmio
import audiobusio
#import audiomixer
import time
import board
import audiomp3
import busio
import digitalio
import board
import pico_rtc_u2u_sd_gpio as gpio
import array
import math

# Storage libraries
import adafruit_sdcard
import storage

from files import print_sd_directory  
import data as D
from uart_com import UCom
from DingDong import DingDong
from Event import Event
# play_wave = True
# use_i2s = True
# sd_card_is_ok = False

# uart = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
try:
    spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
    cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    D.sd_card_is_ok = True
    print("SD Card mounted")
except Exception as e:
    print("SD Card mount failed", e)  
    D.sd_card_is_ok = False  
    
ucom = UCom(gpio.TX0_PIN, gpio.RX0_PIN, 9600)
event = Event()
# dingdong = DingDong()

i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)

if D.sd_card_is_ok:
    print_sd_directory()

main_state = 0
main_timeout = time.monotonic()

while 0:
    event.state_machine()    
    event.print_status()
    event.set_home_mode(D.MODE_AT_HOME)
    event.state_machine()
    event.print_status()
    # event.set_zone_status(D.ZONE_PIHA, 1)
    event.set_zone_status(D.ZONE_RANTA, 1)
    for i in range(10):
        event.state_machine()
        event.print_status()
        time.sleep(1)
    sys.exit(0)

while 1:
    ucom.send_dict_msg(ucom.get_decoded_msg)
    time.sleep(0.5)
    msg = ucom.read_msg()
    if len(msg) > 4:
        print("Received:", msg)
        if ucom.msg_frame_is_ok():
            print("Frame OK")
            ucom.parse_msg()
            if ucom.received_msg['is_ok']:  
                if ucom.msg_id_is_ok(ucom.get_decoded_msg, ucom.received_msg['module_id']):
                    print("ID OK")
                    print(ucom.received_msg)
        else:
            pass
            # print("Frame not OK")
        

while 1:
    event.state_machine()
    if main_state== 0:
        if D.sd_card_is_ok:
            main_state = 1
        else:
            print("No SD Card")
            main_timeout = time.monotonic() + 5.0
            main_state = 10

    elif main_state== 1:
        event.set_home_mode(D.MODE_AT_HOME)
        main_state = 10

    elif main_state== 10:
        ucom.send_get_home_state()
        main_timeout = time.monotonic() + 5.0
        main_state = 20

    elif main_state== 20:
        msg = ucom.read_msg()
        if msg != "":
            print("Received:", msg)
            if ucom.msg_frame_is_ok():
                print("Frame OK")
                ucom.parse_msg()
                print(ucom.parsed)
                if (event.get_zone_status(D.MODE_AT_HOME) == 1 ): 
                    event.set_zone_status(D.ZONE_RANTA, 0)
                else:
                    event.set_zone_status(D.ZONE_RANTA, 1)
            else:
                print("Frame not OK")
            main_state = 30
        elif time.monotonic() > main_timeout:
            print("Timeout waiting for message")
            main_state = 100
    elif main_state== 30:
        main_state = 100
    elif main_state== 100:
        main_timeout = time.monotonic() + 5.0
        main_state = 110
    elif main_state== 110:
        if time.monotonic() > main_timeout:     
            print("Looping")
            main_state = 0 

