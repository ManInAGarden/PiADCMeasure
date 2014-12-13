# -*- coding: utf-8 *-*
from tkinter import *
from tkwindow import *
from sqlitemeasures import *

class ShowLogWindow(TkWindow):


    """create the gui elements of this window"""
    def make_gui(self, title):
        super().make_gui(title)

        self.serieslist = self.makelist(self.frame, lcol=0, lrow = 1,
                      llcol = 0, llrow = 0, width = 100,
                      caption="Log Series:")
        
        self.valueslist = self.makelist(self.frame, lcol=0, lrow = 3,
                      llcol = 0, llrow = 2, width = 100,
                      caption="Measured Values:")

        self.serieslist.bind("<Double-Button-1>", self.serdouble)
        self.valueslist.bind("<Double-Button-1>", self.valdouble)
        self.frame.pack()

    def serdouble(self, event):
        sels = event.widget.curselection()
        if len(sels) == 0:
            return

        self.setvaluesfor(self.series[int(sels[0])].Id)

    
    def valdouble(self, event):
        pass


    def setvaluesfor(self, serid):
        self.values = {}
        dbvalues = Value.select("SeriesId='" + str(serid) +"'", orderBy="t")
        for val in dbvalues:
            if val.UnitId != None:
                unitstr = self.unitdict[val.UnitId].Name
            else:
                unitstr = ""

            if val.t in self.values:
                #print("reusing existing MyValue at <" + str(val.t) + ">")
                currval = self.values[val.t]
            else:
                #print("new MyValue for time <" + str(val.t) + ">")
                currval = MyValue(val.t)
                self.values[val.t] = currval

            #print("appending <"
            #      + str(val.Name)
            #      + ">, <"
            #      + str(val.Value)
            #      + "> <"
            #     + unitstr + ">")
            
            currval.names.append(val.Name)
            currval.values[val.Name] = val.Value
            currval.unitnames[val.Name] = unitstr
            currval.ids[val.Name] = val.Id

        #set the list and have it sorted by time as stored in currval.t
        self.setlistelements(self.valueslist,
                             sorted(self.values.values(), key=lambda myv: myv.t))



    def loaded(self):
        #fill the lists now
        units = Unit().select()
        self.unitdict = {}
        for unit in units:
            self.unitdict[unit.Id] = unit
        
        series = Series().select()
        self.series = []
        for ser in series:
            self.series.append(MySeries(ser.Id, ser.Name, ser.Created))
            
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
