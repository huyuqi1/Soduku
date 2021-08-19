import csv
import codecs
import numpy as np
H_EASY = "../Sudoku/easy.txt"
def get_data(filename):
    final_data = []
    for i in range(0 ,15):
        final_data.append(readFile(filename, i))
    return final_data

def get_DLX_data(fileName):
    with open(fileName, 'r') as file:
        all_file = file.read().strip()
    matrices = all_file.split('\n$\n')
    Soduku = []
    for line in matrices:
        Soduku.append(line.replace("\n", "").replace(" ",""))
    return Soduku


def readFile(fileName, n):
    with open(fileName, 'r') as file:
        all_file = file.read().strip()  # Read and remove any extra new line
    matrices = all_file.split('\n$\n')
    all_file_list = matrices[n].split('\n')  # make a list of lines
    final_data = [[int(each_int) for each_int in line.split()] for line in
                  all_file_list]  # make list of list and convert to int
    return final_data

def get_graph1_data():
    f = csv.reader(open('test.csv', 'r'))
    data_list =[]
    for line in f:
        data_list.append(line[1])
    return data_list

def get_graph3_data():
    f = csv.reader(open('test3.csv', 'r'))
    data_list =[]
    for line in f:
        data_list.append(line[1])
    return data_list

def get_graph2_data():
    f = csv.reader(open('test1.csv', 'r'))
    data_list =[]
    for line in f:
        data_list.append(line[1])
    return data_list

def get_graph4_data():
    f = csv.reader(open('test4.csv', 'r'))
    data_list =[]
    for line in f:
        data_list.append(line[1])
    return data_list

def writ_data(data,filename):
    f = codecs.open(filename, 'a+', 'gbk')
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()

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
