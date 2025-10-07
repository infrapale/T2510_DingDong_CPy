'''
Aamukampa 

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

import audiocore
from audiocore import RawSample
from audiocore import WaveFile
import audiopwmio
import audiobusio
#import audiomixer
import time
import board
import busio
import digitalio
import pico_rtc_u2u_sd_gpio as gpio
import array
import math
# from adafruit_pcf8563.pcf8563 import PCF8563
# import aamukampa
# Storage libraries
import adafruit_sdcard
import storage

# from simple_ssd import simple_ssd
# from rtc_pcf8563 import rtc_pcf8563

 
#ssd.release()

# Display libraries
#import displayio
#import terminalio
#from adafruit_bitmap_font import bitmap_font
#import adafruit_displayio_ssd1306
#from adafruit_display_text import label


uart = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# simple_ssd.release()

i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)


# ssd  = simple_ssd(i2c1)
# rtc = rtc_pcf8563(i2c_bus)
# dac = adafruit_mcp4725.MCP4725(i2c1, address=0x60)

# ssd.print("AAMUKAMPA")
# rtc.set_time()
#rtc.print_time()


DISP_LEN = 16

cur_raw = 0


def ssd_aamuja(n,t):
    global cur_raw
    raw_str = " Aamuja {:n}.{:n} : {:3n} ".format(t.tm_mon,t.tm_mday,n)
    len_raw = len(raw_str)
    last = cur_raw + DISP_LEN
    if last < len_raw:
        aamuja_str = raw_str[cur_raw:cur_raw + DISP_LEN]
    else:
        aamuja_str = raw_str[cur_raw:len_raw]
        aamuja_str = aamuja_str + raw_str[0:DISP_LEN-(len_raw-cur_raw)]
    
    print(aamuja_str)    
    # ssd.print(aamuja_str)
    cur_raw = cur_raw + 1
    if cur_raw >= len_raw:
        cur_raw = 0
    
  
def open_audio(file_name):
    f = open(file_name, "rb")
    w = audiocore.WaveFile(f)
    return f, w

def play_audio(file_name):
    try:
        with open(file_name, "rb") as f:
            wave = WaveFile(f)
            audio = AudioOut(gpio.PWM7B_PIN)
            print("playing", file_name)
            audio.play(wave)
            while audio.playing:
                pass
    except:
        print("failed", file_name)
        

#file_name = "chime_big_ben_2.wav"
file_name = "/sd/chime_big_ben_2.wav"
#file_name = "/sd/cat-time.wav"


# aamuja = 40
aamuja_offset = 0
claer_offset_time  = 0
clear_offset_flag  = False
iter_cnt = 1
SSD_UPDATE_INTERVAL = 0.2
CLEAR_OFFSET_DELAY   = 10.0

clear_offset_time  = time.monotonic() + CLEAR_OFFSET_DELAY
next_ssd_time = time.monotonic() + SSD_UPDATE_INTERVAL

while 1:
    play_audio("/sd/chime_big_ben.wav")
    time.sleep(5.0)



             
    
'''
file_name = "/sd/chime_big_ben_2.wav"
'''
