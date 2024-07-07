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

# LegalMoves class
# Contains a list of legal moves for a given die
class LegalMoves:
    def __init__(self, legal_moves, die):
        self.legal_moves = legal_moves
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
        self.legal_moves = []
        self.win = None

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
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        if die1 == die2:
            self.dice = [die1] * 4
        else:
            self.dice = [die1, die2]

    # Flips turn
    def next_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    # Gets color
    def get_color(self, index):
        if self.board[index] == 0:
            return EMPTY
        if self.board[index] > 0:
            return WHITE
        if self.board[index] < 0:
            return BLACK

    # Generates legal move for a given die and index
    def generate_legal_move(self, die, index):
        # Check if we are on a stone of the current player
        if self.get_color(index) == self.turn:
            end_index = index + (die * self.turn)
            end_color = self.get_color(end_index)
            
            # If end index is empty or same color
            if end_color == EMPTY or end_color == self.turn:
                return (index_to_point(index), index_to_point(end_index))

    # Generates all legal moves for the game state
    def generate_legal_moves(self):
        # Clear legal moves
        self.legal_moves = []

        # Interate through each die
        for die in self.dice:
            legal_moves_list = []
            # Append legal moves for each point
            for index in range(len(self.board)):
                legal_moves_list.append(self.generate_legal_move(die, index))
            
            # Append legal moves for this die
            self.legal_moves.append(LegalMoves(legal_moves_list, die))        

    def move_piece(self, move):
        # If move is not legal, return False
        if move not in self.legal_moves:
            return False
        
        # Get points and index
        start_point, end_point = move
        start_index = point_to_index(start_point)
        end_index = point_to_index(end_point)

        # Move stone
        self.board[start_index] -= self.turn
        self.board[end_index] += self.turn

        # Remove die for this move

        # If no more dice, next turn
        if len(self.dice) == 0:
            self.next_turn()