import copy
import random

from backgammon.engine import BackgammonEngine, Move, Player

from .base import BackgammonBot


class GPTHeuristicBot(BackgammonBot):
    """
    A heuristic bot:
    - Evaluates positions with a pip-based heuristic
      (plus bar, home, blots, and made points)
    - Chooses the move that gives the best immediate resulting position
      for the current player.
    """

    def __init__(self):
        super().__init__()
        self.name = "GPTHeuristicBot"

    def calculate_move(self, engine: BackgammonEngine) -> Move:
        if not engine.legal_moves:
            raise ValueError("Cannot select from empty legal moves")

        player = engine.turn
        best_move = None
        best_value = float("-inf") if player == Player.WHITE else float("inf")

        for move in engine.legal_moves:
            new_engine = copy.deepcopy(engine)
            if not new_engine.attempt_move(move.start_point.index, move.final_point.index):
                continue

            value = self._score_for_player(new_engine, player)
            if player == Player.WHITE and value > best_value:
                best_value = value
                best_move = move
            elif player == Player.BLACK and value < best_value:
                best_value = value
                best_move = move

        if best_move is None:
            return random.choice(engine.legal_moves)
        return best_move

    def _score_for_player(self, engine: BackgammonEngine, player: Player) -> float:
        """Convert a white-centric score to the perspective of the current player."""

        base = self._board_score_white(engine)
        return base if player == Player.WHITE else -base

    def _board_score_white(self, engine: BackgammonEngine) -> float:
        """
        Positive = good for White, negative = good for Black.

        Components:
        - Pip count (lower pip is better)
        - Penalty for checkers on the bar
        - Bonus for borne-off checkers
        - Penalty for blots (single checkers)
        - Bonus for made points (2+ checkers)
        - Huge bonus/penalty for winning/losing
        """

        board = engine.board

        if engine.winner == Player.WHITE:
            return 1e9
        if engine.winner == Player.BLACK:
            return -1e9

        pip_white = 0
        pip_black = 0

        for point in board.points:
            if point.owner == Player.WHITE:
                pip_white += (25 - point.index) * point.count
            elif point.owner == Player.BLACK:
                pip_black += point.index * point.count

        pip_white += 25 * board.bar_white.count
        pip_black += 25 * board.bar_black.count

        home_bonus = 25 * (board.home_white.count - board.home_black.count)

        blot_penalty = 0.0
        made_point_bonus = 0.0

        for point in board.points:
            if point.count == 1:
                if point.owner == Player.WHITE:
                    blot_penalty -= 1.5
                elif point.owner == Player.BLACK:
                    blot_penalty += 1.5
            elif point.count >= 2:
                if point.owner == Player.WHITE:
                    made_point_bonus += 0.5
                elif point.owner == Player.BLACK:
                    made_point_bonus -= 0.5

        pip_component = pip_black - pip_white
        return pip_component + home_bonus + blot_penalty + made_point_bonus
