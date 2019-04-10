import re
import json
def WriteFile(fileName,text,isJson=False):
    """This function is for writing files"""
    if isJson:
        text=json.dumps(text)
    fo = open(fileName, "w")
    fo.write(text)
    fo.close()

def ParseFile(fileName):
    fi=open(fileName)
    TrackedDeviceList={}
    DetectedSignalList=[]
    SensorList={}
    while(True):
        line=fi.readline()
        if not line:
            break

        matchObj1=re.match(r'INSERT INTO "devices" VALUES\((.*),(.*)\)',line,re.M|re.I)
        matchObj2=re.match(r'INSERT INTO "sensors" VALUES\((.*)\)',line,re.M|re.I)
        matchObj4=re.match(r'INSERT INTO "keystore" VALUES\(\'sensorDataStringSizer\',\'"{\\"encoding\\":{(.*)},\\"current\\":(.*)}"\'\)',line,re.M|re.I)#\\"(.*)\\":\\"(.*)\\"
        if matchObj1:
            key=matchObj1.group(1).replace("\'","")
            value=matchObj1.group(2).replace("wifi-","").replace("\'","")
            TrackedDeviceList[key]=value
            # print(matchObj1.group(1))
            # print(matchObj1.group(2))
        if matchObj2:
            result=matchObj2.group(1).split(",")
            newresult=[]
            obj = {}
            dataobj={}
            for i in range(len(result)):
                result[i]=result[i].replace("\'","").replace("\\","")
                matchObj3=re.match(r'\"(.*)\":(.*)',result[i],re.M|re.I)
                if matchObj3:
                    dataobj[str(matchObj3.group(1))]=int(matchObj3.group(2))
                if(result[i]!=''):
                    newresult.append(result[i])

            obj["timestamp"] = newresult[0]
            obj["deviceID"] = newresult[1]
            obj["sensordata"] = dataobj
            DetectedSignalList.append(obj)
        if matchObj4:
            #print(matchObj4.group(1))
            #print(matchObj4.group(2))
            # print(matchObj4.group(3))

            sensors=matchObj4.group(1)
            sensors=sensors.replace("\\","")
            sensors=sensors.replace("\"","")
            sensorsL=sensors.split(",")
            if (len(sensorsL)!=0):
                for i in range(len(sensorsL)):
                    li=sensorsL[i]
                    li=li.split(":")
                    SensorList[li[1]]=li[0]
    return TrackedDeviceList,DetectedSignalList,SensorList