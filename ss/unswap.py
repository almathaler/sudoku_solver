#! /usr/bin/python3

import sys

board = []

#opens file, fills out board, calls check board,
#sorts through wrongs so that it tries swapping a0 and b0, then a0 and b1, then a1 and b0, finally a1 and b1
#whichever one works will be written out to the file

#so far there needs to just be the board in the file!!!!!
def doIt(alist = None):
    if alist == None:
        alist = sys.argv

    #open the file
    fp = open(alist[1], 'r')
    string_buffer = fp.read()
    fp.close()
    fp = open(alist[2], 'w+')
    #now fill out the board, but first remove the words
    string_buffer = ','.join(string_buffer.split()) #make it one continuous list
    list_buffer = string_buffer.split(',')
    i = 0
    while i < len(list_buffer):
        if (list_buffer[i].isdigit()):
            i+=1
        else:
            list_buffer.remove(list_buffer[i])
    #okay removed words


    #LAST STEP -- BREAK UP BOARD INTO HOW MANY PARTS IT IS
    length = len(list_buffer)
    for i in range(length//81):

        board = list_buffer[81*i:81*(i+1)]

        wrongs = []
        swapped = []
        check_board(board, wrongs)
        #WHAT YOU HAVE TO DO HERE IS
        #BEFORE WE WEREN'T CATCHING ALL CASES THAT WE COULD SWAP -- WE WERE LIMITING AT 4
        #INSTEAD WE SHOULD TRY ALL COMBINATIONS OF SWAPS, LIST IS (A,B,C,D,E,F,G), TRY SWITHCING A WITH ALL, B WITH ALL,
        #C WITH ALL ETC

        #where the final 2 swaps will go
        swapped = []
        dummy_wrongs = [] #so that when we check again, won't affect original wrongs
        if len(wrongs) > 0: #we r guaranteed 4 wrongs in this case that we just swap two
            index_wrongs = 0
            while index_wrongs < len(wrongs):
                #try swapping each index with all those that come after it (to avoid redundancy)
                #check board, if dummy_wrongs length > 0, unswap
                #but if it isn't greater than 0, set swapped = to the two variables we swapped
                #and break out of the loop
                for index_board in wrongs[index_wrongs+1:]:
                    swap(board, wrongs[index_wrongs], index_board)
                    check_board(board, dummy_wrongs)
                    if len(dummy_wrongs) > 0:
                        swap(board, wrongs[index_wrongs], index_board) #undo what you just did
                        dummy_wrongs = []
                        #index_wrongs+=1
                    else:
                        swapped.append(index_board)
                        swapped.append(wrongs[index_wrongs])
                        break
                if len(swapped) > 0:
                    break
                else:
                    index_wrongs+=1
            if len(swapped) == 0:
                print("Unfortunately, couldn't solve")


        #ok so at this point, you should have a working swap
        #and the list "swapped" should have the 2 positions you swapped, or be [0] if no swapped

        swapped.sort()
        toAdd = str(swapped[0]) + "," + str(swapped[1]) + "\n"
        fp.write(toAdd)
    fp.close()
    return 0


#takes in a board, does rows+cols+boxes check, and if it finds numbers that overlap it adds them to wrongs list
#make sure not to add duplicates to wrongs
def check_board(board, wrongs):
    #rows
    print("\n")
    print("in rows")
    row_starts = [k*9 for k in range(9)] #[0, 9, 18...]
    for i in row_starts:
        #check if there is a duplicate, and also make a small row
        buffer_board = board[i:i+9]
        buffer_set = set(buffer_board)
        if len(buffer_set) < 9:
            #means we have a duplicate
            #count triggers end of while
            count = 0
            #x will hold value of the duplicate
            x = 0
            while count<2:
                x = int(x)
                x+=1
                x = str(x)
                count = buffer_board.count(x)
                if count == 2:
                    break
            #ok now we got the duplicate so
            #get their positions in this list
            first_instance = buffer_board.index(x)
            second_instance = buffer_board[first_instance+1:].index(x) + (1+first_instance)
            first_instance+=i
            second_instance+=i
            #and add those positions to wrongs if they aren't already there
            if not(first_instance in wrongs):
                wrongs.append(first_instance)
            if not (second_instance in wrongs):
                wrongs.append(second_instance)

    #cols
    print("\n")
    print("in cols")
    col_starts = [k for k in range(9)] #[0, 1, 2...]
    for i in col_starts:
        #check if there is a duplicate, and also make a small col\
        #you build columns differently, you
        #add the positions (0*9)+i, (1*9)+i etc
        buffer_col = []
        for x in range(9):
            buffer_col+=board[i+x*9]
        #
        buffer_set = set(buffer_col)
        if len(buffer_set) < 9:
            #means we have a duplicate
            #count triggers end of while
            count = 0
            #x will hold value of the duplicate
            x = 0
            while count<2:
                x = int(x)
                x+=1
                x = str(x)
                count = buffer_col.count(x)
                if count == 2:
                    break

            #ok now we got the duplicate so
            #get their positions in this list
            first_instance = buffer_col.index(x)
            second_instance = buffer_col[first_instance+1:].index(x) + (1+first_instance)
            #and add those positions to wrongs if they aren't already there
            #adjust first and second back to their original positions on the board
            first_instance = first_instance*9 + i
            second_instance = second_instance*9 + i
            if not(first_instance in wrongs):
                wrongs.append(first_instance)
            if not (second_instance in wrongs):
                wrongs.append(second_instance)

    #boxes
    print("\n")
    print("in boxes")
    box_starts = [0, 3, 6, 27, 30, 33, 54, 57, 60]
    for i in box_starts:
        #check if there is a duplicate, and also make a small col\
        #you build boxes differntly, you
        #do i, i+1, i+2, i+9, i+10, i+11, i+18, i+19, i+20
        #keep your positions!
        buffer_box = []
        #i think before i was adding imaginary numbers to the list, no good
        buffer_box_positions = [i, i+1, i+2, i+9, i+10, i+11, i+18, i+19, i+20]
        #now populate the box
        for k in buffer_box_positions:
            buffer_box += board[k]
        buffer_set = set(buffer_box)
        if len(buffer_set) < 9:
            #means we have a duplicate
            #count triggers end of while
            count = 0
            #x will hold value of the duplicate
            x = 0
            while count<2:
                x = int(x)
                x+=1
                x = str(x)
                count = buffer_box.count(x)
                if count == 2:
                    break

            #ok now we got the duplicate so
            #get their positions in this list (index in buffer_box)

            #for some reason we are subtracting 10 from the second instance?
            first_instance = buffer_box.index(x)
            second_instance = buffer_box[first_instance+1:].index(x) + (1+first_instance)
            #and add those positions to wrongs if they aren't already there
            #adjust first and second back to their original positions on the board
            first_instance = buffer_box_positions[first_instance]
            second_instance = buffer_box_positions[second_instance]
            if not(first_instance in wrongs):
                wrongs.append(first_instance)
            if not (second_instance in wrongs):
                wrongs.append(second_instance)
            

    return 0





#swaps two numbers in the board
def swap(board, pos1, pos2):
    dummy_var = board[pos1]
    board[pos1] = board[pos2]
    board[pos2] = dummy_var
    return 0



doIt()
