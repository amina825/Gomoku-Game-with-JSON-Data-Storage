from itertools import groupby
from typing import Optional, Dict #options
import json
import numpy as np # work with arrays matrices
import PySimpleGUI as sg
import random
from board import Board
from gui import BoardGUI
from gomoku_board import GomokuBoard
from game_logic import GameLogic
from player_stats import PlayerStats

BOARD_SIZE = 3
NEEDED_TO_WIN = 3
BLANK_IMAGE_PATH = 'tiles/gomoku_blank_scaled.png'
X_IMAGE_PATH = 'tiles/gomoku_X_scaled.png'
O_IMAGE_PATH = 'tiles/gomoku_O_scaled.png'

GOMOKU_DRAW_DICT = {
    0: ('', ('black', 'lightgrey'), BLANK_IMAGE_PATH),
    1: ('', ('black', 'lightgrey'), X_IMAGE_PATH),
    2: ('', ('black', 'lightgrey'), O_IMAGE_PATH),
}

#def switch_player(player: int) -> int:
   # return 3 - player
class GomokuGame:
    def __init__(self):
        self.player_name = self.get_player_name()
        self.player_stats = PlayerStats.load_all_from_file('player_stats.json')
        if self.player_name not in self.player_stats:
            self.player_stats[self.player_name] = PlayerStats(name=self.player_name)
        self.board = GomokuBoard(BOARD_SIZE)
        self.game_logic = GameLogic(self.board, self.player_stats, self.player_name)
        self.board_gui = BoardGUI(self.board, GOMOKU_DRAW_DICT)
        self.window = self.create_window()

    def get_player_name(self):
        while True:
            layout = [
                [sg.Text('Enter your name:'), sg.InputText(key='-NAME-')],
                [sg.Button('Start')]
            ]
            window = sg.Window('Gomoku', layout)
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                window.close()
                exit()
            player_name = values['-NAME-']
            if player_name.strip():  # Ensure the name is not empty
                window.close()
                return player_name

            sg.Popup('Please enter your name.')
            window.close()
    def create_window(self):
        layout = [
            [sg.Text('Gomoku', size=(30, 1), justification='center', font=("Helvetica", 25))],
            [sg.Column(self.board_gui.board_layout, justification='center')],#treated as single unit 
            [sg.Text('Player: '), sg.Text(self.player_name, key='-NAME-')],
            [sg.Text('Wins: '), sg.Text(self.player_stats[self.player_name].wins, key='-WINS-')],
            [sg.Text('Losses: '), sg.Text(self.player_stats[self.player_name].losses, key='-LOSSES-')],
            [sg.Text('Draws: '), sg.Text(self.player_stats[self.player_name].draws, key='-DRAWS-')],
            [sg.Button('Restart'), sg.Button('Exit')],
            [sg.Text('Leaderboard:', size=(30, 1), justification='center', font=("Helvetica", 15))],
            [sg.Multiline(size=(40, 10), key='-LEADERBOARD-', disabled=True, justification='center')]
        ]
        screen_width, screen_height = sg.Window.get_screen_size()
        window_width = screen_width - 100  # Add padding from the corners
        window_height = screen_height - 100  # Add padding from the corners

        window = sg.Window('Gomoku',
                         layout,
                         default_button_element_size=(10, 2),
                         auto_size_buttons=False,
                         location=(50, 50),
                         size=(window_width, window_height),
                         element_justification='center', # Center elements in the window
                         finalize=True)
        return window
    
    def update_leaderboard(self):
        #values return list to be sorted#key is tuple which lambda return
        leaderboard = sorted(self.player_stats.values(), key=lambda ps: (ps.win_ratio(), ps.total_games()), reverse=True)#higher on top# anonymous func call without name
        leaderboard_text = "\n".join([f"{ps.name}: {ps.wins} wins, {ps.losses} losses, {ps.draws} draws, {ps.total_games()} total games" for ps in leaderboard])
        self.window['-LEADERBOARD-'].update(leaderboard_text)

    def run(self):
        while True:
            event, values = self.window.read()
            if event is None or event == 'Exit' or event == sg.WIN_CLOSED:
                break
            if event == 'Restart':
                self.game_logic.reset()
                self.board_gui.update()
            elif event == 'Save Game':
                self.game_logic.save_game('gomoku_save.json')
                self.board_gui.update()  # Ensure the GUI is updated after saving the game
            if isinstance(event, tuple):
                row, col = event
                winner = self.game_logic.play(row, col)
                self.board_gui.update()
                if winner is not None:
                    if winner == 1:
                        sg.Popup('You have won, congrats!')
                    elif winner == 2:
                        sg.Popup('You have lost, try again!')
                    else:
                        sg.Popup("It's a draw!")
                    self.game_logic.reset()
                    self.board_gui.update()
                else:
                    # Computer's move
                    winner = self.game_logic.computer_move()
                    self.board_gui.update()
                    if winner is not None:
                        if winner == 1:
                            sg.Popup('You have won, congrats!')
                        elif winner == 2:
                            sg.Popup('You have lost, try again!')
                        else:
                            sg.Popup("It's a draw!")
                        self.game_logic.reset()
                        self.board_gui.update()

            # Update player statistics display
            self.window['-WINS-'].update(self.player_stats[self.player_name].wins)
            self.window['-LOSSES-'].update(self.player_stats[self.player_name].losses)
            self.window['-DRAWS-'].update(self.player_stats[self.player_name].draws)
            self.update_leaderboard()
        self.window.close()
           
if __name__ == "__main__":
    game = GomokuGame()
    game.run()