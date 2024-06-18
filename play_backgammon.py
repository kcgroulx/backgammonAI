from backgammon import Backgammon
from gui import print_board

backgammon = Backgammon()
backgammon.start()
print_board(backgammon)

backgammon.generate_legal_moves([1,2])
print(backgammon.legal_moves)

if backgammon.move(1, 2) == False:
    print("*** invalid move ***")
else:
    print_board(backgammon)

backgammon.generate_legal_moves([1,2])
print(backgammon.legal_moves)