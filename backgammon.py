from utils import check_zeros, EMPTY, WHITE, BLACK
from gui import print_board

# Backgammon class
class Backgammon:
    def __init__(self):
        self.board = [0] * 24 # 24 points on the board
        self.bar = {WHITE: 0, BLACK: 0} # Bar for each player
        self.turn = WHITE

    def start(self):
        self.board = [0] * 24
        self.board[0] = 2
        self.board[5] = -5
        self.board[7] = -3
        self.board[11] = 5
        self.board[12] = -5
        self.board[16] = 3
        self.board[18] = 5
        self.board[23] = -2
        self.bar = {WHITE: 0, BLACK: 0}

    def next_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def check_color(self, pos):
        if self.board[pos] == 0:
            return EMPTY
        if self.board[pos] > 0:
            return WHITE
        if self.board[pos] < 0:
            return BLACK
        
    def move(self, start, end):
        # If not on the same color as the turn, return False
        start_color = self.check_color(start)
        if start_color != self.turn:
            return False
        
        # Check end color
        end_color = self.check_color(end)
        if end_color != self.turn and end_color != EMPTY:
            # If only 1 stone, move to bar
            if abs(self.board[end]) == 1:
                # Move stone to bar
                self.bar[end_color] += 1
                self.board[end] = self.turn
                self.next_turn()
                return True
            # If more than 1 stone, return False
            else:
                return False

        # Empty, so move stone
        self.board[end] += self.turn
        self.board[start] -= self.turn
        self.next_turn()
        return True


        

backgammon = Backgammon()
backgammon.start()
print_board(backgammon)

backgammon.move(0, 1)

print_board(backgammon)

backgammon.move(5, 1)

print_board(backgammon)