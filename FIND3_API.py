import requests
import json

BASE_URL="https://cloud.internalpositioning.com"

def Ping_Server():
    """This is useful for seeing if the server is up."""
    results=requests.get(url=BASE_URL+"/ping")
    content=results.content
    if(content==b"pong"):
        return True
    return False

def Current_Time():
    """This is useful for seeing if the server is up."""
    results = requests.get(url=BASE_URL + "/now")
    content = results.content
    return int(content.decode())

def Family_Setup(familyName):
    """This is the command to setup MQTT on FIND3 for your family. For more information see the MQTT document"""
    results = requests.get(url=BASE_URL + "/api/v1/mqtt/"+familyName)
    js = results.json()
    content = results.content
    return content.decode()

def Get_Database(familyName):
    """This will return the SQL data for the database which can be used to backup the current state of the entire database."""
    results = requests.get(url=BASE_URL + "/api/v1/database/" + familyName)
    content = results.content
    return content.decode()

def Delete_All_Data(familyName):
    """The FAMILY is the name of your family used for your recordings. Making this request will delete all your data, and it is not recoverable."""
    results = requests.delete(url=BASE_URL + "/api/v1/database/" + familyName)
    js = results.json()
    return js["success"]

def Post_Data(JsonData):
    """Post data to server"""
    results = requests.post(url=BASE_URL + "/data",data=json.dumps(JsonData))
    content=results.content
    js = results.json()
    return js["success"]

def Post_PassiveData(JsonData):
    """Post passive data to server"""
    results = requests.post(url=BASE_URL + "/passive",data=json.dumps(JsonData))
    content=results.content
    print(content.decode())
    js = results.json()
    return js["success"]

def Calibrate_AI(familyName):
    """This will update AI algorithms"""
    results = requests.get(url=BASE_URL + "/api/v1/calibrate/"+familyName)
    content = results.content
    return content.decode()

def Return_Json(id,signal):
    lat=[42.36934,42.35982,42.35982]
    lon=[-71.09000,-71.08990,-71.09010]
    location=["L1","L2","L3"]
    sig1 = [-40, -70, -70]
    sig2 = [-70, -40, -70]
    sig3 = [-70, -70, -40]
    time=Current_Time()
    print(time)
    jsonData = {
        "d": "20:25:64:b7:91:40",
        "f": "FYCYC19951012",
        "t": time,
        "l": location[id],
        "s": {
            "wifi": {
                "DEVICE1": sig1[id],
                "DEVICE2": sig2[id],
                "DEVICE3": sig3[id],
            }
        },
        "gps": {
            "lat": lat[id],#42.360,
            "lon": lon[id],#-71.091,
            "alt": 54
        }
    }
    return jsonData