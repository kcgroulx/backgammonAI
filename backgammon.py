from utils import check_zeros

# Constants
EMPTY = 0
WHITE = 1
BLACK = -1


def point_to_index(point):
        return point - 1
    
def index_to_point(index):
    return index + 1

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
        self.legal_moves = []

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

    def next_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_color(self, pos):
        if self.board[pos] == 0:
            return EMPTY
        if self.board[pos] > 0:
            return WHITE
        if self.board[pos] < 0:
            return BLACK
        
    def generate_legal_moves(self, dice):
        self.legal_moves = []
        for die in dice:
            for index in range(len(self.board)):
                if self.get_color(index) == self.turn:
                    end_index = index + (die * self.turn)
                    end_color = self.get_color(end_index)
                    if end_color == EMPTY:
                        new_legal_move = (index_to_point(index), index_to_point(end_index))
                        self.legal_moves.append(new_legal_move)


    def move(self, start_point, end_point):
        move = (start_point, end_point)
        if move not in self.legal_moves:
            return False
        start_index = point_to_index(start_point)
        end_index = point_to_index(start_point)

        self.board[start_index] -= self.turn
        self.board[end_index] += self.turn

        