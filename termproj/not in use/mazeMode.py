import module_manager
module_manager.review()

import math, copy, random
# Code from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
import tempdata as td

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

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

        mode.pX, mode.pY = 0, 0

        mode.grids = []
        mode.stack = []
        for i in range(mode.roomLen):
            rcX, rcY = math.floor(random.randrange(0, mode.cols)), math.floor(random.randrange(0, mode.rows))
            mode.roomCells.append((rcX, rcY))
            r = math.floor(random.randrange(0, 255))
            g = math.floor(random.randrange(0, 100))
            b = math.floor(random.randrange(0, 200))
            mode.rooms.append(RoomMode(i, rgbString(r, g, b), (mode.mazeWidth, mode.mazeHeight)))

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
                r.drawViewport(canvas, [(0, 0), (400, 400)])   
    
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
        elif (event.key == "Enter"):
            # td.r1[0]["status"] = True
            # print(td.r1[0])
            enterRoom = mode.checkIfEnterRoom((mode.pY, mode.pX), mode.roomCells)
            if enterRoom:
                print(enterRoom, mode.roomCells.index((mode.pY, mode.pX)))
                roomId = mode.roomCells.index((mode.pY, mode.pX))
                mode.rooms[roomId].displayRoom = not mode.rooms[roomId].displayRoom
                # mode.drawRoom = True
                
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
    def __init__(self, idx, roomColor, size):
        # scene view settings
        self.idx = idx
        self.roomColor = roomColor
        self.displayRoom = False
        self.width, self.height = size
        self.font = 'Arial 26 bold' 

        self.r1 =[
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
                        "name": "raw eggs",
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
                        "require": ["flour", "raw eggs"],
                        "timed": False
                    }
                ]
        self.r2 =[
                    {
                        "name": "cake mix",
                        "interaction": "password",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "chocolate frosting",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "vanilla frosting",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "shelve",
                        "interaction": "remove",
                        "status": False,
                        "require": None,
                        "timed": False
                    }
                ]
        self.r3 =[
                    {
                        "name": "cow",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "centrifuge",
                        "interaction": "combine",
                        "status": False,
                        "require": ["cow"],
                        "timed": False
                    },
                    {
                        "name": "lettuce",
                        "interaction": "game",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "jellyfish",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "red balloon",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "mixer",
                        "interaction": "combine",
                        "status": False,
                        "require": ["jellyfish", "red balloon"],
                        "timed": False
                    },
                    {
                        "name": "bread",
                        "interaction": "password",
                        "status": False,
                        "require": None,
                        "timed": False
                    }
                ]
        self.r4 =[
                    {
                        "name": "apple",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "marker",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "book",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "bed",
                        "interaction": "remove",
                        "status": False,
                        "require": None,
                        "timed": False
                    },
                    {
                        "name": "bass",
                        "interaction": "add",
                        "status": False,
                        "require": None,
                        "timed": False
                    }
                ]
        self.roomProperties = [self.r1, self.r2, self.r3, self.r4]
    
    def drawViewport(self, canvas, pos):
        canvas.create_rectangle(0, 0,
                                self.width, self.height,
                                fill = self.roomColor, width = 0) 
        currentRoom = self.roomProperties[self.idx]
        for i in range(len(currentRoom)): 
            canvas.create_text(self.width/2, self.height/4 + 30 * (i + 1), 
                               text = f'{currentRoom[i]["name"]} - {currentRoom[i]["interaction"]}', font = self.font, fill = 'white')
    


class TermProject(ModalApp):
    def appStarted(app):
        
        app.mazeMode = MazeMode()
        app.setActiveMode(app.mazeMode)
        app.timerDelay = 50

app = TermProject(width=800, height=600)