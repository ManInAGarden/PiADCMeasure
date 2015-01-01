# -*- coding: utf-8 *-*
from tkinter import *
from tkwindow import *
from sqlitemeasures import *

class EditSeriesWindow(TkWindow):

    def __init__(self, parent, title="Messserie",
                 width=400, height=300, seriesId=None):

        self.my_series = None
        self.seriesId = seriesId
        super().__init__(parent, title, width, height)
    
    
    """create the gui elements of this window"""
    def make_gui(self, title):
        super().make_gui(title)

        c = r = 0

        self.makelabel(self.frame, lcol=c, lrow=r, caption="Id")
        c += 1
        self.id_label = self.makelabel(self.frame, lcol=c, lrow=r,
                                      caption=self.seriesId)

        c=0
        r += 1
        self.name_entry = self.makeentry(self.frame, width=30,
                                        lcol=c, lrow=r,
                                        ecol=c+1, erow=r,
                                        caption="Name")

        c=0
        r += 1
        self.desc_entry = self.maketext(self.frame,
                                        width=50, height = 5,
                                        lcol=c, lrow=r,
                                        ecol=c+1, erow=r,
                                        caption="Beschreibung")

        c = 0
        r += 1
        self.ok_button = self.makebutton(self.frame,
                                         bcol=c, brow=r,
                                         caption="OK",
                                         command=self.ok_press_cb)
        c += 1
        self.cancel_button = self.makebutton(self.frame,
                                             bcol=c, brow=r,
                                             sticky=E,
                                             caption="Cancel",
                                             command=self.canc_press_cb)
        self.frame.pack()

    def ok_press_cb(self):
        
        if self.my_series != None:
            self.my_series.Name = self.name_entry.get()
            self.my_series.Description = self.desc_entry.get(0.0, END)
            self.my_series.flush()

        self.send("SIG_EDIT_SER_OK", self.my_series)    
        self.parent.destroy() #close this win
        

    def canc_press_cb(self):
        self.send("SIGCANCEL")
        self.parent.destroy() #close this win
        

    def loaded(self):
        
        seriess = Series.select("Id='" + str(self.seriesId) + "'")
        if len(seriess)==1:
            self.my_series = seriess[0]
            self.setentryvalue(self.name_entry, self.my_series.Name)
            self.settextvalue(self.desc_entry, self.my_series.Description)
            
