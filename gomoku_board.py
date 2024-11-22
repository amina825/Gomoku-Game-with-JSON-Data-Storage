from itertools import groupby
from typing import Optional
import numpy as np
import json
BOARD_SIZE = 3
NEEDED_TO_WIN = 3
BLANK_IMAGE_PATH = 'tiles/gomoku_blank_scaled.png'
X_IMAGE_PATH = 'tiles/gomoku_X_scaled.png'
O_IMAGE_PATH = 'tiles/gomoku_O_scaled.png'


class GomokuBoard:
    def __init__(self, n: int = BOARD_SIZE, board: Optional[np.ndarray] = None):#nd matrices multi d array
        if board is None:
            self.n = n
            self.board = np.zeros((self.n, self.n), dtype=int)#2d array
        else:
            self.board = board
            self.n = board.shape[0]#number of rows

    def __getitem__(self, index: tuple[int, int]) -> int:
        row, col = index
        return self.board[row, col]

    def __setitem__(self, index: tuple[int, int], value: int) -> None:
        row, col = index
        self.board[row, col] = value

    def winner(self) -> Optional[int]:
        for player, length in ((key, len(list(group))) for row in self.board
                               for key, group in groupby(row) if key != 0):
            if length >= NEEDED_TO_WIN:#groupby consecutive pieces of the same type in each row.
                return player
        for player, length in ((key, len(list(group))) for row in self.board.T#transpose
                               for key, group in groupby(row) if key != 0):
            if length >= NEEDED_TO_WIN:
                return player
        diagonals = (self.board.diagonal(i) for i in range(#shape returns dimension(3 by 3)=3
            NEEDED_TO_WIN-self.board.shape[0], self.board.shape[0] - NEEDED_TO_WIN + 1))
        for player, length in ((key, len(list(group))) for diag in diagonals
                               for key, group in groupby(diag) if key != 0):
            if length >= NEEDED_TO_WIN:
                return player
        diagonals = (np.flipud(self.board).diagonal(i) for i in range(
            NEEDED_TO_WIN-self.board.shape[0], self.board.shape[0] - NEEDED_TO_WIN + 1))
        for player, length in ((key, len(list(group))) for diag in diagonals
                               for key, group in groupby(diag) if key != 0):
            if length >= NEEDED_TO_WIN:
                return player
        if len(np.where(self.board == 0)[0]) == 0:
            return 0
        return None

    def reset(self) -> None:
        self.board = np.zeros((self.n, self.n), dtype=int)

    def to_dict(self):
        return {
            'n': self.n,
            'board': self.board.tolist()
        }

    @classmethod
    def from_dict(cls, data):
        board = np.array(data['board'])
        return cls(n=data['n'], board=board)

    def save_to_file(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load_from_file(cls, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)