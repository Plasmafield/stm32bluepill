import serial
import time

ACK = 0x79
hello_byte = bytes([0x7F])
get_version_cmd = bytes([0x1, 0xFE])
get_cmds_cmd = bytes([0x0, 0xFF])

def valid_resp(data):
    if len(data) == 0:
        return False
    if data[0] != ACK:
        return False
    return True

def get_version(com):
    com.write(get_version_cmd)
    resp = com.read(5)
    if not valid_resp(resp):
        return 0
    return resp[1]

def hello(com):
    retry = 3
    valid = False

    while retry != 0:
        retry = retry - 1

        com.write(hello_byte)
        resp = com.read(1)
        
        valid = valid_resp(resp)
        if valid:
            break
    
    return valid

com = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1, parity=serial.PARITY_EVEN)

if not hello(com):
    print("Coult not establish bootloader UART communication")

version = get_version(com)
print("Bootloader version: " + hex(version))

com.close()
