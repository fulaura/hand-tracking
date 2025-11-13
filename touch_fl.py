import time
import numpy as np
import PythonToFLStudioBridge as PTSB
import mido
import serial

arduino_port = 'COM7'
baud_rate = 9600
input_list=[]

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # allow Arduino to reset

print("Reading touch sensor data from Arduino...")
time1 = None
try:
    with mido.open_output(mido.get_output_names()[1]) as outport:
        while True:
            if(len(input_list)<10): input_list.append(ser.readline().decode('utf-8', errors='ignore').strip())
            else: input_list.pop(0); input_list.append(ser.readline().decode('utf-8', errors='ignore').strip())
            time1 = [time.time() if time1 is None else time1][0] 
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line=="TOUCHED":
                    print("Sensor:", line)
                    time2 = time.time()
                    elapsed_time = time2 - time1
                    print(f"Elapsed time since last touch: {elapsed_time} seconds")
                    if elapsed_time > 0.8:
                        time1=time2
                        pitch= np.random.randint(10, 128)
                        outport.send(mido.Message('note_on', note=pitch, velocity=100, channel=1))
                        time.sleep(0.1)
                        outport.send(mido.Message('note_off', note=pitch, velocity=0, channel=1))
                        print("Sent MIDI Note On/Off")
                        # print(f"Sending random pitch CC: {pitch}")
                        outport.send(mido.Message('control_change', control=2, value=pitch, channel=1))
                    else: print("Ignored")
                
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
