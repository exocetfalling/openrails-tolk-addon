import urllib.request, json 
#with urllib.request.urlopen("http://localhost:2150/API/APISAMPLE") as url:
with urllib.request.urlopen("http://localhost:2150/API/CABCONTROLS") as url:
    data = json.load(url)
    data_str = str(data)
    #data_obj = json.loads(data_str)
    #print(data)

# Print data using loop
for element in data:
    for key in element:
        value = element[key]
        if key == "TypeName":
            print("Name:", value)
        else:
            print(key, ":", element[key])