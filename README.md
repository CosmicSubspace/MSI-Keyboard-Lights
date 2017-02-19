# MSI-Keyboard-Lights
Make your MSI G-Series laptop's RGB keyboard light up according to what's displayed on the screen.

[Video demo](https://youtu.be/7z4rpFJoWxk)

# Requirements
- MSI Laptop with 3-zone RGB lighting
- Windows
- SteelSeries Engine installed
- Python 3.x (Tested on 3.3.4)

# Installation
First, you need to copy the freedraw.lsp file to SteelSeries Engine's folder.

On windows, it is located at:  
`C:\ProgramData\SteelSeries\SteelSeries Engine 3\hax0rBindings`  
copy the freedraw.lsp in the folder so that the filepath looks like:  
`C:\ProgramData\SteelSeries\SteelSeries Engine 3\hax0rBindings\freedraw.lsp`  

The ProgramData folder is usually hidden by default. If you can't find the folder, try enabling hidden folders in the windows explorer settings.  

Now, you need to set up the python script. If you don't have Python, install the 3.x version. The script was only tested on Python 3.3.4, but other versions would work fine. (Probably)

The Python script uses the following external libraries.

- Requests
- Pillow

You can easily install these libraries using pip. Open up the command prompt, navigate to the `C:\Python3x\Scripts` folder and then execute  
`pip install requests`  
and `pip install pillow`  
And then you're good to go!

Finally, double-click on the ScreenMirror.py.  
Now the contents of the screen will be mirrored on the keyboard.

# Problems?
If you run into any exceptions, first try restarting the SteelSeries Engine, and if the problem persists, please post it on the issues tab.
