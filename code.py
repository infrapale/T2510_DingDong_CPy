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

from uart_com import UCom  

play_wave = True
use_i2s = True
sd_card_is_ok = False

# uart = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
try:
    spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
    cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    sd_card_is_ok = True
    print("SD Card mounted")
except Exception as e:
    print("SD Card mount failed", e)    
    


try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

ucom = UCom(gpio.TX0_PIN, gpio.RX0_PIN, 9600)

i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)

if use_i2s:
    audio = audiobusio.I2SOut(gpio.I2S_BCLK, gpio.I2S_WS, gpio.I2S_DOUT)
else:   
    audio = AudioOut(gpio.PWM7B_PIN)

def play_audio(file_name):
    if play_wave:
        try:
            with open(file_name, "rb") as f:
                wave = audiocore.WaveFile(f)
                print("playing", file_name)
                audio.play(wave)
                while audio.playing:
                    pass
        except:
            print("waw failed", file_name)  
    else:
        #audio = audiobusio.I2SOut(gpio.I2S_BCLK, gpio.I2S_WS, gpio.I2S_DOUT)
        try:
            with open(file_name, "rb") as f:
                print("mp3 play", file_name)
                mp3 = audiomp3.MP3Decoder(f)
                audio.play(mp3)
                while audio.playing:
                    pass
        except:
            print("mp3 failed", file_name)


if sd_card_is_ok:
    print_sd_directory()
main_state = 0
main_timeout = time.monotonic()

while 1:
    if main_state== 0:
        if sd_card_is_ok:
            main_state = 1
        else:
            print("No SD Card")
            main_timeout = time.monotonic() + 5.0
            main_state = 10

    elif main_state== 1:
        if play_wave:
            print("Playing wave")
            play_audio("/sd/chime_big_ben.wav")
        else:
            print("Playing mp3")
            play_audio("/sd/Ambulance.mp3")
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

