from adafruit_pcf8563.pcf8563 import PCF8563
import time
import data
from pico_rtc_u2u_sd_gpio import i2c0


class rtc_pcf8563:
    
    def __init__(self, i2c):
        self.rtc_i2c = PCF8563(i2c)
        self.date_time = time.struct_time((2024, 1, 1, 12, 0, 0, 6, -1, -1))
        self.hour = self.date_time.tm_hour
        self.min = self.date_time.tm_min
        self.sec = 0
        if self.rtc_i2c.datetime_compromised:
            self.lost_power = True
        else:
            self.date_time = self.rtc_i2c.datetime
            self.lost_power = False   
        self.days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        # Lookup table for names of days (nicer printing).


    def set_time(self, t):
        #                     year, mon, date, hour, min, sec, wday, yday, isdst
        # t = time.struct_time((2023, 9, 21, 19, 50, 0, 3, -1, -1))
        # you must set year, mon, date, hour, min, sec and weekday
        # yearday is not supported, isdst can be set but we don't do anything with it at this time
        self.date_time = t
        self.rtc_i2c.datetime = t
        print("Setting time to:", self.rtc_i2c.datetime)
        self.print_time()
         
     
    def read_time(self):
        if self.rtc_i2c.datetime_compromised:
            print("RTC unset")
        else:
            pass
            # print("RTC reports time is valid")
        self.datetime = self.rtc_i2c.datetime

   
     
    def get_time(self):
        self.read_time()
        return self.datetime
    
    
    def get_date_str(self):
        t = self.get_time()
        return "{} {}/{}/{}".format(
                self.days[int(t.tm_wday)], t.tm_year, t.tm_mon, t.tm_mday )
        
    def get_time_str(self):
        t = self.get_time()
        return "{}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec)
        


    def print_time(self):  
        
        print(self.get_date_str() + "  " + self.get_time_str())     # uncomment for debugging

rtc = rtc_pcf8563(i2c0)
