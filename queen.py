class Queen:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x  # position of the queen between 1,2,3,4
        self.pos_y = pos_y  # position of the queen between a,b,c,d

    def move(self, board, pos_x, pos_y):
        # Check if position changed
        if pos_x == self.pos_x and pos_y == self.pos_y:
            return False

        # Check if move is possible (according to queen chess movements)
        if pos_x != self.pos_x and pos_y != self.pos_y:
            pos_x_movement = abs(self.pos_x - pos_x)
            pos_y_movement = abs(self.pos_y - pos_y)
            if pos_x_movement != pos_y_movement:
                return False

        # Check if you don't move over an blocked square / used square
        pos_x_between = []
        if self.pos_x < pos_x:
            for num in range(self.pos_x + 1, pos_x):
                pos_x_between.append(num)
        else:
            for num in range(self.pos_x - 1, pos_x, -1):
                pos_x_between.append(num)

        pos_y_between = []
        if self.pos_y < pos_y:
            for num in range(self.pos_y + 1, pos_y):
                pos_y_between.append(num)
        else:
            for num in range(self.pos_y - 1, pos_y, -1):
                pos_y_between.append(num)

        if len(pos_x_between) > 0 and len(pos_y_between) > 0:   # Checks availability between diagonal squares
            count = 0
            for x in pos_x_between:
                for square_id, square_info in board.squares.items():
                    if square_info["pos"] == (x, pos_y_between[count]):
                        if board.squares[square_id]["available"] == False:
                            return False
                count+=1

        elif len(pos_x_between) > 0:  # Checks availability between x-axis squares
            for x in pos_x_between:
                for square_id, square_info in board.squares.items():
                    if square_info["pos"] == (x, pos_y):
                        if board.squares[square_id]["available"] == False:
                            return False

        elif len(pos_y_between) > 0:  # Checks availability between y-axis squares
            for y in pos_y_between:
                for square_id, square_info in board.squares.items():
                    if square_info["pos"] == (pos_x, y):
                        if board.squares[square_id]["available"] == False:
                            return False

        # Check if square is available
        for square_id, square_info in board.squares.items():
            if square_info["pos"] == (pos_x, pos_y):
                if square_info["available"]:
                    # Block new position
                    board.block_pos(pos_x, pos_y)
                    # Save new position
                    self.pos_x = pos_x
                    self.pos_y = pos_y
                    return True
                else:
                    return False