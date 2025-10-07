import busio
# import digitalio
# import time
import pico_rtc_u2u_sd_gpio as gpio

from micropython import const

CONST_MAX_MSG_LEN = const(32)

class UartCom:
    def __init__(self, tx_pin, rx_pin, baudrate ):        
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=10)
        self.msg = ""
        self.parsed = {'module': 'M', 'index': '0', 'key':'xx', 'data':''}
        self.send   = {'module': 'M', 'index': '0', 'key':'xx', 'data':''}
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
        print('msg_frame_is_ok? ',self.msg)
        begin = self.msg.find('<')
        end = self.msg.find('>')
        is_ok = False
        if begin >=0 and end > 0:
            self.msg = self.msg[begin+1:end]
            is_ok = True
        return is_ok
    def parse_msg(self):
        # C1Tg:2023;09;21;19;50
        l = len(self.msg)
        print(l)
        if l >= 4:
            self.parsed['module'] = self.msg[0]
            self.parsed['index'] = self.msg[1]
            self.parsed['key'] = self.msg[2:4]
        if (l >= 6):
            if (self.msg[4] == ':'):
                self.parsed['data'] = self.msg[5:]
                
    def send_dict_msg(self, sdata ):
        buff = '<' + sdata['module'] + sdata['index'] + sdata['key'] + \
            ':' + sdata['data'] + '>\r\n'
        self.send_msg(buff)    
        print(buff)
         
'''
<C1TS:123>
<C1TS:2023;09;21;19;50>
'''
        
        
            
'''
ucom = UartCom(gpio.TX0_PIN, gpio.RX0_PIN, 9600)
while 1:
    msg = ucom.read_msg()
    if len(msg) > 0:
        print(msg)
        ucom.send_msg(msg)
        if ucom.msg_frame_is_ok():
            print(ucom.msg)
            ucom.parse_msg()
            print(ucom.parsed)
        else:
            print("Frame error: ",ucom.msg)
            
'''

