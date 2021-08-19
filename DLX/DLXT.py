from __future__ import division
import math
import time
import Sudoku.csv_tool as csv

class Node(object):

    def __init__(self, left=None, right=None, up=None, down=None,
                 col_header=None, row_header=None):

        self.left = left or self
        self.right = right or self
        self.up = up or self
        self.down = down or self

        self.col_header = col_header
        self.row_header = row_header



class SudokuSolver(object):

    def __init__(self, sudoku):
        self.cycle_number = 0
        self.sudoku = sudoku

        self.num_cells = len(sudoku)
        self.dimension = int(math.sqrt(self.num_cells))
        self.box_size = int(math.sqrt(self.dimension))

        self.num_columns = self.dimension ** 2 * 4 + 36

        self.cell_offset = 0
        self.row_offset = self.dimension ** 2 + self.cell_offset
        self.col_offset = self.dimension ** 2 * 2 + self.cell_offset
        self.box_offset = self.dimension ** 2 * 3 + self.cell_offset
        self.box2_offset = self.dimension ** 2 * 4 + self.cell_offset

        self.col_headers = []
        self.col_size = [0] * self.num_columns
        self.partial_answer = [-1] * self.num_columns
        self.answer = [-1] * self.num_cells

        self.run()

    def run(self):

        self.construct_matrix()

        if self.dlx_search(0):
            self.compute_answer()
            print(self.answer)
        else:
            print('no solution')

    def construct_matrix(self):

        self.root = Node()

        # construct column headers
        for i in range(self.num_columns):
            new_col_header = Node(left=self.root.left, right=self.root)
            self.root.left.right = new_col_header
            self.root.left = new_col_header

            new_col_header.col_header = i
            new_col_header.row_header = 0

            self.col_headers.append(new_col_header)

        for i in range(self.num_cells):
            r = i // self.dimension
            c = i % self.dimension

            # negative(ie, -1) represents an empty cell
            if self.sudoku[i] < 0:
                # fill this empty cell with every possible value
                for value in range(self.dimension):
                    self.insert_value(r, c, value)
            # positive indicates the cell is filled with a value
            else:
                self.insert_value(r, c, self.sudoku[i])

    def insert_value(self, row, col, value):

        # constraint 1: each cell must have a number filled
        cell_idx = row * self.dimension + col + self.cell_offset
        # constraint 2: each row must contain each number exactly once
        row_idx = row * self.dimension + value + self.row_offset
        # constraint 3: each column must contain each number exactly once
        col_idx = col * self.dimension + value + self.col_offset
        # constraint 4: each box must contain each number exactly once
        box_idx = ((row // self.box_size) * self.box_size + (col //
                                                             self.box_size)) * self.dimension + value + self.box_offset

        index = row * self.dimension + col
        if index in [10, 11, 12, 19, 20, 21, 28, 29, 30]:
            box2_idx = value + self.box2_offset
        elif index in [14, 15, 16, 23, 24, 25, 32, 33, 34]:
            box2_idx = self.dimension + value  + self.box2_offset
        elif index in [46, 47, 48, 55, 56, 57, 64, 65, 66]:
            box2_idx = 2 * self.dimension + value  + self.box2_offset
        elif index in [50, 51, 52, 59, 60, 61, 68, 69, 70]:
            box2_idx = 3 * self.dimension + value  + self.box2_offset
        else:
            box2_idx=0


        # map <row, col, #value> to the vertical index of the matrix
        vertical_row_idx = ((row * self.dimension + col) * self.dimension +
                            value + self.cell_offset)

        self.add_row(vertical_row_idx, cell_idx, row_idx, col_idx, box_idx, box2_idx)

    def add_row(self, row, col1, col2, col3, col4, col5):

        self.col_size[col1] += 1

        col_header_node = self.col_headers[col1]

        # add new node to [row, col1]
        row_first_node = Node(up=col_header_node.up,
                              down=col_header_node,
                              col_header=col1,
                              row_header=row)

        # place at vertical bottom of col col1
        col_header_node.up.down = row_first_node
        col_header_node.up = row_first_node

        # add new nodes to the rest columns
        for col in [col2, col3, col4, col5]:
            if col == 0:
                continue
            self.col_size[col] += 1

            col_header_node = self.col_headers[col]

            new_node = Node(left=row_first_node.left,
                            right=row_first_node,
                            up=col_header_node.up,
                            down=col_header_node,
                            col_header=col,
                            row_header=row)

            # place at horizontal tail of the row
            row_first_node.left.right = new_node
            row_first_node.left = new_node
            # place at vertical bottom of the column
            col_header_node.up.down = new_node
            col_header_node.up = new_node

    def dlx_search(self, level):
        self.cycle_number += 1
        # all columns have been removed, success
        if self.root.right == self.root:
            return True

        min_size = 0xfffffff

        j = self.root.right
        # choose the best column j with the least nodes in it
        while j != self.root:
            if self.col_size[j.col_header] < min_size:
                min_size = self.col_size[j.col_header]
                column_header = j
            j = j.right

        # cover this column
        self.cover(column_header)

        node_down = column_header.down

        # stop until node goes back to original (vertically)
        while node_down != column_header:
            # record the possible answer
            self.partial_answer[level] = node_down.row_header
            node_right = node_down.right

            # remove row, stop until node goes back to original (horizontally)
            while node_right != node_down:
                # cover this node's corresponding column
                self.cover(self.col_headers[node_right.col_header])
                node_right = node_right.right

            # after previous removal, continue to next level
            if self.dlx_search(level + 1):
                return True

            # previous cover() failed, restore states
            node_left = node_down.left
            while node_left != node_down:
                self.uncover(self.col_headers[node_left.col_header])
                node_left = node_left.left

            node_down = node_down.down

        # previous cover() failed, so restore original
        self.uncover(column_header)

    def cover(self, column_header):

        # remove this column
        column_header.left.right = column_header.right
        column_header.right.left = column_header.left

        node_down = column_header.down

        # move downwards vertically node by node, 
        while node_down != column_header:
            node_right = node_down.right

            # remove this row vertically
            while node_right != node_down:
                node_right.down.up = node_right.up
                node_right.up.down = node_right.down

                # decreament the corresponding column size counter
                self.col_size[node_right.col_header] -= 1
                # move to next node at the right side
                node_right = node_right.right

            # move to next node at the down side
            node_down = node_down.down

    def uncover(self, column_header):

        # restore this column
        column_header.right.left = column_header
        column_header.left.right = column_header

        node_up = column_header.up

        # move upwards vertically node by node
        while node_up != column_header:
            node_left = node_up.left

            while node_left != node_up:
                # restore this row vertically
                node_left.down.up = node_left
                node_left.up.down = node_left

                # increament the corresponding column size counter
                self.col_size[node_left.col_header] += 1
                # move on the the left node
                node_left = node_left.left

            # move on to the up node
            node_up = node_up.up

    def compute_answer(self):

        # map the value of the choosed row index to cells' value
        for value_row_index in self.partial_answer:
            if value_row_index < 0:
                return

            t = value_row_index - self.cell_offset
            row = t // (self.dimension ** 2)
            col = (t // self.dimension) % self.dimension
            value = t % self.dimension
            self.answer[row * self.dimension + col] = value

def solution(filename):
    Data = csv.get_DLX_data(filename)
    for da in Data:
        input = ""
        for d in da:
            input = input + str(d)
        Sudoku = []
        solved = []
        for i in range(81):
            if input[i]!='0':
                Sudoku.append(ord(input[i]) - ord('1'))
            else:
                Sudoku.append(-1)
        print(Sudoku)
        data = []
        start_time = time.time()
        ss = SudokuSolver(Sudoku)
        for i in range(len(ss.answer)):
            solved.append(chr(ss.answer[i] + ord('1')))
        data.append("".join(solved))
        end_time = time.time()
        data.append(round(end_time - start_time, 5))
        start_time = time.time()
        ss = SudokuSolver(Sudoku)
        end_time = time.time()
        data.append(round(end_time - start_time, 5))
        start_time = time.time()
        ss = SudokuSolver(Sudoku)
        end_time = time.time()
        data.append(round(end_time - start_time, 5))
        if("easy" in filename):
            csv.writ_data(data, "DLX/DLX_h_easy.csv")
        else:
            csv.writ_data(data, "DLX/DLX_h_hard.csv")
        print(solved)
        print("cycles:" + str(ss.cycle_number))

def run(difficulty):
    if difficulty == "h_easy":
        solution("Sudoku/h_easy.txt")
    if difficulty == "h_hard":
        solution("Sudoku/h_hard.txt")


if __name__ == '__main__':
    run("hard")