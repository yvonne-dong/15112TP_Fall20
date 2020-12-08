# Code from: https://www.cs.cmu.edu/~112/notes/term-project.html#tp0
import module_manager
module_manager.review()

import math, copy, random

# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

# external file for storing room properties
import properties as prop

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
                mode.app.setActiveMode(mode.app.mazeMode)
                mode.app.mazeMode.appStarted()
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
        
        mode.generateMaze()
        mode.font = 'Arial 26 bold' 

    def generateMaze(mode):
        # initial values
        mode.roomCells = []
        mode.rooms = []
        mode.grids = []
        mode.stack = []
        mode.currentCell = 0

        mode.pX, mode.pY = 0, 0
        mode.disableMazeKeys = False
        mode.currentRoomIdx = 0
        mode.currentSide = 0
        mode.roomGameMode = False
        mode.hint = ""

        for i in range(mode.roomLen):
            rcX, rcY = math.floor(random.randrange(1, mode.cols)), math.floor(random.randrange(0, mode.rows))
            mode.roomCells.append((rcX, rcY))
            mode.rooms.append(RoomMode(i, mode.width, mode.height))

        mode.drawMaze()
        mode.currentCell = mode.grids[0]
        mode.currentCell.visited = True
        mode.stack.append(mode.currentCell)    

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
                r.drawTextdisplay(canvas, r.textDisplayPos, r.textDisplaySize, r.idx, mode.currentSide, mode.hint)
    
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
                mode.currentSide = 0
                mode.currentRoomIdx = mode.roomCells.index((mode.pY, mode.pX))
                mode.disableMazeKeys = not mode.disableMazeKeys
                mode.rooms[mode.currentRoomIdx].displayRoom = not mode.rooms[mode.currentRoomIdx].displayRoom
        
        elif (event.key == "r"):
            if (not mode.disableMazeKeys):
                mode.generateMaze()
        if (event.key == "Up"):
            if (not mode.disableMazeKeys):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "top")):
                    mode.pY -= 1
        elif (event.key == "Right"):
            if (not mode.disableMazeKeys):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "right")):
                    mode.pX += 1
        elif (event.key == "Down"):
            if (not mode.disableMazeKeys):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "bottom")):
                    mode.pY += 1
        elif (event.key == "Left"):
            if (not mode.disableMazeKeys):
                if (not mode.getPlayerCell(mode.pX, mode.pY, "left")):
                    mode.pX -= 1  
        # Go back to main menu
        elif (event.key == "m"):
            if (not mode.disableMazeKeys):
                mode.app.setActiveMode(mode.app.mainMenuMode)
                # mode.appStarted()

        if (mode.disableMazeKeys):
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
        
    def mousePressed(mode, event):
        if (mode.disableMazeKeys):
            cr = mode.rooms[mode.currentRoomIdx]
            for i in range(len(cr.items)):
                if (mode.currentSide == cr.items[i].sideIdx):
                    if (cr.items[i].clickOnItem(event.x, event.y, cr.collectedItems) != None) and (cr.items[i].status == False):
                        if (cr.items[i].interaction == "add"):
                            mode.hint = f'YOU COLLECTED {cr.items[i].name}'
                            cr.collectedItems.append(cr.items[i].name)
                            cr.items[i].status = True
                        elif (cr.items[i].interaction == "remove"):
                            mode.hint = f"YOU REMOVED {cr.items[i].name}"
                            cr.items[i].status = True
                        elif (cr.items[i].interaction == "see"):
                            mode.hint = f'YOU SAW {cr.items[i].name}'
                        elif (cr.items[i].interaction == "combine"):
                            mode.hint = "COMBINED! (***IN PROGRESS)"
                            # *** change based on room
                            # if (mode.items[i].reachRequire):
                            #     mode.collectedItems.remove("raw eggs")
                            #     mode.collectedItems.remove("flour")
                            #     mode.collectedItems.extend(["eggs","pancakes"])
                            #     mode.items[i].status = True
                            #     print("collected combined!")
                            # else:
                            #     print("collect requirements")
                        elif (cr.items[i].interaction == "password"):
                            mode.hint = "ANSWER THIS PUZZLE"
                            cr.items[i].passwordEntry(cr.userAnswer, cr.question, cr.correctAnswer, cr.addItem, cr.collectedItems, mode.hint)
                    else:
                        mode.hint = "TRY SOMEWHERE ELSE"
        
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
    def __init__(self, idx, w, h):
        # width, height of main window
        self.width = w
        self.height = h

        # scene view settings
        self.idx = idx
        self.roomColor = prop.roomColors[self.idx]
        self.displayRoom = False
        self.viewPortPos = [(0, 0), (self.width, self.height * (2/3))]
        self.textDisplayPos = [(0, self.height * (2/3)), (self.width, self.height)]
        self.viewPortSize = [self.width, self.height * (2/3)]
        self.textDisplaySize = [self.width, self.height * (1/3)]
        
        self.font = 'Arial 18 bold'
        self.roomText = ''
        # list of each side of the room, set current facing side to "front"
        self.roomSides = ["FRONT", "RIGHT", "BACK", "LEFT", "TOP", "BOTTOM"]
        self.currentSide = 0
        
        # check collected items
        self.items = []
        self.collectedItems = []
        
        for i in range(len(prop.roomProperties[self.idx])):
            # *** change based on asset image size
            size = 80
            # *** change to random no overlap 
            x1 = random.randrange(size * 2, self.width - size * 2)
            y1 = random.randrange(size * 2, self.height * (2/3) - size * 2)
            # set which side of the room the object is on
            sideIdx = math.floor(random.randrange(0, 6))
            itm = item(prop.roomProperties[self.idx][i], (x1, y1), size, sideIdx)
            self.items.append(itm)
        
        
        # for answering password
        self.userAnswer = ""
        # change based on which room player is in
        self.correctAnswer = ""
        self.question = ""
        self.addItem = prop.riddleAddItem[self.idx]
        if (self.idx == 1 or self.idx == 3):
            randIdx = math.floor(random.randrange(0, 6))
            self.question = prop.riddles[randIdx]["Q"]
            self.correctAnswer = prop.riddles[randIdx]["A"]

        if (self.idx == 0):
            self.question = prop.r1Question
            self.correctAnswer = prop.r1Answer
        
        # saved text for text editor
        self.previousText = ""

    def drawTextdisplay(self, canvas, pos, size, idx, currentSide, hint):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = 'gold', width = 0)
        textPos = (pos[0][0] + size[0]/2, pos[0][1] + size[1]/2)
        if len(hint) > 0:
            self.roomText = hint
        else:
            self.roomText = f'FIND THE ITEMS FOR {prop.roomNames[self.idx]}'
        verify = set(self.collectedItems)
        if verify == prop.roomAllItems[idx]:
            self.roomText = 'YOU HAVE COLLECTED ALL ITEMS, PRESS M FOR MAIN MENU'
        canvas.create_text(textPos[0], textPos[1], 
                          text = self.roomText, font = self.font, fill = 'white')
        roomsideTextPos = (pos[0][0] + size[0]/20, pos[0][1] + size[0]/20)
        canvas.create_text(roomsideTextPos[0], roomsideTextPos[1], 
                          text = self.roomSides[currentSide], 
                          font = self.font, fill = 'white', anchor='w')
    
    def drawViewport(self, canvas, pos, currentSide):
        # display view background
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = self.roomColor, width = 0)  
        
        # display all items
        for i in range(len(self.items)):
            # draw the item at its room side
            if (currentSide == self.items[i].sideIdx) and (self.items[i].status == False):
                self.items[i].displayItem(canvas)

    # *** redo text editor...
    def displayTextEditor(self, previousText):
        print("call notepad: need more work...")

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
    
    def passwordEntry(self, input, question, answer, addItem, items, hint):
        # Code modified from: https://www.geeksforgeeks.org/python-tkinter-entry-widget/
        root = Tk()
        root.title('PUZZLE')
        Label(root, text = question).grid(row = 0)

        textEntry = Entry(root)
        textEntry.grid(row = 1)

        def reply():
            input = textEntry.get()
            textEntry.delete(0, 'end')
            root.destroy()
            if (input.lower() == answer):
                hint = f"CORRECT! COLLECTED {addItem.upper()}"
                items.append(addItem)
            else:
                hint = "WRONG : ( TRY AGAIN"

        button = Button(root, text = "ANSWER", command = reply)
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
        app.helpMode = HelpMode()
        app.mazeMode = MazeMode()
        app.setActiveMode(app.mazeMode)
        # app.setActiveMode(app.mainMenuMode)
        app.timerDelay = 50

app = TermProject(width=800, height=600)
