import FIND3_API
from FileManipulation import *
from Calculation import *
from Draw import *
familyName="FYCYC19951011"
fileName="rawData.txt"

#print(FIND3_API.Ping_Server())
#print(FIND3_API.Current_Time())
#print(FIND3_API.Family_Setup(familyName))

#print(FIND3_API.Delete_All_Data(familyName))

# print(FIND3_API.Post_Data(jsonData1))
# print(FIND3_API.Post_Data(jsonData2))
# print(FIND3_API.Post_Data(jsonData3))
#print(FIND3_API.Post_PassiveData(jsonData1))
#print(FIND3_API.Post_PassiveData(jsonData2))
#print(FIND3_API.Post_PassiveData(jsonData3))
#print(FIND3_API.Post_Data(FIND3_API.Return_Json(0,-60)))
#print(FIND3_API.Post_Data(FIND3_API.Return_Json(1,-50)))
#print(FIND3_API.Post_Data(FIND3_API.Return_Json(2,-60)))

text=FIND3_API.Get_Database(familyName)
WriteFile(fileName,text)
TrackedDevices,Signals,Sensors=ParseFile(fileName)

WriteFile("TrackedDevices.txt",TrackedDevices,isJson=True)
WriteFile("Signals.txt",Signals,isJson=True)
WriteFile("Sensors.txt",Sensors,isJson=True)

draw=Draw()
sensorPositions={"a":[2,3.29],"c":[6.35,2.1],"b":[6.35,9.5]}
draw.SetMap(12,12,1)
timestamp="1554820270500"
draw.Draw(sensorPositions,TrackedDevices,Signals,Sensors,timestamp)



# Signals=[{"timestamp": "1", "deviceID": "G", "sensordata": {"a": -87,"c":-74,"b":-85,}}]
#
# draw=Draw()
# sensorPositions={"a":[5,5],"b":[5,10],"c":[15,5]}
# draw.SetMap(20,15,1)
# timestamp="1"
# draw.Draw(sensorPositions,TrackedDevices,Signals,Sensors,timestamp)