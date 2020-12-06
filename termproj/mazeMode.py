import module_manager
module_manager.review()

import math, copy, random
# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

class MazeMode(Mode):
    def appStarted(mode):
        mode.mazeWidth = mode.height
        mode.mazeHeight = mode.height
        mode.gridSize = 100
        mode.cols = math.floor(mode.mazeWidth/mode.gridSize) # width/gs
        mode.rows = math.floor(mode.mazeHeight/mode.gridSize) # height/gs
        mode.roomLen = 4
        mode.roomCells = []

        mode.pX, mode.pY = 0, 0

        mode.grids = []
        mode.stack = []
        for i in range(mode.roomLen):
            rcX, rcY = math.floor(random.randrange(0, mode.cols)), math.floor(random.randrange(0, mode.rows))
            mode.roomCells.append((rcX, rcY))


        mode.drawMaze()
        mode.currentCell = mode.grids[0]

        mode.font = 'Arial 26 bold' 

        mode.room = RoomMode(0)
        mode.drawRoom = False

    def drawMaze(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                cell = Cell(col, row, mode.cols, mode.rows, mode.grids, mode.gridSize)
                mode.grids.append(cell)

    def removeWall(mode, current, next):
        dcol = current.col - next.col
        if (dcol == 1):
            current.walls[3] = False
            next.walls[1] = False
        elif (dcol == -1):
            current.walls[1] = False
            next.walls[3] = False

        drow = current.row - next.row
        if (drow == 1):
            current.walls[0] = False
            next.walls[2] = False
        elif (drow == -1):
            current.walls[2] = False
            next.walls[0] = False

    def displayText(mode, canvas, text, pos):
        canvas.create_text(pos[0], pos[1], text = text, font = mode.font, fill = 'white')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
        canvas.create_rectangle(0, 0, mode.mazeWidth, mode.mazeHeight, fill="black", outline = "white", width = 1)
        
        if (len(mode.stack) == 0):
            for cell in range(len(mode.grids)):   
                mode.grids[cell].drawCell(canvas)
        
            for i in range(len(mode.roomCells)):
                row, col = mode.roomCells[i][0], mode.roomCells[i][1]
                mode.drawRoomCell(canvas, row, col, "room")

            mode.currentCell.visited = True
            # mode.currentCell.drawCurrentCell(canvas)  
            mode.drawRoomCell(canvas, mode.pY, mode.pX, "player")
        else:
            mode.displayText(canvas, "LOADING MAZE...", (mode.height/2, mode.height/2))

        next = mode.currentCell.checkNeighbors()
        if (next is not None):
            next.visited = True
            mode.stack.append(mode.currentCell)
            mode.removeWall(mode.currentCell, next)
            mode.currentCell = next
        elif (len(mode.stack) > 0):
            mode.currentCell = mode.stack.pop()    
        
        if mode.drawRoom:
            mode.room.drawViewport(canvas, [(0, 0), (400, 400)])
    
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
        if (event.key == "r"):
            mode.appStarted()
        elif (event.key == "Up"):
            if (not mode.getPlayerCell(mode.pX, mode.pY, 0)):
                mode.pY -= 1
        elif (event.key == "Right"):
            if (not mode.getPlayerCell(mode.pX, mode.pY, 1)):
                mode.pX += 1
        elif (event.key == "Down"):
            if (not mode.getPlayerCell(mode.pX, mode.pY, 2)):
                mode.pY += 1
        elif (event.key == "Left"):
            if (not mode.getPlayerCell(mode.pX, mode.pY, 3)):
                mode.pX -= 1    
        elif (event.key == "Enter"):
            enterRoom = mode.checkIfEnterRoom((mode.pY, mode.pX), mode.roomCells)
            if enterRoom:
                print(enterRoom, mode.roomCells.index((mode.pY, mode.pX)))
                mode.drawRoom = True
                

class Cell(MazeMode):
    def __init__(self, col, row, cols, rows, grids, gridSize):
        self.col = col
        self.row = row
        self.cols = cols
        self.rows = rows
        self.grids = grids

        self.walls = [True, True, True, True]
        self.visited = False
        self.x1 = col * gridSize
        self.y1 = row * gridSize
        self.x2 = (col + 1) * gridSize
        self.y2 = (row + 1) * gridSize
    
    def checkNeighbors(self):
        neighbors = []
        topCell = self.getCell(self.col, self.row - 1)
        rightCell = self.getCell(self.col + 1, self.row)
        downCell = self.getCell(self.col, self.row + 1)
        leftCell = self.getCell(self.col - 1, self.row)

        if (topCell is not None) and (not topCell.visited):
            neighbors.append(topCell)
        
        if (rightCell is not None) and (not rightCell.visited):
            neighbors.append(rightCell)
        
        if (downCell is not None) and (not downCell.visited):
            neighbors.append(downCell)

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

        # up
        if self.walls[0]:
            canvas.create_line(self.x1, self.y1, self.x2, self.y1, fill = "white", width = 1)
        # right
        if self.walls[1]:
            canvas.create_line(self.x2, self.y1, self.x2, self.y2, fill = "white", width = 1)
        # bottom
        if self.walls[2]:
            canvas.create_line(self.x2, self.y2, self.x1, self.y2, fill = "white", width = 1)
        # left
        if self.walls[3]:
            canvas.create_line(self.x1, self.y2, self.x1, self.y1, fill = "white", width = 1)

    def drawCurrentCell(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = "yellow", width = 0)

class RoomMode(MazeMode):  
    def __init__(self, idx):
        # scene view settings
        self.idx = idx
    
    def drawViewport(self, canvas, pos):
        canvas.create_rectangle(pos[0][0], pos[0][1],
                                pos[1][0], pos[1][1], 
                                fill = 'blue', width = 0)  
    

class TermProject(ModalApp):
    def appStarted(app):
        
        app.mazeMode = MazeMode()
        app.setActiveMode(app.mazeMode)
        app.timerDelay = 50

app = TermProject(width=800, height=600)