import tkinter
from tkinter import *
import os, sys


class SettingsMenu():
    def __init__(self, jide):
        self.jide = jide
        self.config = self.jide.c

        self.menu = "Text Editor"

        self.win = Toplevel(bg="#1B1C21")
        self.win.title("Settings")
        self.win.geometry("800x600")
        self.win.protocol("WM_DELETE_WINDOW", self.OnClose)

        self.visualsbtn = Button(self.win, bg='black', fg='white', text="Visuals", width=20, height=2, command=self.VisualsMenu)
        self.visualsbtn.place(x=30, y=300)
        self.textbtn = Button(self.win, bg='black', fg='white', text="Text Editor", width=20, height=2, command=self.TextMenu)
        self.textbtn.place(x=30, y=100)

        self.SetVariables()
        self.UpdateScreens()
        self.UpdateButtons()

    def SetVariables(self):
        self.autosave = StringVar()
        if self.config.auto_save == True:
            self.autosave.set("enabled")
        else:
            self.autosave.set("disabled")

    def VisualsMenu(self):
        self.menu = "Visuals"
        self.UpdateButtons()

    def TextMenu(self):
        print(self.autosavemenu.getvar())
        self.menu = "Text Editor"
        self.UpdateButtons()

    def UpdateScreens(self):
        if self.menu == "Text Editor":
            self.autosavelabel = Label(self.win, text="Auto Save:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            self.autosavelabel.place(x=350, y=30)
            self.autosavemenu = OptionMenu(self.win, self.autosave, "enabled", "disabled")
            self.autosavemenu.config(borderwidth=0, width=15, height=1, highlightthickness=0)
            self.autosavemenu.place(x=385, y=80)

            self.fontlabel = Label(self.win, text="Font Size:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            self.fontlabel.place(x=330, y=150)
            self.fontentry = Entry(self.win, width=5, font=('Arial', 12))
            self.fontentry.insert(0, self.config.fontsize)
            self.fontentry.place(x=490, y=150)

    def UpdateButtons(self):
        if self.menu == "Visuals":
            self.visualsbtn.config(highlightthickness=1, borderwidth=3, text="> Visuals")
            self.textbtn.config(highlightthickness=0, borderwidth=0, text="Text Editor")
        else:
            self.visualsbtn.config(highlightthickness=0, borderwidth=0, text="Visuals")
            self.textbtn.config(highlightthickness=1, borderwidth=3, text="> Text Editor")
        

    def OnClose(self):
        self.win.destroy()