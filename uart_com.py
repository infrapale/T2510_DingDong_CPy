'''

    Get Decoded Message:
    <A1D1?->
     \\\\\\______ value, message (optional ='-')
      \\\\\______ action get    (set: '=' get: '?' reply: ':')
       \\\\______ index         '1' dummy for future use
        \\\______ function      'D' Get Decoded Message
         \\______ module_addr   '1' 
           \_____ module_tag    'A' Gateway



    Get Alarm Status:
    <G1A0?x>
     \\\\\\______ value, message (optional)
      \\\\\______ action get    (set: '=' get: '?' reply: ':')
       \\\\______ index '0' dummy for future use
        \\\______ function      'A' Alarm
         \\______ module_addr '1' 
           \_____ module_tag 'G' Gateway

    Alarm Status Reply 
    <G1A0?x>
     \\\\\\______ value 0 = no alarm, 1..9 = alarm active
      \\\\\______ action reply:  ':'
       \\\\______ index '0' dummy for future use
        \\\______ function      'A' Alarm
         \\______ module_addr '1' 
           \_____ module_tag 'G' Gateway

    Get Home Status:    <G1H0?x>
    Home Status Reply:  <G1H0:n>  n = 0..3  (0=undefined, 1=at home, 2=countdown, 3=away)
           
'''

import busio
# import digitalio
# import time
import pico_rtc_u2u_sd_gpio as gpio

from micropython import const

MODULE_69 = 'A'  # RFM69 Module Address


CONST_MAX_MSG_LEN = const(32)

class UCom:
    def __init__(self, tx_pin, rx_pin, baudrate ):        
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=10)
        self.msg = ""
        self.parsed             = {'module': 'X', 'maddr': '1', 'function':'X', 'index': '0', 'action': '-', 'data': ''}
        self.get_decoded_msg    = {'module': MODULE_69, 'maddr': '1', 'function':'D', 'index': '1', 'action': '?', 'data': '-'}
        self.get_raw_msg        = {'module': MODULE_69, 'maddr': '1', 'function':'W', 'index': '1', 'action': '?', 'data': '-'}
 
    def read_msg(self):
        self.msg = "" 
        if self.uart.in_waiting > 0: 
            bmsg = self.uart.readline(CONST_MAX_MSG_LEN)
            self.msg = ''.join([chr(b) for b in bmsg]) # convert bytearray to string
        return self.msg

    def send_msg(self, message):
        barr = bytearray(message, 'utf-8')
        self.uart.write(barr)

    def msg_frame_is_ok(self):
        begin = self.msg.find('<')
        end = self.msg.find('>')
        is_ok = False
        if begin >=0 and end > 0:
            self.msg = self.msg[begin+1:end]
            #print('msg_frame_is_ok! ',self.msg)
            is_ok = True
        else:    
            #print('msg_frame not ok! ',self.msg)    
            is_ok = False
        return is_ok
    
    def parse_msg(self):
        # C1Tg:2023;09;21;19;50
        l = len(self.msg)
        #print(l)
        if l == 6:
            self.parsed['module'] = self.msg[0]
            self.parsed['maddr'] = self.msg[1]
            self.parsed['function'] = self.msg[2]
            self.parsed['index'] = self.msg[3]
            self.parsed['action'] = self.msg[4]
            self.parsed['data'] = self.msg[5]
                
    def send_dict_msg(self, sdata ):
        #print(sdata)
        buff = '<' + sdata['module'] + sdata['maddr'] + sdata['function'] + sdata['index'] + \
            sdata['action'] + sdata['data'] + '>\r\n'
        # print(buff)
        self.send_msg(buff)    
    
    def send_get_home_state(self):
        pass
        #self.send_dict_msg(self.get_home_state)

    def send_get_alarm_state(self):
        pass
        #cself.send_dict_msg(self.get_alarm_state)
    
        
