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