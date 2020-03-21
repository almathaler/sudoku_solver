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
Boards = []  # all boards read in
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

def loadBoards(argv = None):
    global Boards
    if not argv:
        argv = sys.argv
    with open(argv[1], 'r') as f_in:
        lines = f_in.read().split('\n')
        i = 0
        while i<len(lines):
            if (len(lines[i].split(',')) == 3): #so that's the name of our board
                newboard = []
                for j in range(i+1, i+10):
                    buffer = lines[j].split(',')
                    for num in range(9):
                        try:
                            newboard.append(int(buffer[num]))
                        except: #aka if the position is a '_'
                            newboard.append(0)
                Boards.append(newboard)
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

def fill_output(outname, board):
    with open(outname, 'w') as f_out:
        for row in range(9):
            arow = []
            for col in range(9):
                arow.append(str(board[9*row+col])) #like, at first row == 0. so first append(b[9*0+0]), then append(b[9*0+1]) etc
            f_out.write(','.join(arow)) #print row by row
        f_out.write('\n') #print blank space

def main(argv = None):
    #note args like this: arg[0]:program arg[1]:input arg[2]:output arg[3]:name of board to solve

    #SETTING UP BOARD WE'RE GONNA SOLVE
    global Boards, Neighbors
    if not argv:
        argv = sys.argv
    loadBoards(argv)
    makeNeighbors()
    board = Boards[int(argv[3][1]) - 1]
    #print(Boards[toSolve])

    #Now SOLVE
    myStack = [] #we'll just use append and pop to treat this like a stack
    i = 0
    backtrack = False
    possibilities = []
    while i < len(board):
        #first check if it needs to be switched -- remember if you're gonna backtrack, set the value of board[prev_index] to 0!
        if board[i] == 0:
            #make possibilities, only if you're not backtracking otherwise you already have possibilities
            if not backtrack:
                possibilities = make_p(i, board)
            if len(possibilities) > 1:
                #add to stack BEFORE YOU MAKE ANY ADJUSTMENTS (so that when you backtrack, you don't have to overwrite)
                save = SaveState(i, possibilities[:-1], board[:])
                myStack.append(save)
                #add first possibility
                board[i] = possibilities.pop() #this way the list shortens on its own
                backtrack = False
                i+=1
            else if len(possibilities) == 1: #aka forced
                board[i] = possibilities.pop() #no reason to save, bc can't change this decision
                backtrack = False
                i+=1
            else: #you have nothing to do, back track
                saved = myStack.pop()
                i = saved.index
                possibilities = saved.possibilities
                board = saved.board
                backtrack = True

        #else continue, that is from before
    #hey! finished the board
    fill_output(argv[2], board)
    return 0
main()
'''
--main--
1) start with a loop that begins at position 0.
2) generate a list of all possible vals that can be at that position (if it isn't prefilled, aka if it's null)
    how you generate the list is as follows:
    - have set possibilities. It should = copyOf(allVals) or whatever
    - go through all the neighbor positions. For each position, do if board[position] in possibilities, (remove that value from possibilities)
    - Once that is done you have all your possibilities
3) Now put the first possibility into that position. Push onto the stack an object containing the following:
    - board[:], with this addition
    - position that we changed
    - possibilities (with our choice excluded)
    *** IF THERE WAS ONLY ONE POSSIBILITY, MEANS IT WAS FORCED: DO NOT SAVE THAT STATE ***
4) proceed to the next empty position and generate the possibilities list and continue
NOTE: if there are no possibilities, pop last object off the stack. Set index = index in stack, board = last board, and possibilities to possibilities
5) return the done board once you are on index 80 with only one possibility. AKA if you are on 80 and 'forced', still add to stack
6) return stack.pop, return the board (it's just a list)
'''
