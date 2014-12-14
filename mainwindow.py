# -*- coding: utf-8 *-*
from tkinter import *
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import datetime
import configparser
import sqlitemeasures as sqm
from Fifo import *
from tkwindow import *
from showlogwindow import *

CFGFILENAME = "PIADCMeasure.cfg"
ADCADR1 = 0x6A
ADCADR2 = 0x6B
#Sample rate can be 12,14, 16 or 18
# 12 = 12 bit - 240 sps/s (samples per second max.)
# 14 = 14 bit - 60 sps/s
# 16 = 16 bit - 15 sps/s
# 18 = 18 bit - 3.75 sps/s
ADCACCURACY = 18
ADCRATES = [
    '12 bit - 240 sps/s',
    '14 bit - 60 sps/s',
    '16 bit - 15 sps/s',
    '18 bit - 3.75 sps/s'
    ]

class MainWindow(TkWindow):


    def __init__(self, parent, title):
        self.init_values()
        self.init_db()
        super().__init__(parent, title)
        #print("initialising main window")
        

    """initialize class members that have to be present"""
    def init_values(self):
        self.logstarted = False
        self.currlograte = 1.0 #Hz
        self.quadfactors  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.factors      = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.bases        = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.convvalues   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.convfifos    = []
        self.usedunitidxs = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.convsums     = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.convmeans    = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.convsigma    = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.calcs = 0
        self.calcmax = 10

        for i in range(0,8):
            self.convfifos.append(Fifo())
            
        self.meansvalid = False


    """gui elements have been loaded"""
    def loaded(self):
        self.adc = self.setup_adc(ADCADR1, ADCADR2, ADCACCURACY)
        self.load("defaultparams")
        self.show_values()

    
    def setup_adc(self, adr1, adr2, accu):
        print("setting up adc with accuracy <"
              + str(accu) + "> on addresses <"
              + str(adr1) + "> and <"
              + str(adr2) + ">")
        i2c_helper = ABEHelpers()
        bus = i2c_helper.get_smbus()
        adc = ADCPi(bus, adr1, adr2, accu)
        
        return adc

    """get the unitsettings from the combos"""
    def get_unit_settings(self):
        answ = []
        for i in range(0,8):
            val = self.unitcombos[i].get()
            answ.append(val)
            
        return answ

    def save_cb(self):
        self.save('defaultparams')
        
    """Save the current settings to a config-file"""
    def save(self, cfgname):
        unitss = self.get_unit_settings()
        cp = configparser.ConfigParser()
        cp[cfgname] = {
            'adc_adr1' : ADCADR1,
            'adc_adr2' : ADCADR2,
            'slidingmeanscount' : self.calcmax,
            'adc_accuracy' : ADCACCURACY,
            'lograte' : self.currlograte,
            'units' : unitss,
            'quadcoeffs' : self.quadfactors,
            'lincoeffs' : self.factors,
            'constants' : self.bases
            }

        with open(CFGFILENAME, 'w') as cfgfile:
            cp.write(cfgfile)

    """read a list from the configuration file"""
    def read_list(self, s):
        elems = []
        for elem in s.split(','):
            elem = elem.strip(" []''`")
            elems.append(elem)
            
        return elems
    
    """load another configuration from the conf file"""
    def load_cb(self):
        #let user pick a configuration here and then load
        #that config from the configfile with the following command
        #self.load('defaultparams')
        pass


    def findunit(self, us):
        #print("searching for <" + us + ">")
        for u in self.allunits:
            if u.Name == us:
                return self.allunits.index(u) + 1

        return 0

        
    """load settingsS from a file"""
    def load(self, cfgname):
        cp = configparser.ConfigParser()
        cp.read(CFGFILENAME)
        cfg = cp[cfgname]
        self.currlograte = float(cfg['lograte'])
        self.calcmax = float(cfg['slidingmeanscount'])
        self.setentryvalue(self.lograteentry, self.currlograte)
        quadfactors = self.read_list(cfg['quadcoeffs'])
        factors = self.read_list(cfg['lincoeffs'])
        bases = self.read_list(cfg['constants'])
        units = self.read_list(cfg['units'])
        
        for i in range(0,8):
            if len(factors[i]) > 0:
                self.factors[i] = float(factors[i])
                self.setentryvalue(self.factentries[i], self.factors[i])
            if len(bases[i]) > 0:
                self.bases[i] = float(bases[i])
                self.setentryvalue(self.baseentries[i], self.bases[i])
            if len(units[i]) > 0:
                uidx = self.findunit(units[i])
                self.unitcombos[i].current(uidx)
                self.usedunitidxs[i] = uidx - 1

                
    """toggle logging to the database"""
    def start_stop(self):
        
        self.logstarted = not self.logstarted
        if self.logstarted:
            self.currseries = sqm.Series()
            self.currseries.Name = "PiADCMeasure series"
            self.currseries.flush()
            self.setbuttontext(self.startbu, 'Log stop')
        else:
            self.setbuttontext(self.startbu, 'Log start')
        self.do_log()

            
    """exit from PiADCMeasure"""
    def exit_app(self):
        self.parent.quit()
        self.parent.destroy()

    
    """Initialise database entities"""
    def init_db(self):
        self.db_file_name="/home/pi/piadcmeasure.db"
        self.db_log_file_name = "/home/pi/piadcmeasure.log"
        
        print("Initilising database in " + self.db_file_name);
        sqm.Series.initialize(self.db_file_name);
        sqm.Value.initialize(self.db_file_name);
        sqm.Unit.initialize(self.db_file_name);
        self.allunits = sqm.Unit.select()


    
    """one of the factor has changed - callback""" 
    def base_changed_cb(self, event):
        idx = self.baseentries.index(event.widget)
        vals = event.widget.get()
        if len(vals) > 0:
            base = float(vals)
            self.bases[idx] = base


    """one of the factor has changed - callback""" 
    def factor_changed_cb(self, event):
        idx = self.factentries.index(event.widget)
        vals = event.widget.get()
        if len(vals) > 0:
            fact = float(vals)
            self.factors[idx] = fact

    def quad_factor_changed_cb(self, event):
        idx = self.quadfactentries.index(event.widget)
        vals = event.widget.get()
        if len(vals) > 0:
            qfact = float(vals)
            self.quadfactors[idx] = qfact
            

    def show_values(self):
        self.T = datetime.datetime.now() #remember time of this measures
        for i in range(0, 8):
            val = self.adc.read_voltage(i+1)
            self.setentryvalue(self.dentries[i], val)
            cval = self.quadfactors[i] * val**2 + self.factors[i] * val + self.bases[i]
            self.convvalues[i] = cval
            self.convfifos[i].push(cval)
            self.setentryvalue(self.conventries[i],
                               self.convvalues[i])

            self.convmeans[i] += cval/self.calcmax
            
            if self.calcs == self.calcmax:
                self.convmeans[i] -= self.convfifos[i].pop()/self.calcmax
                self.setentryvalue(self.convmeansentries[i], self.convmeans[i])

        self.calcs += 1
        if self.calcs > self.calcmax:
            self.startbu.config(state='normal')
            self.calcs = self.calcmax #stop this from going to infinty but keep > self,calcmax in next round
            
        self.startbu.after(1000, self.show_values)

    """do a log to the database"""
    def do_log(self):
        if self.logstarted:
            self.setentryvalue(self.logtimeentry, time.strftime('%H:%M:%S'))
            wait = int(1/self.currlograte * 1000)
            self.logtimeentry.after(wait, self.do_log)
            for i in range(0, 8):
                if self.usedunitidxs[i]>=0:
                    sqval = sqm.Value()
                    sqval.SeriesId = self.currseries.Id
                    sqval.Name = "d" + str(i)
                    sqval.UnitId = self.allunits[self.usedunitidxs[i]].Id
                    sqval.Value = self.convmeans[i]
                    sqval.t = self.T
                    sqval.flush()

    """display the log window"""
    def show_log(self):
        logw = ShowLogWindow(Toplevel(), "Log DB")


    def create_menu(self):
        men = Menu(self.parent)
        self.parent.config(menu=men)
        filemen = Menu(men)
        men.add_cascade(label="File", menu=filemen)
        filemen.add_command(label="Save", command=self.save_cb)
        filemen.add_command(label="Load", command=self.load_cb)
        filemen.add_command(label="Show Log", command=self.show_log)
        filemen.add_separator()
        filemen.add_command(label="Exit", command=self.exit_app)

        return men

    """the user my have changed the log rate"""
    def lograte_changed_cb(self, event):
        vals = event.widget.get()
        if len(vals) > 0:
            lr = float(vals)
            self.currlograte = lr

    """create the gui elements of this window"""
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

        allunitnames = [""]
        for unit in self.allunits:
            allunitnames.append(unit.Name)
            
        self.unitcombos = []
        for i in range(0, 8):
            c += 1
            self.unitcombos.append(self.makecombo(self.frame, width = 9,
                       ccol=c, crow=r,
                       state='readonly',
                       values = allunitnames))

        # line of elements - quadratic coefficients
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="quadratic coefficient");

        self.quadfactentries = []
        for i in range(0,8): 
            c += 1
            self.quadfactentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))
            self.setentryvalue(self.quadfactentries[i], self.quadfactors[i]);
            self.quadfactentries[i].bind("<FocusOut>", self.quad_factor_changed_cb)

        
        # line of elements - linear coefficients
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="linear coefficient");

        self.factentries = []
        for i in range(0,8): 
            c += 1
            self.factentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))
            self.setentryvalue(self.factentries[i], self.factors[i]);
            self.factentries[i].bind("<FocusOut>", self.factor_changed_cb)
        
        

        # line of elements - conversion bases
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="constant");

        self.baseentries = []
        for i in range(0,8):
            c += 1
            self.baseentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))
            self.setentryvalue(self.baseentries[i], self.bases[i])
            self.baseentries[i].bind("<FocusOut>", self.base_changed_cb)
        
        
        # line of elements - the converted values
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="converted value");

        self.conventries = []
        for i in range(0, 8):
            c += 1
            self.conventries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))

        # line of elements - the converted values
        c = 0
        r += 1
        self.makelabel(self.frame,
                       lcol = c, lrow=r, caption="converted means");

        self.convmeansentries = []
        for i in range(0, 8):
            c += 1
            self.convmeansentries.append(self.makeentry(self.frame,
                       width=10, ecol=c, erow=r))

        #last row
        r += 1
        c = 5
        self.logtimeentry = self.makeentry(self.frame,
            width=10, ecol=c, erow=r, lcol=c-1, lrow=r,
            caption='log time')
          
        c += 2

        self.lograteentry = self.makeentry(self.frame,
            width=10, ecol=c, erow=r, lcol=c-1, lrow=r,
            caption='log rate [Hz]')
        self.lograteentry.bind("<FocusOut>", self.lograte_changed_cb)
        self.setentryvalue(self.lograteentry, self.currlograte)
        
        c += 1
        self.startbu = self.makebutton(self.frame,
                                       bcol = c, brow = r, caption="Start log",
                                       command=self.start_stop,
                                       state='disabled')
        
        self.frame.pack()


if __name__ == "__main__":
    print("Starting PiADCMeasure")
    root = Tk()
    mainw = MainWindow(root, "PiADCMeasure")
    #print("entering main loop")
    root.mainloop()
    print("thank you for using PiADCMeasure")
    
