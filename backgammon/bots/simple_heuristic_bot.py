import copy
import random

from backgammon.engine import BackgammonEngine, Move, Player

from .base import BackgammonBot


class SimpleHeuristicBot(BackgammonBot):
    """Evaluates each legal move by the simple board score and selects the best."""

    def __init__(self):
        super().__init__()
        self.name = "SimpleHeuristicBot"

    def calculate_move(self, engine: BackgammonEngine) -> Move:
        if not engine.legal_moves:
            raise ValueError("Cannot select from empty legal moves")

        player = engine.turn
        best_score = float("-inf") if player == Player.WHITE else float("inf")
        selected_move = None

        for move in engine.legal_moves:
            new_engine = copy.deepcopy(engine)
            if not new_engine.attempt_move(move.start_point.index, move.final_point.index):
                raise ValueError("Unable to apply legal move to engine copy")

            score = self.calculate_board_score(new_engine)
            if player == Player.WHITE and score > best_score:
                best_score = score
                selected_move = move
            elif player == Player.BLACK and score < best_score:
                best_score = score
                selected_move = move

        if selected_move is None:
            return random.choice(engine.legal_moves)
        return selected_move
