import backgammonEngine
from backgammonEngine import BackgammonEngine, Move, Player, Point
from abc import ABC, abstractmethod
import random
import copy

class BackgammonBot(ABC):
    def __init__(self):
        self.name = ""
        pass

    @abstractmethod
    def calculate_move(self, engine: BackgammonEngine) -> Move:
        pass

    # Returns the total score for a point
    # Score is how far along a stone is
    # Positive for white, negative for black
    def point_score(self, point) -> float:
        score = 0.0
        
        if point.owner == Player.WHITE:
            score = (point.index * point.count)
        elif point.owner == Player.BLACK:
            score = ((25 - point.index) * point.count) * -1.0

        # If there is a single stone, lower the score
        if point.count == 1:
            score = score / 2

        return score

    def calculate_board_score(self, engine: BackgammonEngine) -> float:
        score = 0.0

        # Get scores for homes. Bar is worth 0 so we don't need to add that
        score += self.point_score(engine.board.home_white)
        score += self.point_score(engine.board.home_black)

        # Get scores for all points
        for point in engine.board.points:
            score += self.point_score(point)
        return score

# Brief: Randomly selects a move
class RandomBot(BackgammonBot):
    def __init__(self):
        super().__init__()
        self.name = "RandomBot"

    def calculate_move(self, engine: BackgammonEngine) -> Move:
        if len(engine.legal_moves) == 0:
            raise ValueError("Cannot select from empty legal moves")
        return random.choice(engine.legal_moves)

# Calculates the board score for each move. Selects the highest board score  
class SimpleHeuristicBot(BackgammonBot):
    def __init__(self):
        super().__init__()
        self.name = "SimpleHeuristicBot"

    def calculate_move(self, engine) -> Move:
        if len(engine.legal_moves) == 0:
            raise ValueError("Cannot select from empty legal moves")

        # Start at -inf for white, +inf for black
        score = float('-inf') * engine.turn.value
        selected_move = None

        # Loop through each legal move
        for move in engine.legal_moves:
            new_engine = copy.deepcopy(engine)

            if new_engine.attempt_move(move.start_point.index, move.final_point.index) == False:
                raise ValueError("Unable to move stone")

            new_score = super().calculate_board_score(new_engine)

            if engine.turn == Player.WHITE and new_score > score:
                selected_move = move
                score = new_score
            elif engine.turn == Player.BLACK and new_score < score:
                selected_move = move
                score = new_score
        return selected_move
    
import random
import copy
from abc import ABC, abstractmethod
from backgammonEngine import BackgammonEngine, Move, Player, Point

class BackgammonBot(ABC):
    def __init__(self):
        self.name = ""

    @abstractmethod
    def calculate_move(self, engine: BackgammonEngine) -> Move:
        pass


class GPTHeuristicBot(BackgammonBot):
    """
    A heuristic bot:
    - Evaluates positions with a pip-based heuristic
      (plus bar, home, blots, and made points)
    - Chooses the move that gives the best *immediate* resulting position
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
        # White wants to maximize, Black wants to minimize
        best_value = float("-inf") if player == Player.WHITE else float("inf")

        for move in engine.legal_moves:
            new_engine = copy.deepcopy(engine)

            ok = new_engine.attempt_move(move.start_point.index, move.final_point.index)
            if not ok:
                # Shouldn't happen if legal_moves is correct
                continue

            value = self._score_for_player(new_engine, player)

            if player == Player.WHITE:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:  # BLACK
                if value < best_value:
                    best_value = value
                    best_move = move

        # Fallback: if something really weird happened
        if best_move is None:
            return random.choice(engine.legal_moves)

        return best_move

    # ================================
    # Evaluation / heuristic
    # ================================
    def _score_for_player(self, engine: BackgammonEngine, player: Player) -> float:
        """
        Convert a white-centric score to the perspective of `player`.
        """
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
        b = engine.board

        # 1) Instant win/lose
        if engine.winner == Player.WHITE:
            return 1e9
        if engine.winner == Player.BLACK:
            return -1e9

        pip_white = 0
        pip_black = 0

        # 2) Pip count on board
        for p in b.points:
            if p.owner == Player.WHITE:
                # White moves from low index -> 25
                pip_white += (25 - p.index) * p.count
            elif p.owner == Player.BLACK:
                # Black moves from high index -> 0
                pip_black += p.index * p.count

        # 3) Checkers on the bar: farthest from home
        pip_white += 25 * b.bar_white.count
        pip_black += 25 * b.bar_black.count

        # 4) Borne-off checkers – good for the side that owns them
        home_bonus = 25 * (b.home_white.count - b.home_black.count)

        # 5) Blots and made points
        blot_penalty = 0.0
        made_point_bonus = 0.0

        for p in b.points:
            if p.count == 1:
                # Blot
                if p.owner == Player.WHITE:
                    blot_penalty -= 1.5
                elif p.owner == Player.BLACK:
                    blot_penalty += 1.5
            elif p.count >= 2:
                # Made point
                if p.owner == Player.WHITE:
                    made_point_bonus += 0.5
                elif p.owner == Player.BLACK:
                    made_point_bonus -= 0.5

        # Lower pip count is better → use (pip_black - pip_white)
        pip_component = pip_black - pip_white

        return pip_component + home_bonus + blot_penalty + made_point_bonus
