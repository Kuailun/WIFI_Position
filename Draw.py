import cv2
import numpy as np
from Calculation import *

class Draw:
    sensorList=[]
    map_width=20    #unit: meter
    map_height=20   #unit: meter
    grid_size=1     #unit: meter
    pixel_rate=0
    img_width=1024
    img_height=1024
    def SetSensor(self,positionX,positionY):
        """Set sensor position in the map"""
        self.sensorList.append([positionX,positionY])

    def SetMap(self,width,height,gridsize):
        """Set map parameter"""
        self.map_width=width
        self.map_height=height

    def CalculateGet(self):
        """Return the adapted width and length of the map"""
        if(self.map_width>=self.map_height):
            rate=1024//self.map_width
        if (self.map_width < self.map_height):
            rate = 1024 // self.map_height
        self.pixel_rate=rate
        self.img_width=rate * self.map_width
        self.img_height=rate * self.map_height
        return self.img_width, self.img_height

    def DrawCircle(self,img,list,r,g,b,radius):
        """Draw the circles on the image"""
        for i in range(len(list)):
            x=list[i][0]*self.pixel_rate
            y=list[i][1]*self.pixel_rate
            if(x<0 or x>self.img_width or y<0 or y>self.img_height):
                continue
            cv2.circle(img,(int(x),int(y)),radius,(b,g,r),2)
        return img

    def DrawCircles(self,img,list,r,g,b):
        for i in range(len(list)):
            x=self.sensorList[i][0]*self.pixel_rate
            y = self.sensorList[i][1] * self.pixel_rate
            radius=list[i]*self.pixel_rate
            if(radius==-1):
                continue
            cv2.circle(img,(int(x),int(y)),int(radius),(b,g,r),2)
        return img

    def DrawMap(self,dataList=[],distance=[]):
        """Draw the map with sensor position"""
        w,h=self.CalculateGet()
        img = np.zeros((h,w, 3), dtype=np.uint8)
        imgSensor=self.DrawCircle(img,self.sensorList,r=255,g=0,b=0,radius=2)
        imgData=imgSensor
        if(len(dataList)!=0):
            imgData=self.DrawCircle(img,dataList,r=255,g=0,b=255,radius=self.pixel_rate//2)
        if(len(distance)!=0):
            imgData=self.DrawCircles(img,distance,r=0,g=255,b=0)
        cv2.imshow("Data", imgData)
        cv2.waitKey(0)

    def Draw(self,sensorPositions,TrackedDevices,Signals,Sensors,stamp):
        """Draw the map according to timestamp"""
        find=False
        index=-1
        for i in range(len(Signals)):
            if(stamp==Signals[i]["timestamp"]):
                find = True
                index=i
                break
        if not find:
            print("Timestamp not found, stop drawing")
            return

        print("Timestamp found, start processing data")

        sigdata=Signals[index]["sensordata"]
        deviceID=Signals[index]["deviceID"]

        print("SensorPositions:{0}".format(sensorPositions))
        print("Signal data::{0}".format(sigdata))

        drawPos=[]
        drawSig=[]
        for key1 in sensorPositions:
            for key2 in sigdata:
                if(key1==key2):
                    drawPos.append(sensorPositions[key1])
                    drawSig.append(sigdata[key2])
                    break

        if(len(drawPos)<=2):
            print("Only {0} valid data found, need more!".format(len(drawPos)))
            return

        print("Begin drawing")

        sig = [-42, -48, -14]

        wifi = WIFI()
        wifi.sensorList = drawPos
        result = wifi.CalculateCoordinate(drawSig)
        result = result.getA()
        x = result[0][0]
        y = result[1][0]
        distance = wifi.CalculateDistanceList(drawSig)
        print(x, y)

        draw = Draw()
        draw.SetMap(20, 15, 1)
        draw.sensorList = drawPos
        draw.DrawMap([[x, y]], distance)