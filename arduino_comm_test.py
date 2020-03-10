from serial.tools import list_ports
import numpy
import serial
import time


def serial_ports_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port_no, description, address in ports:
        if 'LOCATION=1-1' in address:
            return port_no



ser_arduino = serial.Serial(
    port=serial_ports_arduino(),
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
print(ser_arduino.isOpen())
print(ser_arduino.name)


if_ici_sayac=0

for a in range(50):
    print(a)
    ser_arduino.write("a".encode('utf-8'))
    time.sleep(1)
    #if(ser_arduino.read()== b'b'):
    #    #ser_arduino.flushInput()
    #    #ac = ser_sensor.write(g_measuring_val_3.encode('utf-8'))
    #    ## time.sleep(0.02)
    #    #if (ser_sensor.inWaiting()):
    #    #    data.append(ser_sensor.readline())
    #    #    print("evet")
    #    #else:
    #    #    print("hayır")
    #    #    data.append(b':01A;0;0;-3000;0 ;9583\r\n')
    #    if_ici_sayac = if_ici_sayac + 1
