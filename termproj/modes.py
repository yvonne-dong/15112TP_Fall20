# Code from: https://www.cs.cmu.edu/~112/notes/term-project.html#tp0
import module_manager
module_manager.review()

import math, copy, random


# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

#################################################
# Helper functions from 112 website:
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
#################################################

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

#################################################
# Term Project
#################################################
# Subclassing: https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#subclassingModalApp
class MainMenuMode(Mode):
    def appStarted(mode):
        mode.boxW, mode.boxH = 150, 25
        mode.topMargin = 350
        mode.gap = 50
        mode.textBoxText = ['NEW GAME', 'RESUME', 'HELP']
        mode.textBoxPos = [(mode.width/2, mode.topMargin + (mode.boxH + mode.gap) * row) for row in range(len(mode.textBoxText))]
        mode.selectId = 0
        mode.font = 'Arial 26 bold'

    def drawTextBox(mode, canvas, text, pos):
        canvas.create_rectangle(pos[0]-mode.boxW, pos[1]-mode.boxH, 
                                pos[0]+mode.boxW, pos[1]+mode.boxH,
                                outline='white', width = 5)
        canvas.create_text(pos[0], pos[1], text = text, font = mode.font, fill = 'white')
    
    def selectTextBox(mode, canvas):
        canvas.create_rectangle(mode.textBoxPos[mode.selectId][0]-mode.boxW, mode.textBoxPos[mode.selectId][1]-mode.boxH,
                                mode.textBoxPos[mode.selectId][0]+mode.boxW, mode.textBoxPos[mode.selectId][1]+mode.boxH,
                                outline='gold', width = 5)
    
    def keyPressed(mode, event):
        if (event.key == "Down"):
            if (mode.selectId < len(mode.textBoxText)-1):
                mode.selectId += 1
            else:
                mode.selectId = 0
        elif (event.key == "Up"):
            if (mode.selectId > 0):
                mode.selectId -= 1
            else:
                mode.selectId = len(mode.textBoxText)-1
        elif (event.key == "Enter"):
            if mode.selectId == 0:
                mode.app.setActiveMode(mode.app.roomMode)
            elif mode.selectId == 2:
                mode.app.setActiveMode(mode.app.helpMode)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'blue')
        canvas.create_text(mode.width/2, mode.topMargin * 1/3, 
                           text = "ROOM ESCAPE", font = mode.font, fill = 'white')
        canvas.create_text(mode.width/2, mode.topMargin * 2/3, 
                           text = "PRESS UP/DOWN TO SELECT", font = mode.font, fill = 'white')
        for row in range(len(mode.textBoxText)):
            mode.drawTextBox(canvas, mode.textBoxText[row], mode.textBoxPos[row])
        mode.selectTextBox(canvas)

class RoomMode(Mode):
    def appStarted(mode):
        # scene view settings
        mode.viewPortPos = [(0, 0), (mode.width, mode.height * (2/3))]
        mode.textDisplayPos = [(0, mode.height * (2/3)), (mode.width, mode.height)]
        mode.viewPortSize = [mode.width, mode.height * (2/3)]
        mode.textDisplaySize = [mode.width, mode.height * (1/3)]
        # font size
        mode.font = 'Arial 18 bold'
        # list of each side of the room
        mode.roomSides = ["front", "right", "back", "left", "top", "bottom"]
        mode.currentSide = 0
        # list of all items in the room (currently: r1)
        mode.r1=[
                    {
                        "name": "bacon",
                        "interaction": "game",
                        "status": False,
                        "require": None,
                        "timed": True
                    },
                    {
                        "name": "flour",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "eggs",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "G",
                        "interaction": "see",
                        "status": False,
                        "require": None,
                        "timed": True
                    },
                    {
                        "name": "Em",
                        "interaction": "see",
                        "status": False,
                        "require": None,
                        "timed": True
                    },
                    {
                        "name": "C",
                        "interaction": "see",
                        "status": False,
                        "require": None,
                        "timed": True
                    },
                    {
                        "name": "D7",
                        "interaction": "see",
                        "status": False,
                        "require": None,
                        "timed": True
                    },
                    {
                        "name": "pan",
                        "interaction": "combine",
                        "status": False,
                        "require": ["flour", "eggs"],
                        "timed": False
                    }
                ]
        mode.r1AllItems = {"bacon", "flour", "eggs"}
        # check collected items
        mode.items = []
        mode.collectedItems = []
        for i in range(len(mode.r1)):
            size = 80
            x1 = random.randrange(size * 2, mode.width - size * 2)
            y1 = random.randrange(size * 2, mode.height * (2/3) - size * 2)
            # set which side of the room the object is on
            sideIdx = math.floor(random.randrange(0, 6))
            itm = item(mode.r1[i], (x1, y1), size, sideIdx)
            mode.items.append(itm)
        
        # for answering password
        mode.userAnswer = ""
        mode.answer = "G,Em,C,D7"
        
        # init empty text editor
        mode.previousText = ""

    def drawTextdisplay(mode, canvas, pos, size):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = 'gold')
        textPos = (pos[0][0] + size[0]/2, pos[0][1] + size[1]/2)
        text = 'FIND THE ITEMS'
        if (mode.collectedItems == mode.r1AllItems):
            text = 'YOU HAVE COLLECTED ALL ITEMS, PRESS M FOR MAIN MENU'
        canvas.create_text(textPos[0], textPos[1], 
                          text = text, font = mode.font, fill = 'white')
        roomsideTextPos = (pos[0][0] + size[0]/20, pos[0][1] + size[0]/20)
        canvas.create_text(roomsideTextPos[0], roomsideTextPos[1], 
                          text = mode.roomSides[mode.currentSide], 
                          font = mode.font, fill = 'white', anchor='w')
    
    def drawViewport(mode, canvas, pos):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = 'blue')  

    def displayTextEditor(mode, previousText):
        # Code modified from: https://www.tutorialspoint.com/python/tk_text.htm
        textEditor = Toplevel()
        textEditor.title('Notepad')
        textEditor.geometry("300x300")
        
        def saveText():
            previousText = textInput.get("1.0", END).strip()
            print(previousText)
        
        saveButton = Button(textEditor, text = "save", command = saveText)
        saveButton.pack(side = TOP, anchor = NW)
        
        textInput = Text(textEditor)
        textInput.pack()

    def keyPressed(mode, event):
        # "front", "right", "back", "left", "top", "bottom"
        if (event.key == "1"):
            mode.currentSide = 0
        elif (event.key == "2"):
            mode.currentSide = 1
        elif (event.key == "3"):
            mode.currentSide = 2
        elif (event.key == "4"):
            mode.currentSide = 3
        elif (event.key == "5"):
            mode.currentSide = 4
        elif (event.key == "6"):
            mode.currentSide = 5
        
        # Go back to main menu
        elif (event.key == "m"):
            mode.app.setActiveMode(mode.app.mainMenuMode)
            mode.appStarted()
        
        # Call notebook
        elif (event.key == "n"):
            mode.displayTextEditor(mode.previousText)

        # elif (event.key == "l"):
        #     print(f"You've collected {mode.collectedItems}")
        # elif (event.key == "v"):
        #     verify = set(mode.collectedItems)
        #     if verify == mode.r1AllItems:
        #         print("collected all")
        #     else:
        #         print("still missing sth")

    def mousePressed(mode, event):
        for i in range(len(mode.items)):
            if (mode.currentSide == mode.items[i].sideIdx):
                if (mode.items[i].clickOnItem(event.x, event.y, mode.collectedItems) != None) and (mode.items[i].status == False):
                    if (mode.items[i].interaction == "add"):
                        mode.collectedItems.append(mode.items[i].name)
                        mode.items[i].status = True
                        print(f'collected {mode.items[i].name}')
                    elif (mode.items[i].interaction == "see"):
                        print(f'see {mode.items[i].name}')
                    elif (mode.items[i].interaction == "combine"):
                        if (mode.items[i].reachRequire):
                            print("combined!")
                        else:
                            print("collect requirements")
                    elif (mode.items[i].interaction == "game"):
                        mode.items[i].passwordEntry(mode.userAnswer, mode.answer)

    def redrawAll(mode, canvas):
        # draw viewport
        mode.drawViewport(canvas, mode.viewPortPos)
        
        # draw text display
        mode.drawTextdisplay(canvas, mode.textDisplayPos, mode.textDisplaySize)
        
        # draw items in room
        for i in range(len(mode.items)):
            # draw the item at its room side
            if (mode.currentSide == mode.items[i].sideIdx) and (mode.items[i].status == False):
                mode.items[i].displayItem(canvas)

class item(RoomMode):
    def __init__(self, properties, pos, size, sideIdx):
        self.properties = properties
        self.name = properties["name"]
        self.interaction = properties["interaction"]
        self.status = properties["status"]
        self.require = properties["require"]
        self.reachRequire = None

        self.size = size
        self.sideIdx = sideIdx
        self.centerPos = pos
    
    def displayItem(self, canvas):
        x0, y0 = self.centerPos[0]-self.size/2, self.centerPos[1]-self.size/2
        x1, y1 = self.centerPos[0]+self.size/2, self.centerPos[1]+self.size/2
        canvas.create_rectangle(x0, y0, x1, y1, outline='white', width = 1)
        canvas.create_text(self.centerPos[0], self.centerPos[1], 
                          text = self.name, font = 'Arial 16 bold', fill = 'white')        

    def clickOnItem(self, mX, mY, collected):
        x0, y0 = self.centerPos[0]-self.size/2, self.centerPos[1]-self.size/2
        x1, y1 = self.centerPos[0]+self.size/2, self.centerPos[1]+self.size/2
        if (x0 < mX < x1) and (y0 < mY < y1):
            if (self.require != None):
                if (set(self.require).issubset(collected)):
                    self.reachRequire = True
            return True
    
    def passwordEntry(self, input, answer):
        # Code modified from: https://www.geeksforgeeks.org/python-tkinter-entry-widget/
        root = Tk()
        root.title('text entry')
        Label(root, text = "Sing the bacon pancake song! (connect with ',')").grid(row = 0)
        textEntry = Entry(root)
        textEntry.grid(row = 1)

        def reply():
            input = textEntry.get()
            textEntry.delete(0, 'end')
            root.destroy()
            if (input == answer):
                print("Correct!")
            else:
                print("Wrong : (")

        button = Button(root, text = "send", command = reply)
        button.grid(row = 2)
       
class HelpMode(Mode):
    def appStarted(mode):
        mode.topMargin = 350
        mode.font = 'Arial 26 bold'
    
    def displayText(mode, canvas, text, pos):
        canvas.create_text(pos[0], pos[1], text = text, font = mode.font, fill = 'white')
    
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'blue')
        mode.displayText(canvas, 'HELP', (mode.width/2, mode.topMargin * 1/3))
        mode.displayText(canvas, '(SOME INSTRUCTIONS & BG STORY)', 
                        (mode.width/2, mode.topMargin * 2/3))
        mode.displayText(canvas, 'PRESS M FOR MENU', 
                        (mode.width/2, mode.topMargin))
    
    def keyPressed(mode, event):
        if (event.key == "m"):
            mode.app.setActiveMode(mode.app.mainMenuMode)

class TermProject(ModalApp):
    def appStarted(app):
        app.mainMenuMode = MainMenuMode()
        app.roomMode = RoomMode()
        app.helpMode = HelpMode()
        # app.mazeMode = MazeMode()
        # app.setActiveMode(app.mainMenuMode)
        app.setActiveMode(app.roomMode)
        app.timerDelay = 50

app = TermProject(width=800, height=600)
