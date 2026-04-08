import serial
import time

ACK = 0x79
NACK = 0x1F
hello_byte = bytes([0x7F])
get_version_cmd = bytes([0x1, 0xFE])
get_cmds_cmd = bytes([0x0, 0xFF])
read_mem_cmd = bytes([0x11, 0xEE])

def valid_resp(data):
    if len(data) == 0:
        return False
    if data[0] != ACK:
        return False
    return True

def check_nack(data):
    if len(data) == 0:
        return False
    if data[0] != NACK:
        return False
    return True

def get_version(com):
    com.write(get_version_cmd)
    resp = com.read(5)
    if not valid_resp(resp):
        return 0
    return resp[1]

def hello(com):
    retry = 2

    while retry != 0:
        retry = retry - 1

        com.write(hello_byte)
        resp = com.read(1)
        
        valid = valid_resp(resp)
        if valid:
            return True
        if check_nack(resp): # Bootloader already initialized for UART
            return True
    
    return False

def read_uart(com, addr, size):
    data = bytes(size)
    read_len = 0

    #while read_len < size:
        size_left = size - read_len

        #com.write(read_mem_cmd)
        #resp = com.read(1)
        #if not valid_resp(resp):
        #    return None

        addr_bytes = addr.to_bytes(4, "big")
        addr_xor = addr_bytes[0]
        for byte in addr_bytes[1:]:
            addr_xor = addr_xor ^ byte
        addr_xor = addr_xor.to_bytes(1)

        #com.write(addr_bytes)
        #com.write(addr_xor)
        #resp = com.read(1)
        #if not valid_resp(resp):
        #    return None

        to_read = size_left
        if to_read > 255:
            to_read = 255
        to_read_checksum = to_read ^ (to_read ^ 0xFF)

        #com.write(bytes([to_read, to_read_checksum]))
        #rest = com.read(1)
        #if not valid_resp(resp):
        #    return None

        bt1 = bytes([0x1, 0x2])
        bt2 = bytes([0x3, 0x4])
        bt3 = bt1 + bt2
        print(bt3)

com = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1, parity=serial.PARITY_EVEN)

if not hello(com):
    print("Coult not establish bootloader UART communication")
    exit()
else:
    print("Bootloader initialized for UART")

version = get_version(com)
print("Bootloader version: " + hex(version))

read_uart(com, 0x8000000, 255)

com.close()
