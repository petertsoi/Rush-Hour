#!/usr/bin/python

# Rush Hour
# Peter Tsoi
# UC Berkeley

from sets import Set
from sys import stdout

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
    
    def makeMove(self, move):
        v = self.getVehicle(move[0])
        v.printInfo()
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
                self.position = (start - 1, self.position[1])
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
                self.position = (end + 1, self.position[1])
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
                self.position = (self.position[0], start - 1)
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
                self.position = (self.position[0], end + 1)
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

def main():
    g = Grid(6, 6, 3)
    truckA = Vehicle('A', 4, (1,2), "down", g)
    carB = Vehicle('B', 3, (4, 3), "down", g)
    carC = Vehicle('C', 2, (5, 1), "down", g)
    carD = Vehicle('D', 2, (4, 6), "left", g)
    special = Vehicle('S', 2, (2, 3), "right", g)
    g.printGrid()

if __name__ == "__main__":
    main()