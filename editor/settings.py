import tkinter
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox
import json
import os, sys
from editor.config import default_settings


class SettingsMenu():
    def __init__(self, jide):
        self.saved = False
        self.text_gui = []
        self.visuals_gui = []
        self.jide = jide
        self.config = self.jide.c

        self.menu = "Text Editor"

        self.win = Toplevel(bg="#1B1C21")
        self.win.title("Settings")
        self.win.geometry("800x600")
        self.win.protocol("WM_DELETE_WINDOW", self.OnClose)
        self.win.focus_set()

        self.visualsbtn = Button(self.win, bg='black', fg='white', text="Visuals", width=20, height=2, command=self.VisualsMenu)
        self.visualsbtn.place(x=30, y=300)
        self.textbtn = Button(self.win, bg='black', fg='white', text="Text Editor", width=20, height=2, command=self.TextMenu)
        self.textbtn.place(x=30, y=100)

        self.SetVariables()
        self.SetGUI()
        self.UpdateButtons()
        self.TextMenu()

        self.savebtn = Button(self.win, bg='black', fg='white', text="Save Settings", width=20, height=2, command=self.Save)
        self.savebtn.place(x=200, y=530)
        self.resetbtn = Button(self.win, bg='black', fg='white', text="Reset Default Settings", width=20, height=2, command=self.Reset)
        self.resetbtn.place(x=400, y=530)

    def SetVariables(self):
        self.autosave = StringVar()
        self.autocomplete = StringVar()
        if self.config.auto_save == True:
            self.autosave.set("enabled")
        else:
            self.autosave.set("disabled")
        if self.config.new_lines == True:
            self.autocomplete.set("enabled")
        else:
            self.autocomplete.set("disabled")
        self.color = self.config.font_color
        self.bg_color = self.config.bg_color
        self.highlight = StringVar()
        if self.config.highlight == True:
            self.highlight.set("enabled")
        else:
            self.highlight.set("disabled")
        self.alpha = self.config.alpha
        self.string_color = self.config.string_color

    def Save(self):
        with open("editor/data/config.json") as f: data=json.load(f); f.close()
        data["highlight"]["enabled"] = self.IsTrue(self.highlight)
        data["highlight"]["string"] = self.string_color
        data["visuals"]["editor-bg"] = self.bg_color
        data["visuals"]["transparency"] = self.ToAlpha()
        data["text editor"]["auto-save"] = self.IsTrue(self.autosave)
        data["text editor"]["font-size"] = self.fontentry.get()
        data["text editor"]["font-color"] = self.color
        data["text editor"]["indentation"] = self.tabentry.get()
        data["text editor"]["indent-new-lines"] = self.IsTrue(self.autocomplete)
        data["text editor"]["auto-bracket"] = self.IsTrue(self.autocomplete)
        data["text editor"]["auto-quote"] = self.IsTrue(self.autocomplete)

        with open(self.jide.path + "config.json", "w") as f:
            json.dump(data, f, indent=4)
            f.close()
        
        self.saved = True

    def Reset(self):
        MsgBox = messagebox.askquestion('Exit',f'Are you sure you want to reset your settings to default?', icon='warning')
        if MsgBox == 'yes':
            with open(self.jide.path + "config.json", "w") as f:
                json.dump(default_settings, f, indent=4)
                f.close()
        
            self.saved = True       
        self.win.focus_set()


    def VisualsMenu(self):
        for x in self.text_gui:
            x.place_forget()
        i = 0
        for x in self.visuals_gui:
            x.place(x=self.visuals_coords_x[i], y=self.visuals_coords_y[i])
            i += 1
        self.menu = "Visuals"
        self.UpdateButtons()

    def TextMenu(self):
        for x in self.visuals_gui:
            x.place_forget()
        i = 0
        for x in self.text_gui:
            x.place(x=self.text_coords_x[i], y=self.text_coords_y[i])
            i += 1
        self.menu = "Text Editor"
        self.UpdateButtons()

    def SetGUI(self):
        if True:
            self.text_coords_x = [350, 385, 330, 490, 330, 490, 380, 560, 490, 360, 390]
            self.text_coords_y = [30, 80, 150, 150, 220, 222, 290, 292, 290, 360, 410]
            self.autosavelabel = Label(self.win, text="Auto Save:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            #self.autosavelabel.place(x=350, y=30)
            self.autosavemenu = OptionMenu(self.win, self.autosave, "enabled", "disabled")
            self.autosavemenu.config(borderwidth=0, width=15, height=1, highlightthickness=0)
            #self.autosavemenu.place(x=385, y=80)

            self.fontlabel = Label(self.win, text="Font Size:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            #self.fontlabel.place(x=330, y=150)
            self.fontentry = Entry(self.win, width=5, font=('Arial', 12))
            self.fontentry.insert(0, self.config.fontsize)
            #self.fontentry.place(x=490, y=150)

            self.fontclabel = Label(self.win, text="Font Color:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            #self.fontclabel.place(x=330, y=220)
            self.fontcolorbtn = Button(self.win, text="Change Color",  width=10, height=1, bg='white', font=('Arial', 10), command=self.ChangeColor)
            #self.fontcolorbtn.place(x=490, y=222)

            self.tablabel = Label(self.win, text="Tab size", height=1, bg='#1B1C21', fg='white', font=('Arial', 12))
            #self.tablabel.place(x=380, y=290)
            self.tablabel2 = Label(self.win, text="(how many spaces are in a tab)", height=1, bg='#1B1C21', fg='white', font=('Arial', 9))
            #self.tablabel2.place(x=560, y=292)
            self.tabentry = Entry(self.win, width=5, font=('Arial', 12))
            self.tabentry.insert(0, self.config.indentation)
            #self.tabentry.place(x=490, y=290)

            self.autocompletelabel = Label(self.win, text="Auto Complete:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            #self.autocompletelabel.place(x=360, y=360)
            self.autocompletemenu = OptionMenu(self.win, self.autocomplete, "enabled", "disabled")
            self.autocompletemenu.config(borderwidth=0, width=15, height=1, highlightthickness=0)
            #self.autocompletemenu.place(x=390, y=410)

            self.text_gui = [self.autosavelabel, self.autosavemenu, self.fontlabel, self.fontentry, self.fontclabel, self.fontcolorbtn,
            self.tablabel, self.tablabel2, self.tabentry, self.autocompletelabel, self.autocompletemenu]
        if True:
            self.visuals_coords_x = [350, 385, 380, 380, 330, 510, 330, 510]
            self.visuals_coords_y = [30, 80, 150, 220, 315, 315, 390, 390]

            self.highlightlabel = Label(self.win, text="Highlighting:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            #self.highlightlabel.place(x=350, y=30)
            self.highlightmenu = OptionMenu(self.win, self.highlight, "enabled", "disabled")
            self.highlightmenu.config(borderwidth=0, width=15, height=1, highlightthickness=0)
            #self.highlightmenu.place(x=385, y=80)

            self.alphalabel = Label(self.win, text="Screen Transparency:", height=1, bg='#1B1C21', fg='white', font=('Arial', 10))
            #self.alphalabel.place(x=380, y=150)
            self.alphaslider = Scale(self.win, from_=0, to=100, orient=HORIZONTAL, command=self.AlphaSlider)
            #self.alphaslider.place(x=380, y=220)
            self.alphaslider.set(self.GetAlpha())

            self.bglabel = Label(self.win, text="Background Color:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
           # self.bglabel.place(x=330, y=315)
            self.bgbtn = Button(self.win, text="Change Color",  width=10, height=1, bg='white', font=('Arial', 10), command=self.ChangeBGColor)
            #self.bgbtn.place(x=510, y=315)

            self.stringlabel = Label(self.win, text="Highlight Color:", width=20, height=1, bg='#1B1C21', fg='white', font=('Arial', 13))
            #self.stringlabel.place(x=330, y=390)
            self.stringbtn = Button(self.win, text="Change Color",  width=10, height=1, bg='white', font=('Arial', 10), command=self.ChangeHighlightColor)
            #self.stringbtn.place(x=510, y=390)
            
            self.visuals_gui = [self.highlightlabel, self.highlightmenu, self.alphalabel, self.alphaslider, 
            self.bglabel, self.bgbtn, self.stringlabel, self.stringbtn]


    def AlphaSlider(self, event=None):
        self.jide.win.wm_attributes('-alpha', self.ToAlpha())

    def UpdateButtons(self):
        if self.menu == "Visuals":
            self.visualsbtn.config(highlightthickness=1, borderwidth=3, text="> Visuals")
            self.textbtn.config(highlightthickness=0, borderwidth=0, text="Text")
        else:
            self.visualsbtn.config(highlightthickness=0, borderwidth=0, text="Visuals")
            self.textbtn.config(highlightthickness=1, borderwidth=3, text="> Text")

    def ChangeColor(self):
        (triple, hexstr) = askcolor(title="Change Font Color")
        if hexstr is not None:
            self.color = hexstr
        self.win.focus_set()

    def ChangeBGColor(self):
        (triple, hexstr) = askcolor(title="Change Background Color")
        if hexstr is not None:
            self.bg_color = hexstr
        self.win.focus_set()

    def ChangeHighlightColor(self):
        (triple, hexstr) = askcolor(title="Change Highlight Color")
        if hexstr is not None:
            self.string_color = hexstr        
        self.win.focus_set()

    def OnClose(self):
        if self.saved == False:
            MsgBox = messagebox.askquestion('Exit',f'Do you want to save your settings before quiting?', icon='question')
            if MsgBox == 'yes':
                self.Save()
        self.jide.reload()
        self.jide.win.focus_set()
        del self.jide.settings
        self.win.destroy()

    def IsOpen(self):
        return True

    def GetAlpha(self):
        a = self.config.alpha
        if int(float(a)) == 0:
            r = str(a)[2:]
            return int(r) * 10
        else:
            return 100

    def ToAlpha(self):
        a = str(self.alphaslider.get())
        if len(a) == 1:
            return 0
        elif len(a) == 2:
            a = f"0.{a[:1]}"
            return a
        elif len(a) == 3:
            return 1

    def IsTrue(self, val):
        val = val.get()
        if val == "enabled":
            return "true"
        else:
            return "false"