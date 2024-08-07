from utils import check_zeros, switch_values
from backgammon import EMPTY, WHITE, BLACK, Backgammon, LegalMove

B_CHAR = "\033[94mO\033[0m"
W_CHAR = "O"

def print_turn(backgammon_board: Backgammon):
    if backgammon_board.turn == WHITE:
        print("Turn: White")
    elif backgammon_board.turn == BLACK:
        print("Turn: Black")

def print_dice(backgammon_board: Backgammon):
    print(f"Dice: {backgammon_board.dice}")

def print_legal_moves(backgammon_board: Backgammon):
    moves_list_to_print = []
    for legal_move in backgammon_board.legal_moves:
        moves_list_to_print.append((legal_move.start_point, legal_move.end_point))
    moves_list_to_print = list(set(moves_list_to_print))
    print(f"legal moves: {moves_list_to_print}")

def print_board(backgammon_board):
    board = backgammon_board.board.copy()
    bar = backgammon_board.bar.copy()
    string_list = []

    string_list.append("|-----------------------------------------------------------------|")
    string_list.append("| 13 | 14 | 15 | 16 | 17 | 18 |     | 19 | 20 | 21 | 22 | 23 | 24 |")
    string_list.append("|-----------------------------------------------------------------|")

    # Print the top half of the board
    while not check_zeros(board, 12, 23) or bar[BLACK] > 0:
        # Print top left
        row = ""
        for i in range(12, 18):
            if board[i] == 0:
                row += "|    "
            elif board[i] > 0:
                row += f"|  {W_CHAR} "
                board[i] -= 1
            elif board[i] < 0:
                row += f"|  {B_CHAR} "
                board[i] += 1

        # Print black bar
        if bar[BLACK] > 0:
            row += f"|  {B_CHAR}  "
            bar[BLACK] -= 1
        else:
            row += "|     "
        
        for i in range(18, 24):
            if board[i] == 0:
                row += "|    "
            elif board[i] > 0:
                row += f"|  {W_CHAR} "
                board[i] -= 1
            elif board[i] < 0:
                row += f"|  {B_CHAR} "
                board[i] += 1
        row += "|"
        string_list.append(row)

    string_list.append("|    |    |    |    |    |    |     |    |    |    |    |    |    |")
    string_list.append("|-----------------------------| BAR |-----------------------------|")
    string_list.append("|    |    |    |    |    |    |     |    |    |    |    |    |    |")

    top_half_size = len(string_list)

    # Print the bottom half of the board
    while not check_zeros(board, 0, 12) or bar[WHITE] > 0:
        row = ""
        for i in range(11, 5, -1):
            if board[i] == 0:
                row += "|    "
            elif board[i] > 0:
                row += f"|  {W_CHAR} "
                board[i] -= 1
            elif board[i] < 0:
                row += f"|  {B_CHAR} "
                board[i] += 1

        # Print WHITE bar
        if bar[WHITE] > 0:
            row += f"|  {W_CHAR}  "
            bar[WHITE] -= 1
        else:
            row += "|     "

        for i in range(5, -1, -1):
            if board[i] == 0:
                row += "|    "
            elif board[i] > 0:
                row += f"|  {W_CHAR} "
                board[i] -= 1
            elif board[i] < 0:
                row += f"|  {B_CHAR} "
                board[i] += 1
        row += "|"
        string_list.append(row)

    # Flip bottom half of the board
    string_list[top_half_size:] = reversed(string_list[top_half_size:])
    string_list.append("|-----------------------------------------------------------------|")
    string_list.append("| 12 | 11 | 10 |  9 |  8 |  7 |     |  6 |  5 |  4 |  3 |  2 |  1 |")
    string_list.append("|-----------------------------------------------------------------|")

    for row in string_list:
        print(row)