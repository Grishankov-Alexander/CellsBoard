import random
import time
import sys
import copy
import argparse
import re


class Cell(object):
    """Represents dead(0) or alive(1) cell object"""

    ALIVE = 1
    DEAD = 0
    def __init__(self, state):
        if state not in [self.DEAD, self.ALIVE]:
            raise ValueError("Cell could be either DEAD(0) or ALIVE(1)")
        self.state = state

    def __repr__(self):
        return f"Cell({self.state})"
    
    def __str__(self):
        return str(self.state)
        
        
class CellsBoard(object):
    """2-dimensional board of Cell objects."""

    def __init__(self, rows, columns, file=None):
        """Create rows x columns board.

        Create from file if specified.
        else - fill the board with random Cell objects"""
        if file:
            self.initFromFile(file)
        else:
            self.rows = rows
            self.columns = columns
            # Create a 2D board with random state cells
            random.seed()
            self.board = [
                [Cell(random.randint(Cell.DEAD, Cell.ALIVE))
                 for j in range(self.columns)] for i in range(self.rows)
                ]
    
    def __repr__(self):
        """Can be used to recreate a CellsBoard"""
        return f"CellsBoard({self.rows}, {self.columns}, {self.file})"

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

    def initFromFile(self, file):
        """Initialize the board from file."""
        with open(file) as fp:
            # Get rid of empty lines and spaces
            lines = [
                re.sub(r"\s*", "", line) for line in fp.readlines()
                if re.sub(r"\s*", "", line)
                ]
            self.rows = len(lines)
            self.columns = len(lines[0])
            self.board = [
                [Cell(int(lines[i][j]))
                 for j in range(self.columns)] for i in range(self.rows)
                ]
            
    def findNeighbors(self, board, row: int, column: int) -> list:
        """Returns a list of neighbors for a board[row][column] cell."""
        neighbors = [
            board[i][j]
            for i in range(row - 1, row + 2)
            if i >= 0 and i < len(board)
            for j in range(column - 1, column + 2)
            if j >= 0 and j < len(board[i])
            and board[i][j] != board[row][column]
            ]
        return neighbors

    def updateBoard(self):
        """Change board cells state"""
        boardCopy = copy.deepcopy(self.board)
        for row in range(self.rows):
            for column in range(self.columns):
                cell = boardCopy[row][column]
                cellNeighbors = self.findNeighbors(boardCopy, row, column)
                aliveNeighbors = len(
                    [neighbor for neighbor in cellNeighbors
                     if neighbor.state == Cell.ALIVE]
                    )
                if cell.state == Cell.ALIVE:
                    if aliveNeighbors < 2 or aliveNeighbors > 3:
                        self.board[row][column].state = Cell.DEAD
                else:
                    if aliveNeighbors == 3:
                        self.board[row][column].state = Cell.ALIVE


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate cells interaction in the 2D board"
        )
    parser.add_argument("rows", type=int, nargs="?", default=10,
                        help="Number of rows in the 2D board.")
    parser.add_argument("columns", type=int,nargs="?", default=10,
                        help="Number of columns in the row")
    parser.add_argument("-f", "--file", help="Init a board from file.")
    args = parser.parse_args()
    if args.file:
        board = CellsBoard(args.rows, args.columns, file = args.file)
    else:
        board = CellsBoard(args.rows, args.columns)
    while True:
        print(board)
        board.updateBoard()
        time.sleep(1)
