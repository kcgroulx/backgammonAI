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
    

# Selects the highest board score from the best combination of available dice
class BestDiceCombinationHeuristicBot(BackgammonBot):
    def __init__(self):
        super().__init__()
        self.name = "BestDiceCombinationHeuristicBot"

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

            new_score = self.calculate_best_score_from_dice_combination(engine=new_engine, turn=engine.turn)

            if engine.turn == Player.WHITE and new_score > score:
                selected_move = move
                score = new_score
            elif engine.turn == Player.BLACK and new_score < score:
                selected_move = move
                score = new_score
        return selected_move

    
    # Finds the score from the BEST combination of dice moves
    def calculate_best_score_from_dice_combination(self, engine:BackgammonEngine, turn:Player) -> float:
        # End case
        if engine.turn != turn or len(engine.legal_moves):
            # If turn has been updated or there are no more legal moves, evaluate the current board score and return it
            return super().calculate_board_score(engine=engine)
        
        # We are not at the end yet, keep going
        for move in engine.legal_moves:
            new_engine = copy.deepcopy(engine)

            if new_engine.attempt_move(move.start_point.index, move.final_point.index) == False:
                raise ValueError("Unable to move stone")

            return self.calculate_best_score_from_dice_combination(new_engine, new_engine.turn)

