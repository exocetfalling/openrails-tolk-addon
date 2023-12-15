import urllib.request, json 
from cytolk import tolk
import keyboard
import time 

is_active = True

cab_controls_dict = {
    "CUTOFF": 0.00,
    "REGULATOR": 0.00,
    "FIREBOX": 0.00,
    "FIREHOLE": 0.00,
    "TRAIN_BRAKE": 0.00,
    "STEAM_PR": 0.00,
    "BRAKE_PIPE": 0.00,
    "WHISTLE": 0.00,
    "ENGINE_BRAKE": 0.00,
    "MAIN_RES": 0.00,
}

time_current = 0.00
time_previous = 0.00
time_elapsed = 0.00

conn_success = False
conn_retries = 0
CONN_RETRIES_MAX = 10

# load the library
tolk.load()

def on_hotkey_full(): 
    pass

def on_hotkey_regulator(): 
    tolk.speak("REGULATOR")
    tolk.speak(str(round(cab_controls_dict["REGULATOR"] * 100)))
    tolk.speak("percent")
    print("REGULATOR:", str(round(cab_controls_dict["REGULATOR"] * 100)))

def on_hotkey_reverser():
    tolk.speak("REVERSER")
    tolk.speak(str(round(cab_controls_dict["CUTOFF"] * 100)))
    tolk.speak("percent")
    print("REVERSER:", str(round(cab_controls_dict["CUTOFF"] * 100)))

keyboard.add_hotkey('ctrl+a', on_hotkey_full)
keyboard.add_hotkey('a', on_hotkey_regulator)
keyboard.add_hotkey('d', on_hotkey_regulator)
keyboard.add_hotkey('w', on_hotkey_reverser)
keyboard.add_hotkey('s', on_hotkey_reverser)

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
                cab_controls_dict[element["TypeName"]] = element["RangeFraction"]
            
            #print("USER DICT:")
            #print(cab_controls_dict)



            time_elapsed = 0