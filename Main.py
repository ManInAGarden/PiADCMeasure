# -*- coding: utf-8 *-*
from tkinter import *
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import sqlitemeasures as sqm
import TkWindow as tkw


class MainWindow(tkw.TkWindow):

    def __init__(self, title):
        super().initialize(title)

    """gui elements have been loaded"""
    def loaded(self):
        i2c_helper = ABEHelpers()
        bus = i2c_helper.get_smbus()
        self.adc = ADCPi(bus, 0x6A, 0x6B, 12)
        self.show_values()
        self.init_db()

    def connect(self):
        pass

    def start_stop(self):
        pass
    
    def exit_app(self):
        self.root.quit()
    
    """Initialise database entities"""
    def init_db(self):
        sqm.Series.FileName="~/pimeasurebase"
        sqm.Series.LogFile = "~/pimeasure.log"

    def show_values(self):
        self.d1entry.insert(END, self.adc.read_voltage(1))
        self.d2entry.insert(END, self.adc.read_voltage(2))
        self.d3entry.insert(END, self.adc.read_voltage(3))
        self.d4entry.insert(END, self.adc.read_voltage(4))
        self.d5entry.insert(END, self.adc.read_voltage(5))
        self.d6entry.insert(END, self.adc.read_voltage(6))
        self.d7entry.insert(END, self.adc.read_voltage(7))
        self.d8entry.insert(END, self.adc.read_voltage(8))

    def create_menu(self):
        men = Menu(self.root)
        self.root.config(menu=men)
        filemen = Menu(men)
        men.add_cascade(label="File", menu=filemen)
        filemen.add_command(label="Connect", command=self.connect)
        filemen.add_separator()
        filemen.add_command(label="Exit", command=self.exit_app)

        return men


        
    def make_gui(self, title):
        super().make_gui(title)

        self.menu = self.create_menu()
        r = 1
        c = 0
        self.makelabel(self.frame,
                       lcol = c, lrow=1, caption="ADC voltage [V]");
        c+= 1
        self.d1entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d1")
        c += 1
        self.d2entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d2")
        c += 1
        self.d3entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d3")
        c += 1
        self.d4entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d4")
        c += 1
        self.d5entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d5")
        c += 1
        self.d6entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d6")
        c += 1
        self.d7entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d7")
        c += 1
        self.d8entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d8")
        c = 0
        r+=1

        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="unit");

        c += 1
        
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="conversion factor");

        c += 1

        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="converted value");

        c += 1
        self.conv1entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conv2entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conv3entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conv4entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conv5entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conv6entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conv7entry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)
        c += 1
        self.conventry = self.makeentry(self.frame,
                       width=10, ecol=c, erow=r)

        c = 0
        r += 1
        self.startbu = self.makebutton(self.frame,
                                       bcol = c, brow = r, caption="Start log",
                                       command=self.start_stop)
        self.frame.pack()


if __name__ == "__main__":
    mainw = MainWindow("Pi-Measures")
    mainw.mainloop()
