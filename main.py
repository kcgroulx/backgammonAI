# See BackgammonEngine.py for implementation
import backgammonEngine
from backgammonEngine import Player
import backgammonBot
import time
import backgammonArbiter

engine = backgammonEngine.BackgammonEngine()
engine.start()

bot = backgammonBot.RandomBot()

bot1 = backgammonBot.GPTHeuristicBot()
bot2 = backgammonBot.SimpleHeuristicBot()

arbiter = backgammonArbiter.BackgammonArbiter(bot1=bot1, bot2=bot2)

results = arbiter.simulate(iterations=500)

print(f"Results: {bot1.name} wins: {results.bot1_wins}    {bot2.name} wins: {results.bot2_wins}   Simulation Time (ms): {results.simulation_time_ms}")
