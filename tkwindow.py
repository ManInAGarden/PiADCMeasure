# -*- coding: utf-8 *-*
# made for python3!

from tkinter import *
from tkinter.ttk import *


class TkWindow():

    registers = {}
    
    def __init__(self, parent, title, width=400, height=300):    
        self.parent = parent #Tk or toplevel
        self.w = width
        self.h = height
        self.make_gui(title)
        self.loaded()

    def loaded(self):
        pass # overload me

    """register another window to receive a signal"""
    @classmethod
    def register(cls, target, signame):
        if not target in cls.registers:
            cls.registers[target] = []

        cls.registers[target].append(signame)

    """send a signal to all registered windows"""
    def send(self, signame, data=None):
        cls = self.__class__
        for targ, sigs in cls.registers.items():
            if sigs != None:
                if signame in sigs:
                    targ.receive(self, signame, data)
                
    """receive a signame"""
    def receive(self, sender, signame, data):
        print("receive not overloaded but signal registered for <"
              + signame + "> from <"
              + str(sender) + "> with <" + str(data) +">")
        # overload me in your receiving window for your application

    
    def make_gui(self, title):
        self.parent.title(title)
        Style().configure("TFrame", padding=5)
        self.frame = Frame(self.parent,
            width=self.w,
            height=self.h)



    def makelabel(self, parent, lcol=0, lrow=0, caption='', **options):
        entry = Label(parent, text=caption, **options).grid(row=lrow, column=lcol, sticky=NE)
        return entry
        
    """create a multiline text entry field with a label"""
    def maketext(self, parent, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, **options):
        print(lrow, lcol)
        if caption != '':
            Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=NE)
            
        entry = Text(parent, **options)
        if width:
            entry.config(width=width)

        entry.grid(row=erow, column=ecol, sticky=W)
        return entry

    def makeentry(self, parent, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, **options):
        if caption!='':
            Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=E)
            
        entry = Entry(parent, **options)
        if width:
            entry.config(width=width)

        entry.grid(row=erow, column=ecol, sticky=W)
        return entry

    def setentryvalue(self, entry, value):
        entry.delete(0,END)
        entry.insert(0, value)

    def settextvalue(self, entry, value):
        entry.delete(0.0,END);
        entry.insert(0.0, value);

    def setbuttontext(self, button, txt):
        button['text'] = txt
        
    def makecombo(self, parent, ccol=1, crow=0, lcol=0, lrow=0, caption='',
                  width=None, **options):
        if caption!='':
            Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=E)
            
        cbox = Combobox(parent, **options)

        if width:
            cbox.config(width=width) 
            
        cbox.grid(row=crow, column=ccol)

        return cbox
    

    def makecheck(self, parent, ecol=0, erow=0, caption='', **options):
        cb = Checkbutton(parent, text=caption, **options)
        cb.grid(row=erow, column=ecol, sticky=W)
        return cb

    def makebutton(self, parent, bcol=0, brow=0, caption='Press me', sticky=W, **options):
        bu = Button(parent, text=caption, **options)
        bu.grid(row=brow, column=bcol, sticky=sticky)
        return bu

    """create a list at the givne position"""
    def makelist(self, parent, llcol=0, llrow=1, lcol=0, lrow=0,
                 caption='List', elements=[], mode='v',
                 lrowspan=1, lcolspan=1,
                 **options):

        frame = Frame(parent)
        frame.grid(row=lrow, column=lcol, rowspan=lrowspan, columnspan=lcolspan)
        
        hscroll = vscroll = None
        
        if caption!='':
            Label(parent, text=caption).grid(row=llrow, column=llcol, sticky=W)

        lb = Listbox(frame, **options)
        

        if 'v' in mode:
            vscroll = Scrollbar(frame, orient=VERTICAL)
            lb.config(yscrollcommand = vscroll.set)
            vscroll.config(command=lb.yview)
            vscroll.pack(side=RIGHT, fill=Y)

        if 'h' in mode:
            hscroll = Scrollbar(frame, orient=HROZONTAL)
            lb.configure(xscrollcommand = hscroll.set)
            hscroll.config(command = lb.xview)
            hscroll.pack(side=BOTTOM, fill=X)
            
        lb.pack(side=LEFT, fill=BOTH, expand=1)
        
        if len(elements)>0:
            self.setlistelements(elements)
        
        return lb


    def setlistelements(self, lb, elements):
        lb.delete(0, END)
        for element in elements:
            lb.insert(END, element)



    
