# -*- coding: utf-8 *-*
from tkinter import *
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import sqlitemeasures as sqm
import TkWindow as tkw


class MainWindow(tkw.TkWindow):

    def __init__(self, title):
        print("initialising main window")
        self.init_values()
        self.init_db()
        super().initialize(title)

    def init_values(self):
        self.factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.bases   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    """gui elements have been loaded"""
    def loaded(self):
        i2c_helper = ABEHelpers()
        bus = i2c_helper.get_smbus()
        self.adc = ADCPi(bus, 0x6A, 0x6B, 12)
        self.show_values()
        

    def connect(self):
        pass

    def start_stop(self):
        pass
    
    def exit_app(self):
        self.root.quit()
    
    """Initialise database entities"""
    def init_db(self):
        self.db_file_name="/home/pi/piadcmeasure.db"
        self.db_log_file_name = "/home/pi/piadcmeasure.log"
        
        print("Initilising database in " + self.db_file_name);
        sqm.Series.initialize(self.db_file_name);
        sqm.Value.initialize(self.db_file_name);
        sqm.Unit.initialize(self.db_file_name);
        self.units = sqm.Unit.select()

    def factor_changed_cb(self, event):
        print("it happened")

    def show_values(self):
        for i in range(0, 8):
            val = self.adc.read_voltage(i+1)
            self.setentryvalue(self.dentries[i], val)
            self.setentryvalue(self.conventries[i],
                                       val * self.factors[i] + self.bases[i])

        self.startbu.after(1000, self.show_values)

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
        #first line of elements
        
        self.makelabel(self.frame,
                       lcol = c, lrow=1, caption="ADC voltage [V]");

        self.dentries = []
        for i in range(0, 8):
            c+= 1
            self.dentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r, lcol=c, lrow=r-1,
                       caption = "d" + str(i + 1)))
        
        #second line of elements - units
        c = 0
        r+=1

        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="unit");

        self.unitcombos = []
        for i in range(0, 8):
            c += 1
            self.unitcombos.append(self.makecombo(self.frame, width = 9,
                       ccol=c, crow=r,
                       values = self.units))
            
        

        #third line of elements - conversion factors
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="conversion factor");

        self.factentries = []
        for i in range(0,8): 
            c += 1
            self.factentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))
            self.setentryvalue(self.factentries[i], self.factors[i]);
            self.factentries[i].bind("<FocusOut>", self.factor_changed_cb)
        
        

        #fourth line of elements - conversion bases
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="conversion bases");

        self.baseentries = []
        for i in range(0,8):
            c += 1
            self.baseentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))
            self.setentryvalue(self.baseentries[i], self.bases[i])
        
        
        #fifth line of elements - the converted values
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="converted value");

        self.conventries = []
        for i in range(0, 8):
            c += 1
            self.conventries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))

        
        c = 8
        r += 1
        self.startbu = self.makebutton(self.frame,
                                       bcol = c, brow = r, caption="Start log",
                                       command=self.start_stop)
        
        self.frame.pack()


if __name__ == "__main__":
    print("Starting PiADCMeasure")
    mainw = MainWindow("PiADCMeasure")
    print("entering main loop")
    mainw.mainloop()
