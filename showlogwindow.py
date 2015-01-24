# -*- coding: utf-8 *-*
from tkinter import *
from tkwindow import *
from sqlitemeasures import *
from editserieswindow import *
import numpy as np
import matplotlib.pyplot as plt



class ShowLogWindow(TkWindow):


    """create the gui elements of this window"""
    def make_gui(self, title):
        super().make_gui(title)

        c = r = 0
        self.serbuframe = Frame(self.frame)
        self.serbuframe.grid(column = c, row=r)
        
        self.editserbu = Button(self.serbuframe, text="E", width=1,
                                command=self.ser_edit_cb)
        self.editserbu.pack(side=LEFT)
        
        self.diaserbu = Button(self.serbuframe, text="#",
                               width=1,
                               command=self.ser_plot_cb)
        self.diaserbu.pack(side=LEFT)
        
        self.delserbu = Button(self.serbuframe, text="X", width=1, command=self.ser_del_cb)
        self.delserbu.pack(side=LEFT)
        

        c = 0
        r += 1
        self.serieslist = self.makelist(self.frame, lcol=c, lrow = r+1,
                      llcol = c, llrow = r, width = 100,
                      lcolspan=4,
                      caption="Log Series:")

        r += 2
        self.delvalbu = self.makebutton(self.frame, bcol = c, brow=r, caption="X",
                                        width=1)

        c = 0
        r += 1
        self.valueslist = self.makelist(self.frame, lcol=c, lrow = r+1,
                      llcol = c, llrow = r, width = 100,
                      lcolspan=4,
                      caption="Measured Values:")

        self.serieslist.bind("<<ListboxSelect>>", self.serselect)
        self.valueslist.bind("<<ListboxSelect>>", self.valselect)
        self.frame.pack()
        TkWindow.register(self, "SIG_EDIT_SER_OK")

    """receive all my signals given in signame"""
    def receive(self, sender, signame, data):
        if signame=="SIG_EDIT_SER_OK":
            series = Series().select()
            self.series = []
            for ser in series:
                self.series.append(MySeries(ser.Id, ser.Name, ser.Created))

            self.show_lists()

    """get the selected MySeries object"""
    def get_sel_ser(self):
        selidx = self.serieslist.curselection()
        #print("Delete series at {0}".format(selidx))
        if len(selidx) == 0:
            return None
        
        return self.series[int(selidx[0])]

    """edit selected series"""
    def ser_edit_cb(self):
        toedit= self.get_sel_ser()
        editwin = EditSeriesWindow(Toplevel(), seriesId=toedit.Id)
        

    """delete selected series"""
    def ser_del_cb(self):
        todel= self.get_sel_ser()
        sertodel = Series.select(whereClause="Id='" + str(todel.Id) + "'")
        if len(sertodel)==1:
            sertodel[0].delete()
        else:
            raise "Häh!"

        # reload the series and values
        del self.series[int(selidx[0])]
        self.show_lists()

    """return a numpy array filled with the current values"""
    def get_value_array(self, values, times, vd):
        answ = []
        for time in times:
            v = values[time]
            answ.append(v.values[vd])

        return np.array(answ)

    """plot the diagram for a selected series"""
    def ser_plot_cb(self):
        selidx = self.serieslist.curselection()
        if len(selidx) == 0:
            return
        
        toplot = self.series[int(selidx[0])]
        vals = self.current_vals
        if vals==None:
            return

        # now create the diagram
        times = []
        for d in vals:
            times.append(d)

        fig, ax = plt.subplots()
        x = np.array(sorted(times))
        # x1 = np.array(range(0,len(times)))
        for d in vals[times[0]].values:
            y = self.get_value_array(vals, x, d)
            line = ax.plot(x, y)
            
        plt.show()

    """set the values list with the measured values for the series with
       the given id"""
    def setvaluesfor(self, id):
        vals = self.getvaluesfor(id)
        self.current_vals = vals
        self.setlistelements(self.valueslist,
                             sorted(vals.values(), key=lambda myv: myv.t))
        
    def serselect(self, event):
        sels = event.widget.curselection()
        if len(sels) == 0:
            return

        self.setvaluesfor(self.series[int(sels[0])].Id)

    
    def valselect(self, event):
        pass


    def getvaluesfor(self, serid):
        values = {}
        dbvalues = Value.select("SeriesId='" + str(serid) +"'", orderBy="t")
        for val in dbvalues:
            if val.UnitId != None:
                unitstr = self.unitdict[val.UnitId].Name
            else:
                unitstr = ""

            if val.t in values:
                # print("reusing existing MyValue at <" + str(val.t) + ">")
                currval = values[val.t]
            else:
                # print("new MyValue for time <" + str(val.t) + ">")
                currval = MyValue(val.t)
                values[val.t] = currval
            
            currval.names.append(val.Name)
            currval.values[val.Name] = val.Value
            currval.unitnames[val.Name] = unitstr
            currval.ids[val.Name] = val.Id

        return values



    def loaded(self):
        self.current_vals = None
        
        # fill the lists now
        units = Unit().select()
        self.unitdict = {}
        for unit in units:
            self.unitdict[unit.Id] = unit
        
        series = Series().select()
        self.series = []
        for ser in series:
            self.series.append(MySeries(ser.Id, ser.Name, ser.Created))

        self.show_lists()


    def show_lists(self):
        self.setlistelements(self.serieslist, self.series)

        if len(self.series) > 0:
            self.setvaluesfor(self.series[0].Id)




class MySeries():

    def __init__(self, sid, name, created):
        self.Id = sid
        self.name = name
        self.created = created
        

    def __str__(self):
        return str(self.created) + " | " + self.name


class MyValue():
    
    def __init__(self, t):
        self.ids = {}
        self.t = t
        self.names = []
        self.values = {}
        self.unitnames = {}

    def getdata(self, name):
        if name in self.unitnames:
            u = self.unitnames[name]
        else:
            u = ""

        if name in self.values:
            v = self.values[name]
        else:
            v = 0.0

        return "{0:8.2f}{1}".format(v,u)
        
    def __str__(self):
        answ = str(self.t)

        for i in range(0,8):
            dx = "d" + str(i)
            answ += " | " + self.getdata(dx)
        
        return answ
