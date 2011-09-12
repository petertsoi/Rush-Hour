#!/usr/bin/python

# Rush Hour
# Peter Tsoi
# UC Berkeley

from sets import Set
from sets import ImmutableSet
from sys import stdout
from sys import argv
import heapq

class PriorityQueue:
  def  __init__(self):  
    self.heap = []
    
  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      return item
  
  def isEmpty(self):
    return len(self.heap) == 0

class Grid:
    def __init__(self, width, height, exitRow):
        self.width = width
        self.height = height
        self.exitRow = exitRow
        self.traffic = Set()
        self.special = None
        self.occupied = Set()

    # Adds a vehicle to the grid. Flags special car.
    def addVehicle(self, v):
        self.traffic.add(v)
        if v.id == 'S':
            self.special = v
        self.occupiedSpaces()

    # Returns the vehicle in the space if occupied, None if not occupied
    def vehicleAt(self, position):
        for v in self.traffic:
            if v.position[0] != position[0] and v.position[1] != position[1]:
                continue
            else:
                if position in v.occupiedSpaces():
                    return v
        return None
    
    def getVehicle(self, id):
        for v in self.traffic:
            if v.id == id:
                return v
        return None

    # Set of all occupied spaces in the grid
    def occupiedSpaces(self):
        occupied = Set()
        for v in self.traffic:
            occupied = v.occupiedSpaces() | occupied
        self.occupied = occupied
        return occupied

    # Returns a list of all possible moves
    def allMoves(self):
        moves = []
        for v in self.traffic:
            moves.extend( v.validMoves())
        return moves
    
    def state(self):
        state = []
        for v in self.traffic:
            state.append((v.id, v.position))
        state.sort()
        return state
    
    def loadState(self, state):
        for v in state:
            self.getVehicle(v[0]).position = v[1]
    
    def makeMove(self, move):
        v = self.getVehicle(move[0])
        v.move(move[1], move[2])

    # Prints the grid and the cars in it
    def printGrid(self):
        for r in range(self.width + 1):
            for c in range(self.height + 1):
                if r == 0:
                    if c == 0:
                        stdout.write(" ")
                    else:
                        stdout.write(str(c))
                    stdout.write("  ")
                else:
                    if c != 0:
                        vehicle = self.vehicleAt( (c, r) )
                        if vehicle == None:
                            stdout.write(" ")
                        else:
                            stdout.write(vehicle.id)
                    else:
                        stdout.write(str(r))
                    stdout.write("  ")
            if r == self.exitRow:
                stdout.write(">> exit")
            stdout.write("\n\n")
    
    def isFinished(self):
        if self.special.orientation == "right" and self.special.position[0] + self.special.length - 1 == self.width :
            return True
        elif self.special.orientation == "left" and self.special.position[0] == self.width:
            return True
        else:
            return False

class Vehicle:
    def __init__(self, id, length, position, orientation, grid):
        self.id = id
        self.length = length
        self.position = position
        self.orientation = orientation
        self.grid = grid
        grid.addVehicle(self)
    
    # assumes starting position and move are legal
    def move(self, distance, direction):
        if direction == "up":
            self.position = (self.position[0], self.position[1] - distance)
        elif direction == "down":
            self.position = (self.position[0], self.position[1] + distance)
        elif direction == "left":
            self.position = (self.position[0] - distance, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + distance, self.position[1])
        self.grid.occupiedSpaces()

    def validMoves(self):
        taken = self.grid.occupied - self.occupiedSpaces()
        savedPosition = self.position
        validMoves = []
        if self.orientation == "left" or self.orientation == "right":
            distance = 1
            start = self.position[0] if self.orientation == "right" else self.position[0] - self.length + 1
            while start > 1:
                self.position = (self.position[0] - 1, self.position[1])
                if taken & self.occupiedSpaces() == Set():
                    validMoves.append([self.id, distance, "left"])
                else:
                    distance = 0
                    break
                start -= 1
                distance += 1
            self.position = savedPosition
            end = self.position[0] if self.orientation == "left" else self.position[0] + self.length - 1
            distance = 1
            while end < self.grid.width:
                self.position = (self.position[0] + 1, self.position[1])
                if taken & self.occupiedSpaces() == Set():
                    validMoves.append([self.id, distance, "right"])
                else:
                    distance = 0
                    break
                end += 1
                distance += 1
            self.position = savedPosition
        elif self.orientation == "up" or self.orientation == "down":
            distance = 1
            start = self.position[1] if self.orientation == "down" else self.position[1] - self.length + 1
            while start > 1:
                self.position = (self.position[0], self.position[1] - 1)
                if taken & self.occupiedSpaces() == Set():
                    validMoves.append([self.id, distance, "up"])
                else:
                    distance = 0
                    break
                start -= 1
                distance += 1
            self.position = savedPosition
            end = self.position[1] if self.orientation == "up" else self.position[1] + self.length - 1
            distance = 1
            while end < self.grid.height:
                self.position = (self.position[0], self.position[1] + 1)
                if taken & self.occupiedSpaces() == Set():
                    validMoves.append([self.id, distance, "down"])
                else:
                    distance = 0
                    break
                end += 1
                distance += 1
            self.position = savedPosition
        else:
            raise TypeError('orientation')
        return validMoves

    # returns a set of locations occupied by the vehicle
    def occupiedSpaces(self):
        occupied = Set()
        for i in range(self.length):
            if self.orientation == "up":
                occupied.add( (self.position[0], self.position[1] - i) )
            elif self.orientation == "down":
                occupied.add( (self.position[0], self.position[1] + i) )
            elif self.orientation == "left":
                occupied.add( (self.position[0] - i, self.position[1]) )
            elif self.orientation == "right":
                occupied.add( (self.position[0] + i, self.position[1]) )
        return occupied

    # Debug Info
    def printInfo(self):
        print ("Vehicle " + str(self.id) + "\tSize: 1 x " + str(self.length) + "\tAt: " + str(self.position) + "\tOrientation: " + str(self.orientation))

class Search:
    def __init__(self, grid):
        self.fringe = PriorityQueue()
        self.map = dict()
        self.grid = grid
        self.expandedNodes = 0
    
    def costOfMoves(self, moveList):
        return 10 * len(moveList)

    def aStarSearch(self):
        # Start with initial state
        initialState = self.grid.state()
        self.map[str(initialState)] = []
        for move in self.grid.allMoves():
            g_cost = self.costOfMoves(self.map[str(initialState)]) + 1
            h_cost = self.heuristic(move, initialState)
            self.fringe.push((move, initialState), g_cost + h_cost)

        # The actual algorithm
        if self.grid.isFinished():
            print("Expanded %i positions" % self.expandedNodes)
            return self.map[str(self.grid.state())]
        
        while not self.fringe.isEmpty():
            move = self.fringe.pop()
            self.grid.loadState(move[1])
            self.grid.makeMove(move[0])
            newState = self.grid.state()
            
            # If this state has been visited
            if str(newState) in self.map:
                # If I took a shorter route to here, update it
                #if self.costOfMoves(self.map[str(move[1])]) + 1 < self.costOfMoves(self.map[str(newState)]):
                #    self.map[str(newState)] = self.map[str(move[1])].append(move[0])
                # Then forget about it.
                continue
            else:
                self.expandedNodes += 1
                #print move[0]
                newMoveList = self.map[str(move[1])][:]
                newMoveList.append(move[0])
                self.map[str(newState)] = newMoveList
                
                if self.grid.isFinished():
                    print("Expanded %i positions" % self.expandedNodes)
                    self.grid.loadState(initialState)
                    return self.map[str(newState)]
                
                for move in self.grid.allMoves():
                    g_cost = self.costOfMoves(self.map[str(newState)]) + 1
                    h_cost = self.heuristic(move, newState)
                    self.fringe.push((move, newState), g_cost + h_cost)
        print("Expanded %i positions" % self.expandedNodes)
        print("Exhausted Fringe")
        return[]
    
    def heuristic(self, successor, state):
        # Rank by how many cars in between the special car and exit
        restoreState = self.grid.state()
        self.grid.loadState(state)
        self.grid.makeMove(successor)
        score = 0
        endOfSpecial = self.grid.special.position[0] + self.grid.special.length
        for x in range(endOfSpecial, self.grid.width):
            atLocation = self.grid.vehicleAt((x, self.grid.exitRow))
            if atLocation != None:
                score += 10
                score -= 1 * len(atLocation.validMoves())
        # Break ties by mobility of blocking cars
        if self.grid.isFinished():
            score -= 9999
        self.grid.loadState(restoreState)
        return score
    
    def nullHeuristic(self, successor, state):
        return 0
        
    def printSolution(self, moves):
        initialState = self.grid.state()
        for move in moves:
            print ("Move " + str(move[0]) + " " + str(move[1]) + " space(s) " + move[2])
            self.grid.makeMove(move)
            self.grid.printGrid()
            print "\n"

def loadToGrid(path, grid):
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        args = line.split(' ')
        coords = []
        if ',' in args[2]:
            coords = args[2].split(',')
        coord = (int(coords[0]), int(coords[1]))
        imported = Vehicle(args[0], int(args[1]), coord, args[3].rstrip(), grid)

def writeToFile(path, moves):
    f = open(path, 'w')
    i = 1
    for move in moves:
        f.write(str(i) + " " + str(move[0]) + " " + str(move[1]) + " " + str(move[2]) + "\n")
        i += 1

def main():
    printSolutions = False
    if len(argv) < 3 or (len(argv) != 3 and not (len(argv) == 4 or argv[1] == "-p")):
        print "Usage:\t rushhour.py [-p] inputFile outputFile"
        print "\t -p \t print solution to stdout"
        exit()
    printSolutions = len(argv) > 3 and (argv[1] == "-p" and len(argv) == 4)
    inPath = argv[2] if printSolutions else argv[1]
    outPath = argv[3] if printSolutions else argv[2]
            
    g = Grid(6, 6, 3)
    loadToGrid(inPath, g)
    g.printGrid()
    Solver = Search(g)
    moves = Solver.aStarSearch()
    if moves != []:
        print ("Solved in %i moves" % len(moves))
        if printSolutions:
            Solver.printSolution(moves)
        writeToFile(outPath, moves)
    else:
        print "No Solution Found"

if __name__ == "__main__":
    main()