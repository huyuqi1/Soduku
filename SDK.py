import numpy as np
import random
import time

def CreateSudoku():
    '''
    create a random Sudoku which must have an answer
    '''
    arr = np.array(range(1, 10, 1))
    np.random.shuffle(arr)
    n = arr
    offsetArr = [3, 6, 1, 4, 7, 2, 5, 8]
    for offset in offsetArr:
        x = np.zeros(9, dtype = np.int)
        for num in range(9):
            if num+offset <= 8:
                x[num] = arr[num+offset]
            else:
                x[num] = arr[num + offset -9]
        n = np.vstack([n, x])
    return n

def ShowSudoku(n):
    '''
    Formatting Sudoku for output
    :param n: a Sudoku
    '''
    [rows, cols] = n.shape
    for i in range(rows):
        if i % 3 == 0 and i != 0:
            print("                  ---+---+---")
        a = ""
        for j in range(cols):
            if j % 3 == 0:
                a = a + "|"
            a = a + str(n[i, j])
        a = a + "|"
        print("                 "+a)


def BFS(search_queue):
    while(len(search_queue) > 0):
        n = search_queue.popleft()
        row = 0
        column = 0
        while(n[row][column] != 0):
            if row == 8 and column == 8:
                if CheckAnswer(n):
                    return n
                break
            else:
                column, row = moveRowAndColum(column, row)
        sample = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 9):
            if n[row][i] != 0:
                sample.remove(n[row][i])
        for i in sample:
            Sudoku_copy = n.copy()
            Sudoku_copy[row][column] = i
            search_queue.append(Sudoku_copy)
    return []


def DFS(n, row, column):
    if row == 8 and column == 8:
        if CheckAnswer(n):
            return n
        else:
            return []
    while(n[row][column] != 0):
        if row == 8 and column == 8:
            return DFS(n, 8, 8)
        else:
            column, row = moveRowAndColum(column, row)
    sample = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 9):
        if n[row][i] != 0:
            sample.remove(n[row][i])
    for i in sample:
        n[row][column] = i
        column1, row1 = moveRowAndColum(column, row)
        medium = DFS(n, row1, column1)
        if medium != []:
            return n
        else:
            n[row][column] = 0
        # if DFS(n, row1, column1) != []:
        #     return DFS(n, row1, column1)
        # else:
        #     n[row][column] = 0
    return []

def moveRowAndColum(column, row):
    if column < 8:
        column += 1
    elif row < 8 and column == 8:
        row += 1
        column = 0
    return column, row


def CheckAnswer(n):
    sample = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 9):
        if not sample == sorted(n[i]) or not sample == sorted(n.take([i], 1)):
            return False
    for i in range(0, 9, 3):
        a = n.take([i, i + 1, i + 2], 1)
        for q in range(0, 9, 3):
           b = np.hstack((np.hstack((a[q], a[q + 1])), a[q + 2]))
           if not sample == sorted(b):
               return False
    return True

def randomDigging(n, sudoku):
    cavelist = []
    for i in range(0, n):
        while(1):
            a = random.randint(0, 8)
            b = random.randint(0, 8)
            while( (a*10+b) in cavelist):
                a = random.randint(0, 8)
                b = random.randint(0, 8)
            cavelist.append(a*10+b)
            memoryNum = sudoku[a][b]
            sudoku[a][b] = 0
            sudokuCopy = sudoku.copy()
            if DFS(sudokuCopy,0,0) != []:
                break
            else:
                sudoku[a][b] = memoryNum
    return sudoku

if __name__ == '__main__':
    # sys.setrecursionlimit(1000000)
    # dfs_result = dfs.DFS()
    # dfs_result.get_solution()
    # n = Sudoku()
    # n = randomDigging(20, n)
    # print("\n")
    # print("\n")
    # print("\n")
    # ShowSudoku(n)
    # print("\n")
    # print("\n")
    # print("\n")
    # print("\n")
    # print("answer:")
    # # # search_queue = deque()
    # # # search_queue.append(n)
    # # # n = BFS(search_queue)
    # # # ShowSudoku(n)
    # # test1.get_solution(n)
    # f = csv.reader(open('sudoku.csv', 'r'))
    # data1 = []
    # num = 0
    # for line in f:
    #     if num > 90:
    #         break
    #     if num <= 60:
    #         num += 1
    #         continue
    #     data1.append(line[0])
    #     num += 1
    # for data in data1:
    #     start_time = time.time()
    #     Sudoku = []
    #     solved = []
    #     for i in range(81):
    #         if data[i]!='0':
    #             Sudoku.append(ord(data[i]) - ord('1'))
    #         else:
    #             Sudoku.append(-1)
    #     print(Sudoku)
    #     ss = test.SudokuSolver(Sudoku)
    #     end_time = time.time()
    #     for i in range(len(ss.answer)):
    #         solved.append(chr(ss.answer[i] + ord('1')))
    #     data = [ss.answer, round(end_time - start_time, 5)]
    #     csv1.writ_data(data,"test4.csv")
    #     print(solved)
    #     print("cycles:" + str(ss.cycle_number))
    # result = cons.Constraint()
    # result.get_solution()
    print("*************************************************\n")
    print("*               Sudoku Puzzles                  *\n")
    print("*************************************************\n")
    # print("*Please enter your options:                   *\n")
    # print("*1.Create standard Sudoku                     *\n")
    # print("*2.Solving a sudoku by Backtracking algorithm *\n")
    # print("*3.Solving a sudoku by Constraint Programming *\n")
    # print("*4.Solving a sudoku by Dancing Links algorithm*\n")
    # # print("*1.Easy standard sudoku                       *\n")
    # # print("*2.Difficult standard sudoku                  *\n")
    # print("***********************************************\n")
    # sys.setrecursionlimit(1000000)
    # dfs_result = dfs.DFS()
    # dfs_result.get_solution()
    n = CreateSudoku()
    n = randomDigging(50, n)
    # ShowSudoku(n)
    start_time = time.time()
    n = DFS(n, 0, 0)
    end_time = time.time()
    ShowSudoku(n)
    print("*             used time:"+str(round(end_time - start_time, 5))+"ms               *\n")
    print("*************************************************\n")
    # print("*Please enter your options:                     *\n")
    # print("*1.Solving the sudoku by Backtracking algorithm *\n")
    # print("*2.Solving the sudoku by Constraint Programming *\n")
    # print("*3.Solving the sudoku by Dancing Links algorithm*\n")
    # print("*************************************************\n")