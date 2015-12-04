import time

import serial

ser = serial.Serial(0)
print ser.portstr
o_str_hex = '\xfe\x05\x00\x03\xff\x00\x68\x35'
c_str_hex = '\xfe\x05\x00\x03\x00\x00\x29\xc5'
ser.write(o_str_hex)
time.sleep(5)
ser.write(c_str_hex)
ser.close()
