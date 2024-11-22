from typing import Any
import PySimpleGUI as sg 
from board import Board


class BoardGUI:
    def __init__(self, board: Board,
                 draw_dict: dict[Any, tuple[str, tuple[str, str], str]],#x,o colour path
                 draw_function=None):
        # instance board         
        self.board = board
        self.draw_dict = draw_dict
        self.draw_function = draw_function
        self.create()

    def create(self) -> None:
        self.board_layout = []
        #board 2d
        for i, row in enumerate(self.board.board):
            row_layout = []
            for j, item in enumerate(row):#return index and row
                if self.draw_function:#if already defined
                    item = self.draw_function(item)
                text, color, image = self.draw_dict[item]
                row_layout.append(
                    sg.RButton(text,
                               size=(50, 50),
                               button_color=color,
                               key=(i, j),
                               image_filename=image,
                               pad=(0, 0),
                               border_width=0))
            self.board_layout.append(row_layout)

    def update(self) -> None:
        for i, row in enumerate(self.board.board):
            for j, item in enumerate(row):
                if self.draw_function:
                    item = self.draw_function(item)
                text, color, image = self.draw_dict[item]
                self.board_layout[i][j].Update(text,
                                               button_color=color,
                                               image_filename=image)