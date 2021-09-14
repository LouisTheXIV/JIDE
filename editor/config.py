import json

default_settings = {  
    "highlight": {
        "enabled": "true",
        "string": "green"
    }, 

    "visuals": {
        "width": 850,
        "height": 750,
        "editor-bg": "black",
        "transparency" : 1
    },

    "text editor": {
        "auto-save": "false",
        "font-size": 16,
        "font": "Arial",
        "font-color": "white",
        "indentation": 4,
        "indent-new-lines": "true",
        "auto-bracket": "true",
        "auto-quote": "true"
    }
}


def getData():
    with open("editor/data/config.json") as f:
        data = json.load(f)
        f.close()
    return data

class Config():
    def __init__(self):
        self.data = getData()
        self.setVariables()

    def setVariables(self):
        visuals = self.data["visuals"]
        text = self.data["text editor"]

        self.bg_color = visuals["editor-bg"]
        self.font_color = text["font-color"]
        self.width = visuals["width"]
        self.height = visuals["height"]
        self.alpha = float(visuals["transparency"])
        self.auto_save = bool(text['auto-save'] == "true")
        self.indentation = int(text["indentation"])
        self.fontsize = int(text["font-size"])
        self.font = text["font"]
        self.new_lines = bool(text["indent-new-lines"] == "true")
        self.quote = bool(text["auto-quote"] == "true")
        self.brackets = bool(text["auto-bracket"] == "true")
        self.highlight = bool(self.data["highlight"]["enabled"] == "true")
        self.string_color = self.data["highlight"]["string"]

    def reload(self):
        self.data = getData()
        self.setVariables()