# DingDong

#import data
import data as D
import time
import time
import board
import pico_rtc_u2u_sd_gpio as gpio
from micropython import const



STATE_UNDEFINED = const(0)
STATE_IDLE      = const(1)  
STATE_ALARM     = const(2)
STATE_SIGNAL    = const(3)


class Event:
    def __init__(self):
        self.state = STATE_UNDEFINED
        self.prev_state = STATE_UNDEFINED
        self.timeout = time.monotonic()
        self.home_mode = D.MODE_UNDEFINED
        self.prev_home_mode = D.MODE_UNDEFINED
        self.alarm_zone = D.ZONE_UNDEF
        self.zone_status = [0,0,0,0,0]  # ZONE_UNDEF, ZONE_PIHA, ZONE_RANTA, ZONE_VA, ZONE_LA
        self.zone_active_status = [0,0,0,0,0] 
        self.zone_prev_active_status = [0,0,0,0,0] 

        self.melody = [
            [D.ZONE_UNDEF,  0.0,    "/sd/chime_big_ben.wav"],
            [D.ZONE_PIHA,   10.0,   "/sd/chime_big_ben.wav"], 
            [D.ZONE_RANTA,  10.0,   "/sd/chime_big_ben.wav"],
            [D.ZONE_VA,     20.0,   "/sd/chime_big_ben.wav"],
            [D.ZONE_LA,     20.0,   "/sd/chime_big_ben.wav"]
        ]
       
        self.mode_mask = [1<<i for i in range(5)]  # 1,2,4,8,16
        self.zone_mask = [1<<i for i in range(5)]  # 1,2,4,8,16

        self.active_zone = [
            self.zone_mask[D.ZONE_UNDEF],    # MODE_UNDEFINED
            self.zone_mask[D.ZONE_PIHA] | self.zone_mask[D.ZONE_RANTA],     # MODE_AT_HOME 
            self.zone_mask[D.ZONE_PIHA] | self.zone_mask[D.ZONE_RANTA],      # MODE_COUNT_DOWN
            self.zone_mask[D.ZONE_PIHA] | self.zone_mask[D.ZONE_RANTA] | self.zone_mask[D.ZONE_VA] | self.zone_mask[D.ZONE_LA], # MODE_AWAY
            self.zone_mask[D.ZONE_PIHA] | self.zone_mask[D.ZONE_RANTA] | self.zone_mask[D.ZONE_VA] | self.zone_mask[D.ZONE_LA]  # MODE_WARNING  
        ]
        print("zone mask: ",self.zone_mask)
 
 
    def set_home_mode(self, mode):
        self.home_mode = mode   
        for zone in range(5):
            self.set_zone_active_status(zone)

    def set_zone_active_status(self, zone):     
        if ((self.active_zone[self.home_mode] & self.zone_mask[zone]) != 0):
            self.zone_active_status[zone] = self.zone_status[zone]   
        else:
            self.zone_active_status[zone] = 0
      
    def set_zone_status(self, zone, status):
        self.zone_status[zone] = status
        self.set_zone_active_status(zone)
        print("Zone", zone, "status set to", status)    
    
    def print_status(self):
        print("--- Event status ---")
        print("State:", self.state, " Home mode:", self.home_mode)
        print("Zone status:", self.zone_status)
        print("Zone active status:", self.zone_active_status)
        print("Zone prev active status:", self.zone_prev_active_status)

   
    def state_machine(self):
        if self.state ==STATE_UNDEFINED:
            self.state = STATE_IDLE
            self.timeout = time.monotonic() + 1.0
        elif self.state == STATE_IDLE:
            for zone in range(1,5):
                if self.zone_active_status[zone] == 1 and self.zone_prev_active_status[zone] == 0:
                    self.alarm_zone = zone
                    print("Alarm ON, zone:", zone)
                    self.state = STATE_ALARM
                    break
        elif self.state == STATE_ALARM:
                self.timeout = time.monotonic() + self.melody[self.alarm_zone][1]
                print("Alarm timeout")
                self.state = STATE_SIGNAL

        elif  self.state == STATE_SIGNAL:
           if time.monotonic() > self.timeout:
                print("Signal timeout")
                self.zone_prev_active_status[self.alarm_zonezone] = 0
                self.state = STATE_IDLE           
            
 

