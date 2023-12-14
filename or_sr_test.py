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

def on_hotkey_full(): 
    print('space was pressed')

    with tolk.tolk():
        pass

def on_hotkey_regulator(): 
    with tolk.tolk():
        tolk.speak("REGULATOR")
        tolk.speak(str(round(cab_controls_dict["REGULATOR"] * 100)))
        tolk.speak("percent")

def on_hotkey_reverser(): 
    with tolk.tolk():
        tolk.speak("REVERSER")
        tolk.speak(str(round(cab_controls_dict["CUTOFF"] * 100)))
        tolk.speak("percent")

keyboard.add_hotkey('ctrl+a', on_hotkey_full)
keyboard.add_hotkey('a', on_hotkey_regulator)
keyboard.add_hotkey('d', on_hotkey_regulator)
keyboard.add_hotkey('w', on_hotkey_regulator)
keyboard.add_hotkey('s', on_hotkey_regulator)

while is_active == True:
    #with urllib.request.urlopen("http://localhost:2150//API/TRAININFO") as url:

    with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
        data = json.load(url)
    
    time_current = time.time()
    time_elapsed += (time_current - time_previous)
    time_previous = time_current


    if time_elapsed >= 10:
        print("time")

        # Print data using loop
        for element in data:
            cab_controls_dict[element["TypeName"]] = element["RangeFraction"]
        
        print("USER DICT:")
        print(cab_controls_dict)



        time_elapsed = 0