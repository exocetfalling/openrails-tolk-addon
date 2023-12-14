import urllib.request, json 
from cytolk import tolk
import keyboard

is_active = True

cutoff = 0.00
regulator = 0.00
firebox = 0.00
firehole = 0.00
train_brake = 0.00
steam_pr = 0.00
brake_pipe = 0.00
main_res = 0.00

min_value = 0.00
max_value = 0.00
dec_value = 0.00
pct_value = 0.00

def on_space():
    print('space was pressed')

    with tolk.tolk():
        with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
            data = json.load(url)
            data_str = str(data)
            #data_obj = json.loads(data_str)
            #print(data)
        #    print()

        # Print data using loop
        for element in data:
            for key in element:
                value = element[key]
                print(key, ":", value)
                if key == "TypeName":
                    if value == "TRAIN_BRAKE":
                        tolk.speak("TRAIN BRAKE")
                    elif value == "STEAM_PR":
                        tolk.speak("STEAM_PRESSURE")
                    else:
                        tolk.speak(value)
                
                if key == "RangeFraction":
                    pct_value = round(value * 100)
                    tolk.speak(str(pct_value))
                    tolk.speak("percent")
 
keyboard.add_hotkey('space', on_space)

while is_active == True:
    #with urllib.request.urlopen("http://localhost:2150//API/TRAININFO") as url:
    pass