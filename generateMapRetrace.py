import random
import logging
import curses
import time

class Cell:
    def __init__(self, puzzle, x, y):
        self.puzzle = puzzle
        self.x = x
        self.y = y
        
        self.untested = list(range(1, 10))
        random.shuffle(self.untested)
        self.block = []
        # Find which block cell belongs to
        for i in [x, y]:
            if(i > 5):
                self.block.append(3)
            elif(i > 2):
                self.block.append(2)
            else:
                self.block.append(1)
        self.value = 0

    # Attempts to find a valid untested number
        # if none is found return false
    def findNewValue(self):
        for integer in self.untested:
            if( 
                alreadyInRow(self.puzzle, self, integer) or
                alreadyInColumn(self.puzzle, self, integer) or
                alreadyInBlock(self.puzzle, self, integer)
            ):
                pass
            else:
                self.value = integer
                self.untested.remove(integer)
                logging.info(("New value {0} for cell {1},{2}").format
                        (self.value, self.x, self.y))
                return True
        logging.debug("Failed to find new value for cell")
        self.resetUntested()
        self.value = 0
        return False

    def resetUntested(self):
        self.untested = list(range(1, 10))
        random.shuffle(self.untested)

def getPuzzle(stdscr, puzzle):
    output = puzzleASCII(puzzle)
    stdscr.addstr(0, 0, output)
    stdscr.refresh()

def puzzleASCII(puzzle):
    output = ""
    output += "Puzzle:\n\n"
    for row in puzzle:
        output += "-"*9*3 + '\n'
        for cell in row:
            output += str(cell.value) + '||'
        output += "\n"
    return output



def alreadyInRow(puzzle, cell, integer):
    for otherCell in puzzle[cell.y]:
        if otherCell.value == integer:
            return True
    return False

def alreadyInColumn(puzzle, cell, integer):
    for y in range(9):
        if(integer == puzzle[y][cell.x].value):
            return True
    return False


def alreadyInBlock(puzzle, cell, integer):
    for row in puzzle:
        for otherCell in row:
            if otherCell.block == cell.block and otherCell.value == integer:
                return True
    return False


def genPuzzle(stdscr):
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    puzzle = []
    for y in range(9):
        puzzle.append([])
        for x in range(9):
            puzzle[y].append(Cell(puzzle, x, y))
    current = [0, 0]

    while True:
        getPuzzle(stdscr, puzzle)
        if current[1] > 8:
            break
        cell = puzzle[current[1]][current[0]]

        # Reset the cell and move current to previous cell
        if not cell.findNewValue():
            # If touching left
            if current[0] == 0:
                current[1] -= 1
                current[0] = 8
            else:
                current[0] -= 1

        # Move to the next cell
        else:
            if current[0] == 8:
                current[0] = 0
                current[1] += 1
            else:
                current[0] += 1

        time.sleep(0.1)
    logging.debug(puzzleASCII(puzzle))
    return puzzle

puzzle = curses.wrapper(genPuzzle)
print(puzzleASCII(puzzle))

