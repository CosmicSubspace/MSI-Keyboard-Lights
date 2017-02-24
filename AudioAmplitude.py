## MSI-Keyboard-Lights v1.0 by CosmicSubspace
## https://github.com/CosmicSubspace/MSI-Keyboard-Lights
## Licensed under the MIT License.

import pyaudio
import time
import struct
import math
import MsiKeyboardLib as msi

## Setup
audio = pyaudio.PyAudio()
deg=0
reference=0
lastTime=time.time()
nextCenter=msi.Color()
nextnext=msi.Color()

## PyAudio returns a byes object for the recording.
## We have to convert that to a float before doing stuff
## Outputs: A list of tuples, each being a tuple of R and L data. Or was it L and R....
def stereo_from_bytes(b):
    res=[]
    #print(b)
    for i in range(0,len(b),4):
        res.append((struct.unpack("=h",b[i:i+2])[0]/32768,
                    struct.unpack("=h",b[i+2:i+4])[0]/32768))
    return res

## get the RMS value of the stereo data.
## pretty straghtforward.
def rms_stereo(dat):
    r=0
    l=0
    for i in dat:
        r+=i[0]*i[0]
        l+=i[1]*i[1]
    return (math.sqrt(r/len(dat)/2),math.sqrt(l/len(dat)/2))

## Recording callback function
def cb(in_data,frame_count,time_info,status_flags):

    global current_data
    global deg
    global reference
    global lastTime


    currentTime=time.time()
    print("Time delta: {:.03f}".format(currentTime-lastTime),end="\t")
    lastTime=currentTime

    ## We convert the data received from PyAudio
    ## And we take the RMS value of that.
    ## RMS is a good representation of loudness here
    ## ...I think?
    dat=rms_stereo(stereo_from_bytes(in_data))


    ## We calculate a "Reference Value".
    ## Since we sometimes turn our volume up, listen to quiet songs, etc,
    ## Using the same range of loudness to map the brightness of the keyboard
    ## won't work well.
    ## So we make a dynamically changing reference value
    ## Used to map the loudness to RGB values.

    ## This is the average(sorta) value of the recent loudness values.
    ## It changes to about the average value of the currently playing audio,
    ## But does this in a smooth manner.
    reference=reference*0.99+((dat[0]+dat[1])/2)*0.01

    ## If we stop there, we will get strange results when nothing is playing
    ## because the reference will converge to zero.
    ## So we set a minimum value here. (0.1% of maximum amplitude)
    if reference<0.001:
        reference=0.001

    print("Reference: {:.04f}".format(reference),end="\t")

    ## We map the amplitude to the color value.
    ## If the amplitude is exactly at reference, it is mapped to 0.5

    ## The ^2 here makes things look a bit better
    ## It gives the brightness a bit more of an abrupt ramp.

    val_L=(dat[0]/reference/2)**2
    val_R=(dat[1]/reference/2)**2
    print("L: {:.04f}\tR: {:.04f}\tDeg:{:.01f}".format(val_L,val_R,deg%360))

    deg+=1



    ## Actual colors. The colors are set in the HSV color space.
    ## The colors' H value changes so it will look rainbowy.

    kb=msi.Keyboard()
    kb.L=msi.Color(v=val_L,h=((deg+180)%360)/360,s=1)
    kb.R=msi.Color(v=val_R,h=(deg%360)/360,s=1)

    ## The center color is just the average of L and R.
    kb.C=(kb.L+kb.R)/2


    ## Now we send the keyboard config!
    msi.send_keyboard(kb)

    #print(str(time.time()-st))
    return (None, pyaudio.paContinue)

print("Which audio device should be used?")
print("Some of them might not return a sound, and some may just throw an error.")
print("If you don't know, just guess until you get the one you want.\n")
for i in range(audio.get_device_count()):
    print(i+1,audio.get_device_info_by_index(i)["name"],sep="\t")
idx=int(input("\nEnter index: "))-1

## PyAudio code.
## See the PyAudio docs for an explanation.
s=audio.open(format=pyaudio.paInt16,
             channels=2,
             rate=44100,
             input=True,
             frames_per_buffer=2048,
             input_device_index=idx,
             stream_callback=cb)

## The process must not die.
while True:
    time.sleep(0.1)
