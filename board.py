from __future__ import annotations#reference to class before defined
# not to make init eq or some other func store data
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)#cant be changed final
class Position:
    row: int
    col: int

    def __add__(self, other: Position) -> Position:
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Position) -> Position:
        return Position(self.row - other.row, self.col - other.col)


class Board:
    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.create_board()

    def create_board(self) -> None:
        self.board = []
        for i in range(self.m):
            row = []
            for j in range(self.n):
                row.append(self._default_state_for_coordinates(i, j))
            self.board.append(row)
    #iteratable
    def __iter__(self):
        return iter(self.board)

    def __getitem__(self, index: tuple[int, int] | Position | int) -> Any:
        if isinstance(index, tuple):
            i, j = index
            return self.board[i][j]
        elif isinstance(index, Position):
            return self.board[index.row][index.col]
        else:
            return self.board[index]

    def __setitem__(self, index: tuple[int, int] | Position | int, item) -> None:
        if isinstance(index, tuple):
            i, j = index
            self.board[i][j] = item
        elif isinstance(index, Position):
            self.board[index.row][index.col] = item
        else:
            self.board[index] = item
    #will be overriden by subclass can be used to make any board
    def _default_state_for_coordinates(self, i: int, j: int):
        raise NotImplementedError()