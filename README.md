# Backgammon Engine & Bots

A pure-Python playground for experimenting with Backgammon AI ideas.  
It bundles a feature-complete game engine, a match arbiter for headless
simulation, and a growing zoo of bot implementations ranging from random
play to light-weight heuristics.

## Features
- Full Backgammon rules: dice rolling (incl. doubles), bar/home handling,
  move validation, bearing off, and win detection (`backgammon/engine.py`).
- Bot framework with a reusable `BackgammonBot` base class plus:
  - `RandomBot`: picks a legal move uniformly at random.
  - `SimpleHeuristicBot`: scores moves using board progress and blot safety.
  - `GPTHeuristicBot`: a richer pip-based evaluation with bar/home bonuses.
- Match arbiter capable of simulating hundreds of headless games to compare bots.
- CLI entry point (`backgammon/main.py`) that runs a sample tournament and
  reports aggregate results.

## Project Layout
```
backgammonAI/
├── backgammon/
│   ├── __init__.py
│   ├── arbiter.py          # Match simulation driver
│   ├── engine.py           # Core Backgammon engine
│   ├── main.py             # Example CLI entry point
│   └── bots/
│       ├── __init__.py
│       ├── base.py         # BackgammonBot abstract base class
│       ├── random_bot.py
│       ├── simple_heuristic_bot.py
│       └── gpt_heuristic_bot.py
└── tests/                  # (placeholder for future test coverage)
```

## Requirements
- Python 3.11+ (tested with CPython 3.13)
- No third-party dependencies; everything lives in the standard library.

## Getting Started
1. **Clone and enter the repo**
   ```bash
   git clone https://github.com/<you>/backgammonAI.git
   cd backgammonAI
   ```
2. **Run the sample tournament**
   ```bash
   python -m backgammon.main
   ```
   Using `-m` is the preferred (package-aware) form. For a quick local run you
   can also execute `python backgammon/main.py` from the repo root; the script
   temporarily amends `sys.path` to keep imports working.

The CLI instantiates `GPTHeuristicBot` vs `SimpleHeuristicBot`, simulates 500
games via the arbiter, and prints win counts plus total simulation time.

## Using the Engine Programmatically
```python
from backgammon.engine import BackgammonEngine
from backgammon.bots import RandomBot
from backgammon.arbiter import BackgammonArbiter

engine = BackgammonEngine()
engine.start()

arbiter = BackgammonArbiter(RandomBot(), RandomBot())
results = arbiter.simulate(iterations=1000)
print(results.bot1_wins, results.bot2_wins)
```

## Creating Your Own Bot
1. Derive from `BackgammonBot` (`backgammon/bots/base.py`).
2. Implement `calculate_move(self, engine)` and return one of
   `engine.legal_moves`. The base class exposes helper methods such as
   `calculate_board_score` and `point_score`.
3. Drop the new bot class into `backgammon/bots/`, import it in
   `backgammon/bots/__init__.py`, and wire it up in `main.py` or your own runner.

Both heuristic examples (`simple_heuristic_bot.py` and `gpt_heuristic_bot.py`)
serve as templates that show how to clone the engine, attempt candidate moves,
and evaluate the resulting boards without mutating the real game state.

## Testing
The `tests/` directory is reserved for upcoming unit and integration tests.
Until then, rely on the CLI tournament or light-weight scripts for regression
checks. When adding new features, consider seeding the `tests/` folder with
pytest suites that cover engine rules, bot evaluations, and arbiter flow.
