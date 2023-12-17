"""
Python script for making Open Rails screen reader friendly using cytolk.
"""

import urllib.request, json 
from cytolk import tolk
import keyboard
import time 

CAB_CONTROLS_API_URL = "http://localhost:2150/API/CABCONTROLS"

# Currently just True, might change in future
is_active = True

# Dictionaries for data
cab_controls_dict = {}
cab_controls_dict_prev = {}
cab_controls_dict_changed = {}

# Time variables
time_current = 0.00
time_previous = 0.00
time_elapsed = 0.00

# Connection variables
conn_success = False
CONN_INTERVAL = 0.5 
conn_retries = 0
CONN_RETRIES_MAX = 10
CONN_RETRIES_INTERVAL = 5

# Load the library
tolk.load()
tolk.try_sapi(True)

def get_data():
    """Get data from the API."""
    with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
        data = json.load(url)

def map_value_to_range(value_frac, value_max, value_min):
    """Map from fraction to Open Rails range.

    Converts between the fraction in the API to the in-game displayed value.
    Note that, for percentages, the returned value must be multiplied by 100.
    """
    value_range = value_max - value_min
    value_mapped = value_range * value_frac + value_min
    return value_mapped

def on_hotkey_speed_check():
    """Output speed displayed by speedometer.

    Outputs speed after rounding the value in cab_controls_dict and converting it to a string.
    """
    tolk.speak("SPEEDOMETER")
    tolk.speak(str(round(cab_controls_dict["SPEEDOMETER"])))
    print("SPEEDOMETER:", str(round(cab_controls_dict["SPEEDOMETER"])))

def on_hotkey_exit():
    """Output closing message and exit."""
    tolk.speak("Exiting script")
    tolk.unload()

# Add a keyboard hotkey for speed checks
keyboard.add_hotkey('shift+v', on_hotkey_speed_check)
# Add a keyboard hotkey for exiting
keyboard.add_hotkey('alt+f4', on_hotkey_exit)

# Main loop
while is_active == True:
    try:
        # Try loading the API's cab controls URL
        with urllib.request.urlopen(CAB_CONTROLS_API_URL) as url:
            pass
    
    except:
        # If connection failed
        time_current = time.time()
        time_elapsed += (time_current - time_previous)
        time_previous = time_current

        # If it was connected in the last iteration
        if conn_success == True:
            conn_success = False
            print("Connection lost.")
            tolk.speak("Connection lost.")

        if time_elapsed >= CONN_RETRIES_INTERVAL:
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
        # If connection succeeded, proceed as normal
        with urllib.request.urlopen(CAB_CONTROLS_API_URL) as url:
            data = json.load(url)
        
        if conn_success == False:
            conn_success = True
            print("Connection success.")
            tolk.speak("Connection success.")

            print("Version 0.0.8.")
            tolk.speak("Version 0.0.8.")

        time_current = time.time()
        time_elapsed += (time_current - time_previous)
        time_previous = time_current

        if time_elapsed >= 0.25:
            # Load data using loop
            for element in data:
                cab_controls_dict[element["TypeName"]] = \
                    map_value_to_range( \
                    element["RangeFraction"],
                    element["MaxValue"] ,
                    element["MinValue"]
                    )
            
            # Purge dictionary of changes
            cab_controls_dict_changed = {}

            # Compare current and previous data
            # If values changed, add them to cab_controls_dict_changed
            for key in cab_controls_dict:
                if cab_controls_dict_prev == {}:
                    cab_controls_dict_prev = cab_controls_dict.copy()
                if cab_controls_dict[key] != cab_controls_dict_prev[key]:
                    cab_controls_dict_changed[key] = cab_controls_dict[key]
            
            # Bring old data up to date 
            cab_controls_dict_prev = cab_controls_dict.copy()
            
            for key in cab_controls_dict_changed:
                value = cab_controls_dict_changed[key]

                # If words like these are in the dictionary
                # We match substrings, not the whole string
                # This is because different trains have different vars
                # They usually contain these substrings
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
                if "THROTTLE" in key:
                    print(key, "->", value * 100)
                    tolk.speak("THROTTLE")
                    tolk.speak(str(round(value * 100)))
                    tolk.speak("Percent")
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