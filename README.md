# MSI-Keyboard-Lights
Make your MSI G-Series laptop's RGB keyboard light up according to what's displayed on the screen.

[Video demo](https://youtu.be/LV5GNS1c5tg)

# Requirements
- MSI Laptop with 3-zone RGB lighting
- Windows
- SteelSeries Engine installed
- Python 3.x (Tested on 3.3.4)

# Installation
### Step 1: Copying the GoLisp Handler
First, you need to copy the `freedraw.lsp` file to SteelSeries Engine's folder.  
On windows, it is located at `C:\ProgramData\SteelSeries\SteelSeries Engine 3\hax0rBindings`.  
Copy the `freedraw.lsp` into that folder.

Note: The ProgramData folder is usually hidden by default. If you can't find the folder, try enabling hidden folders in the windows explorer settings.  

### Step 2: Installing Python
Now, you need to set up the python script. If you don't have Python, [install the 3.x version](https://www.python.org/downloads/). The script was only tested on Python 3.3.4, but other 3.x versions would work fine. (Probably)

### Step 3: Installing Libraries
With Python installed, you have to install some libraries. The Python script uses the following external libraries:

- Requests
- Pillow

You can easily install these libraries using pip. Open up the command prompt, navigate to the `C:\Python3x\Scripts` folder and then execute  
`pip install requests`  
and `pip install pillow`  
And then you're good to go!

### Step 4: Running the script
Finally, double-click on the `ScreenMirror.py`.  
If all goes well, the contents of the screen will now be mirrored on the keyboard.

# Problems?
- Make sure the keyboard is not in "No Illumination" mode.  
- Try restarting the SteelSeries Engine.  
- If you run into any exceptions, please post it on the issues tab.  

#Technical stuff
The [SteelSeries Gamesense API documentation](https://github.com/SteelSeries/gamesense-sdk) is worth a read, if you want to understand what's going on in this script.  
Other than that, I've left a handful of comments in the python script, so feel free to read through it.  
For the lisp script, all it's doing is taking values from the Gamesense POST data and directly pushing those values to the SteelSeries Engine.
