# -*- coding: utf-8 *-*
# made for python3!

from tkinter import *


class TkWindow:

    def initialize(self, title):
        self.w = 400
        self.h = 300
        self.make_gui(title)
        self.loaded()

    def mainloop(self):
        self.root.mainloop()

    def make_gui(self, title):
        self.root = Tk()
        self.root.title(title)
        self.frame = Frame(self.root,
            width=self.w,
            height=self.h,
            padx=5, pady=5)

    """create a standalone label"""
    def makelabel(self, parent, lcol=0, lrow=0, caption='', **options):
        entry = Label(parent, text=caption, **options).grid(row=lrow, column=lcol, sticky=NE)
        return entry
        
    """create a multiline text entry field with a label"""
    def maketext(self, parent, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, **options):
        Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=NE)
        entry = Text(parent, **options)
        if width:
            entry.config(width=width)

        entry.grid(row=erow, column=ecol, sticky=W)
        return entry

    def makeentry(self, parent, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, **options):
        Label(parent, text=caption).grid(row=lrow, column=lcol, sticky=E)
        entry = Entry(parent, **options)
        if width:
            entry.config(width=width)

        entry.grid(row=erow, column=ecol, sticky=W)
        return entry

    def makecheck(self, parent, ecol=0, erow=0, caption='', **options):
        cb = Checkbutton(parent, text=caption, **options)
        cb.grid(row=erow, column=ecol, sticky=W)
        return cb

    def makebutton(self, parent, bcol=0, brow=0, caption='Press me', **options):
        bu = Button(parent, text=caption, **options)
        bu.grid(row=brow, column=bcol, sticky=W)
        return bu
