# Code from: https://www.cs.cmu.edu/~112/notes/term-project.html#tp0
import module_manager
module_manager.review()

import math, copy, random

# import items

# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

#################################################
# Helper functions from 112 website:
# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

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
                mode.app.setActiveMode(mode.app.gameMode)
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

class GameMode(Mode):
    def appStarted(mode):
        # scene view settings
        mode.viewPortPos = [(mode.width * (1/4), 0), (mode.width, mode.height * (2/3))]
        mode.itemBarPos = [(0, 0), (mode.width * (1/4), mode.height)]
        mode.textDisplayPos = [(mode.width * (1/4), mode.height * (2/3)), (mode.width, mode.height)]
        mode.viewPortSize = [mode.width * (3/4), mode.height * (2/3)]
        mode.itembarSize = [mode.width * (1/4), mode.height]
        mode.itembarRows = 5 
        mode.itembarCols = 2
        mode.textDisplaySize = [mode.width * (3/4), mode.height * (1/3)]
        # font size
        mode.font = 'Arial 18 bold'
        # list of each side of the room
        mode.roomSides = ["front", "right", "back", "left", "top", "bottom"]
        mode.currentSide = 0
        # list of all items in the room (currently: r1)
        mode.r1Items = 0
        mode.r1=[
                    {
                        "name": "bacon",
                        "interaction": ["add", "combine"]
                    },
                    {
                        "name": "pan",
                        "interaction": ["add", "combine"]
                    },
                    {
                        "name": "flour",
                        "interaction": ["add", "combine"]
                    },
                    {
                        "name": "eggs",
                        "interaction": ["add", "combine"]
                    },
                    {
                        "name": "pattern",
                        "interaction": ["remove"]
                    }
                ]
        # add items
        mode.items = []
        for i in range(len(mode.r1)):
            size = 80
            px = random.randrange(mode.width * (1/4) + size * 2, mode.width - size * 2)
            py = mode.height/2
            # set which side of the room the object is on
            sideIdx = math.floor(random.randrange(0, 6))
            itm = item(mode.r1[i], (px, py), size, sideIdx)
            mode.items.append(itm)
            print(sideIdx, itm.name)
        # current selected item cell and item
        mode.cellselected = (-1, -1)
        mode.itemselected = (-1, -1)
        mode.itemNewPos = (-1, -1)
        mode.cellpositions = []

    # Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(mode, row, col, rows, cols, posMode):
        gridWidth  = mode.itembarSize[0]
        gridHeight = mode.itembarSize[1]
        cellWidth = gridWidth / cols
        cellHeight = gridHeight / rows
        if (posMode == "corner"):
            x0 = col * cellWidth
            x1 = (col+1) * cellWidth
            y0 = row * cellHeight
            y1 = (row+1) * cellHeight
            return (x0, y0, x1, y1)
        elif (posMode == "center"):
            x = col * cellWidth + cellWidth / 2
            y = row * cellHeight + cellHeight / 2
            return (x, y)
    
    # Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def pointInGrid(mode, x, y):
    # return True if (x, y) is inside the grid
        return ((0 <= x <= mode.itembarSize[0]) and
                (0 <= y <= mode.itembarSize[1]))

    # Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids 
    def getCell(mode, x, y, rows, cols):
        if (not mode.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = mode.itembarSize[0]
        gridHeight = mode.itembarSize[1]
        cellWidth  = mode.itembarSize[0] / cols
        cellHeight = mode.itembarSize[1] / rows
        row = int(y / cellHeight)
        col = int(x / cellWidth)
        return (row, col)

    def drawItembar(mode, canvas, rows, cols):
        canvas.create_rectangle(mode.itemBarPos[0][0], mode.itemBarPos[0][1],
                                mode.itemBarPos[1][0], mode.itemBarPos[1][1], 
                                fill = 'purple')
        for row in range(rows):
            for col in range(cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col, rows, cols, "corner")
                if (mode.cellselected == (row, col)): 
                    fill = 'gold'
                else:
                    fill = 'purple'
                canvas.create_rectangle(x0, y0, x1, y1, fill = fill, outline = 'white', width = 3)
                mode.cellpositions.append((row, col))
    
    def drawTextdisplay(mode, canvas, pos, size):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = 'gold')
        textPos = (pos[0][0] + size[0]/2, pos[0][1] + size[1]/2)
        text = 'FIND THE ITEMS'
        if (mode.r1Items == 5):
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
        elif (event.key == "m"):
            mode.app.setActiveMode(mode.app.mainMenuMode)
            mode.appStarted()

    def mousePressed(mode, event):
        if (event.x > mode.viewPortPos[0][0]):
            mode.cellselected = (-1, -1)
            for i in range(len(mode.items)):
                if (mode.currentSide == mode.items[i].sideIdx):
                    if (mode.items[i].addItem(event.x, event.y) != None) and mode.itemNewPos != (-1, -1):
                        mode.items[i].centerPos = mode.itemNewPos
                        mode.items[i].sideIdx = -1
                        mode.itemNewPos = (-1, -1)
                        mode.r1Items += 1
                        # mode.cellpositions.remove(mode.cellselected)
        else:
            (row, col) = mode.getCell(event.x, event.y, mode.itembarRows, mode.itembarCols)
            # select this (row, col) unless it is selected
            if (mode.cellselected == (row, col)):
                mode.cellselected = (-1, -1)
                mode.itemNewPos = (-1, -1)
            else:
                mode.cellselected = (row, col)
                mode.itemNewPos = mode.getCellBounds(row, col, mode.itembarRows, mode.itembarCols, "center")

    def redrawAll(mode, canvas):
        # draw viewport
        mode.drawViewport(canvas, mode.viewPortPos)
        
        # draw text display
        mode.drawTextdisplay(canvas, mode.textDisplayPos, mode.textDisplaySize)
        
        # draw item bar
        mode.drawItembar(canvas, mode.itembarRows, mode.itembarCols)
        for i in range(len(mode.items)):
            # draw the item at its room side, if it's in itembar then always draw it
            if (mode.currentSide == mode.items[i].sideIdx) or (mode.items[i].sideIdx == -1):
                mode.items[i].displayItem(canvas)

class item(GameMode):
    def __init__(self, properties, pos, size, sideIdx):
        self.name = properties["name"]
        self.interaction = properties["interaction"]
        self.size = size
        self.sideIdx = sideIdx
        self.centerPos = pos
    
    def displayItem(self, canvas):
        x0, y0 = self.centerPos[0]-self.size/2, self.centerPos[1]-self.size/2
        x1, y1 = self.centerPos[0]+self.size/2, self.centerPos[1]+self.size/2
        canvas.create_rectangle(x0, y0, x1, y1, outline='white', width = 1)
        canvas.create_text(self.centerPos[0], self.centerPos[1], 
                          text = self.name, font = 'Arial 16 bold', fill = 'white')        

    def addItem(self, mX, mY):
        x0, y0 = self.centerPos[0]-self.size/2, self.centerPos[1]-self.size/2
        x1, y1 = self.centerPos[0]+self.size/2, self.centerPos[1]+self.size/2
        if (x0 < mX < x1) and (y0 < mY < y1):
            return self.centerPos
       
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
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        # app.setActiveMode(app.mainMenuMode)
        app.setActiveMode(app.gameMode)
        app.timerDelay = 50

app = TermProject(width=800, height=600)
