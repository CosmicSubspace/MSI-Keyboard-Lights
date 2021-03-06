## MSI-Keyboard-Lights v1.0.1a by CosmicSubspace
## https://github.com/CosmicSubspace/MSI-Keyboard-Lights
## Licensed under the MIT License.

if __name__=="__main__":
    import sys
    import traceback
    ## This will make it so the console won't close on its own when an exception is raised.
    def show_exception_and_exit(exc_type, exc_value, tb):
        if not str(exc_value)=='name \'exit\' is not defined':
            print("\n\n---ERROR---\n")
            traceback.print_exception(exc_type, exc_value, tb)
            input("\nPress any key to exit.")
        sys.exit(-1)
    sys.excepthook = show_exception_and_exit

import requests
import json
import os
import os.path
import time
import colorsys
import urllib.parse



## https://github.com/SteelSeries/gamesense-sdk




## We need to get the address of the steelseries engine.
port_info=os.path.join(os.getenv("PROGRAMDATA"),
                       r"SteelSeries\SteelSeries Engine 3\coreProps.json")

with open(port_info) as f:
    global address
    dat=json.load(f)
    address="http://"+dat["address"]


## Post using Requests, and print the errors.
def post(addr_append,dat):
    final_addr=urllib.parse.urljoin(address,addr_append)
    #print("\n\nPOST to",final_addr, "\nContents:"+str(dat))
    #r=grequests.post(final_addr, json=dat)

    r=requests.post(final_addr, json=dat)
    #print(r.elapsed)
    if r.status_code != 200:
        print("POST unsuccessful. Status code",r.status_code)
        print("POST address:",final_addr)
        print("POST data:",dat)
        print("-----Response from server-----")
        print(r.text)
        print("------------------------------")
        raise
    else:
        #print("POST success.")
        pass

## Register our "Game"
def game_register():
    post("/load_golisp_handlers",
         {"game":"FREEDRAW","golisp":"freedraw.lsp"})


## Send a event, with a data.
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
def wrapf(val):
    while val>1:
        val-=1
    while val<0:
        val+=1
    return val
## A simple class for managing color.
class Color():
    def __add__(self,other):
        res=Color()
        res.r=self.r+other.r
        res.g=self.g+other.g
        res.b=self.b+other.b
        return res
    def __sub__(self,other):
        res=Color()
        res.r=self.r-other.r
        res.g=self.g-other.g
        res.b=self.b-other.b
        return res
    def __truediv__(self,num):
        res=Color()
        res.r=self.r/num
        res.g=self.g/num
        res.b=self.b/num
        return res

    def __init__(self,r=0,g=0,b=0,h=0,s=0,v=0):
        self.r=r
        self.g=g
        self.b=b
        if h!=0 or s!=0 or v!=0:
            rgb=colorsys.hsv_to_rgb(h,s,v)
            self.r=rgb[0]
            self.g=rgb[1]
            self.b=rgb[2]
    def duplicate(self):
        return Color(self.r,self.g,self.b)

    def hsv_offset(self,h=0,s=0,v=0, wrap=False):
        hsv_current=colorsys.rgb_to_hsv(self.r,self.g,self.b)
        if wrap:
            h_new=wrapf(hsv_current[0]+h)
            s_new=wrapf(hsv_current[1]+s)
            v_new=wrapf(hsv_current[2]+v)
        else:
            h_new=clamp(hsv_current[0]+h)
            s_new=clamp(hsv_current[1]+s)
            v_new=clamp(hsv_current[2]+v)

        self.hsv_set(h_new,s_new,v_new)

    def hsv_mult(self,h=1,s=1,v=1):
        hsv_current=colorsys.rgb_to_hsv(self.r,self.g,self.b)
        h_new=clamp(hsv_current[0]*h)
        s_new=clamp(hsv_current[1]*s)
        v_new=clamp(hsv_current[2]*v)

        self.hsv_set(h_new,s_new,v_new)

    def hsv_set(self,h,s,v):
        rgb_new=colorsys.hsv_to_rgb(h,s,v)
        self.r=rgb_new[0]
        self.g=rgb_new[1]
        self.b=rgb_new[2]

    def rgb_set(self,r=None,g=None,b=None):
        if r!=None:
            self.r=r
        if g!=None:
            self.g=g
        if b!=None:
            self.b=b

    def rgb_offset(self,r=0,g=0,b=0, wrap=False):
        if wrap:
            self.r=wrapf(self.r+r)
            self.g=wrapf(self.g+g)
            self.b=wrapf(self.b+b)
        else:
            self.r=clamp(self.r+r)
            self.g=clamp(self.g+g)
            self.b=clamp(self.b+b)



    def __str__(self):
        return "[{:.02f},{:.02f},{:.02f}]".format(self.r,self.g,self.b)

## Class containing all the colors for the keyboard
class Keyboard():
    def __init__(self,L=Color(),C=Color(),R=Color()):
        self.L=L
        self.C=C
        self.R=R
    def __str__(self):
        return str(self.L)+" "+str(self.C)+" "+str(self.R)

## Prepare the JSON dict that will actually be sent to the SteelSeries Engine.
def prepare_post_data(kb):
    res=dict()
    res["r1"]=kb.L.r*255
    res["g1"]=kb.L.g*255
    res["b1"]=kb.L.b*255
    res["r2"]=kb.C.r*255
    res["g2"]=kb.C.g*255
    res["b2"]=kb.C.b*255
    res["r3"]=kb.R.r*255
    res["g3"]=kb.R.g*255
    res["b3"]=kb.R.b*255
    return res

## Round/clamp all the values in the JSON dict generated by prepare_post_data()
## You don't actually have to do this, but whatever
def round_data(d):
    res=dict()
    for i in d:
        res[i]=round(d[i])
        if res[i]<0:
            res[i]=0
        if res[i]>255:
            res[i]=255
    return res

## Takes in an Keyboard object, sending it to SSE.
def send_keyboard(kb):
    event_send("LIGHTS",round_data(prepare_post_data(kb)))

## Takes in an already-prepared dict, sending it to SSE.
def send_dict(d):
    event_send("LIGHTS",round_data(d))

## Simpler function with no classes
def send_simple(r1,g1,b1,r2,g2,b2,r3,g3,b3):
    res=dict()
    res["r1"]=r1*255
    res["g1"]=g1*255
    res["b1"]=b1*255
    res["r2"]=r2*255
    res["g2"]=g2*255
    res["b2"]=b2*255
    res["r3"]=r3*255
    res["g3"]=g3*255
    res["b3"]=b3*255
    event_send("LIGHTS",round_data(res))

## Register the game before doing anything.
game_register()

## Test
if __name__=="__main__":
    while True:
        input()
        send_keyboard(Keyboard(L=Color(1,1,1),C=Color(1,1,1),R=Color(1,1,1)))
        input()
        send_keyboard(Keyboard(L=Color(1,0.5,0),C=Color(0,1,0.5),R=Color(0.5,0,1)))
        input()
        send_keyboard(Keyboard())
