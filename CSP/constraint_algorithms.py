import constraint
import Sudoku.csv_tool as csv
import time
import numpy as np
class Constraint:

    def __init__(self, n):
        self.isHyper = False
        if (isinstance(n , str)):
            self.data = csv.get_data(n)
        else:
            self.data = []
            self.data.append(n)

    def get_rule(self):
        self.problem = constraint.Problem()
        global i, j
        # We're letting VARIABLES 11 through 99 have an interval of [1..9]
        for i in range(1, 10):
            self.problem.addVariables(range(i * 10 + 1, i * 10 + 10), range(1, 10))
        # We're adding the constraint that all values in a row must be different
        # 11 through 19 must be different, 21 through 29 must be all different,...
        for i in range(1, 10):
            self.problem.addConstraint(constraint.AllDifferentConstraint(), range(i * 10 + 1, i * 10 + 10))
        # Also all values in a column must be different
        # 11,21,31...91 must be different, also 12,22,32...92 must be different,...
        for i in range(1, 10):
            self.problem.addConstraint(constraint.AllDifferentConstraint(), range(10 + i, 100 + i, 10))
        # The last rule in a Sudoku 9x9 puzzle is that those nine 3x3 squares must have all different values,
        # we start off by noting that each square"starts" at row indices 1, 4, 7
        for i in [1, 4, 7]:
            # Then we note that it's the same for columns, the squares start at indices 1, 4, 7 as well
            # basically one square starts at 11, the other at 14, another at 41, etc
            for j in [1, 4, 7]:
                square = [10 * i + j, 10 * i + j + 1, 10 * i + j + 2, 10 * (i + 1) + j, 10 * (i + 1) + j + 1,
                          10 * (i + 1) + j + 2, 10 * (i + 2) + j, 10 * (i + 2) + j + 1, 10 * (i + 2) + j + 2]
                # As an example, for i = 1 and j = 1 (bottom left square), the cells 11,12,13,
                # 21,22,23, 31,32,33 have to be all different
                self.problem.addConstraint(constraint.AllDifferentConstraint(), square)
        # file_name = input("Enter the name of the .json file containing the Sudoku puzzle:")

        if(self.isHyper):
            for i in [2, 6]:
                # Then we note that it's the same for columns, the squares start at indices 1, 4, 7 as well
                # basically one square starts at 11, the other at 14, another at 41, etc
                for j in [2, 6]:
                    square = [10 * i + j, 10 * i + j + 1, 10 * i + j + 2, 10 * (i + 1) + j, 10 * (i + 1) + j + 1,
                              10 * (i + 1) + j + 2, 10 * (i + 2) + j, 10 * (i + 2) + j + 1, 10 * (i + 2) + j + 2]
                    # As an example, for i = 1 and j = 1 (bottom left square), the cells 11,12,13,
                    # 21,22,23, 31,32,33 have to be all different
                    self.problem.addConstraint(constraint.AllDifferentConstraint(), square)

    def get_solution(self, filename):
        for board in self.data:
            data =[]
            for count in range(0,3):
                start_time = time.time()
                self.get_rule()
                global i, j
                for i in range(9):
                    for j in range(9):
                        if board[i][j] != 0:
                            def c(variable_value, value_in_table=board[i][j]):
                                if variable_value == value_in_table:
                                    return True
                            # Basically we're making sure that our program doesn't change the values already on the board
                            # By telling it that the values NEED to equal the corresponding ones at the base board
                            self.problem.addConstraint(c, [((i + 1) * 10 + (j + 1))])
                solutions = self.problem.getSolutions()
                end_time = time.time()
                for s in solutions:
                    print("==================")
                    answer = ""
                    for i in range(1, 10):
                        print("|", end='')
                        for j in range(1, 10):
                            answer += str(s[i * 10 + j])
                            if j % 3 == 0:
                                print(str(s[i * 10 + j]) + " |", end='')
                            else:
                                print(str(s[i * 10 + j]), end='')
                        print("")
                        if i % 3 == 0 and i != 9:
                            print("------------------")
                    print("==================")
                    data.append(round(end_time-start_time, 5))
                if len(solutions) == 0:
                    print("No solutions found.")
            csv.writ_data(data, filename)

    def get_answer(self):
        for board in self.data:
            for count in range(0,3):
                self.get_rule()
                global i, j
                for i in range(9):
                    for j in range(9):
                        if board[i][j] != 0:
                            def c(variable_value, value_in_table=board[i][j]):
                                if variable_value == value_in_table:
                                    return True
                            self.problem.addConstraint(c, [((i + 1) * 10 + (j + 1))])
                solutions = self.problem.getSolutions()
                if len(solutions) == 0:
                    print("No solutions found.")
            answer =[]
            for s in solutions:
                for i in range(1, 10):
                    a = []
                    for j in range(1, 10):
                        a.append(s[i * 10 + j])
                    answer.append(a)
        return np.asarray(answer)


def run(difficulty):
    if difficulty == "easy":
        cos = Constraint("Sudoku/easy.txt")
        cos.get_solution("CSP/CSP_easy.csv")
    if difficulty == "hard":
        cos = Constraint("Sudoku/hard.txt")
        cos.get_solution("CSP/CSP_hard.csv")
    if difficulty == "h_easy":
        cos = Constraint("Sudoku/h_easy.txt")
        cos.isHyper = True
        cos.get_solution("CSP/CSP_h_easy.csv")
    if difficulty == "h_hard":
        cos = Constraint("Sudoku/h_hard.txt")
        cos.isHyper = True
        cos.get_solution("CSP/CSP_h_hard.csv")

