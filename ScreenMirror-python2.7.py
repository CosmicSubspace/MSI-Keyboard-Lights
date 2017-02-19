from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
# by CosmicSubspace
# https://github.com/CosmicSubspace/MSI-Keyboard-Lights
import requests
import json
import os
import os.path
import time
import PIL.ImageGrab
import PIL.Image
import PIL.ImageStat
import colorsys
import sys

from builtins import open
from builtins import dict
from builtins import input
from builtins import round
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object


# https://github.com/SteelSeries/gamesense-sdk

#This will make it so the console won't close on its own when an exception is raised.
def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback

    if not str(exc_value)=='name \'exit\' is not defined':
        print("\n\n---ERROR---\n")
        traceback.print_exception(exc_type, exc_value, tb)
        input("\nPress any key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit


#We need to get the address of the steelseries engine.
port_info=os.path.join(os.getenv("PROGRAMDATA"),
                       r"SteelSeries\SteelSeries Engine 3\coreProps.json")

with open(port_info) as f:
    global address
    dat=json.load(f)
    address="http://"+dat["address"]


#Post using Requests, and print the errors.
def post(addr_append,dat):
    final_addr=address+addr_append
    #print("\n\nPOST to",final_addr, "\nContents:"+str(dat))
    r=requests.post(final_addr, json=dat)
    if r.status_code != 200:
        print("POST unsuccessful. contents:")
        print(r.text)
        raise
    else:
        #print("POST success.")
        pass


#Register our "Game"
def game_register():
    post("/load_golisp_handlers",
         {"game":"FREEDRAW","golisp":"freedraw.lsp"})


#Send a event, with a data.
def event_send(evt,dat):
    post("/game_event",{
        "game":"FREEDRAW",
        "event":evt,
        "data":dat
        })

def clamp(val):
    if val>1:
        return 1
    if val<0:
        return 0
    return val

#A simple class for managing color.
class Color(object):
    def __init__(self,r=0,g=0,b=0):
        self.r=r
        self.g=g
        self.b=b
    def duplicate(self):
        return Color(self.r,self.g,self.b)
    def hsv_offset(self,h=0,s=0,v=0):
        hsv_current=colorsys.rgb_to_hsv(self.r,self.g,self.b)
        h_new=clamp(hsv_current[0]+h)
        s_new=clamp(hsv_current[1]+s)
        v_new=clamp(hsv_current[2]+v)
        rgb_new=colorsys.hsv_to_rgb(h_new,s_new,v_new)
        self.r=rgb_new[0]
        self.g=rgb_new[1]
        self.b=rgb_new[2]

    def hsv_mult(self,h=1,s=1,v=1):
        hsv_current=colorsys.rgb_to_hsv(self.r,self.g,self.b)
        h_new=clamp(hsv_current[0]*h)
        s_new=clamp(hsv_current[1]*s)
        v_new=clamp(hsv_current[2]*v)
        rgb_new=colorsys.hsv_to_rgb(h_new,s_new,v_new)
        self.r=rgb_new[0]
        self.g=rgb_new[1]
        self.b=rgb_new[2]


    def __str__(self):
        return "[{:.02f},{:.02f},{:.02f}]".format(self.r,self.g,self.b)


#Take a screenshot, and return the median of the three zones in the screen
#Instead of a median, we could use the mean value
#But median looks a bit better imo
def screenshot():
    res=[]

    img=PIL.ImageGrab.grab()

    w=img.size[0]//3
    h=img.size[1]


    img_r=img.crop(box=(w*0,0,w*1,h))
    img_r_avg=PIL.ImageStat.Stat(img_r).median
    res.append(
        Color(img_r_avg[0]/255,img_r_avg[1]/255,img_r_avg[2]/255)
        )

    img_c=img.crop(box=(w*1,0,w*2,h))
    img_c_avg=PIL.ImageStat.Stat(img_c).median
    res.append(
        Color(img_c_avg[0]/255,img_c_avg[1]/255,img_c_avg[2]/255)
        )

    img_l=img.crop(box=(w*2,0,w*3,h))
    img_l_avg=PIL.ImageStat.Stat(img_l).median
    res.append(
        Color(img_l_avg[0]/255,img_l_avg[1]/255,img_l_avg[2]/255)
        )

    return res

#Prepare the dict that will actually be sent to the SteelSeries Engine.
def prepare_post_data(colors):
    res=dict()
    res["r1"]=colors[0].r*255
    res["g1"]=colors[0].g*255
    res["b1"]=colors[0].b*255
    res["r2"]=colors[1].r*255
    res["g2"]=colors[1].g*255
    res["b2"]=colors[1].b*255
    res["r3"]=colors[2].r*255
    res["g3"]=colors[2].g*255
    res["b3"]=colors[2].b*255
    return res

def round_data(d):
    res=dict()
    for i in d:
        res[i]=round(d[i])
    return res

#A "Lowpass" to make the color transition smoother.
def lowpass(current_data,newest_data,ratio):
    for i in current_data:
        current_data[i]=current_data[i]*ratio+newest_data[i]*(1-ratio)


#Register the game before doing anything.
game_register()


#Initial variables.
last_time=time.time()
newest_data=prepare_post_data([Color(),Color(),Color()])
current_data=prepare_post_data([Color(),Color(),Color()])
updates=0


#This is our main loop.
#Since image processing takes a lot of CPU time, we only take a screenshot every ~0.2 seconds.
#But, to get a smooth transition, we must push the RGB values to the SteelSeries engine much faster than that.
#So, we loop every ~0.02 seconds, and unless ~0.2 seconds has passed, we only smooth the value and send the value
#to the SteelSeries Engine.
while True:

    #This value can be reduced to increase smoothness.
    #However, going lower than 0.02 doesn't really make a difference.
    time.sleep(0.02) ###Magic number: loop frequency.

    current_time=time.time()
    time_delta=current_time-last_time

    #Only if 0.2 seconds have passed do we take another screenshot.
    if time_delta>0.2:  ##Magic number: screenshot frequency.

        last_time=current_time

        #Take a screenshot!
        colordata=screenshot()

        print()

        #We can push the median values of each zones as is,
        #But the colors look rather dull that way.
        #So, we multiply the saturation of the colors by 3.
        #This gives a much more colorful look.
        colordata[0].hsv_mult(s=3) ##Magic number: Saturation boost.
        colordata[1].hsv_mult(s=3)
        colordata[2].hsv_mult(s=3)

        #Print the time elapsed since the last screenshot,
        #And how many intermediate updates (updates without taking a screenshot) has happened.
        print("Time delta: {:.03f}\tUpdates:{}".format(time_delta,updates))
        updates=0

        #RGB values of each zones.
        print(str(colordata[0]),end="\t")
        print(str(colordata[1]),end="\t")
        print(str(colordata[2]))

        #Put the new data into a variable.
        newest_data=prepare_post_data(colordata)

    #This part performs a simple "Lowpass" to smooth the color transition.
    #The current RGB values slowly approach the newest RGB value.
    #The higher the lowpass ratio (0.85 in this case), the smoother(and slower) the transition.
    lowpass(current_data,newest_data,0.85) ##Magic number: Lowpass strength


    updates+=1

    #We now send the data to the Steelseries engine.
    event_send("LIGHTS",round_data(current_data))
