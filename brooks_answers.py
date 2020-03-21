#! /usr/bin/python3

import sys

Cliques=[[0,1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16,17],[18,19,20,21,22,23,24,25,26],[27,28,29,30,31,32,33,34,35],[36,37,38,39,40,41,42,43,44],[45,46,47,48,49,50,51,52,53],[54,55,56,57,58,59,60,61,62],[63,64,65,66,67,68,69,70,71],[72,73,74,75,76,77,78,79,80],[0,9,18,27,36,45,54,63,72],[1,10,19,28,37,46,55,64,73],[2,11,20,29,38,47,56,65,74],[3,12,21,30,39,48,57,66,75],[4,13,22,31,40,49,58,67,76],[5,14,23,32,41,50,59,68,77],[6,15,24,33,42,51,60,69,78],[7,16,25,34,43,52,61,70,79],[8,17,26,35,44,53,62,71,80],[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]

Neighbors = {}  # key is cell-id, value is set of neighbors.  Neighbors[2] = set(0,1,3,4,5,6,7,8,11,20,29,38,47,56,65,74,9,10,18,19)
Boards = []  # all boards read in


def getBoards(argv = None):
    global Boards

    if not argv:
        argv = sys.argv
    with open(argv[1],'r') as f_in:
        lines = f_in.read().split('\n')
        i = 0
        while i < len(lines):
            if len(lines[i].split(',')) == 3: #if this is the name of a board
                newboard = [] #make a newboard
                for j in range(i+1,i+10): #fill in the new board with the next 9 lines
                    newboard += [int(x) for x in lines[j].split(',')]
                Boards.append(newboard) #so now we have a list of all boards
                i += 9 #move past this board
            else:
                i += 1 #this is when you're just on an empty line like "\n"


def makeNeighbors():
    global Neighbors
    for cell in range(81):
        nb = set()
        for clique in Cliques:
            if cell in clique:
                nb.update(clique) #add all the values from that clique, but ofc no repatitions
        nb.discard(cell) #you shouldn't be checking if that cell itself == value of that cell
        Neighbors[cell] = nb #now add this buffer to the dictionary

def getSwapped(board):
    # returns the pair of positions that must be swapped to make this board a correct solution
    # get the positions that have incorrect values
    incorrect = getIncorrect(board)

    # now try all pairs of swaps
    #ok say incorrect is like this: [a, b, c, d, e, f]
    for ileft in range(len(incorrect)-1): #aka [a, b, c, d, e]. for a go thru b, c, d, e, f then for b go through b, c, d, e, f...? Guess there are reps
        for iright in range(ileft+1,len(incorrect)): #aka [b, c, d, e, f]
            left = incorrect[ileft]
            right = incorrect[iright]
            swapped_board = board[:]
            # try swapping these two positions
            swapped_board[left],swapped_board[right] = swapped_board[right],swapped_board[left]
            # see if the board is now correct
            if len(getIncorrect(swapped_board)) == 0:
                return [left,right]

    return []

def getIncorrect(board):
    # returns a list of the positions on this board whose values are incorrect
    inc = []
    for pos in range(len(board)):
        val = board[pos] #this is the value of that cell
        for neighbor in Neighbors[pos]:
            if board[neighbor] == val: #if in that cell's neighbors there is a duplicate
                inc.append(pos) #mark this cell as problematic. then when this goes through again, the duplicate will be marked as problematic
                break
    return inc

def printBoard(title,b):
    print(title)
    for row in range(9):
        arow = []
        for col in range(9):
            arow.append(str(b[9*row+col])) #like, at first row == 0. so first append(b[9*0+0]), then append(b[9*0+1]) etc
        print(','.join(arow)) #print row by row
    print() #print blank space


def main(argv = None):
    global Boards, Neighbors
    if not argv: argv = sys.argv
    Boards = []
    Neighbors = {}
    getBoards(argv)
    makeNeighbors()
    with open(argv[2],'w') as f_out:
        for board in Boards:
            swapped = getSwapped(board)
            s_swapped = [str(x) for x in swapped] #b/c getSwapped returns a list
            out = ','.join(s_swapped) #join that list w comma
            f_out.write(out+'\n') #since out is a string we can write it to the file
            print(out)

main()
