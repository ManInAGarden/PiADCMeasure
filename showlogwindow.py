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
        self.values = []
        values = Value.select("SeriesId='" + str(serid) +"'")
        for val in values:
            if val.UnitId != None:
                unitstr = self.unitdict[val.UnitId].Name
            else:
                unitstr = ""
                
            self.values.append(MyValue(val.Id, val.t,
                                       val.Name, val.Value,
                                       unitstr))
                               
        self.setlistelements(self.valueslist, self.values)



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
        return self.name + ", " + str(self.created)


class MyValue():
    
    def __init__(self, uid, t, name, value, unitname):
        self.Id = uid
        self.t = t
        self.name = name
        self.value = value
        self.unitname = unitname

    def __str__(self):
        return str(self.t) + " - " + self.name + ":" + str(self.value) + self.unitname
