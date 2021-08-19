import Sudoku.csv_tool as csv
import numpy as np
import time

def Sudoku():
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
            print(" ---+---+---")
        a = ""
        for j in range(cols):
            if j % 3 == 0:
                a = a + "|"
            a = a + str(n[i, j])
        a = a + "|"
        print(a)


def DFS(n, row, column,isHyper):
    print(n)
    if row == 8 and column == 8:
        if CheckAnswer(n,isHyper):
            return n
        else:
            return []
    while(n[row][column] != 0):
        if row == 8 and column == 8:
            return DFS(n, 8, 8,isHyper)
        else:
            column, row = moveRowAndColum(column, row)
    sample = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(0, 9):
        if n[row][i] != 0:
            sample.remove(n[row][i])
    for i in sample:
        n[row][column] = i
        column1, row1 = moveRowAndColum(column, row)
        medium = DFS(n, row1, column1,isHyper)
        if medium != []:
            return n
        else:
            n[row][column] = 0
    return []

def moveRowAndColum(column, row):
    if column < 8:
        column += 1
    elif row < 8 and column == 8:
        row += 1
        column = 0
    return column, row


def CheckAnswer(n,isHyper):
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
    if isHyper:
        a = np.hstack(n[1][1], n[1][2], n[1][3], n[2][1], n[2][2], n[2][3], n[3][1], n[3][2], n[3][3])
        if not sample == sorted(a):
            return False
        a = np.hstack(n[5][1], n[5][2], n[5][3], n[6][1], n[6][2], n[6][3], n[7][1], n[7][2], n[7][3])
        if not sample == sorted(a):
            return False
        a = np.hstack(n[1][5], n[1][6], n[1][7], n[2][5], n[2][6], n[2][7], n[3][5], n[3][6], n[3][7])
        if not sample == sorted(a):
            return False
        a = np.hstack(n[5][5], n[5][6], n[5][7], n[6][5], n[6][6], n[6][7], n[7][5], n[7][6], n[7][7])
        if not sample == sorted(a):
            return False
    return True


def run(difficulty):
    if difficulty == "easy":
        get_answer(difficulty,False)
    if difficulty == "hard":
        get_answer(difficulty,False)
    if difficulty == "h_easy":
        get_answer(difficulty, True)
    if difficulty == "h_hard":
        get_answer(difficulty, True)


def get_answer(difficulty, isHyper):
    inputdata = csv.get_data("Sudoku/"+difficulty+".txt")
    data = []
    for board in inputdata:
        sdk = []
        for line in board:
            a = []
            for c in line:
                a.append(int((c)))
            sdk.append(a)
        n = np.asarray(sdk)
        for i in range(0, 3):
            start_time = time.time()
            DFS(n, 0, 0, isHyper)
            end_time = time.time()
            data.append(round(end_time - start_time, 5))
        csv.writ_data(data, "DFS"+difficulty+".csv")