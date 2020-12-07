# Code from: https://www.cs.cmu.edu/~112/notes/term-project.html#tp0
import module_manager
module_manager.review()

import math, copy, random


# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

# external file for storing room properties
import properties as prop
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

# Algorithm (written in English) from: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_implementation
class MazeMode(Mode):
    def appStarted(mode):
        mode.mazeWidth = mode.height
        mode.mazeHeight = mode.height
        mode.gridSize = 100
        mode.cols = math.floor(mode.mazeWidth/mode.gridSize) # width/gs
        mode.rows = math.floor(mode.mazeHeight/mode.gridSize) # height/gs
        mode.roomLen = 4
        mode.roomCells = []
        mode.rooms = []
        mode.disableMazeKeys = False
        mode.currentSide = 0

        mode.pX, mode.pY = 0, 0

        mode.grids = []
        mode.stack = []
        for i in range(mode.roomLen):
            rcX, rcY = math.floor(random.randrange(1, mode.cols)), math.floor(random.randrange(0, mode.rows))
            mode.roomCells.append((rcX, rcY))
            # *** setting up individual room bg color
            r = math.floor(random.randrange(0, 255))
            g = math.floor(random.randrange(0, 100))
            b = math.floor(random.randrange(0, 200))
            mode.rooms.append(RoomMode(i, rgbString(r, g, b), mode.width, mode.height))

        mode.drawMaze()
        mode.currentCell = mode.grids[0]
        mode.currentCell.visited = True
        mode.stack.append(mode.currentCell)
        mode.font = 'Arial 26 bold' 

    def drawMaze(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                cell = Cell(col, row, mode.cols, mode.rows, mode.grids, mode.gridSize)
                mode.grids.append(cell)

    def displayText(mode, canvas, text, pos):
        canvas.create_text(pos[0], pos[1], text = text, font = mode.font, fill = 'white')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
        canvas.create_rectangle(0, 0, mode.mazeWidth, mode.mazeHeight, fill="black", outline = "white", width = 1)
        
        for cell in range(len(mode.grids)):   
            mode.grids[cell].drawCell(canvas)
        
        for i in range(len(mode.roomCells)):
            row, col = mode.roomCells[i][0], mode.roomCells[i][1]
            mode.drawRoomCell(canvas, row, col, "room")
        
        mode.drawRoomCell(canvas, mode.pY, mode.pX, "player")

        while (len(mode.stack) > 0):
            mode.currentCell = mode.stack.pop()    
            next = mode.currentCell.checkNeighbors()
            if (next is not None):
                mode.stack.append(mode.currentCell)
                mode.removeWall(mode.currentCell, next)
                mode.currentCell = next
                mode.currentCell.visited = True
                mode.stack.append(mode.currentCell)
                
        for r in mode.rooms:
            if r.displayRoom:
                r.drawViewport(canvas, r.viewPortPos, mode.currentSide)
                r.drawTextdisplay(canvas, r.textDisplayPos, r.textDisplaySize, r.idx, mode.currentSide)
    
    def removeWall(mode, current, next):
        dcol = current.col - next.col
        # r - l
        if (dcol == 1):
            current.walls["left"] = False
            next.walls["right"] = False
        # l - r
        elif (dcol == -1):
            current.walls["right"] = False
            next.walls["left"] = False

        drow = current.row - next.row
        # d - t
        if (drow == 1):
            current.walls["top"] = False
            next.walls["bottom"] = False
        # t - d
        elif (drow == -1):
            current.walls["bottom"] = False
            next.walls["top"] = False         
    
    def drawRoomCell(mode, canvas, row, col, drawMode):
        x1, y1, x2, y2 = col * mode.gridSize, row * mode.gridSize, (col + 1) * mode.gridSize, (row + 1) * mode.gridSize
        if drawMode == "room":
            r = 5
            canvas.create_rectangle(x1+r, y1+r, x2-r, y2-r, fill = "pink", width = 0)
        elif drawMode == "player":
            r = 20
            canvas.create_oval(x1+r, y1+r, x2-r, y2-r, fill = "gold", width = 0)

    def getPlayerCell(mode, col, row, side):
        playerCellWalls = mode.grids[col + row * mode.cols].walls
        return playerCellWalls[side]

    def checkIfEnterRoom(mode, playerPos, roomPoses):
        return playerPos in roomPoses
    
    def keyPressed(mode, event):
        if (event.key == "Enter"):
            enterRoom = mode.checkIfEnterRoom((mode.pY, mode.pX), mode.roomCells)
            if enterRoom:
                roomId = mode.roomCells.index((mode.pY, mode.pX))
                mode.disableMazeKeys = not mode.disableMazeKeys
                mode.rooms[roomId].displayRoom = not mode.rooms[roomId].displayRoom
        if (not mode.disableMazeKeys):
            if (event.key == "r"):
                mode.appStarted()
            elif (event.key == "Up"):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "top")):
                    mode.pY -= 1
            elif (event.key == "Right"):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "right")):
                    mode.pX += 1
            elif (event.key == "Down"):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "bottom")):
                    mode.pY += 1
            elif (event.key == "Left"):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "left")):
                    mode.pX -= 1  
        else:
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
        
        
                
class Cell(MazeMode):
    def __init__(self, col, row, cols, rows, grids, gridSize):
        self.col = col
        self.row = row
        self.cols = cols
        self.rows = rows
        self.grids = grids

        self.x1 = col * gridSize
        self.y1 = row * gridSize
        self.x2 = (col + 1) * gridSize
        self.y2 = (row + 1) * gridSize
        self.walls ={
                        "top": True,
                        "right": True,
                        "bottom": True,
                        "left": True
                    }
        self.visited = False
        
    
    def checkNeighbors(self):
        # create a list to store all possible neighbors
        neighbors = []
        topCell = self.getCell(self.col, self.row - 1)
        rightCell = self.getCell(self.col + 1, self.row)
        bottomCell = self.getCell(self.col, self.row + 1)
        leftCell = self.getCell(self.col - 1, self.row)

        if (topCell is not None) and (not topCell.visited):
            neighbors.append(topCell)
        
        if (rightCell is not None) and (not rightCell.visited):
            neighbors.append(rightCell)
        
        if (bottomCell is not None) and (not bottomCell.visited):
            neighbors.append(bottomCell)

        if (leftCell is not None) and (not leftCell.visited):
            neighbors.append(leftCell)
            
        if (len(neighbors) > 0):
            rand = math.floor(random.randrange(0, len(neighbors)))
            return neighbors[rand]
        else:
            return None
    
    def getCell(self, col, row):
        if (col < 0) or (row < 0) or (col > self.cols - 1) or (row > self.rows - 1):
            return None
        return self.grids[col + row * self.cols]

    def drawCell(self, canvas):
        if self.visited:
            canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "purple", width = 0)

        # top
        if self.walls["top"]:
            canvas.create_line(self.x1, self.y1, self.x2, self.y1, fill = "white", width = 1)
        # right
        if self.walls["right"]:
            canvas.create_line(self.x2, self.y1, self.x2, self.y2, fill = "white", width = 1)
        # bottom
        if self.walls["bottom"]:
            canvas.create_line(self.x2, self.y2, self.x1, self.y2, fill = "white", width = 1)
        # left
        if self.walls["left"]:
            canvas.create_line(self.x1, self.y2, self.x1, self.y1, fill = "white", width = 1)

    def drawCurrentCell(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "yellow", width = 0)

class RoomMode(MazeMode): 
    def __init__(self, idx, roomColor, w, h):
        # width, height of main window
        self.width = w
        self.height = h

        # scene view settings
        self.idx = idx
        self.roomColor = roomColor
        self.displayRoom = False
        self.viewPortPos = [(0, 0), (self.width, self.height * (2/3))]
        self.textDisplayPos = [(0, self.height * (2/3)), (self.width, self.height)]
        self.viewPortSize = [self.width, self.height * (2/3)]
        self.textDisplaySize = [self.width, self.height * (1/3)]
        
        self.font = 'Arial 18 bold'

        # list of each side of the room, set current facing side to "front"
        self.roomSides = ["front", "right", "back", "left", "top", "bottom"]
        self.currentSide = 0

        # get properties stored in properties.py
        self.roomAllItems = [prop.r1AllItems, prop.r2AllItems, prop.r3AllItems, prop.r4AllItems]
        self.roomProperties = [prop.r1, prop.r2, prop.r3, prop.r4]
        
        # check collected items
        self.items = []
        self.collectedItems = []
        
        for i in range(len(self.roomProperties[self.idx])):
            # *** change based on asset image size
            size = 80
            # *** change to random no overlap 
            x1 = random.randrange(size * 2, self.width - size * 2)
            y1 = random.randrange(size * 2, self.height * (2/3) - size * 2)
            # set which side of the room the object is on
            sideIdx = math.floor(random.randrange(0, 6))
            itm = item(self.roomProperties[self.idx][i], (x1, y1), size, sideIdx)
            self.items.append(itm)
        
        
        # for answering password
        self.userAnswer = ""
        # change based on which room player is in
        self.correctAnswer = ""
        
        # saved text for text editor
        self.previousText = ""

    def drawTextdisplay(self, canvas, pos, size, idx, currentSide):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = 'gold', width = 0)
        textPos = (pos[0][0] + size[0]/2, pos[0][1] + size[1]/2)
        text = f'FIND THE ITEMS FOR ROOM {self.idx}'
        verify = set(self.collectedItems)
        if verify == self.roomAllItems[idx]:
            text = 'YOU HAVE COLLECTED ALL ITEMS, PRESS M FOR MAIN MENU'
        canvas.create_text(textPos[0], textPos[1], 
                          text = text, font = self.font, fill = 'white')
        roomsideTextPos = (pos[0][0] + size[0]/20, pos[0][1] + size[0]/20)
        canvas.create_text(roomsideTextPos[0], roomsideTextPos[1], 
                          text = self.roomSides[currentSide], 
                          font = self.font, fill = 'white', anchor='w')
    
    def drawViewport(self, canvas, pos, currentSide):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = self.roomColor, width = 0)  
        for i in range(len(self.items)):
            # draw the item at its room side
            if (currentSide == self.items[i].sideIdx) and (self.items[i].status == False):
                self.items[i].displayItem(canvas)


    # *** redo text editor...
    def displayTextEditor(self, previousText):
        print("call notepad: need more work...")
    
    '''
    # *** move to maze mode!!!   
    # check if room display is on or not
 
    def keyPressed(mode, event):
        
        
        # Go back to main menu
        elif (event.key == "m"):
            mode.app.setActiveMode(mode.app.mainMenuMode)
            mode.appStarted()
        
        # Call notebook
        elif (event.key == "n"):
            mode.displayTextEditor(mode.previousText)
    '''

    '''
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
                            mode.collectedItems.remove("raw eggs")
                            mode.collectedItems.remove("flour")
                            mode.collectedItems.extend(["eggs","pancakes"])
                            mode.items[i].status = True
                            print("collected combined!")
                        else:
                            print("collect requirements")
                    elif (mode.items[i].interaction == "game"):
                        mode.items[i].passwordEntry(mode.userAnswer, mode.answer, mode.collectedItems)

    def redrawAll(mode, canvas):
        # draw viewport
        mode.drawViewport(canvas, mode.viewPortPos)
        
        # draw text display
        mode.drawTextdisplay(canvas, mode.textDisplayPos, mode.textDisplaySize)
        
        # draw items in room
        
    '''

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
    
    def passwordEntry(self, input, answer, items):
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
                items.append("bacon")
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
        # app.roomMode = RoomMode()
        app.helpMode = HelpMode()
        app.mazeMode = MazeMode()
        app.setActiveMode(app.mazeMode)
        # app.setActiveMode(app.mainMenuMode)
        # app.setActiveMode(app.roomMode)
        app.timerDelay = 50

app = TermProject(width=800, height=600)
