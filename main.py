# See BackgammonEngine.py for implementation
import backgammonEngine
from backgammonEngine import Player
import backgammonBot
import time
import backgammonArbiter

engine = backgammonEngine.BackgammonEngine()
engine.start()

bot = backgammonBot.RandomBot()

# For testing, not final

# def get_user_inputs():
#     start, end = map(int, input("Enter start and end points: ").split())
#     if engine.attempt_move(start, end) == False:
#         print("invalid move")

# while engine.winner == None:
#     while engine.turn == Player.WHITE and engine.winner == None:
#         print("\033[2J\033[H", end="")
#         print(engine.generate_ascii_image())
#         get_user_inputs()

#     while engine.turn == Player.BLACK and engine.winner == None:
#         print("\033[2J\033[H", end="")
#         print(engine.generate_ascii_image())
#         move = bot.calculate_move(engine=engine)
#         engine.make_move(move)
#         time.sleep(1)


bot1 = backgammonBot.SimpleHeuristicBot()
bot2 = backgammonBot.SimpleHeuristicBot()
arbiter = backgammonArbiter.BackgammonArbiter(bot1=bot1, bot2=bot2)

results = arbiter.simulate(iterations=100, print_progress=True)

print(f"Results: {bot1.name} wins: {results.bot1_score}    {bot2.name} wins: {results.bot2_score}   Simulation Time (ms): {results.simulation_time_ms}")
