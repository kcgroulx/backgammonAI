import random

from backgammon.engine import BackgammonEngine, Move

from .base import BackgammonBot


class RandomBot(BackgammonBot):
    """Selects a random move from the legal move list."""

    def __init__(self):
        super().__init__()
        self.name = "RandomBot"

    def calculate_move(self, engine: BackgammonEngine) -> Move:
        if not engine.legal_moves:
            raise ValueError("Cannot select from empty legal moves")
        return random.choice(engine.legal_moves)
