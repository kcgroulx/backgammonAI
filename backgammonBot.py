import backgammonEngine
from backgammonEngine import BackgammonEngine, Move, Player
from abc import ABC, abstractmethod
import random
import copy

class BackgammonBot(ABC):
    def __init__(self):
        pass

    def calculate_move(self, engine: BackgammonEngine) -> Move:
        pass

    # Simple board score: 
    # Positive means better for white
    # Negative means better for black
    def calculate_board_score(self, engine: BackgammonEngine) -> float:
        score = 0.0

        # Check homes
        score += engine.board.home_white.count * 25.0
        score -= engine.board.home_black.count * 25.0

        # Add all points
        for point in engine.board.points:
            if point.owner == Player.WHITE:
                score += point.index * point.count
            elif point.owner == Player.BLACK:
                score -= (25 - point.index) * point.count
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
    

# Calculates the board score for each move. Iterates through each dice
# Selects the highest board score  
class DepthHeuristicBot(BackgammonBot):
    def __init__(self):
        super().__init__()
        self.name = "DepthHeuristicBot"

    def find_move_with_highest_score(self, engine) -> Move:
        if len(engine.legal_moves) == 0:
            raise ValueError("Cannot select from empty legal moves")
        raise NotImplementedError
        
