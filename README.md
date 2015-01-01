This ist PiADCMeasure, a program based on AB electronics' PI-ADC hardware extension board for
the raspberry PI computer. I also used sample python code owned and released by ABElectronics. See below for more details
on that.

PIADCMeasure can be used to show the voltage values on all 8 ADC-channels. You can also set the sample rate for
the ADC and also set it's accuracy in bits. For more info about the capablities of the board read ABelectronics'
web page. Also make sure you configure the PiADCMeasure for the i2C addresses you have in use for the board 
(according to the jumper settings on the board).

You can also start logging the measured values into a sqlite datbase. Set an apporpriate sample rate for that. The 
raspi is not able to store several values per second int the database. So that feature is more or less meant to be
used for long term measures with lower sample rates at a maximum of 1Hz (1 per second).

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

Now git clone this repository into the virtual environment so that you get a sub directory named PiADCMeasure under the 
path you created with virtualenv above.

Optinally you can install matplotlib for python3 if you want to use the diagram functions for logged data. I'm sure you want that. 

In your virtual environment use:

pip install numpy

to install numpy for python3 in your virtualenv.

For a pip install you'll most certainly be missing a dev-modlue named libpng-dev. Install this outside of your virtual
envirtonment with

sudo apt-get install libpng-dev

Then install matplotlib in your virtualenv with the command:

pip install matplotlib

To start PiADCMeasure cd into that dircitory with your activated virtualenv and type

python Main.py


<em>NOTE: This git repository contains example code made and owned by ABelectronics. Namely
these are the files:</em>

ABE_ADCPi.py<br/>
ABE_helpers.py

<em>
which are used to access the ADC extension board init it's paramaters and read
the sampled voltages for all 8 channels.</em>
