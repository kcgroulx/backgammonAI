from abc import ABC, abstractmethod
from backgammon.engine import BackgammonEngine, Move, Player, Point

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