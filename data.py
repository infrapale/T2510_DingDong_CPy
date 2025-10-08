# data module
from micropython import const
import time

MODE_UNDEFINED     = const(0)
MODE_AT_HOME       = const(1)
MODE_COUNT_DOWN    = const(2)
MODE_AWAY          = const(3)
MODE_WARNING       = const(4)

ALARM_OFF         = const(0)
ALARM_ON          = const(1)

STATE_UNDEFIED = const(0)
STATE_AT_HOME_ALARM_OFF     = MODE_AT_HOME * 10 + ALARM_OFF
STATE_AT_HOME_ALARM_ON      = MODE_AT_HOME * 10 + ALARM_ON 
STATE_COUNT_DOWN_ALARM_OFF  = MODE_COUNT_DOWN * 10 + ALARM_OFF
STATE_COUNT_DOWN_ALARM_ON   = MODE_COUNT_DOWN * 10 + ALARM_ON
STATE_AWAY_ALARM_OFF        = MODE_AWAY * 10 + ALARM_OFF
STATE_AWAY_ALARM_ON         = MODE_AWAY * 10 + ALARM_ON    

mode = {'index': MODE_UNDEFINED, 'changed':True}
date_time = time.struct_time((2024, 3, 28, 12, 0, 0, 6, -1, -1))

#hms = {'hour':0,'minute':0,'second':0}
#ymd = {'year':0,'month':0,'day':0}