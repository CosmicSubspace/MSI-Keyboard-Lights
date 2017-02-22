# MSI-Keyboard-Lights
Make your MSI G-Series laptop's RGB keyboard light up according to what's displayed on the screen.

[Video demo](https://youtu.be/LV5GNS1c5tg)

## Requirements
- MSI Laptop with 3-zone RGB lighting
- Windows
- SteelSeries Engine installed

## Installation
First of all, download the repository using the download button on the top right side of this page.

#### Step 1: Copying the GoLisp Handler
To begin, you need to copy the `freedraw.lsp` file to SteelSeries Engine's folder.  
On windows, it is located at `C:\ProgramData\SteelSeries\SteelSeries Engine 3\hax0rBindings`.  
Copy the `freedraw.lsp` into that folder.

Note: The ProgramData folder is usually hidden by default. If you can't find the folder, try enabling hidden folders in the windows explorer settings.  

#### Step 2: Installing Python
Now, you need to set up the python script. If you don't have Python, [install the 3.x version](https://www.python.org/downloads/). The script was only tested on Python 3.3.4, but other 3.x versions would work fine. (Probably)

#### Step 3: Installing Libraries
With Python installed, you have to install some libraries. The Python script uses the following external libraries:

- Requests
- Pillow

For those who are not familiar with Python, here's how to install them:  
Go to start, and search for: `cmd`. A program named `Command Prompt` will be the first result. Open it up.  
Now, in the black window that appeared, type in `py -m pip install requests` and press Enter. If it works, a bunch of things will appear on the command prompt, ending with `Successfully installed...`  
If it worked, now type `py -m pip install pillow` and press Enter. If this command also succeeds, you're good to go!

#### Step 4: Running the script
Finally, double-click on the `ScreenMirror.py`.  
If all goes well, the contents of the screen will now be mirrored on the keyboard.

## Problems?
- Make sure the keyboard is not in "Disable Illumination" mode. All zones must NOT be in "Disable Illumination" mode!  
- Try restarting the SteelSeries Engine.  
- If the keyboard goes black while playing a game, try playing in windowed mode. The script cannot take a screenshot of a game in fullscreen mode, since the game writes directly to the screen. For games that do support it, using a borderless-windowed mode is optimal, since it will look just like fullscreen mode while allowing this script to take screenshots.  
- If you run into any exceptions, please post it on the issues tab.  

## Make that console window go away!
You can make the console window not appear, by renaming the `.py` file to `.pyw` file.  
Please note that if you do this, you won't be able to see error messages, and you will have to go to the task manager to close the script.

## I want to use Python 2.7!
Well, okay! Just run `ScreenMirror-python2.7.py` instead of `ScreenMirror.py`.  
The Python2.7 version also requires the `Future` library: `py -m pip install future`

## Technical stuff
The [SteelSeries Gamesense API documentation](https://github.com/SteelSeries/gamesense-sdk) is worth a read, if you want to understand what's going on in this script.  
Other than that, I've left a handful of comments in the python script, so feel free to read through it.  
For the lisp script, all it's doing is taking values from the Gamesense POST data and directly pushing those values to the SteelSeries Engine.
