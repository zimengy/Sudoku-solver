from collections import deque
import copy


def readSudoku(fileName): # read the Sudoku and convert it to elements in list
    rawpuzzle = []
    puzzle = {}
    queue = deque()
    sudokuFile = open(fileName,"r");
    for line in sudokuFile.readlines():
        rawpuzzle.append(list(line[0:9]))
    sudokuFile.close()
    for i in range(0,9):
        for j in range(0,9):
            if rawpuzzle[i][j]!='*':
                puzzle[(i,j)] = [(ord(rawpuzzle[i][j])-ord('0'))]
            else:
                puzzle[(i,j)] = [1,2,3,4,5,6,7,8,9]
                queue.append((i,j))
    return (puzzle, queue)

def checkResult(puzzle): # check the result
    for ele in puzzle:
        if (len(puzzle[ele])>1):
            return 2
        elif (len(puzzle[ele]) == 0):
            return 0
    return 1
    
def printOrigSudoku(puzzle): # print the puzzle line by line
    for i in range(0,9):
        row = ''
        for j in range(0,9):
            if(len(puzzle[i,j])==1):
                row = row + str(puzzle[i,j][0])
            else:
                row = row + '*'
        print row                            
    
def removeInconsistentValues(i,j,puzzle):
    removed = False
    for jj in range(0,9):
        if(jj!=j):
            if(len(puzzle[i,jj])==1):
                if(puzzle[i,jj][0] in puzzle[i,j]):
                    puzzle[i,j].remove(puzzle[i,jj][0])
                    removed = True
    for ii in range(0,9):
        if(ii!=i):
            if(len(puzzle[ii,j])==1):
                if(puzzle[ii,j][0] in puzzle[i,j]):
                    puzzle[i,j].remove(puzzle[ii,j][0])
                    removed = True
    if(i%3 == 0 and j%3 == 0): #1
        a1 = i+1; b1 = j+1
        a2 = i+1; b2 = j+2
        a3 = i+2; b3 = j+1
        a4 = i+2; b4 = j+2
    elif(i%3 == 0 and j%3 == 1): #2
        a1 = i+1; b1 = j-1
        a2 = i+1; b2 = j+1
        a3 = i+2; b3 = j-1
        a4 = i+2; b4 = j+1
    elif(i%3 == 0 and j%3 == 2): #3
        a1 = i+1; b1 = j-1
        a2 = i+1; b2 = j-2
        a3 = i+2; b3 = j-1
        a4 = i+2; b4 = j-2
    elif(i%3 == 1 and j%3 == 0): #4
        a1 = i-1; b1 = j+1
        a2 = i-1; b2 = j+2
        a3 = i+1; b3 = j+1
        a4 = i+1; b4 = j+2
    elif(i%3 == 1 and j%3 == 1): #5
        a1 = i-1; b1 = j-1
        a2 = i-1; b2 = j+1
        a3 = i+1; b3 = j-1
        a4 = i+1; b4 = j+1
    elif(i%3 == 1 and j%3 == 2): #6
        a1 = i-1; b1 = j-1
        a2 = i-1; b2 = j-1
        a3 = i+1; b3 = j-2
        a4 = i+1; b4 = j-2
    elif(i%3 == 2 and j%3 == 0): #7
        a1 = i-1; b1 = j+1
        a2 = i-1; b2 = j+2
        a3 = i-2; b3 = j+1
        a4 = i-2; b4 = j+2
    elif(i%3 == 2 and j%3 == 1): #8
        a1 = i-1; b1 = j-1
        a2 = i-1; b2 = j+1
        a3 = i-2; b3 = j-1
        a4 = i-2; b4 = j+1
    elif(i%3 == 2 and j%3 == 2): #9
        a1 = i-1; b1 = j-1
        a2 = i-1; b2 = j-2
        a3 = i-2; b3 = j-1
        a4 = i-2; b4 = j-2                            
    if(len(puzzle[a1,b1])==1):
        if(puzzle[a1,b1][0] in puzzle[i,j]):
            puzzle[i,j].remove(puzzle[a1,b1][0])
            removed = True
    if(len(puzzle[a2,b2])==1):
        if(puzzle[a2,b2][0] in puzzle[i,j]):
            puzzle[i,j].remove(puzzle[a2,b2][0])
            removed = True
    if(len(puzzle[a3,b3])==1):
        if(puzzle[a3,b3][0] in puzzle[i,j]):
            puzzle[i,j].remove(puzzle[a3,b3][0])
            removed = True
    if(len(puzzle[a4,b4])==1):
        if(puzzle[a4,b4][0] in puzzle[i,j]):
            puzzle[i,j].remove(puzzle[a4,b4][0])
            removed = True    
    return removed

def AC3(puzzlenew, queue):
    puzzle = copy.deepcopy(puzzlenew)
    
    while(len(queue)!=0):
        #print puzzlenew
        (i,j) = queue.popleft()
        if removeInconsistentValues(i,j,puzzle):
            for jj in range(0,9):
                if(jj!=j and queue.count((i,jj))==0):
                    queue.append((i,jj))
            for ii in range(0,9):
                if(ii!=i and queue.count((ii,j))==0):
                    queue.append((ii,j))
            for ii in range(i-i%3, (i/3+1)*3):
                for jj in range(j-j%3, (j/3+1)*3):
                    if(ii!=i and jj!=j and queue.count((ii,jj))==0):
                        queue.append((ii,jj))
    return puzzle

def otherConstraints(puzzle):
    flag = 0
    newpuzzle = copy.deepcopy(puzzle)
    # row
    for i in range(0,9):
        flag_row = 0
        for j in range(0,9):
            if (len(newpuzzle[i,j])>1):
                for ele in newpuzzle[i,j]:
                    for jj in range(0,9):
                        if(jj!=j):
                            if(ele in newpuzzle[i,jj]):
                                flag_row = 1
                    if(flag_row == 0):
                        newpuzzle[i,j] = [ele]
                        flag = 1
                        flag_row = 0
                        continue
                    else:
                        flag_row = 0
    queue = deque()
    for el in newpuzzle:
        if (len(newpuzzle[el])>1): queue.append(el);#print queue
    newpuzzle = AC3(newpuzzle, queue)

    # col
    for j in range(0,9):
        flag_col = 0
        for i in range(0,9):
            if (len(newpuzzle[i,j])>1):
                for ele in newpuzzle[i,j]:
                    for ii in range(0,9):
                        if(ii!=i):
                            if(ele in newpuzzle[ii,j]):
                                flag_col = 1
                    if(flag_col == 0):
                        newpuzzle[i,j] = [ele]
                        flag = 1
                        flag_col = 0
                        continue
                    else:
                        flag_col = 0
    queue = deque()
    for el in newpuzzle:
        if (len(newpuzzle[el])>1): queue.append(el);#print queue
    newpuzzle = AC3(newpuzzle, queue)

    # block
    for blockIdx in range(0,9):
        flag_block = 0
        for i in range(0,3):
            for j in range(0,3):
                block_i = blockIdx/3;
                block_j = blockIdx%3;
                
                if (len(newpuzzle[block_i*3+i, block_j*3+j])>1):
                    for ele in newpuzzle[block_i*3+i, block_j*3+j]:
                        for ii in range(0,3):
                            for jj in range(0,3):
                                if((i,j)!=(ii,jj)):
                                    if(ele in newpuzzle[block_i*3+ii, block_j*3+jj]):
                                        flag_block = 1
                        if(flag_block == 0):
                            newpuzzle[block_i*3+i, block_j*3+j] = [ele]
                            flag = 1
                            flag_block = 0
                            continue
                        else:
                            flag_block = 0
    queue = deque()
    for el in newpuzzle:
        if (len(newpuzzle[el])>1): queue.append(el);#print queue
    newpuzzle = AC3(newpuzzle, queue)
  
    return (newpuzzle, flag)
                    
                    
    
def mainConstraints(puzzle):
    newpuzzle = copy.deepcopy(puzzle)
    
    (newpuzzle,flag) = otherConstraints(newpuzzle)
    while(flag==1):
        (newpuzzle,flag) = otherConstraints(newpuzzle)
    return newpuzzle


def recursiveAC3(puzzle): 
    for ele in puzzle: 
        if (len(puzzle[ele])>1):  
            for i in puzzle[ele]:
                #print puzzle
                #print puzzle
                #print ele
                #print i
                newpuzzle = puzzle.copy()
                newpuzzle[ele] = [i]
                                
                queue = deque()
                for el in newpuzzle:
                    if (len(newpuzzle[el])>1): queue.append(el);#print queue
                
                result = AC3(newpuzzle, queue)
                                
                if(checkResult(result) == 1): return result
                elif(checkResult(result) == 0): continue
                else:                    
                    result2 =  recursiveAC3(result)
                    if(result2 == None): continue
                    else: return result2
            return None
    return None

    
def solveSudoku(puzzle, queue):
    solvedSudoku = AC3(puzzle, queue)
    if(checkResult(solvedSudoku) == 0):
        print "No solution!"
    elif(checkResult(solvedSudoku) == 1):
        print "The Sudoku being solved!"
        printOrigSudoku(solvedSudoku)
    else:
        finalSolution = mainConstraints(solvedSudoku)
        if(checkResult(finalSolution)==0):
            print "No solution!"
        elif(checkResult(finalSolution)==1):
            print "The Sudoku being solved!"
            printOrigSudoku(finalSolution)
        else:
            guessSolution = recursiveAC3(finalSolution)
            if(guessSolution==None):
                print "No solution!"
            else:
                print "The Sudoku being solved!"
                printOrigSudoku(guessSolution)
    return    
    
if __name__ == '__main__':
    # solve ac3solvable_example
    fileName1 = "ac3solvable_example"
    puzzle1, queue1 = readSudoku(fileName1)
    print "1. ac3solvable_example:"
    solvedSudoku1 = solveSudoku(puzzle1, queue1)

    print "------------------------------------------------------------"
    # solve dp_puzzle
    fileName2 = "dp_puzzle"
    puzzle2, queue2 = readSudoku(fileName2)
    print "2. dp_puzzle:"
    solvedSudoku2 = solveSudoku(puzzle2, queue2)
    
    print "------------------------------------------------------------"     
    # solve gentle_sudoku
    fileName3 = "gentle_sudoku"
    puzzle3, queue3 = readSudoku(fileName3)
    print "3. gentle_sudoku:"
    solvedSudoku3 = solveSudoku(puzzle3, queue3)

    print "------------------------------------------------------------"     
    # solve moderate_sudoku
    fileName4 = "moderate_sudoku"
    puzzle4, queue4 = readSudoku(fileName4)
    print "4. moderate_sudoku:"
    solvedSudoku4 = solveSudoku(puzzle4, queue4)

    print "------------------------------------------------------------"     
    # solve guessing_puzzle
    fileName5 = "guessing_puzzle"
    puzzle5, queue5 = readSudoku(fileName5)
    print "5. guessing_puzzle:"
    solvedSudoku5 = solveSudoku(puzzle5, queue5)
    

    print "------------------------------------------------------------"     
    # solve diabolical_sudoku
    fileName6 = "diabolical_sudoku"
    puzzle6, queue6 = readSudoku(fileName6)
    print "6. diabolical_sudoku:"
    solvedSudoku6 = solveSudoku(puzzle6, queue6)   

    

        
    
    
     
    
    

    
