import json
from typing import Dict
class PlayerStats:
    def __init__(self, name: str, wins=0, losses=0, draws=0):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.draws = draws

    def to_dict(self):
        return {
            'name': self.name,
            'wins': self.wins,
            'losses': self.losses,
            'draws': self.draws
        }
    #take class an input 
    @classmethod
    def from_dict(cls, data):
        return cls(name=data.get('name', ''), wins=data.get('wins', 0), losses=data.get('losses', 0), draws=data.get('draws', 0))
    
    #keys are str (player name)
    @staticmethod
    def load_all_from_file(filename: str) -> Dict[str, 'PlayerStats']:
        try:
            # r is read mode with(closed later)
            with open(filename, 'r') as f:
                data = json.load(f)
            return {name: PlayerStats.from_dict(stats) for name, stats in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save_all_to_file(filename: str, player_stats: Dict[str, 'PlayerStats']):
        with open(filename, 'w') as f:
            #to json str
            json.dump({name: stats.to_dict() for name, stats in player_stats.items()}, f)

    def total_games(self):
        return self.wins + self.losses + self.draws

    def win_ratio(self):
        total_games = self.total_games()
        return self.wins / total_games if total_games > 0 else 0
