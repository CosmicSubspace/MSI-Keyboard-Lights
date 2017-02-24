## MSI-Keyboard-Lights v1.0 by CosmicSubspace
## https://github.com/CosmicSubspace/MSI-Keyboard-Lights
## Licensed under the MIT License.

import time
import PIL.ImageGrab
import PIL.Image
import PIL.ImageStat
import MsiKeyboardLib as msi

## Take a screenshot, and return the median of the three zones in the screen
## Instead of a median, we could use the mean value
## But median looks a bit better imo
def screenshot():
    res=msi.Keyboard()

    img=PIL.ImageGrab.grab()


    w=img.size[0]//3
    h=img.size[1]


    img_r=img.crop(box=(w*0,0,w*1,h))
    img_r_avg=PIL.ImageStat.Stat(img_r).median
    res.L=msi.Color(img_r_avg[0]/255,img_r_avg[1]/255,img_r_avg[2]/255)


    img_c=img.crop(box=(w*1,0,w*2,h))
    img_c_avg=PIL.ImageStat.Stat(img_c).median
    res.C=msi.Color(img_c_avg[0]/255,img_c_avg[1]/255,img_c_avg[2]/255)


    img_l=img.crop(box=(w*2,0,w*3,h))
    img_l_avg=PIL.ImageStat.Stat(img_l).median
    res.R=msi.Color(img_l_avg[0]/255,img_l_avg[1]/255,img_l_avg[2]/255)


    return res


## A "Lowpass" to make the color transition smoother.
def lowpass(current_data,newest_data,ratio):
    for i in current_data:
        current_data[i]=current_data[i]*ratio+newest_data[i]*(1-ratio)



## Initial variables.
last_time=time.time()
newest_data=msi.prepare_post_data(msi.Keyboard())
current_data=msi.prepare_post_data(msi.Keyboard())
updates=0


## This is our main loop.
## Since image processing takes a lot of CPU time, we only take a screenshot every ~0.2 seconds.
## But, to get a smooth transition, we must push the RGB values to the SteelSeries engine much faster than that.
## So, we loop every ~0.02 seconds, and unless ~0.2 seconds has passed, we only smooth the value and send the value
## to the SteelSeries Engine.
while True:

    ##This value can be reduced to increase smoothness.
    ##However, going lower than 0.02 doesn't really make a difference.
    time.sleep(0.02) ###Magic number: loop frequency.

    current_time=time.time()
    time_delta=current_time-last_time

    ##Only if 0.2 seconds have passed do we take another screenshot.
    if time_delta>0.2:  ##Magic number: screenshot frequency.

        last_time=current_time

        #Take a screenshot!
        kb=screenshot()

        ## We can push the median values of each zones as is,
        ## But the colors look rather dull that way.
        ## So, we multiply the saturation of the colors by 3.
        ## This gives a much more colorful look.
        kb.L.hsv_mult(s=3) ##Magic number: Saturation boost.
        kb.C.hsv_mult(s=3)
        kb.R.hsv_mult(s=3)

        ## Print the time elapsed since the last screenshot,
        ## And how many intermediate updates (updates without taking a screenshot) has happened.
        print("Time delta: {:.03f}\tUpdates:{}".format(time_delta,updates),end="\t")
        updates=0

        ## RGB values of each zones.
        print(str(kb.L),end="\t")
        print(str(kb.C),end="\t")
        print(str(kb.R))

        ## Put the new data into a variable.
        newest_data=msi.prepare_post_data(kb)

    ## This part performs a simple "Lowpass" to smooth the color transition.
    ## The current RGB values slowly approach the newest RGB value.
    ## The higher the lowpass ratio (0.85 in this case), the smoother(and slower) the transition.
    lowpass(current_data,newest_data,0.85) ##Magic number: Lowpass strength


    updates+=1

    ## We now send the data to the Steelseries engine.
    msi.send_dict(current_data)
