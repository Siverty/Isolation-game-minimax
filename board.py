import copy


class Board:
    def __init__(self):
        self.squares = {  # X_axis = 1 to 4, y_axis = a to d
            "A1": {"pos": (0, 3), "available": True},
            "A2": {"pos": (1, 3), "available": True},
            "A3": {"pos": (2, 3), "available": True},
            "A4": {"pos": (3, 3), "available": True},
            "B1": {"pos": (0, 2), "available": True},
            "B2": {"pos": (1, 2), "available": True},
            "B3": {"pos": (2, 2), "available": True},
            "B4": {"pos": (3, 2), "available": True},
            "C1": {"pos": (0, 1), "available": True},
            "C2": {"pos": (1, 1), "available": True},
            "C3": {"pos": (2, 1), "available": True},
            "C4": {"pos": (3, 1), "available": True},
            "D1": {"pos": (0, 0), "available": True},
            "D2": {"pos": (1, 0), "available": True},
            "D3": {"pos": (2, 0), "available": True},
            "D4": {"pos": (3, 0), "available": True}
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

