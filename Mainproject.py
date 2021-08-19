import SDK
import time
import CSP.constraint_algorithms
import DLX.DLX as dlx
import DLX.DLXT as dlxt
import DFS.DFS as dfs
def show_title():
    print("*************************************************\n")
    print("*               Sudoku Puzzles                  *\n")
    print("*************************************************\n")


if __name__ == '__main__':
    while(True):
        show_title()
        print("*Please enter your options:                     *\n")
        print("*1.Create standard Sudoku                       *\n")
        print("*2.Solving a sudoku by Backtracking algorithm   *\n")
        print("*3.Solving a sudoku by Constraint Programming   *\n")
        print("*4.Solving a sudoku by Dancing Links algorithm  *\n")
        print("*************************************************\n")
        choice = input();
        if choice == "1":
            show_title()
            print("*1.Easy standard sudoku                         *\n")
            print("*2.Difficult standard sudoku                    *\n")
            print("*************************************************\n")
            choice = input();
            n = []
            if choice == "1":
                show_title()
                n = SDK.CreateSudoku()
                n = SDK.randomDigging(10, n)
            if choice == "2":
                show_title()
                n = SDK.CreateSudoku()
                n = SDK.randomDigging(20, n)
            SDK.ShowSudoku(n)
            print("*Please enter your options:                     *\n")
            print("*1.Solving the sudoku by Backtracking algorithm *\n")
            print("*2.Solving the sudoku by Constraint Programming *\n")
            print("*3.Solving the sudoku by Dancing Links algorithm*\n")
            print("*************************************************\n")
            choice = input();
            if choice == "1":
                start_time = time.time()
                n = dfs.DFS(n, 0, 0, False)
                end_time = time.time()
                SDK.ShowSudoku(n)
                print("*             used time:" + str(round(end_time - start_time, 5)) + "ms               *\n")
                print("*************************************************\n")
            if choice == "2":
                start_time = time.time()
                csp = CSP.constraint_algorithms.Constraint(n)
                n = csp.get_answer()
                end_time = time.time()
                show_title()
                SDK.ShowSudoku(n)
                print("*             used time:" + str(round(end_time - start_time, 5)) + "ms               *\n")
                print("*************************************************\n")
            if choice == "3":
                start_time = time.time()
                n = dlx.solute_Soduko(n)
                end_time = time.time()
                show_title()
                SDK.ShowSudoku(n)
                print("*             used time:" + str(round(end_time - start_time, 5)) + "ms               *\n")
                print("*************************************************\n")
        if choice == "2":
            show_title()
            print("*1.Easy standard sudoku                         *\n")
            print("*2.Difficult standard sudoku                    *\n")
            print("*3.Easy hyper sudoku                            *\n")
            print("*4.Hard hyper sudoku                            *\n")
            print("*************************************************\n")
            choice = input();
            if choice == "1":
                dfs.run("easy")
            if choice == "2":
                dfs.run("hard")
            if choice == "3":
                dfs.run("h_easy")
            if choice == "4":
                dfs.run("h_hard")
        if choice == "3":
            show_title()
            print("*1.Easy standard sudoku                         *\n")
            print("*2.Difficult standard sudoku                    *\n")
            print("*3.Easy hyper sudoku                            *\n")
            print("*4.Hard hyper sudoku                            *\n")
            print("*************************************************\n")
            choice = input();
            if choice == "1":
                CSP.constraint_algorithms.run("easy")
            if choice == "2":
                CSP.constraint_algorithms.run("hard")
            if choice == "3":
                CSP.constraint_algorithms.run("h_easy")
            if choice == "4":
                CSP.constraint_algorithms.run("h_hard")
        if choice == "4":
            show_title()
            print("*1.Easy standard sudoku                         *\n")
            print("*2.Difficult standard sudoku                    *\n")
            print("*3.Easy hyper sudoku                            *\n")
            print("*4.Hard hyper sudoku                            *\n")
            print("*************************************************\n")
            choice = input();
            if choice == "1":
                dlx.run("easy")
            if choice == "2":
                dlx.run("hard")
            if choice == "3":
                dlxt.run("h_easy")
            if choice == "4":
                dlxt.run("h_hard")