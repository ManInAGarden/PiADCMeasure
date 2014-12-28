# -*- coding: utf-8 *-*
from tkinter import *
from tkwindow import *
from sqlitemeasures import *
from editserieswindow import *


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
        
        #self.dupserbu = Button(self.serbuframe, text="Duplicate")
        #self.dupserbu.pack(side=LEFT)
        
        self.diaserbu = Button(self.serbuframe, text="#",
                               width=1)
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

    """receive all my signals signame"""
    def receive(self, sender, signame, data):
        if signame=="SIGOK":
            series = Series().select()
            self.series = []
            for ser in series:
                self.series.append(MySeries(ser.Id, ser.Name, ser.Created))

            self.show_lists()

    def ser_edit_cb(self):
        selidx = self.serieslist.curselection()
        #print("Delete series at {0}".format(selidx))
        if len(selidx) == 0:
            return
        
        toedit= self.series[int(selidx[0])]
        editwin = EditSeriesWindow(Toplevel(), seriesId=toedit.Id)
        editwin.register(self, "SIGOK")
        
    def ser_del_cb(self):
        selidx = self.serieslist.curselection()
        #print("Delete series at {0}".format(selidx))
        if len(selidx) == 0:
            return
        
        todel= self.series[int(selidx[0])]
        sertodel = Series.select(whereClause="Id='" + str(todel.Id) + "'")
        if len(sertodel)==1:
            sertodel[0].delete()
        else:
            raise "Häh!"

        #reload the series and values
        del self.series[int(selidx[0])]
        self.show_lists()


    def serselect(self, event):
        sels = event.widget.curselection()
        if len(sels) == 0:
            return

        self.setvaluesfor(self.series[int(sels[0])].Id)

    
    def valselect(self, event):
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
        return str(self.created) + " | " + self.name + " | " + self.description


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
