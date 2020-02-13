import random
import time
import sys
import copy


class Cell(object):
    ALIVE = 1
    DEAD = 0
    def __init__(self, state):
        if state not in [self.DEAD, self.ALIVE]:
            raise ValueError("Cell could be either DEAD(0) or ALIVE(1)")
        self.state = state
        self.neighbors = []

    def __repr__(self):
        return f"Cell({self.state})"
    
    def __str__(self):
        return str(self.state)
        
        
class CellsBoard(object):
    def __init__(self, rows=10, columns=10, fromFile=False):
        self.rows = rows
        self.columns = columns
        self.fromFile = fromFile
        if self.fromFile is False:
            # Create a 2D board with random state cells
            random.seed()
            self.board = [
                [Cell(random.randint(Cell.DEAD, Cell.ALIVE))
                 for j in range(self.columns)] for i in range(self.rows)
                ]
            # Find neighbors for each cell.
            for row in range(self.rows):
                for column in range(self.columns):
                    cell = self.board[row][column]
                    cell.neighbors = self.findNeighbors(row, column)
#TODO: initialize from file
    
    def __repr__(self):
        """Can be used to recreate a CellsBoard"""
        return f"CellsBoard({self.rows}, {self.columns}, {self.fromFile})"

    def __str__(self):
        """Returns printable view of a CellsBoard"""
        strBoard = [
            [str(self.board[i][j]) for j in range(self.columns)]
            for i in range(self.rows)
            ]
        boardView = ""
        for i in range(self.rows):
            boardView += " ".join(strBoard[i]) + "\n"
        return boardView

    def findNeighbors(self, row: int, column: int) -> list:
        """Returns a list of neighbors for a board[row][column] cell."""
        neighbors = [
            self.board[i][j]
            for i in range(row - 1, row + 2)
            if i >= 0 and i < len(self.board)
            for j in range(column - 1, column + 2)
            if j >= 0 and j < len(self.board[i])
            and self.board[i][j] != self.board[row][column]
            ]
        return neighbors

    def updateBoard(self):
        """Change board cells state"""
        boardCopy = copy.deepcopy(self.board)
        for row in range(self.rows):
            for column in range(self.columns):
                cell = boardCopy[row][column]
                aliveNeighbors = len(
                    [neighbor for neighbor in cell.neighbors
                     if neighbor.state == Cell.ALIVE]
                    )
                if cell.state == Cell.ALIVE:
                    if aliveNeighbors < 2 or aliveNeighbors > 3:
                        self.board[row][column].state = Cell.DEAD
                else:
                    if aliveNeighbors == 3:
                        self.board[row][column].state = Cell.ALIVE

    
if __name__ == "__main__":
    board = CellsBoard()
    while True:
        print(board)
        board.updateBoard()
        #time.sleep(1)
