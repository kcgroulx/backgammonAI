from enum import Enum
import random

# | 12 | 11 | 10 |  9 |  8 |  7 | BAR | 6  |  5 |  4 |  3 |  2 |  1 |
# | W  |    |    |    |  B |    |     | B  |    |    |    |    |  W |    
# | W  |    |    |    |  B |    |     | B  |    |    |    |    |  W |   
# | W  |    |    |    |  B |    |     | B  |    |    |    |    |    |
# | W  |    |    |    |    |    |     | B  |    |    |    |    |    |   
# | W  |    |    |    |    |    |     | B  |    |    |    |    |    |   
# |----|----|----|----|----|----|-----|----|----|----|----|----|----| 
# | B  |    |    |    |    |    |     | W  |    |    |    |    |    |   
# | B  |    |    |    |    |    |     | W  |    |    |    |    |    |   
# | B  |    |    |    | W  |    |     | W  |    |    |    |    |    |   
# | B  |    |    |    | W  |    |     | W  |    |    |    |    | B  |   
# | B  |    |    |    | W  |    |     | W  |    |    |    |    | B  |   
# | 13 | 14 | 15 | 16 | 17 | 18 | BAR | 19 | 20 | 21 | 22 | 23 | 24 |

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

class Home(Point):
    def __init__(self, index, owner=None, count=0):
        super().__init__(index=index, owner=owner, count=count)

class Bar(Point):
    def __init__(self, index, owner=None, count=0):
        super().__init__(index=index, owner=owner, count=count)

class Dice:
    def __init__(self):
        self.values = []

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

    def clear(self):
         for point in self.points:
            point.count = 0
            point.owner = None

    def setup(self):
        self.home.clear()
        self.bar.clear()
        self.clear()

        # Set up board to the standard state
        self.points[0].owner = Player.WHITE
        self.points[0].count = 2
        self.points[5].owner = Player.BLACK
        self.points[5].owner = 5
        self.points[7].owner = Player.BLACK
        self.points[7].owner = 3
        self.points[11].owner = Player.WHITE
        self.points[11].owner = 5
        self.points[12].owner = Player.BLACK
        self.points[12].owner = 5
        self.points[16].owner = Player.WHITE
        self.points[16].owner = 3
        self.points[18].owner = Player.WHITE
        self.points[18].owner = 5
        self.points[23].owner = Player.BLACK
        self.points[23].owner = 2

    def get_point(self, index) -> Point:
        if index < 1 or index > 24:
            raise ValueError("Index out of bounds")
        return self.points[index-1]
    
    # Checks if a point is in a players home
    def in_home(self, player:Player, point:Point) -> bool:
        if player == Player.WHITE:
            if point.index < 25 and point.index > 17:
                return True
            return False
        elif player == Player.BLACK:
            if point.index > 0 and point.index < 6:
                return True
            return False
    
    # Returns the point with a stone of player furthest from its home
    def get_point_furthest_from_home(self, player:Player) -> Point:
        # White: Start at index = 1
        if player == Player.WHITE:
            for point in self.points:
                if point.owner == Player.WHITE:
                    return point
        
        # Black: Start at index = 24
        if player == Player.BLACK:
            for point in reversed(self.points):
                if point.owner == Player.BLACK:
                    return point

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

class Move:
    def __init__(self, start_point = None, end_point = None, home = None, bar = None, hit=False):
        self.start_point = start_point
        self.end_point = end_point
        self.home = home
        self.bar = bar
        self.hit = hit

# Class contains engine
class BackgammonEngine:
    def __init__(self):
        # Board class
        self.board = Board()

        # Game state data
        self.dice = Dice()
        self.turn = Player.WHITE
        self.winner = None
        self.legal_moves = []

    def start(self):
        # Reinitialize board object
        self.board.setup()
        self.turn = None
        self.winner = None
        self.next_turn()
       
    def next_turn(self):
        # New game
        if self.turn == None:
            self.turn = Player.WHITE
        else:
            # Swaps turn
            if self.turn == Player.WHITE:
                self.turn = Player.BLACK
            else:
                self.turn = Player.WHITE

        self.dice.roll()
        self.generate_legal_moves()

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
                                self.legal_moves.append(Move(start_point=point, final_point=final_point))
                                continue

                            # Case 1b - opponent point (hit)
                            if final_point.owner != None and final_point.owner != self.turn and final_point.count == 1:
                                self.legal_moves.append(Move(start_point=point, final_point=final_point, hit=True))
                                continue

                        # Case 2 - Point to home
                        if self.board.are_all_player_stones_home(self.turn):
                            # Case 2a - Bearing off directly into home
                            if final_point_index == home.index:
                                self.legal_moves.append(Move(start_point=point, home=home))

                            # Case 2b - Bearing off with an overshoot
                            if point.index == self.board.get_point_furthest_from_home(self.turn).index:
                                if (final_point_index - home.index) * self.turn.value > 0:
                                    self.legal_moves.append(Move(start_point=point, home=home))
                                    continue
        elif bar.count > 0:
            pass
        # Case 3 - Bar to points
            # Case 3a - Empty or same player

            # Case 3b - Opponent player (hit)




    def make_move(self, move: Move):
        pass