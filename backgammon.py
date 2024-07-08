from utils import check_zeros
import random

# Constants
EMPTY = 0
WHITE = 1
BLACK = -1


def point_to_index(point):
        return point - 1
    
def index_to_point(index):
    return index + 1

# LegalMove Class
class LegalMove:
    def __init__(self, start_point, end_point, die):
        self.start_point = start_point
        self.end_point = end_point
        self.die = die

# Backgammon class
# Backgammon board is a list indexed from 0-23.
# However, the user interacts with the board indexed from 1-24. with 0/25 being the home/bar
# In code, we differeciate theses two with _index or _point.
class Backgammon:
    def __init__(self):
        self.board = [0] * 24 # 24 points on the board
        self.bar = {WHITE: 0, BLACK: 0} # Bar for each player
        self.home = {WHITE: 0, BLACK: 0} # Home for each player
        self.turn = WHITE
        self.dice = []
        self.legal_moves: list[LegalMove] = []
        self.win = None

        self.start()
        self.roll_dice()
        self.generate_legal_moves()

    # Initialize board to starting position
    def start(self):
        # Reset board to initial conditions
        self.board = [0] * 24
        self.bar = {WHITE: 0, BLACK: 0}
        self.home = {WHITE: 0, BLACK: 0}
        self.board[0] = 2
        self.board[5] = -5
        self.board[7] = -3
        self.board[11] = 5
        self.board[12] = -5
        self.board[16] = 3
        self.board[18] = 5
        self.board[23] = -2

    # Randomly roll dice
    def roll_dice(self):
        # Get both die between 1 and 6
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        # Check if dice are the same
        if die1 == die2:
            self.dice = [die1] * 4
        else:
            self.dice = [die1, die2]
        self.dice.sort()

    # Flips turn
    def next_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        self.roll_dice()
        self.generate_legal_moves()

    # Gets color
    def get_color(self, index):
        if self.board[index] == 0:
            return EMPTY
        if self.board[index] > 0:
            return WHITE
        if self.board[index] < 0:
            return BLACK

    # Generates legal moves for a given die and index
    def generate_legal_moves(self):
        # Clear legal_moves list
        self.legal_moves = []

        # Interate through each die
        for die in self.dice:
            # Interate through each index on the board
            for start_index in range(len(self.board)):
                # Check if start index is the same color as turn
                start_index_color = self.get_color(start_index)
                if start_index_color != self.turn:
                    continue

                # Get and verify end_index
                end_index = start_index + (die * self.turn)
                if end_index > 23 or end_index < 0:
                    continue # TODO: Skip for now
                end_index_color = self.get_color(end_index)

                # Convert index to point
                start_point = index_to_point(start_index)
                end_point = index_to_point(end_index)

                # If end_index is empty or the same color
                if end_index_color == EMPTY or end_index_color == self.turn:
                    self.legal_moves.append(LegalMove(start_point, end_point, die))

    def check_legal_move(self, start_point, end_point):
        # Check if move exists in legal moves list
        for legal_move in self.legal_moves:
            if legal_move.start_point == start_point and legal_move.end_point == end_point:
                return legal_move
        # Move not in legal move list
        return False

    # Removes a die from the self.dice list
    def remove_die(self, die):
        if die in self.dice:
            self.dice.remove(die)
        else:
            raise ValueError(f"Die value {die} not in dice list")

    # Moves piece on board
    def move_piece(self, start_point, end_point):
        # Verify move is legal
        legal_move = self.check_legal_move(start_point, end_point)
        if legal_move == False:
            return False

        # Convert to index
        start_index = point_to_index(start_point)
        end_index = point_to_index(end_point)
        end_index_color = self.get_color(end_index)

        # case: empty or same color
        if end_index_color == EMPTY or end_index_color == self.turn: 
            # Move stone
            self.board[start_index] -= self.turn
            self.board[end_index] += self.turn
        self.remove_die(legal_move.die)
        self.generate_legal_moves()

        # Next turn if no more dice
        if len(self.dice) == 0:
            self.next_turn()

        return True
