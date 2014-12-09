# -*- coding: utf-8 *-*
# made for python3!

from tkinter import *
from tkinter.ttk import *


class TkWindow():

    def __init__(self, parent, title, width=400, height=300):
        self.parent = parent #Tk or toplevel
        self.w = width
        self.h = height
        self.make_gui(title)
        self.loaded()

    def loaded(self):
        pass # overload me
    
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
        if caption != '':
            Label(self, parent, text=caption).grid(row=lrow, column=lcol, sticky=NE)
            
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
        entry.delete(0,END);
        entry.insert(0, value);

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

    def makebutton(self, parent, bcol=0, brow=0, caption='Press me', **options):
        bu = Button(parent, text=caption, **options)
        bu.grid(row=brow, column=bcol, sticky=W)
        return bu

    """create a list at the givne position"""
    def makelist(self, parent, llcol=0, llrow=1, lcol=0, lrow=0,
                 caption='List', elements=[], **options):
        if caption!='':
            Label(parent, text=caption).grid(row=llrow, column=llcol, sticky=W)

        lb = Listbox(parent, **options)
        lb.grid(row=lrow, column=lcol)
        if len(elements)>0:
            self.setlistelements(elements)
        
        return lb


    def setlistelements(self, lb, elements):
        lb.delete(0, END)
        for element in elements:
            lb.insert(END, element)



    
