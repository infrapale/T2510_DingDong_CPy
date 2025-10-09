# DingDong

#import data
import data as D
import time

# Storage libraries
import adafruit_sdcard
import storage
# Aufio libraries
import audiocore
import audiobusio
import time
import board
import audiomp3
import busio
import digitalio
import board
import pico_rtc_u2u_sd_gpio as gpio
from micropython import const

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

if D.play_wave:
    audio = audiobusio.I2SOut(gpio.I2S_BCLK, gpio.I2S_WS, gpio.I2S_DOUT)
else:   
    audio = AudioOut(gpio.PWM7B_PIN)


class DingDong:
    def __init__(self):       
        self.timeout = time.monotonic()

    def play_audio(self, file_name):
        if file_name.lower().endswith('.wav'):
            try:
                with open(file_name, "rb") as f:
                    wave = audiocore.WaveFile(f)
                    print("playing", file_name)
                    audio.play(wave)
                    while audio.playing:
                        pass
            except Exception as e:
                print("wav failed", file_name, e)
        elif file_name.lower().endswith('.mp3'):
            try:
                with open(file_name, "rb") as f:
                    print("mp3 play", file_name)
                    mp3 = audiomp3.MP3Decoder(f)
                    audio.play(mp3)
                    while audio.playing:
                        pass
            except Exception as e:
                print("mp3 failed", file_name, e)
        else:
            print("Unsupported file type:", file_name)

      
 
