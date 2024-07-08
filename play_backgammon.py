from backgammon import Backgammon
from gui import print_board, print_dice, print_legal_moves, print_turn

backgammon = Backgammon()
backgammon.start()


while backgammon.win == None:
    print_board(backgammon)
    print_turn(backgammon)
    print_dice(backgammon)
    print_legal_moves(backgammon)

    user_input = input("Enter move: ")
    elements = user_input.split(',')

    start_point = int(elements[0])
    end_point= int(elements[1])

    backgammon.move_piece(start_point, end_point)