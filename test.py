import time
import mido
import threading

def timed_input(prompt, timeout=5):
    result = {"value": None}

    def ask():
        try:
            result["value"] = input(prompt)
        except EOFError:
            result["value"] = None

    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None
    return result["value"]

def note_val(timeout=5):
    val = timed_input("Enter MIDI note number (0-127) or -1 to exit: ", timeout)
    if val is None: return None
    try: return int(val)
    except ValueError: return None

note = 60
velocity = 80
channel = 0
duration = 0

# Open MIDI port once
with mido.open_output(mido.get_output_names()[1]) as outport:
    while True:
        val = note_val(timeout=5)
        if val == -1:
            outport.send(mido.Message('note_off', note=note, velocity=0, channel=channel))
            print("Exiting…")
            break
        elif val is not None and 0 <= val <= 127:
            outport.send(mido.Message('note_off', note=note, velocity=0, channel=channel))
            note = val

        print(f"Playing note {note}")
        outport.send(mido.Message('note_on', note=note, velocity=velocity, channel=channel))
        time.sleep(duration)
        
        
        
def handle_note_iteration(outport, note, velocity, channel, duration, timeout=5):
    """
    Perform a single iteration of reading a note value and playing it.
    Returns (new_note, should_exit: bool).
    """
    val = note_val(timeout=timeout)
    if val == -1:
        outport.send(mido.Message('note_off', note=note, velocity=0, channel=channel))
        print("Exiting…")
        return note, True

    if val is not None and 0 <= val <= 127:
        outport.send(mido.Message('note_off', note=note, velocity=0, channel=channel))
        note = val

    print(f"Playing note {note}")
    outport.send(mido.Message('note_on', note=note, velocity=velocity, channel=channel))
    time.sleep(duration)

    return note, False