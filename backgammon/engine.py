# File Name: backgammon_engine.py
# Author: Kyle Groulx
# Date: November 7, 2025
# Brief: Simple implementation of a backgammon engine

from enum import Enum
import random
import copy

# ==============================================================
# | 12| 11| 10|  9|  8|  7| BAR |  6|  5|  4|  3|  2|  1| HOME |
# |===|===|===|===|===|===|=====|===|===|===|===|===|===|======|
# | W |   |   |   | B |   |     | B |   |   |   |   | W |      |
# | W |   |   |   | B |   |     | B |   |   |   |   | W |      |
# | W |   |   |   | B |   |     | B |   |   |   |   |   |      |
# | W |   |   |   |   |   |     | B |   |   |   |   |   |      |
# | W |   |   |   |   |   |     | B |   |   |   |   |   |      |
# |---|---|---|---|---|---|-----|---|---|---|---|---|---|------|
# | B |   |   |   |   |   |     | W |   |   |   |   |   |      |
# | B |   |   |   |   |   |     | W |   |   |   |   |   |      |
# | B |   |   |   | W |   |     | W |   |   |   |   |   |      |
# | B |   |   |   | W |   |     | W |   |   |   |   | B |      |
# | B |   |   |   | W |   |     | W |   |   |   |   | B |      |
# |===|===|===|===|===|===|=====|===|===|===|===|===|===|======|
# | 13| 14| 15| 16| 17| 18| BAR | 19| 20| 21| 22| 23| 24| HOME |
# ==============================================================

# White Bar : 0
# Black Bar: 25
# White Home: 25
# Black Home: 0

class Player(Enum):
    WHITE = 1
    BLACK = -1

class Point:
    def __init__(self, index, owner=None, count=0):
        self.index = index
        self.owner = owner
        self.count = count

    def __deepcopy__(self, memo):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj
        new_obj.index = self.index
        new_obj.owner = self.owner
        new_obj.count = self.count
        return new_obj

    def remove_stone(self):
        if self.count > 0:
            self.count -= 1
            if self.count == 0:
                self.owner = None
        else:
            raise ValueError("Trying to remove from an empty point")
        
    def add_stone(self, owner):
        if self.owner == None or self.owner == owner:
            self.count += 1
        elif self.owner != owner and self.count == 1:
            self.count = 1
        else:
            raise ValueError("add_stone")
        self.owner = owner

    def set_stones(self, count, owner):
        self.owner = owner
        self.count = count

    def clear(self):
        self.owner = None
        self.count = 0

class Home(Point):
    def __init__(self, index, owner=None, count=0):
        super().__init__(index=index, owner=owner, count=count)

class Bar(Point):
    def __init__(self, index, owner=None, count=0):
        super().__init__(index=index, owner=owner, count=count)

class Dice:
    def __init__(self):
        self.values = []
    
    def __deepcopy__(self, memo):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj
        new_obj.values = list(self.values)
        return new_obj

    def roll(self):
        self.values.clear()

        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        # Check if we rolled two of the same dice
        if die1 == die2:
            # If we rolled a double, we get 4 die
            self.values.append(die1)
            self.values.append(die1)
            self.values.append(die1)
            self.values.append(die1)
        else:
            self.values.append(die1)
            self.values.append(die2)
    
    def remove_die(self, die):
        self.values.remove(die)

class Board:
    def __init__(self):
        # Points 1-24
        self.points = [Point(index=i+1) for i in range(24)]

        # Bars 0 and 25
        self.bar_white = Bar(index=0, owner=Player.WHITE)
        self.bar_black = Bar(index=25, owner=Player.BLACK)

        # Home 25 and 0
        self.home_white = Home(index=25, owner=Player.WHITE)
        self.home_black = Home(index=0, owner=Player.BLACK)
    
    def __deepcopy__(self, memo):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj

        new_obj.points = [copy.deepcopy(p, memo) for p in self.points]
        new_obj.bar_white = copy.deepcopy(self.bar_white, memo)
        new_obj.bar_black = copy.deepcopy(self.bar_black, memo)
        new_obj.home_white = copy.deepcopy(self.home_white, memo)
        new_obj.home_black = copy.deepcopy(self.home_black, memo)
        return new_obj

    def clear(self):
        for point in self.points:
            point.clear()
        self.bar_white.clear()
        self.bar_black.clear()
        self.home_white.clear()
        self.home_black.clear()
        self.bar_white.owner = Player.WHITE
        self.bar_black.owner = Player.BLACK
        self.home_white.owner = Player.WHITE
        self.home_black.owner = Player.BLACK

    def setup(self):
        # Clear board
        self.clear()

        # Set up board to the standard state
        self.points[0].set_stones(2, Player.WHITE)
        self.points[5].set_stones(5, Player.BLACK)
        self.points[7].set_stones(3, Player.BLACK)
        self.points[11].set_stones(5, Player.WHITE)
        self.points[12].set_stones(5, Player.BLACK)
        self.points[16].set_stones(3, Player.WHITE)
        self.points[18].set_stones(5, Player.WHITE)
        self.points[23].set_stones(2, Player.BLACK)

    def get_point(self, index) -> Point:
        if index < 1 or index > 24:
            raise ValueError("Index out of bounds")
        return self.points[index-1]
    
    # Returns the point with a stone of player furthest from its home
    def get_point_furthest_from_home(self, player:Player) -> Point:
        # White: Start at index = 1
        if player == Player.WHITE:
            for point in self.points:
                if point.owner == Player.WHITE:
                    return point
            return self.home_white
        
        # Black: Start at index = 24
        if player == Player.BLACK:
            for point in reversed(self.points):
                if point.owner == Player.BLACK:
                    return point
            return self.home_black

        return None

    # Returns true if all stones of player are home, false otherwise
    def are_all_player_stones_home(self, player) -> bool:
        if player == Player.WHITE:
            if self.get_point_furthest_from_home(Player.WHITE).index > 18:
                return True
            return False
        elif player == Player.BLACK:
            if self.get_point_furthest_from_home(Player.BLACK).index < 7:
                return True
            return False
        else:
            raise ValueError("Unknown Player enum")
    
    # Returns how far a point is from its home
    def distance_from_home(self, point:Point) -> int:
        if point.owner == Player.WHITE:
            return 25 - point.index
        elif point.owner == Player.BLACK:
            return point.index
        else:
            raise ValueError

class Move:
    def __init__(self, start_point:Point, final_point:Point, die, hit=False):
        self.start_point = start_point
        self.final_point = final_point
        self.hit = hit
        self.die = die
    
    def __deepcopy__(self, memo):
        # Usually not used by engine deepcopy; provided for safety
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj
        # Keep references (do NOT deepcopy points here)
        new_obj.start_point = self.start_point
        new_obj.final_point = self.final_point
        new_obj.hit = self.hit
        new_obj.die = self.die
        return new_obj

    def get_player(self) -> Player:
        return self.start_point.owner

# Class contains engine
class BackgammonEngine:
    def __init__(self):
        # Board class
        self.board = Board()

        # Game state data
        self.dice = Dice()
        self.turn = Player.WHITE
        self.winner = None
        self.legal_moves: list[Move] = []

    def __deepcopy__(self, memo):
        cls = self.__class__
        new_obj = cls.__new__(cls)
        memo[id(self)] = new_obj

        # Deep copy the independent game state
        new_obj.board = copy.deepcopy(self.board, memo)
        new_obj.dice = copy.deepcopy(self.dice, memo)

        # Enums (Player) are immutable/safe to reuse
        new_obj.turn = self.turn
        new_obj.winner = self.winner

        # Never copy old legal moves; rebuild for the new board/dice state
        new_obj.legal_moves = []
        new_obj.generate_legal_moves()
        return new_obj

    def start(self):
        # Reinitialize board object
        self.board.setup()
        self.turn = None
        self.winner = None
        self.next_turn()
       
    def next_turn(self, roll=True):
        # Swaps turn
        if self.turn == None:
            self.turn = Player.BLACK
        elif self.turn == Player.WHITE:
            self.turn = Player.BLACK
        else:
            self.turn = Player.WHITE

        if roll == True:
            self.dice.roll()
            self.generate_legal_moves()
            if len(self.legal_moves) == 0:
                self.next_turn()

    def generate_legal_moves(self):
        self.legal_moves.clear()
        # Get the home and bar of the player's turn
        home = self.board.home_white if self.turn == Player.WHITE else self.board.home_black
        bar = self.board.bar_white if self.turn == Player.WHITE else self.board.bar_black

        # Loop through the points if bar is empty
        if bar.count == 0:
            for point in self.board.points:
                # Check if point owner is the same as the turn owner
                if point.owner == self.turn:
                    # Loop through die
                    for die in self.dice.values:
                        final_point_index = point.index + (die * self.turn.value)

                        # Case 1 - point to point
                        if final_point_index < 25 and final_point_index > 0:
                            final_point = self.board.get_point(final_point_index)

                            # Case 1a - empty or same player
                            if final_point.owner == None or final_point.owner == self.turn:
                                self.legal_moves.append(Move(start_point=point, final_point=final_point, die=die))
                                continue

                            # Case 1b - opponent point (hit)
                            if final_point.owner != None and final_point.owner != self.turn and final_point.count == 1:
                                self.legal_moves.append(Move(start_point=point, final_point=final_point, die=die, hit=True))
                                continue

                        # Case 2 - Point to home
                        if self.board.are_all_player_stones_home(self.turn):
                            # Case 2a - Bearing off directly into home
                            if final_point_index == home.index:
                                self.legal_moves.append(Move(start_point=point, final_point=home, die=die))

                            # Case 2b - Bearing off with an overshoot
                            if point.index == self.board.get_point_furthest_from_home(self.turn).index:
                                if (final_point_index - home.index) * self.turn.value > 0:
                                    self.legal_moves.append(Move(start_point=point, final_point=home, die=die))
                                    continue
        # Case 3 - Bar to points
        elif bar.count > 0:
            for die in self.dice.values:
                final_point_index = bar.index + (die * self.turn.value)
                final_point = self.board.get_point(final_point_index)
            
                # Case 3a - Empty or same player
                if final_point.owner == None or final_point.owner == self.turn:
                    self.legal_moves.append(Move(start_point=bar, final_point=final_point, die=die))
                    continue

                # Case 3b - Opponent player (hit)
                if final_point.owner != None and final_point.owner != self.turn and final_point.count == 1:
                    self.legal_moves.append(Move(start_point=bar, final_point=final_point, die=die, hit=True))
                    continue

    def make_move(self, move: Move):
        # Check if move exists in legal_moves list
        if any(legal_move is move for legal_move in self.legal_moves) == False:
            raise ValueError("Move not found in legal_moves")
        
        if self.winner != None:
            raise ValueError("Already a winner")

        # Decrement start point count
        move.start_point.remove_stone()

        # Add stone to end point
        move.final_point.add_stone(self.turn)

        # If hit, add stone to enemy bar
        if move.hit == True:
            if self.turn == Player.WHITE:
                self.board.bar_black.count += 1
            else:
                self.board.bar_white.count += 1

        # Check for win
        if self.turn == Player.WHITE and self.board.get_point_furthest_from_home(Player.WHITE).index == 25:
            self.winner = Player.WHITE
        elif self.turn == Player.BLACK and self.board.get_point_furthest_from_home(Player.BLACK).index == 0:
            self.winner = Player.BLACK

        # Remove die used for move
        self.dice.remove_die(move.die)

        if len(self.dice.values) == 0:
            self.next_turn()
        else:
            self.generate_legal_moves()
            if len(self.legal_moves) == 0:
                self.next_turn()

    # Attempts to make move based on provided start and end index
    # Returns True if successful and False otherwise
    def attempt_move(self, start_index, end_index) -> bool:
        # Check for winner
        if self.winner != None:
            return False

        # Search if move exists within the legal_moves list
        for move in self.legal_moves:
            if move.start_point.index == start_index and move.final_point.index == end_index:
                self.make_move(move=move)
                return True
        return False
    

    def swap_player_value(self, player: Player) -> Player:
        return {
            Player.WHITE: Player.BLACK,
            Player.BLACK: Player.WHITE
        }[player]

    # Used for debugging or playing inside the terminal
    def generate_ascii_image(self) -> str:
        CELL_W, BAR_W, HOME_W = 3, 5, 6

        def pad(s: str, w: int) -> str:
            s = s[:w] if len(s) > w else s
            return s + (" " * (w - len(s)))

        def sym(owner):
            return " " if owner is None else ("W" if owner == Player.WHITE else "B")

        # Point cells
        def top_cell(p: Point, r: int) -> str:
            c = p.count
            if c == 0:
                return " " * CELL_W
            s = sym(p.owner)
            if c <= 5:
                return " " + s + " " if r < c else " " * CELL_W
            return pad(f"{s}{c:>2}" if r == 4 else f" {s} ", CELL_W)

        def bot_cell(p: Point, r: int) -> str:
            c = p.count
            if c == 0:
                return " " * CELL_W
            s = sym(p.owner)
            if c <= 5:
                return " " + s + " " if r >= 5 - c else " " * CELL_W
            return pad(f"{s}{c:>2}" if r == 0 else f" {s} ", CELL_W)

        # Bar/Home cells
        def bar_top_cell(w_count: int, r: int) -> str:
            """Top bar shows White (since White re-enters downward)."""
            if w_count == 0:
                return " " * BAR_W
            if w_count <= 5:
                return pad("  W  " if r < w_count else "", BAR_W)
            return pad(f" W{w_count:>2}" if r == 4 else "  W  ", BAR_W)

        def bar_bot_cell(b_count: int, r: int) -> str:
            """Bottom bar shows Black (since Black re-enters upward)."""
            if b_count == 0:
                return " " * BAR_W
            if b_count <= 5:
                return pad("  B  " if r >= 5 - b_count else "", BAR_W)
            return pad(f" B{b_count:>2}" if r == 0 else "  B  ", BAR_W)

        def home_top_cell(b_off: int, r: int) -> str:
            """Top home shows Black borne-off checkers."""
            if b_off == 0:
                return " " * HOME_W
            if b_off <= 5:
                return pad("  B   " if r < b_off else "", HOME_W)
            return pad(f" B{b_off:>2} " if r == 4 else "  B   ", HOME_W)

        def home_bot_cell(w_off: int, r: int) -> str:
            """Bottom home shows White borne-off checkers."""
            if w_off == 0:
                return " " * HOME_W
            if w_off <= 5:
                return pad("  W   " if r >= 5 - w_off else "", HOME_W)
            return pad(f" W{w_off:>2} " if r == 0 else "  W   ", HOME_W)

        # Points in display order
        top_points = [self.board.get_point(i) for i in range(12, 0, -1)]
        bot_points = [self.board.get_point(i) for i in range(13, 25)]

        # Tally values
        barW = self.board.bar_white.count
        barB = self.board.bar_black.count
        offW = self.board.home_white.count
        offB = self.board.home_black.count

        # Header/footer builder
        def _index_segment(a: int, b: int):
            step = 1 if b >= a else -1
            return range(a, b + step, step)

        def header_line(left_start, left_end, right_start, right_end) -> str:
            left_nums = _index_segment(left_start, left_end)
            right_nums = _index_segment(right_start, right_end)
            left  = "|" + "|".join(f"{i:>3}" for i in left_nums) + "|"
            right = "|" + "|".join(f"{i:>3}" for i in right_nums) + "|"
            return f"{left} BAR {right} HOME |"

        header = header_line(12, 7, 6, 1)
        footer = header_line(13, 18, 19, 24)

        border  = "=" * len(header)
        sep_top = "|" + ("===|" * 6) + "=====|" + ("===|" * 6) + "======|"
        sep_mid = "|" + ("---|" * 6) + "-----|" + ("---|" * 6) + "------|"

        # Build the board
        lines = []
        lines.append(border)
        lines.append(header)
        lines.append(sep_top)

        # Top half (5 rows)
        for r in range(5):
            row = "|"
            for p in top_points[:6]:
                row += top_cell(p, r) + "|"
            row += bar_top_cell(barW, r) + "|"
            for p in top_points[6:]:
                row += top_cell(p, r) + "|"
            row += home_top_cell(offB, r) + "|"
            lines.append(row)

        lines.append(sep_mid)

        # Bottom half (5 rows)
        for r in range(5):
            row = "|"
            for p in bot_points[:6]:
                row += bot_cell(p, r) + "|"
            row += bar_bot_cell(barB, r) + "|"
            for p in bot_points[6:]:
                row += bot_cell(p, r) + "|"
            row += home_bot_cell(offW, r) + "|"
            lines.append(row)

        lines.append(sep_top)
        lines.append(footer)
        lines.append(border)

        # Dice + turn + winner
        dice_str = " ".join(str(v) for v in self.dice.values) or "No dice rolled"
        lines.append("")
        lines.append(f"Turn: {self.turn.name:<8}    Dice: {dice_str}")

        winner_text = f" WINNER: {self.winner.name} " if self.winner else " WINNER: (none) "
        lines.append(winner_text.center(len(border), "="))

        return "\n".join(lines)
