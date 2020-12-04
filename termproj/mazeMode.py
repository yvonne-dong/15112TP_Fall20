import module_manager
module_manager.review()

import math, copy, random
# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

class MazeMode(Mode):
    def appStarted(mode):
        mode.gridSize = 50
        mode.cols = 16 # width/gs
        mode.rows = 12 # height/gs

        mode.grids = []
        mode.drawMaze()
        mode.currentCell = mode.grids[0]

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

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, 800, 600, fill="black")
        for cell in range(len(mode.grids)):   
            mode.grids[cell].drawCell(canvas)
        
        mode.currentCell.visited = True
        mode.currentCell.drawCurrentCell(canvas)
        next = mode.currentCell.checkNeighbors()
        if (next is not None):
            next.visited = True
            mode.removeWall(mode.currentCell, next)
            mode.currentCell = next

    def keyPressed(mode, event):
        if (event.key == "r"):
            mode.appStarted()

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

        # top
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

class TermProject(ModalApp):
    def appStarted(app):
        app.mazeMode = MazeMode()
        app.setActiveMode(app.mazeMode)
        app.timerDelay = 100

app = TermProject(width=800, height=600)
