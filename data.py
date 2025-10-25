# data module
from micropython import const
import time

MODE_UNDEFINED     = const(0)
MODE_AT_HOME       = const(1)
MODE_COUNT_DOWN    = const(2)
MODE_AWAY          = const(3)
MODE_WARNING       = const(4)

ZONE_UNDEF  = const(0)
ZONE_PIHA   = const(1)
ZONE_RANTA  = const(2)
ZONE_VA     = const(3)
ZONE_LA     = const(4)

play_wave = True
use_i2s = True
sd_card_is_ok = False


mode = {'index': MODE_UNDEFINED, 'changed':True}
rfm_gateway = {'module_tag':'G', 'module_addr':'1', 'function': 'O', 'index': '1'}
   
date_time = time.struct_time((2024, 3, 28, 12, 0, 0, 6, -1, -1))

#hms = {'hour':0,'minute':0,'second':0}
#ymd = {'year':0,'month':0,'day':0}