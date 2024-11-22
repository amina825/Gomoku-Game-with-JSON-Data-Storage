import random
from typing import Dict
from gomoku_board import GomokuBoard
from player_stats import PlayerStats


class GameLogic:
    def __init__(self, board: GomokuBoard, player_stats: Dict[str, PlayerStats], current_player_name: str):
        self.board = board
        self.current_player = 1
        self.player_stats = player_stats
        self.current_player_name = current_player_name

    def play(self, row_ind, col_ind):
        if self.board[row_ind, col_ind] != 0:#already occupied
            return None
        self.board[row_ind, col_ind] = self.current_player
        winner = self.board.winner()
        if winner is not None:
            if winner == 1:
                self.player_stats[self.current_player_name].wins += 1
            elif winner == 2:
                self.player_stats[self.current_player_name].losses += 1
            else:
                self.player_stats[self.current_player_name].draws += 1
            PlayerStats.save_all_to_file('player_stats.json', self.player_stats)
            return winner
        self.switch_player()
        return None

    def switch_player(self):
        self.current_player = 3-self.current_player

    def reset(self):
        self.board.reset()
        self.current_player = 1

    def save_game(self, filename: str):
        self.board.save_to_file(filename)

    def computer_move(self):
        empty_tiles = [(i, j) for i in range(self.board.n) for j in range(self.board.n) if self.board[i, j] == 0]
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.board[row, col] = self.current_player
            winner = self.board.winner()
            if winner is not None:
                if winner == 1:
                    self.player_stats[self.current_player_name].wins += 1
                elif winner == 2:
                    self.player_stats[self.current_player_name].losses += 1
                else:
                    self.player_stats[self.current_player_name].draws += 1
                PlayerStats.save_all_to_file('player_stats.json', self.player_stats)
                return winner
            self.switch_player()
        return None
