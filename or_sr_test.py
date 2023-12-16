import urllib.request, json 
from cytolk import tolk
import keyboard
import time 

is_active = True

cab_controls_dict = {}

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

def on_hotkey_regulator(): 
    tolk.speak("REGULATOR")
    tolk.speak(str(round(cab_controls_dict["REGULATOR"] * 100)))
    tolk.speak("percent")
    print("REGULATOR:", str(round(cab_controls_dict["REGULATOR"] * 100)))

def on_hotkey_reverser():
    tolk.speak("REVERSER")
    tolk.speak(str(round(cab_controls_dict["REVERSER_PLATE"] * 100)))
    tolk.speak("percent")
    print("REVERSER:", str(round(cab_controls_dict["REVERSER_PLATE"] * 100)))

def on_hotkey_train_brake():
    tolk.speak("TRAIN BRAKE")
    tolk.speak(str(round(cab_controls_dict["TRAIN_BRAKE"] * 100)))
    tolk.speak("percent")
    print("TRAIN BRAKE:", str(round(cab_controls_dict["TRAIN_BRAKE"] * 100)))

def on_hotkey_cyl_cocks():
    tolk.speak("CYLINDER COCKS")
    tolk.speak(str(round(cab_controls_dict["CYL_COCKS"] * 100)))
    tolk.speak("percent")
    print("CYLINDER COCKS:", str(round(cab_controls_dict["CYL_COCKS"] * 100)))

def on_hotkey_speed_check():
    tolk.speak("SPEED")
    tolk.speak(str(round(cab_controls_dict["SPEEDOMETER"])))
    tolk.speak("miles per hour")
    print("SPEED:", str(round(cab_controls_dict["SPEEDOMETER"])))

def on_hotkey_gear():
    tolk.speak("GEAR")
    tolk.speak(str(round(cab_controls_dict["GEARS"])))
    print("GEAR:", str(round(cab_controls_dict["GEARS"])))

keyboard.add_hotkey('ctrl+a', on_hotkey_full)
keyboard.add_hotkey('a', on_hotkey_regulator)
keyboard.add_hotkey('d', on_hotkey_regulator)
keyboard.add_hotkey('w', on_hotkey_reverser)
keyboard.add_hotkey('s', on_hotkey_reverser)
keyboard.add_hotkey('semicolon', on_hotkey_train_brake)
keyboard.add_hotkey('apostrophe', on_hotkey_train_brake)
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
            
            #print("USER DICT:")
            #print(cab_controls_dict)



            time_elapsed = 0