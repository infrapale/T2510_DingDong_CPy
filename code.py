'''
Aamukampa 
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

uart = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

play_wave = True
use_i2s = True

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!


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

def print_directory(path, tabs=0):
    for file in os.listdir(path):
        if file == "?":
            continue  # Issue noted in Learn
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


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



print("Files on filesystem:")
print("====================")
print_directory("/sd")



while 1:
    if play_wave:
        print("Playing wave")
        play_audio("/sd/chime_big_ben.wav")
    else:
        print("Playing mp3")
        play_audio("/sd/Ambulance.mp3")
    time.sleep(5.0)



             
    
'''
file_name = "/sd/chime_big_ben_2.wav"
'''
