# See Backgammon_engine for implementation
import backgammon_engine
from backgammon_engine import Player

engine = backgammon_engine.BackgammonEngine()

engine.start()

print(engine.generate_ascii_image())