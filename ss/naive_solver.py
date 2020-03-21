#! /usr/bin/python3

import sys
import time
import copy

#for the stack
class SaveState:
    def __init__(self, index, possibilities, board):
        self.index = index
        self.possibilities = possibilities
        self.board = board


#globals
Cliques=[[0,1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16,17],[18,19,20,21,22,23,24,25,26],[27,28,29,30,31,32,33,34,35],[36,37,38,39,40,41,42,43,44],[45,46,47,48,49,50,51,52,53],[54,55,56,57,58,59,60,61,62],[63,64,65,66,67,68,69,70,71],[72,73,74,75,76,77,78,79,80],[0,9,18,27,36,45,54,63,72],[1,10,19,28,37,46,55,64,73],[2,11,20,29,38,47,56,65,74],[3,12,21,30,39,48,57,66,75],[4,13,22,31,40,49,58,67,76],[5,14,23,32,41,50,59,68,77],[6,15,24,33,42,51,60,69,78],[7,16,25,34,43,52,61,70,79],[8,17,26,35,44,53,62,71,80],[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]

Neighbors = {}  # key is cell-id, value is set of neighbors.  Neighbors[2] = set(0,1,3,4,5,6,7,8,11,20,29,38,47,56,65,74,9,10,18,19)
Boards = {}  # all boards read in
allVals = set([1,2,3,4,5,6,7,8,9])

#make Neighbors
def makeNeighbors():
    global Neighbors, Cliques
    for cell in range(81):
        nb = set()
        for clique in Cliques:
            if cell in clique:
                nb.update(clique) #add all the values from that clique, but ofc no repatitions
        nb.discard(cell) #you shouldn't be checking if that cell itself == value of that cell
        Neighbors[cell] = nb #now add this buffer to the dictionary

#to check if my resulting board is actually correct
def getIncorrect(board):
    global Neighbors
    # returns a list of the positions on this board whose values are incorrect
    inc = []
    for pos in range(len(board)):
        val = board[pos] #this is the value of that cell
        for neighbor in Neighbors[pos]:
            if board[neighbor] == val: #if in that cell's neighbors there is a duplicate
                inc.append(pos) #mark this cell as problematic. then when this goes through again, the duplicate will be marked as problematic
                break
    return inc

def loadBoards(argv = None):
    global Boards
    if not argv:
        argv = sys.argv
    with open(argv[1], 'r') as f_in:
        lines = f_in.read().split('\n')
        i = 0
        while i<len(lines):
            if (len(lines[i].split(',')) == 3): #so that's the name of our board
                name = lines[i].split(',') #aka so if it's titled "A1-1, NYTIMES, Easy", that's th name but as a list
                #print("processing " + name[0]);
                newboard = []
                for j in range(i+1, i+10):
                    buffer = lines[j].split(',')
                    for num in range(9):
                        try:
                            newboard.append(int(buffer[num]))
                        except: #aka if the position is a '_'
                            newboard.append(0)
                Boards[name[0]] = newboard
                i+=9
            else:
                i+=1

def make_p(index, board):
    global Neighbors, allVals
    possibilities = list(allVals)
    for pos in Neighbors[index]:
        if board[pos] in possibilities:
            possibilities.remove(board[pos])
    return possibilities

def printBoard(title,b):
    print(title)
    for row in range(9):
        arow = []
        for col in range(9):
            arow.append(str(b[9*row+col])) #like, at first row == 0. so first append(b[9*0+0]), then append(b[9*0+1]) etc
        print(','.join(arow)) #print row by row
    print() #print blank space

def fill_output(argv, board):
    with open(argv[2], 'w') as f_out:
        #f_out.write("for "+argv[3]+'\n')
        for row in range(9):
            arow = []
            for col in range(9):
                arow.append(str(board[9*row+col])) #like, at first row == 0. so first append(b[9*0+0]), then append(b[9*0+1]) etc
            f_out.write(','.join(arow) + '\n') #print row by row


def main(argv = None):
    #note args like this: arg[0]:program arg[1]:input arg[2]:output arg[3]:name of board to solve

    #SETTING UP BOARD WE'RE GONNA SOLVE
    global Boards, Neighbors
    if not argv:
        argv = sys.argv
    loadBoards(argv)
    makeNeighbors()
    board = Boards[argv[3]]
    #print(Boards[toSolve])

    #Now SOLVE
    myStack = [] #we'll just use append and pop to treat this like a stack
    i = 0
    backtrack = False
    numtrials = 0
    numbacks = 0
    possibilities = []
    while i < len(board):
        #first check if it needs to be switched -- remember if you're gonna backtrack, set the value of board[prev_index] to 0!
        if board[i] == 0:
            #print("board[%d] == 0"%i)
            #make possibilities, only if you're not backtracking otherwise you already have possibilities
            if not backtrack:
                possibilities = make_p(i, board)
                #print("for index %d, possibilities:"%i)
                #print(possibilities)
            if len(possibilities) > 1:
                #add to stack BEFORE YOU MAKE ANY ADJUSTMENTS (so that when you backtrack, you don't have to overwrite)
                save = SaveState(i, possibilities[:-1], board[:])
                myStack.append(save)
                #add first possibility
                board[i] = possibilities.pop() #this way the list shortens on its own
                backtrack = False
                i+=1
            elif len(possibilities) == 1: #aka forced
                board[i] = possibilities.pop() #no reason to save, bc can't change this decision
                backtrack = False
                i+=1
            else: #you have nothing to do, back track
                saved = myStack.pop()
                i = saved.index
                possibilities = saved.possibilities
                board = saved.board
                backtrack = True
                numbacks+=1
        else:
            i+=1

        numtrials+=1
    #hey! finished the board
    #checking...
    numwrong = getIncorrect(board)
    if len(numwrong)>0:
        print("did not pass check")
    else:
        print("board is correct!")

    fill_output(argv, board)
    print("numtrials: %d, numbacktracks: %d"%(numtrials, numbacks))
    return 0
main()
