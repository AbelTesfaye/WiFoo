# WiFoo
![WiFoo](https://raw.githubusercontent.com/AbelTesfaye/WiFoo/master/screenshots/wifoo.png)
![Choose Interface](https://raw.githubusercontent.com/AbelTesfaye/WiFoo/master/screenshots/1.png)
![Routers and Devices](https://raw.githubusercontent.com/AbelTesfaye/WiFoo/master/screenshots/2.png)

A tool to disconnect any device from any wifi hotspots, even if you are not connected to it. 

## Features ##
- Disconnect any device from any wifi hotspot
- Auto channel-lock your wifi interface
- Disable monitor mode on script exit

This is a lightweight GUI front-end for [aireplay-ng](https://www.aircrack-ng.org/doku.php?id=aireplay-ng). 


All modules used in this script are from the python standard library. No need to download additional libraries :)

Tested with [aircrack-ng-1.2](http://download.aircrack-ng.org/aircrack-ng-1.2.tar.gz). You should use this version for the script to work as expected.


Anyone is welcome to contribute.





## Installation instructions ##


### Step 1: Aircrack-ng installation ###

WiFoo has been tested on [aircrack-ng-1.2](http://download.aircrack-ng.org/aircrack-ng-1.2.tar.gz). This is the recommended version you should use. 

The above link includes complete aircrack-ng-1.2 installation instructions


### Step 2: Tkinter installation ###

The following command works on Ubuntu 16.04 LTS

      $ sudo apt-get install python3-tk


### Step 3: Testing WiFoo ###

Open a terminal in the same directory as WiFoo and run the following:

      $ sudo python3 main.py
   
   You should see the WiFoo splash-screen followed by a little window asking you to choose an interface.
   
