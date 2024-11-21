from utils import check_zeros
import random

# Constants
EMPTY = 0
WHITE = 1
BLACK = -1
NUM_OF_POINTS = 26 


def point_to_index(point):
        return point - 1
    
def index_to_point(index):
    return index + 1

def opposite_color(color):
    return -color

def num_of_pieces(point):
    return abs(point)

# Move Class
class Move:
    def __init__(self, start_point, end_point, die, piece_hit = False):
        self.start_point = start_point
        self.end_point = end_point
        self.die = die 
        self.piece_hit = piece_hit

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
        self.legal_moves: list[Move] = []
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
        
        # If there are no legal moves, next turn
        if len(self.legal_moves) == 0:
            print("No legal moves") # TODO: Debug. Remove later
            self.next_turn()

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
            # Check if there is a piece on the bar
            if self.bar[self.turn] > 0:
                # Check if the end_index is valid
                start_point = 0
                if self.turn == WHITE:
                    end_index = die - 1
                else: # BLACK
                    start_point = 25
                    end_index = 24 - die
                
                # Convert index to point
                end_point = index_to_point(end_index)
                end_index_color = self.get_color(end_index)

                # Case: end_index is empty or same color
                if end_index_color == EMPTY or end_index_color == self.turn:
                    self.legal_moves.append(Move(start_point, end_point, die, piece_hit=False))
                # Case: end_index is opposite color
                elif end_index_color == opposite_color(self.turn):
                    # Can only hit if there is one piece
                    if num_of_pieces(self.board[end_index]) == 1:
                        self.legal_moves.append(Move(start_point, end_point, die, piece_hit=True))
 
                continue # Continue since we can only move from the bar


            # Iterate through the board
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

                # Case: end_index is empty or same color
                if end_index_color == EMPTY or end_index_color == self.turn:
                    self.legal_moves.append(Move(start_point, end_point, die, piece_hit=False))
                # Case: end_index is opposite color
                elif end_index_color == opposite_color(self.turn):
                    # Can only hit if there is one piece
                    if num_of_pieces(self.board[end_index]) == 1:
                        self.legal_moves.append(Move(start_point, end_point, die, piece_hit=True))

    # Checks if start_point and end_point is in the legal moves list, if it is, return the move else return False
    def get_legal_move(self, start_point, end_point):
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
    def user_move_piece(self, start_point, end_point):
        # Verify move is legal
        legal_move = self.get_legal_move(start_point, end_point)
        if legal_move == False:
            return False # Move is not legal

        end_index = point_to_index(end_point)

        # Remove piece for start point
        if start_point == 0 or start_point == 25:
            if start_point == 0:
                self.bar[WHITE] -= 1
            else:
                self.bar[BLACK] -= 1
        else:
            # Convert to index notiation
            start_index = point_to_index(start_point)
            self.board[start_index] -= self.turn

        # Add piece for end point
        # Case: No stone hit
        if legal_move.piece_hit == False:
            self.board[end_index] += self.turn

        # Case: Stone hit
        elif legal_move.piece_hit == True:
            self.board[end_index] = self.turn
            self.bar[opposite_color(self.turn)] += 1

        self.remove_die(legal_move.die)
        self.generate_legal_moves()

        # Next turn if no more dice or legal moves
        if len(self.dice) == 0 or len(self.legal_moves) == 0:
            self.next_turn()

        return True
 