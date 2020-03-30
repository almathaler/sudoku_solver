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

#possibilities of each index
def make_p(index, board):
    global Neighbors, allVals
    possibilities = list(allVals)
    for pos in Neighbors[index]:
        if board[pos] in possibilities:
            possibilities.remove(board[pos])
    return possibilities

#make the whole possibilities dict
def make_poss(possibilities, board):
    for i in range(81):
        if board[i] == 0:
            possibilities[i] = make_p(i, board)
        else:
            possibilities[i] = []
    return possibilities

def update_poss(possibilities, index, value):
    #print("in update poss, index: %d, value: %d"%(index, value))
    global Neighbors
    dummy = 0
    for neighbor in Neighbors[index]:
        if value in possibilities[neighbor]:
            possibilities[neighbor].remove(value)
            #means that updating that position doesn't affect others' possibilities
    return possibilities

#returns a list of 0-80, sorted by lowest possibilities first
#you should re-make the list like every 10 additions or so and also save this in savestate

#yea.. feeling lazy. don't want to write a compare_to
def order_poss(possibilities):
    ordered = []
    for i in range(81):
        if len(possibilities[i]) != 0:
            to_add = []
            to_add.append(i)
            to_add.extend(possibilities[i])
            ordered.append(to_add)
    ordered = sorted(ordered, key=len)
    for k in range(len(ordered)):
        ordered[k] = ordered[k][0]
    return ordered

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

def forced(board, possibilities):
    #create possibilities
    print(possibilities)
    #boolean still_forced = true, false once loop starts, becomes true when len(p) of one of the neighbors is ever 1.
    #if false at end of loop, stop and you're done w this function
    #go thru possibilities. If len(p) == 1, modify board and update possibilities of all neighbors (use subtraction)
    #keep going until still_forced is false. then you're done with this
    still_forced = True
    while (still_forced):
        still_forced = False
        for index in range(81):
            if len(possibilities[index])==1:
                #means that's forced!
                value = possibilities[index][0]
                possibilities[index] = []
                print("found forced! pos: %d, value: %d"%(index, value))
                board[index] = value
                update_poss(possibilities, index, value)
                still_forced = True #yea... it'll go thru one more time to see if there are any forced

    #no more forceds... finish
    return board, possibilities

def induced(board, possibilities):
    #in each clique, go to each position
    #while the length of that position's possibilities (s1) is > 0:
    #go through each of the other position's possibilities in that clique and do s1-set(possibilities[position])
    #you might end up with len(s1) == 0 or == 1 (if it's > 1, that's an error)
    #if len(s1) == 1, that means that's an 'induced' position and you should put that down on the board
    #and ofc update all the other possibilities. I'm not sure how many times this should go but we can have a boolean
    #that's again only set to True once len(s1) == 1 for one case. so the loop will run once for no reason to check if it
    #should still go on
    global Cliques
    print("in induced, possibilities:")
    print(possibilities)
    induced = True
    while (induced):
        induced = False
        for clique in Cliques: #boxes, cols, rows
            for i in clique: #top left, top right etc
                s1 = set(possibilities[i])
                #print("for position: %d, s1: "%i)
                print(s1)
                if len(s1) != 0: #(no danger of it == 1, cuz that was covered by forced)
                    #cuz if it equals zero, then don't touch it -- it was set by forced
                    for other in clique:
                        if other != i:
                            #cuz we want possibilities of everythng that isn't i
                            s1 = s1.difference(set(possibilities[other])) #get rid of everything that the other blocks can be
                print("after modification, s1:")
                print(s1)
                if len(s1) == 1:
                    induced = True #continue, you'll have one round j to check
                    #that means it is forced induced
                    value = list(s1) #here value is a list -- be aware of that
                    possibilities[i] = [] #remember -- index is which clique in Cliques, i is which pos in a clique
                    #print("found induced forced! pos: %d, value: %d"%(i, value[0]))
                    board[i] = value[0]
                    update_poss(possibilities, i, value[0])

    return board, possibilities

def naive(board, possibilities):
    myStack = []
    print("in naive")
    print(possibilities)
    print("least to highest:")
    ordered = order_poss(possibilities)
    print(ordered)

    return board


def main(argv = None):
    #note args like this: arg[0]:program arg[1]:input arg[2]:output arg[3]:name of board to solve
    start_time = time.time()
    #SETTING UP BOARD WE'RE GONNA SOLVE
    global Boards, Neighbors
    if not argv:
        argv = sys.argv
    loadBoards(argv)
    makeNeighbors()
    board = Boards[argv[3]]
    #print(Boards[toSolve])

    #possibilities is a mini-global; just need it for forced and induced to share. It's set up in forced
    #possibilities is a dictionary of each index and its possibilities, created before modification
    possibilities = {}
    possibilities = make_poss(possibilities, board)
    '''
    #sad these procedures ADD TIME TO MY THING!!!!
    board, possibilities = forced(board, possibilities)
    printBoard("after forced:", board)
    board, possibilities = induced(board, possibilities)
    printBoard("after induced:", board)
    '''
    #Now SOLVE
    board = naive(board, possibilities)
    printBoard("from naive", board)
    ttime = time.time() - start_time
    print("time elapsed: %f"%ttime)
    fill_output(argv, board)
    return 0


main()
