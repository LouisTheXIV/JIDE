from tkinter import *
import sys
import webbrowser


class MenuBar():
    def __init__(self, jide, config):
        self.jide = jide
        self.screen = jide.win
        self.config = config
        self.autosavetxt = "Auto Save ✘"

        self.menu_bar = Menu(self.screen)
        self.screen.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label='New File', command=self.jide.NewFile, accelerator="Ctrl+N")
        self.file_menu.add_command(label='Open File', command=self.jide.OpenFile, accelerator="Ctrl+O")
        #self.file_menu.add_command(label="Recent Files", command=None, accelerator=">")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.jide.Save, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.jide.SaveAs, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.OnQuit, accelerator="Ctrl+Q")

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.jide.Undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.jide.Redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.jide.Cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.jide.Copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.jide.Paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.jide.Find, accelerator="Ctrl+F")

        self.info_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Information", menu=self.info_menu)
        self.info_menu.add_command(label="Source Code", command=self.Src)
        self.info_menu.add_command(label="Report Bug", command=self.ReportBug)
        self.info_menu.add_command(label="Settings", command=self.jide.OpenSettingsMenu)

        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Open Settings Menu", command=self.jide.OpenSettingsMenu)
        #self.autosave = self.file_menu.add_command(label=self.autosavetxt, command=self.AutoSaveCheckMark)

        self.SetKeyboardShortcuts()

    def SetKeyboardShortcuts(self):
        self.screen.bind('<Control-n>', self.jide.NewFile)
        self.screen.bind('<Control-o>', self.jide.OpenFile)
        self.screen.bind('<Control-s>', self.jide.Save)
        self.screen.bind('<Control-Shift-s>', self.jide.SaveAs)
        self.screen.bind('<Control-z>', self.jide.Undo)
        self.screen.bind('<Control-y>', self.jide.Redo)
        self.screen.bind('<Control-x>', self.jide.Cut)
        self.screen.bind('<Control-c>', self.jide.Copy)
        self.screen.bind('<Control-f>', self.jide.Find)
        self.screen.bind('<Control-q>', self.OnQuit)
        #self.screen.bind('<Control-v>', self.jide.Paste)

    def AutoSaveCheckMark(self):
        if self.autosavetxt == "Auto Save ✘":
            self.autosavetxt = "Auto Save ✓"
        else:
            self.autosavetxt = "Auto Save ✘"
        self.file_menu.entryconfigure(5, label=self.autosavetxt)
        #self.jide.AutoSave(True)

    def OnQuit(self, event=None):
        self.jide.OnClose()

    def Src(self):
        webbrowser.open("https://github.com/LouisTheXIV/JIDE")
    
    def ReportBug(self):
        webbrowser.open("https://github.com/LouisTheXIV/JIDE/issues/new")