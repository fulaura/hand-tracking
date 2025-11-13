path = r"C:\Users\Niitro_musics\Documents\Image-Line\FL Studio\Settings\Hardware\a\script.py"
floor_point=[0,0]

def setFloor(floor_point: int):
    floor_point=floor_point

def img_percent(img, pos, axis):
    return 1-((pos-floor_point[axis])/(img-floor_point[axis]))#*100        +0.0000001

def Percent_from_current(img:tuple, pos:tuple): #, floor_point:tuple
    x_full, y_full=img
    x_pos, y_pos=pos
    # x_min, y_min=floor_point
    # a=img_percent(x_full, x_pos, 0), img_percent(y_full, y_pos, 1)
    # print(a)
    return (img_percent(x_full, x_pos, 0), img_percent(y_full, y_pos, 1))

def data_writer(data, path=path):
    with open(path, 'w') as file:
        # file.write(f"data = {str(data)}")
        #file.write(f"data = {Percent_from_current((480,640), tuple(data))}")
        # print("saved")
        return Percent_from_current((480,640), tuple(data))


import mido
from mido import Message
import time

def SendCC(percent, ctrl):
    with mido.open_output(mido.get_output_names()[1]) as outport:
        # print(f"Sending signals to: {outport}")
        try:
            #percent = float(input("Enter a percentage value (0-100): "))
            if percent < 0: percent=0
            elif percent > 1: percent=1
            # print("********************")
            #midi_value = int((percent / 100) * 127)
            midi_value = int(percent * 127)
            # print('midi_val: ', midi_value)
                
                # Create and send a Control Change (CC) message
            cc_message = Message('control_change', control=ctrl, value=midi_value)
            outport.send(cc_message)
            print(f"Sent CC message: {cc_message}")
            #time.sleep(1)

        except KeyboardInterrupt:
            print("\nExiting...")
            exit()