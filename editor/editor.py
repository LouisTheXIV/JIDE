import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showerror
import re
from editor.highlighting import HighLighter
from editor.config import Config
from editor.menubar import MenuBar


class JIDE:
    def __init__(self):
        self.c = Config()
        self.file = None
        self.issaved = False

        self.win = Tk()
        self.win.geometry(f"{self.c.width}x{self.c.height}")
        self.win.title("JIDE")
        self.win.config(bg=self.c.bg_color)
        self.win.wait_visibility(self.win)
        self.win.wm_attributes('-alpha', self.c.alpha)
        
        self.indentation = self.c.indentation

        self.code = Text(self.win, bg=self.c.bg_color, insertbackground="white", fg=self.c.font_color, padx=10, pady=10, font=(self.c.font, self.c.fontsize), undo=True)
        self.code.pack(fill=BOTH, expand=YES)

        self.MenuBar = MenuBar(self, self.c)

        self.code.bind("<Tab>", self.Indentation)
        if self.c.brackets:
            self.bracket1bind = self.code.bind("{", self.AutoIndentation)
            self.bracket2bind = self.code.bind("[", self.AutoSquareBracket)
        if self.c.quote:
            self.quotebind = self.code.bind('"', self.AutoQuote)
            self.backspacebind = self.code.bind("<BackSpace>", self.Backspace)
        if self.c.new_lines:
            self.returnbind = self.code.bind("<Return>", self.AutoIndentNewLines)
        if self.c.highlight:
            self.Lighter = HighLighter(self)
        self.onkeydownbind = self.code.bind("<Key>", self.OnKeyDown)
        #self.code.bind("f", self.reload)


    def reload(self, event):
        self.c.reload()
        self.Lighter.reload = True
        self.MenuBar.config = self.c
        self.MenuBar.reload()

        self.code.config(bg=self.c.bg_color, fg=self.c.font_color, font=(self.c.font, self.c.fontsize))
        self.indentation = self.c.indentation
        self.win.config(bg=self.c.bg_color)
        self.win.wm_attributes('-alpha', self.c.alpha)
        self.win.geometry(f"{self.c.width}x{self.c.height}")
        if self.c.highlight:
            self.highlightbind = self.code.bind("<Key>", self.SyntaxHighlight)
        else:
            self.code.unbind("<Key>", self.highlightbind)
        if self.c.brackets:
            self.bracket1bind = self.code.bind("{", self.AutoIndentation)
            self.bracket2bind = self.code.bind("[", self.AutoSquareBracket)
        else:
            self.code.unbind("{", self.bracket1bind)
            self.code.unbind("[", self.bracket2bind)
        if self.c.quote:
            self.quotebind = self.code.bind('"', self.AutoQuote)
            self.backspacebind = self.code.bind("<BackSpace>", self.Backspace)
        else:
            self.code.unbind('"', self.quotebind)
            self.code.unbind("<BackSpace>", self.backspacebind)
        if self.c.new_lines:
            self.returnbind = self.code.bind("<Return>", self.AutoIndentNewLines)
        else:
            self.code.unbind("<Return>", self.returnbind)

    def OnKeyDown(self, event):
        if self.c.highlight:
            self.Lighter.Highlight(event)
        #print(self.code.xview())
        #print(self.code.yview())
        if self.file is not None:
            self.win.title(f"*JIDE ~ {self.file}")
        else:
            self.win.title(f"*JIDE")

    def Indentation(self, event):
        self.code.insert(INSERT, " " * self.indentation)
        return 'break'

    def AutoIndentation(self, event):
        widget = event.widget
        line = widget.get("insert linestart", "insert lineend")

        match = re.match(r'^(\s+)', line)
        current_indent = len(match.group(0)) if match else 0

        new_indent = current_indent + self.indentation

        widget.insert(INSERT, event.char + " " * new_indent + "\n")
        index = self.code.index(INSERT)
        widget.insert(INSERT, "\n")
        widget.insert(INSERT, " " * current_indent + "}")
        widget.mark_set(INSERT, index)
        widget.insert(INSERT, " " * new_indent)

        return "break"

    def AutoIndentNewLines(self, event):
        widget = event.widget
        index = self.code.index(INSERT)
        char = self.code.get(round(float(index)-float(0.1), 1), float(index))
        
        if char == "," or char.endswith(","):
            line = widget.get("insert linestart", "insert lineend")

            match = re.match(r'^(\s+)', line)
            current_indent = len(match.group(0)) if match else 0

            widget.insert(INSERT, "\n")
            widget.insert(INSERT, " " * current_indent)

            return "break"

        else:
            pass

    def AutoSquareBracket(self, event):
        widget = event.widget
        index = self.code.index(INSERT)
        widget.insert(INSERT, ']')
        widget.mark_set(INSERT, index)

    def AutoQuote(self, event):
        widget = event.widget
        index = self.code.index(INSERT)
        widget.insert(INSERT, '"')
        widget.mark_set(INSERT, index)

    def Backspace(self, event):
        widget = event.widget
        index = self.code.index(INSERT)
        char = self.code.get(self.ModifyColumn(index, False, 1), index)
        second_char = self.code.get(index, self.ModifyColumn(index, True, 1))
        if char == '"' and second_char == '"' or char == "[" and second_char == "]":
            widget.mark_set(INSERT, self.ModifyColumn(index, True, 1))
            self.code.delete("insert -1 chars", "insert")
            widget.mark_set(INSERT, index)

    def OpenSettingsMenu(self):
        pass

    def ModifyColumn(self, index, add, chars):
        try:
            ls_index = list(index)
            line = ""
            column = ""
            for x in ls_index:
                if x == ".":
                    break
                else:
                    line += str(x)
            iscolumn = False
            for x in ls_index:
                if iscolumn:
                    column += str(x)
                if x == ".":
                    iscolumn = True
            line = int(line)
            column = int(column)
            if add == True:
                column += chars
            elif add == False:
                column -= chars
            
            r = f"{str(line)}.{str(column)}"
            return float(r)
        except:
            return 1.0

    def NewFile(self, event=None):
        fpath = asksaveasfile(mode='w+', defaultextension=".json", filetypes=(("Json files", "*.json"),
                                           ("All files", "*.*") ))

        if fpath is not None:
            with open(fpath.name, "w+") as f:
                f.close()
            
            self.file = fpath.name
            self.win.title(f"*JIDE ~ {fpath.name}")
            self.issaved = False

    def OpenFile(self, event=None):
        fpath = askopenfilename(filetypes=(("Json files", "*.json"),
                                           ("All files", "*.*") ))

        if fpath is not None:

            with open(fpath, "r") as f:
                contents = f.read()
                f.close()
            
            self.code.delete(1.0,"end")
            self.code.insert(1.0, contents)
            self.file = fpath
            self.win.title(f"JIDE ~ {fpath}")
            self.issaved = True

    def Save(self, event=None):
        try:
            if self.file is None:
                self.NewFile()
            else:
                with open(self.file, "w") as f:
                    f.write(self.code.get(1.0, "end"))
                    f.close()
                self.issaved = True
                self.win.title(f"JIDE ~ {self.file}")
        except:
            pass

    def SaveAs(self, event=None):
        fpath = asksaveasfile(mode='w+', defaultextension=".json", filetypes=(("Json files", "*.json"),
                                           ("All files", "*.*") ))

        if fpath is not None:
            with open(fpath.name, "w+") as f:
                f.write(self.code.get(1.0, "end"))
                f.close()
            
            self.file = fpath.name
            self.win.title(f"JIDE ~ {fpath.name}")
            self.issaved = True

    def Undo(self, event=None):
        try:
            self.code.edit_undo()
        except TclError:
            pass
    
    def Redo(self, event=None):
        try:
            self.code.edit_redo()
        except TclError:
            pass

    def Cut(self, event=None):
        try:
            widget = event.widget
            line = widget.get("insert linestart", "insert lineend")
            self.code.delete(f"insert -{len(line)} chars", "insert")
            self.win.clipboard_clear()
            self.win.clipboard_append(line)
            self.win.update()
        except:
            pass

    def Copy(self, event=None):
        try:
            widget = event.widget
            line = widget.get("insert linestart", "insert lineend")
            self.win.clipboard_clear()
            self.win.clipboard_append(line)
            self.win.update()
        except:
            pass

    def Paste(self, event=None):
        try:
            text2paste = self.code.selection_get(selection='CLIPBOARD')
            self.win.clipboard_clear()
            self.code.insert('insert', text2paste)
            self.win.update()
        except:
            pass

    def Find(self, event=None):
        self.searchbox = Toplevel()
        self.searchbox.title('Search')
        self.searchbox.geometry('300x100')

        self.search_label = Label(self.searchbox, text="Search for:", font=('Arial', 11))
        self.search_label.pack()
        self.kw = Entry(self.searchbox, width=20, font=('Arial', 14))
        self.kw.pack()
        btn = Button(self.searchbox, width=10, text="Find", command=self.SearchKeyWord)
        btn.pack()

        self.searchbox.protocol("WM_DELETE_WINDOW", self.OnCloseSearchBox)
        self.searchbox.focus_set()


    def SearchKeyWord(self):
        try:
            keyword = self.kw.get()
            start = self.code.index(INSERT)
            count = 0
            endpos = 1.0
            firstpos = self.code.search(keyword, endpos, "end")

            while True:
                startpos = self.code.search(keyword, endpos, "end")
                endpos = self.ModifyColumn(startpos, True, len(keyword))
                if startpos == firstpos and count != 0:
                    break
                count += 1

            count = count -1
            self.code.mark_set(INSERT, startpos)
            self.Lighter.AddCustomChars(keyword)
            self.search_label.config(text=f"{count} found")
        except:
            pass

    def OnCloseSearchBox(self):
        self.Lighter.RemoveCustomChars(self.kw.get())
        self.searchbox.destroy()
        
        


jide = JIDE()
