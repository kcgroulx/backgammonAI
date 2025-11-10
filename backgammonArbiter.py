# File Name: arbiter.py
# Author: Kyle Groulx
# Date: November 9, 2025
# Brief: Responsible for arbiting a backgammon game between two bots

import backgammonBot
from backgammonBot import BackgammonBot, RandomBot
from backgammonEngine import BackgammonEngine, Player
import time

class ArbiterResults():
    def __init__(self):
        self.bot1_score = 0
        self.bot2_score = 0
        self.simulation_time_ms = 0

class BackgammonArbiter():
    def __init__(self, bot1:BackgammonBot, bot2:BackgammonBot):
        self.bot1 = bot1
        self.bot2 = bot2

    def simulate(self, iterations, print_board=False, print_progress=False, delay=0) -> ArbiterResults:
        results = ArbiterResults()
        current_iteration = 0

        start_time = time.perf_counter()

        white_bot = self.bot1
        black_bot = self.bot2

        while iterations > 0:
            iterations -= 1
            current_iteration += 1
            moves = 0
            hits = 0

            # Initialize a Backgammon game
            engine = BackgammonEngine()
            engine.start()

            while engine.winner == None:
                bot = white_bot if engine.turn == Player.WHITE else black_bot
                move = bot.calculate_move(engine=engine)
                engine.make_move(move)
                moves += 1
                if move.hit == True:
                    hits += 1

                if print_board:
                    print("\033[2J\033[H", end="")
                    print(engine.generate_ascii_image())
                    print(f"Game: {current_iteration}    Moves: {moves}    Hits: {hits}")
                    time.sleep(delay)

            if print_progress:
                print(f"Game: {current_iteration}    Moves: {moves}    Hits: {hits}")

            # Swap which bot is playing black and white
            white_bot, black_bot = black_bot, white_bot

            if engine.winner == Player.WHITE:
                if white_bot == self.bot1:
                    results.bot1_score += 1
                elif white_bot == self.bot2:
                    results.bot2_score += 1
            elif engine.winner == Player.BLACK:
                if black_bot == self.bot1:
                    results.bot1_score += 1
                elif black_bot == self.bot2:
                    results.bot2_score += 1
            else:
                raise ValueError("Invalid winner value")
            
        end_time = time.perf_counter()

        results.simulation_time_ms = (end_time - start_time) * 1000

        return results
