import time

if __package__ is None or __package__ == "":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    import backgammon.arbiter as arbiter
    import backgammon.engine as engine
    from backgammon.bots import GPTHeuristicBot, RandomBot, SimpleHeuristicBot
else:  # pragma: no cover - module execution path
    from . import arbiter, engine
    from .bots import GPTHeuristicBot, RandomBot, SimpleHeuristicBot


def main():
    game_engine = engine.BackgammonEngine()
    game_engine.start()

    bot = RandomBot()

    bot1 = GPTHeuristicBot()
    bot2 = SimpleHeuristicBot()

    match_arbiter = arbiter.BackgammonArbiter(bot1=bot1, bot2=bot2)

    results = match_arbiter.simulate(iterations=10)

    print(
        f"Results: {bot1.name} wins: {results.bot1_wins}    "
        f"{bot2.name} wins: {results.bot2_wins}   Simulation Time (ms): {results.simulation_time_ms}"
    )


if __name__ == "__main__":
    main()
