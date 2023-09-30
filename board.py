import copy


class Board:
    def __init__(self):
        self.squares = {  # X_axis = 1 to 6, y_axis = a to f
            "A1": {"pos": (0, 5), "available": True},
            "A2": {"pos": (1, 5), "available": True},
            "A3": {"pos": (2, 5), "available": True},
            "A4": {"pos": (3, 5), "available": True},
            "A5": {"pos": (4, 5), "available": True},
            "A6": {"pos": (5, 5), "available": True},
            "B1": {"pos": (0, 4), "available": True},
            "B2": {"pos": (1, 4), "available": True},
            "B3": {"pos": (2, 4), "available": True},
            "B4": {"pos": (3, 4), "available": True},
            "B5": {"pos": (4, 4), "available": True},
            "B6": {"pos": (5, 4), "available": True},
            "C1": {"pos": (0, 3), "available": True},
            "C2": {"pos": (1, 3), "available": True},
            "C3": {"pos": (2, 3), "available": True},
            "C4": {"pos": (3, 3), "available": True},
            "C5": {"pos": (4, 3), "available": True},
            "C6": {"pos": (5, 3), "available": True},
            "D1": {"pos": (0, 2), "available": True},
            "D2": {"pos": (1, 2), "available": True},
            "D3": {"pos": (2, 2), "available": True},
            "D4": {"pos": (3, 2), "available": True},
            "D5": {"pos": (4, 2), "available": True},
            "D6": {"pos": (5, 2), "available": True},
            "E1": {"pos": (0, 1), "available": True},
            "E2": {"pos": (1, 1), "available": True},
            "E3": {"pos": (2, 1), "available": True},
            "E4": {"pos": (3, 1), "available": True},
            "E5": {"pos": (4, 1), "available": True},
            "E6": {"pos": (5, 1), "available": True},
            "F1": {"pos": (0, 0), "available": True},
            "F2": {"pos": (1, 0), "available": True},
            "F3": {"pos": (2, 0), "available": True},
            "F4": {"pos": (3, 0), "available": True},
            "F5": {"pos": (4, 0), "available": True},
            "F6": {"pos": (5, 0), "available": True}
        }

    # Block a position
    def block_pos(self, pos_x, pos_y):
        for square_id, square_info in self.squares.items():
            if square_info["pos"] == (pos_x, pos_y):
                self.squares[square_id]["available"] = False

    # Check is a queen is in a blocked position, where there are no other available moves
    def blocked_pos(self, queen):
        queen_copy = copy.deepcopy(queen)  # Making copies so the game doesn't change
        board_copy = copy.deepcopy(self)  # Making copies so the game doesn't change
        for square in board_copy.squares:
            possible_move = queen_copy.move(board_copy, board_copy.squares[square]["pos"][0], board_copy.squares[square]["pos"][1])
            if possible_move:
                return False
        return True

