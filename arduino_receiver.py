import serial
import time

arduino_port = 'COM7'
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # allow Arduino to reset

print("Reading touch sensor data from Arduino...")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line=="TOUCHED":
                print("Sensor:", line)

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
