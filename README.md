# MSI-Keyboard-Lights
A set of scripts that makes your MSI G-Series laptop's RGB keyboard light up in a colorful way.
#### ScreenMirror.py
The keyboard will mirror what's displayed on the screen.  
[Video demo](https://youtu.be/LV5GNS1c5tg)
#### AudioAmplitude.py
The keyboard lights will react to your computer's stereo speaker output. The louder the sound, the brighter the keyboard.  
[Video demo](https://youtu.be/rExPTK0rIv0)

## Requirements
- MSI Laptop with 3-zone RGB lighting
- Windows
- SteelSeries Engine installed

## Installation
The installation is not really a one-click process, but it should not take too long either.

First of all, download the repository using the download button on the top right side of this page, and extract the files to a folder.  
The .py files must be located in a same folder - they reference each other, so putting them in different folder will cause an error.

#### Step 1: Copying the GoLisp Handler
To begin, you need to copy the `freedraw.lsp` file to SteelSeries Engine's folder.  
On windows, it is located at `C:\ProgramData\SteelSeries\SteelSeries Engine 3\hax0rBindings`.  
Copy the `freedraw.lsp` into that folder.

Note: The ProgramData folder is usually hidden by default. If you can't find the folder, try enabling hidden folders in the windows explorer settings.  

#### Step 2: Installing Python
Now, you need to set up the python script. If you don't have Python, [install the 3.x version](https://www.python.org/downloads/). The script was tested on Python 3.6, but other 3.x versions would work fine. (Probably)

#### Step 3: Installing Libraries
With Python installed, you have to install some libraries. The Python script uses the following external libraries:

- Requests (Required for both scripts)
- Pillow (Required for `ScreenMirror.py`)
- PyAudio (Required for `AudioAmplitude.py`)

For those who are not familiar with Python, here's how to install them:  
Go to start, and search for: `cmd`. A program named `Command Prompt` will be the first result. Open it up.  
Now, in the black window that appeared, type in `py -m pip install requests` and press Enter. If it works, a bunch of things will appear on the command prompt, ending with `Successfully installed...`  
If it worked, now type `py -m pip install pillow` and press Enter.  
If that worked, now type `py -m pip install pyaudio` and press Enter. If all of them succeed, you're good to go!

#### Step 4: Enabling Stereo Mix
This step is only required if you'd like to use `AudioAmplitude.py`.  
`AudioAmplitude.py` takes a microphone input and visualizes it on the keyboard. But most of the time you'd want a visualization of your computer's speaker output, not a mic input. So, we need a way to fake that speaker output as a mic input.  
Fortunately, Realtek audio cards (which MSI laptops use) provide a way to do just that. However, this feature is disabled by default, so you'll have to enable it yourself. Follow [this guide](https://www.howtogeek.com/howto/39532/how-to-enable-stereo-mix-in-windows-7-to-record-audio/) on how to enable this feature.

#### Step 5: Running the script
Finally, double-click on the `ScreenMirror.py` or `AudioAmplitude.py`.  
Note that running multiple scripts at once will cause erratic behavior.

## Problems?
- Make sure the keyboard is not in "Disable Illumination" mode. All zones must NOT be in "Disable Illumination" mode!  
- Try restarting the SteelSeries Engine.  
- (ScreenMirror.py): If the keyboard goes black while playing a game, try playing in windowed mode. The script cannot take a screenshot of a game in fullscreen mode, since the game writes directly to the screen. For games that do support it, using a borderless-windowed mode is optimal, since it will look just like fullscreen mode while allowing this script to take screenshots.  
- If you run into any exceptions, please post it on the issues tab.  

## Make that console window go away!
You can make the console window not appear, by renaming the `.py` file to `.pyw` file.  
Please note that if you do this, you won't be able to see error messages, and you will have to go to the task manager to close the script.

## API
The `MsiKeyboardLib.py` is basically a wrapper for the SteelSeriesEngine's HTTP API.  
If you'd like to make your own python script for controlling the keyboard lights, simply import `MsiKeyboardLib.py` and then you can easily control the keyboard lights through simple python calls!  
Before doing this, you have to follow step 1 of the install instructions before you can utilize the module.  
Sample code that illustrates most of the functions of this module:  
```python
import MsiKeyboardLib as msi
import time

keyboard=msi.Keyboard() # Make a keyboard object. You can provide three Color object to the constructor to set the initial colors.
# [L]eft, [C]enter, and [R]ight keyboard zones.
keyboard.L=msi.Color(1.0,0,0) # Define a color, the three values are R, G, and B. Note that their range is 0 to 1, NOT 0 to 255.
keyboard.C=msi.Color(g=1.0) # keyword args work too. Default values for unset channels is 0.
keyboard.R=msi.Color(h=0.667,s=0,v=0) # HSV also works.

while True:
  time.sleep(0.1)

  # Some of the things you can do with the color controls:
  keyboard.L.hsv_offset(h=0.03,wrap=True) # Offset the hue so it loops rainbow colors.
  keyboard.R.rgb_offset(0.01,0.02,0.03,wrap=True) # Offsetting the RGB works too.
  keyboard.R.r=1.0 # Directly manipulating the colors work too.
  keyboard.C=(keyboard.R+keyboard.L)/2 # You can even do this!
  print(str(keyboard)) # You can print some debug data after you str() the Keyboard or Color.

  msi.send_keyboard(keyboard) # This function sends the keyboard object to SteelSeriesEngine, making these colors appear on your keyboard.

# For those who would like to use a simpler API, the below function lets you push RGB values directly without using any classes:
msi.send_simple(r_left,g_left,b_left,r_center,g_center,b_center,r_right,g_right,b_right) # Again, the arguments should be in 0~1 range.
```
## Technical stuff
The [SteelSeries Gamesense API documentation](https://github.com/SteelSeries/gamesense-sdk) is worth a read, if you want to understand what's going on in this script.  
Other than that, I've left a handful of comments in the python script, so feel free to read through it.  
For the lisp script, all it's doing is taking values from the Gamesense POST data and directly pushing those values to the SteelSeries Engine.

## Changelog
#### v0.1
 - initial release

#### v1.0
 - added AudioAmplitude.py
 - seperated modules so that it can be used as a library
