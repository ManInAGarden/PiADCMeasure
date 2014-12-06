This ist PiADCMeasure, a program based on AB electronics' PI-ADC hardware extension board for
the raspberry PI computer. I also used sample python code owned and released by ABElectronics. See below for more details
on that.

PiADCMeasure is written in python (3.3) and uses tkinter for a graphical user interface. Make sure your kernel has i2c and smbase enabled. See ABelectronic's web page for 
more info on that.

Unfortunately the python module smbus is not supplied as an installation package (the apt-get way) 
for python3. So I did the following to get this working with python3.

Install some system prerequistes with:

sudo apt-get install build-essential libi2c-dev i2c-tools python-dev

And also do:

sudo apt-get install libffi-dev

Then I used virtualenv to get a virtual environment for the rest to not spoil my raspian (which relys on python) too much.
On a location (directory) where you want your virtual env to reside type:

virtualenv -p python3 <name>

(As <name> I used PiACDMeasure_env. Do that to your liking.)

Then cd into the new directory and type

source bin/activate

to activate the new environment. Then use pip to install the rest.

pip install cffi<br/>
pip install smbus-cffi

em>NOTE: This git repository contains example code made and owned by ABelectronics. Namely
these are the files:

ABE_ADCPi.py<br/>
ABE_helpers.py

which are used to access the ADC extension board init it's paramaters and read
the sampled voltages for all 8 channels.</em>
