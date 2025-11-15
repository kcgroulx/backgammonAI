import time
from backgammonBot import BackgammonBot
from backgammonEngine import BackgammonEngine, Player


class ArbiterResults:
    def __init__(self):
        self.bot1_wins = 0
        self.bot2_wins = 0
        self.simulation_time_ms = 0

class BackgammonArbiter:
    def __init__(self, bot1: BackgammonBot, bot2: BackgammonBot):
        self.bot1 = bot1
        self.bot2 = bot2

    def simulate(self, iterations, print_board=False, print_progress=False, delay=0.0):
        results = ArbiterResults()
        start_time = time.perf_counter()

        while iterations > 0:
            iterations -= 1
            self.simulate_single_game(white_bot=self.bot1, black_bot=self.bot2, results=results)

        results.simulation_time_ms = (time.perf_counter() - start_time) * 1000.0
        return results
    
    def simulate_single_game(self, white_bot:BackgammonBot, black_bot:BackgammonBot, results:ArbiterResults):
        engine = BackgammonEngine()
        engine.start()
        hits = 0
        moves = 0

        while engine.winner is None:
            # print(f"Turn: {engine.turn.name}    Moves{moves}")
            bot = white_bot if engine.turn is Player.WHITE else black_bot
            move = bot.calculate_move(engine=engine)
            engine.make_move(move)

            moves += 1
            if move.hit == True:
                hits += 1

        if engine.winner == Player.WHITE:
            results.bot1_wins += 1
        elif engine.winner == Player.BLACK:
            results.bot2_wins += 1
        else:
            raise ValueError("Unknown Winner Value")