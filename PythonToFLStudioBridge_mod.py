import mido
from mido import Message
import time

path = r"C:\Users\Niitro_musics\Documents\Image-Line\FL Studio\Settings\Hardware\a\script.py"
floor_point = [0, 0]

def setFloor(new_floor_point: list = [0, 0]):
    global floor_point
    if isinstance(new_floor_point, list) and len(new_floor_point) == 2:
        floor_point = new_floor_point
        print(f"Floor point updated to: {floor_point}")
    else:
        print("Invalid floor point input. Must be a list with two elements.")

def img_percent(img_size, pos, axis):
    return 1 - ((pos - floor_point[axis]) / (img_size - floor_point[axis]))

def Percent_from_current(img: tuple, pos: tuple, custom_floor_point: tuple = None):
    floor_point_to_use = custom_floor_point if custom_floor_point else floor_point
    x_full, y_full = img
    x_pos, y_pos = pos
    return (img_percent(x_full, x_pos, 0), img_percent(y_full, y_pos, 1))

def data_writer(data, path=path):
    with open(path, 'w') as file:
        percent_data = Percent_from_current((480, 640), tuple(data))
        file.write(f"Data: {percent_data}")
        print(f"Data saved to {path}")
        return percent_data

def SendCC(percent, ctrl, channel=1):
    percent = max(0, min(percent, 1))
    
    try:
        with mido.open_output(mido.get_output_names()[1]) as outport:
            midi_value = int(percent * 127)
            cc_message = Message('control_change', control=ctrl, value=midi_value, channel=channel)
            outport.send(cc_message)
            print(f"Sent CC message: {cc_message}")

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

    except Exception as e:
        print(f"Error sending MIDI message: {e}")
        
def getCC(ctrl, channel=0, timeout=2):
    try:
        with mido.open_input(mido.get_input_names()[1]) as inport:
            print(f"Listening on {mido.get_input_names()[1]} for control {ctrl}...")
            start_time = time.time()
            while time.time() - start_time < timeout:
                if inport.poll():
                    msg = inport.receive()
                    # print(f"Received message: {msg}")
                    if msg.control == ctrl and msg.channel == channel: #msg.type == 'control_change' and 
                        print(f"Received CC message: {msg}")
                        return msg.value
            print("Timeout reached, no message received.")
    except Exception as e:
        print(f"Error receiving MIDI message: {e}")
    return 0

a=getCC(2)
print(a)
print('end')