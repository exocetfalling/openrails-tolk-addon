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

def get_data():
    with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
        data = json.load(url)

def map_value_to_range(value_frac, value_max, value_min):
    value_range = value_max - value_min
    value_mapped = value_range * value_frac + value_min
    return value_mapped

def on_hotkey_full(): 
    pass

def on_hotkey_speed_check():
    tolk.speak("SPEED")
    tolk.speak(str(round(cab_controls_dict["SPEEDOMETER"])))
    print("SPEED:", str(round(cab_controls_dict["SPEEDOMETER"])))

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
            tolk.speak("Connection lost.")

        if time_elapsed >= 5:
            print("Error trying to connect.")
            print("Retrying.")
            tolk.speak("Error trying to connect. Retrying.")

            conn_retries += 1
            print("Attempt", conn_retries)
            tolk.speak("Attempt")
            tolk.speak(str(conn_retries))

            time_elapsed = 0
        
        if conn_retries >= CONN_RETRIES_MAX:
            print("Too many connection failures. Exiting script.")
            tolk.speak("Too many connection failures. Exiting script.")

            tolk.unload()
            exit()
    
    else:
        with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
            data = json.load(url)
        
        if conn_success == False:
            conn_success = True
            print("Connection success.")
            tolk.speak("Connection success.")

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
                    print("Dict empty, populating.")
                    cab_controls_dict_prev = cab_controls_dict.copy()
                if cab_controls_dict[key] != cab_controls_dict_prev[key]:
                    cab_controls_dict_changed[key] = cab_controls_dict[key]
                
            cab_controls_dict_prev = cab_controls_dict.copy()
            
            # print(cab_controls_dict_changed)

            for key in cab_controls_dict_changed:
                value = cab_controls_dict_changed[key]

                if "REGULATOR" in key:
                    print(key, "->", value * 100)
                    tolk.speak("REGULATOR")
                    tolk.speak(str(round(value * 100)))
                    tolk.speak("Percent")
                if "REVERSER" in key:
                    print(key, "->", value * 100)
                    tolk.speak("REVERSER")
                    tolk.speak(str(round(value * 100)))
                    tolk.speak("Percent")
                if "COCKS" in key:
                    if value > 0.5:
                        print("Cylinder cocks open.")
                        tolk.speak("Cylinder cocks open.")
                    else:
                        print("Cylinder cocks closed.")
                        tolk.speak("Cylinder cocks closed.")
                if "GEAR" in key:
                    print(key, "->", value)
                    tolk.speak("GEAR")
                    tolk.speak(str(round(value)))
                if "DIRECTION" in key:
                    print(key, "->", value)
                    tolk.speak("DIRECTION")
                    if value == 0:
                        tolk.speak("REVERSE")
                    if value == 1:
                        tolk.speak("NEUTRAL")
                    if value == 2:
                        tolk.speak("FORWARD")
                    tolk.speak(str(round(value)))
                if "TRAIN_BRAKE" in key:
                    print(key, "->", value * 100)
                    tolk.speak("TRAIN BRAKE")
                    tolk.speak(str(round(value * 100)))
                    tolk.speak("Percent")
                if "ENGINE_BRAKE" in key:
                    print(key, "->", value * 100)
                    tolk.speak("ENGINE BRAKE")
                    tolk.speak(str(round(value * 100)))
                    tolk.speak("Percent")
            time_elapsed = 0