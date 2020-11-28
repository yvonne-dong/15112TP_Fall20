# Code from: https://www.cs.cmu.edu/~112/notes/term-project.html#tp0
import module_manager
module_manager.review()

import math, copy, random

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
        mode.playerPos = [mode.width/2, mode.height/2]
        mode.playerSize = 25
        mode.objCounts = 10
        mode.objPoses = [(random.randrange(random.randint(10, 25), mode.width-random.randint(10, 25)), 
                         random.randrange(random.randint(10, 25), mode.height-random.randint(10, 25)), 
                         random.randint(10, 25)) 
                         for i in range(mode.objCounts)]
        mode.textDisplay = 100
        mode.font = 'Arial 26 bold'

    def drawPlayer(mode, canvas):
        canvas.create_rectangle(mode.playerPos[0]-mode.playerSize, mode.playerPos[1]-mode.playerSize, 
                                mode.playerPos[0]+mode.playerSize, mode.playerPos[1]+mode.playerSize,
                                fill='white', width = 0)

    def drawObjects(mode, canvas, objXYSize):
        canvas.create_rectangle(objXYSize[0] - objXYSize[2], objXYSize[1] - objXYSize[2], 
                                objXYSize[0] + objXYSize[2], objXYSize[1] + objXYSize[2],
                                fill='gold', width = 0)

    def keyPressed(mode, event):
        moveStep = 10
        if (event.key == "Left"):
            mode.playerPos[0] -= moveStep
            if (mode.playerPos[0] - mode.playerSize < 0):
                mode.playerPos[0] = mode.playerSize
        elif (event.key == "Right"):
            mode.playerPos[0] += moveStep
            if (mode.playerPos[0] + mode.playerSize > mode.width):
                mode.playerPos[0] = mode.width - mode.playerSize
        elif (event.key == "Up"):
            mode.playerPos[1] -= moveStep
            if (mode.playerPos[1] - mode.playerSize < 0):
                mode.playerPos[1] = mode.playerSize
        elif (event.key == "Down"):
            mode.playerPos[1] += moveStep
            if (mode.playerPos[1] + mode.playerSize > mode.height):
                mode.playerPos[1] = mode.height - mode.playerSize
        elif (event.key == "m"):
            mode.app.setActiveMode(mode.app.mainMenuMode)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'blue')
        canvas.create_text(mode.width/2, mode.height - mode.textDisplay, 
                          text = 'PRESS M FOR MENU', font = mode.font, fill = 'white')
        for i in range(mode.objCounts):
            mode.drawObjects(canvas, mode.objPoses[i])
        mode.drawPlayer(canvas)

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
        app.setActiveMode(app.mainMenuMode)
        app.timerDelay = 50

app = TermProject(width=600, height=600)
