import urllib.request, json 
from cytolk import tolk
import keyboard
import time 

is_active = True

cab_controls_dict = {}
cab_controls_dict_prev = {}
cab_controls_dict_changed = {}

time_current = 0.00
time_previous = 0.00
time_elapsed = 0.00

conn_success = False
conn_retries = 0
CONN_RETRIES_MAX = 10

# load the library
tolk.load()
tolk.try_sapi(True)

def get_data():
    with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
        data = json.load(url)

def map_value_to_range(value_frac, value_max, value_min):
    value_range = value_max - value_min
    value_mapped = value_range * value_frac + value_min
    return value_mapped

def on_hotkey_full(): 
    pass

def on_hotkey_brake_button():
    tolk.output("EMERGENCY BRAKE")

def on_hotkey_speed_check():
    tolk.output("SPEEDOMETER")
    tolk.output(str(round(cab_controls_dict["SPEEDOMETER"])))
    print("SPEEDOMETER:", str(round(cab_controls_dict["SPEEDOMETER"])))

keyboard.add_hotkey('ctrl+a', on_hotkey_full)
keyboard.add_hotkey('shift+v', on_hotkey_speed_check)

while is_active == True:
    #with urllib.request.urlopen("http://localhost:2150//API/TRAININFO") as url:
    try:
        with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
            pass
    
    except:
        time_current = time.time()
        time_elapsed += (time_current - time_previous)
        time_previous = time_current

        if conn_success == True:
            conn_success = False
            print("Connection lost.")
            tolk.output("Connection lost.")

        if time_elapsed >= 5:
            print("Error trying to connect.")
            print("Retrying.")
            tolk.output("Error trying to connect. Retrying.")

            conn_retries += 1
            print("Attempt", conn_retries)
            tolk.output("Attempt")
            tolk.output(str(conn_retries))

            time_elapsed = 0
        
        if conn_retries >= CONN_RETRIES_MAX:
            print("Too many connection failures. Exiting script.")
            tolk.output("Too many connection failures. Exiting script.")

            tolk.unload()
            exit()
    
    else:
        with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
            data = json.load(url)
        
        if conn_success == False:
            conn_success = True
            print("Connection success.")
            tolk.output("Connection success.")

            tolk.output("This is confirmed to be the correct version.")

        time_current = time.time()
        time_elapsed += (time_current - time_previous)
        time_previous = time_current


        if time_elapsed >= 0.5:
            #print("time")

            # Print data using loop
            for element in data:
                cab_controls_dict[element["TypeName"]] = \
                    map_value_to_range( \
                    element["RangeFraction"],
                    element["MaxValue"] ,
                    element["MinValue"]
                    )
            
            # Purge dictionary of changes for next iteration
            cab_controls_dict_changed = {}

            for key in cab_controls_dict:
                if cab_controls_dict_prev == {}:
                    # print("Dict empty, populating.")
                    cab_controls_dict_prev = cab_controls_dict.copy()
                if cab_controls_dict[key] != cab_controls_dict_prev[key]:
                    cab_controls_dict_changed[key] = cab_controls_dict[key]
                
            cab_controls_dict_prev = cab_controls_dict.copy()
            
            # print(cab_controls_dict_changed)

            for key in cab_controls_dict_changed:
                value = cab_controls_dict_changed[key]

                if "REGULATOR" in key:
                    print(key, "->", value * 100)
                    tolk.output("REGULATOR")
                    tolk.output(str(round(value * 100)))
                    tolk.output("Percent")
                if "REVERSER" in key:
                    print(key, "->", value * 100)
                    tolk.output("REVERSER")
                    tolk.output(str(round(value * 100)))
                    tolk.output("Percent")
                if "COCKS" in key:
                    if value > 0.5:
                        print("Cylinder cocks open.")
                        tolk.output("Cylinder cocks open.")
                    else:
                        print("Cylinder cocks closed.")
                        tolk.output("Cylinder cocks closed.")
                if "GEAR" in key:
                    print(key, "->", value)
                    tolk.output("GEAR")
                    tolk.output(str(round(value)))
                if "DIRECTION" in key:
                    print(key, "->", value)
                    tolk.output("DIRECTION")
                    if value == 0:
                        tolk.output("REVERSE")
                    if value == 1:
                        tolk.output("NEUTRAL")
                    if value == 2:
                        tolk.output("FORWARD")
                if "THROTTLE" in key:
                    print(key, "->", value * 100)
                    tolk.output("THROTTLE")
                    tolk.output(str(round(value * 100)))
                    tolk.output("Percent")
                if "TRAIN_BRAKE" in key:
                    print(key, "->", value * 100)
                    tolk.output("TRAIN BRAKE")
                    tolk.output(str(round(value * 100)))
                    tolk.output("Percent")
                if "ENGINE_BRAKE" in key:
                    print(key, "->", value * 100)
                    tolk.output("ENGINE BRAKE")
                    tolk.output(str(round(value * 100)))
                    tolk.output("Percent")
            time_elapsed = 0