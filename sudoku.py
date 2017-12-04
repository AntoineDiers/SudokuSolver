from itertools import * 
import numpy as np
from time import *

class Cell():
    def __init__(self,value):
        self.value = value
        if value:
            self.possible_values = [value]
        else:
            self.possible_values = [1,2,3,4,5,6,7,8,9]
        self.line = None
        self.column = None
        self.square = None
        
class Line():
    def __init__(self,cells):
        self.cells = cells
        
class Column():
    def __init__(self,cells):
        self.cells = cells

class Square():
    def __init__(self,cells):
        self.cells = cells
        
class Grid():
    def __init__(self,grid):
        self.grid = grid
        self.init_grid()
    def init_grid(self):
        start_grid = self.grid
        self.grid = [[Cell(start_grid[i][j]) for j in range(9)]for i in range(9)]
        self.lines = [Line(self.grid[i]) for i in range(9)]
        self.columns = []
        for j in range(9):
            column = Column([])
            for i in range(9):
                cell = self.grid[i][j]
                column.cells.append(cell)
                cell.column = column
                cell.line = self.lines[i]
            self.columns.append(column)
        self.squares = []
        for i_1 in range(3):
            for j_1 in range(3):
                square = Square([])
                for i in range(3):
                    for j in range(3):
                        cell = self.grid[3*i_1+i][3*j_1+j]
                        square.cells.append(cell)
                        cell.square = square
                self.squares.append(square)
    def solved(self):
        for i in range(9):
            for j in range(9):
                cell = self.grid[i][j]
                if not cell.value:
                    return(0)
        return(1)
    def update(self):
        for i in range(9):
            for j in range(9):
                cell = self.grid[i][j]
                if not cell.value:
                    for cell_2 in cell.line.cells:
                        if cell_2.value and (cell_2.value in cell.possible_values):
                            cell.possible_values.remove(cell_2.value)
                    for cell_2 in cell.column.cells:
                        if cell_2.value and (cell_2.value in cell.possible_values):
                            cell.possible_values.remove(cell_2.value)
                    for cell_2 in cell.square.cells:
                        if cell_2.value and (cell_2.value in cell.possible_values):
                            cell.possible_values.remove(cell_2.value)
    def solve_obvious(self):
        res = 0
        for i in range(9):
            for j in range(9):
                cell = self.grid[i][j]
                if not cell.value:
                    if cell.possible_values:
                        if len(cell.possible_values) == 1:
                            cell.value = cell.possible_values[0]
                            return(1)
                    else:
                        return(2)
        return(0)
    def check_valid(self):
        features = [self.lines,self.columns,self.squares]
        for feature in features:
            for thing in feature:
                values = []
                for cell in thing.cells:
                    val = cell.value
                    if val:
                        if val in values:
                            return(0)
                        values.append(val)
        return(1)
    def get_grid(self):
        return(np.matrix([[self.grid[i][j].value for j in range(9)] for i in range(9)]))
    def make_guesses(self):
        min_unknown = 9
        unknown_pos = []
        taken_values = []
        for i in range(9):
            line = self.lines[i]
            pos = []
            taken = []
            for j in range(9):
                value = line.cells[j].value
                if value:
                    taken.append(value)
                else:
                    pos.append([i,j])
            if (9-len(taken))<min_unknown and (9-len(taken))>0:
                min_unknown = (9-len(taken))
                unknown_pos = pos
                taken_values = taken
        for j in range(9):
            column = self.columns[j]
            pos = []
            taken = []
            for i in range(9):
                value = column.cells[i].value
                if value:
                    taken.append(value)
                else:
                    pos.append([i,j])
            if (9-len(taken))<min_unknown and (9-len(taken))>0:
                min_unknown = (9-len(taken))
                unknown_pos = pos
                taken_values = taken
        for i_1 in range(3):
            for j_1 in range(3):
                square = self.squares[i_1*3+j_1]
                pos = []
                taken = []
                for i in range(3):
                    for j in range(3):
                        value = square.cells[3*i+j].value
                        if value:
                            taken.append(value)
                        else:
                            pos.append([i_1*3+i,j_1*3+j])
                if (9-len(taken))<min_unknown and (9-len(taken))>0:
                    min_unknown = (9-len(taken))
                    unknown_pos = pos
                    taken_values = taken
        possible_values = [1,2,3,4,5,6,7,8,9]
        for val in taken_values:
            if val in possible_values:
                possible_values.remove(val)
        cases = list(permutations(possible_values))
        n = len(cases)
        grids = [[[self.grid[i][j].value for j in range(9)] for i in range(9)]for k in range(n)]
        for k in range(n):
            case = cases[k]
            for l in range(len(case)):
                i,j = unknown_pos[l]
                grids[k][i][j] = case[l]
        return(grids)
                
        
class Sudoku():
    def __init__(self,grid):
        self.grid = Grid(grid)
    def init_solving(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j]>0:
                    self.grid[i][j] = [self.grid[i][j]]
                else:
                    self.grid[i][j] = [1,2,3,4,5,6,7,8,9]
    def solve(self):
        while not self.grid.solved():
            self.grid.update()
            obvious = self.grid.solve_obvious()
            if obvious == 0:
                new_grids = self.grid.make_guesses()
                new_sudokus = [Sudoku(new_grid) for new_grid in new_grids]
                res = 0
                for sudoku in new_sudokus:
                    if sudoku.grid.check_valid():
                        res = sudoku.solve()
                        if len(res)>0:
                            return(res)
                if not res:
                    return("")
            elif obvious == 1:
                ()
            else:
                return("")
        return(self.grid.get_grid())
        
my_sudoku = Sudoku([[1,0,0,0,0,7,0,9,0],[0,3,0,0,2,0,0,0,8],[0,0,9,6,0,0,5,0,0],[0,0,5,3,0,0,9,0,0],[0,1,0,0,8,0,0,0,2],[6,0,0,0,0,4,0,0,0],[3,0,0,0,0,0,0,1,0],[0,4,0,0,0,0,0,0,7],[0,0,7,0,0,0,3,0,0]])
t0 = time()
print(my_sudoku.solve())
print("time to solve : ",time()-t0)
            
            
            
            
            
            
            
            
            
            
            
            