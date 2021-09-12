import TKlighter
from tkinter import *
import json


class HighLighter:
    def __init__(self, jide):
        self.jide = jide
        self.code = jide.code
        self.reload = False
        self.LoadConfig()
        self.SetSyntaxColors()

    def LoadConfig(self):
        with open("editor/data/config.json", "r") as f:
            self.syntax_colors = json.load(f)["highlight"]
            f.close()

    def SetSyntaxColors(self):
        self.string = self.syntax_colors['string']

    def Highlight(self, event):
        if self.reload == True:
            self.LoadConfig()
            self.SetSyntaxColors()
        TKlighter.double_qouts_h(self.code, self.string)   
        #TKlighter.custom_regex_h(self.code, r'"\w+"', self.string)

    def AddCustomChars(self, char):
        TKlighter.custom_h(self.code, char, "red")

    def RemoveCustomChars(self, char):
        TKlighter.custom_h(self.code, char, self.jide.c.font_color)