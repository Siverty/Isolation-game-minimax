import copy

# Having the agent not forget the board, the queen and the opponent queen
class Agent:
    def __init__(self, queen, board, opponent_queen, depth):
        for square in board.squares:
            if board.squares[square]['pos'] == (queen.pos_x, queen.pos_y):
                self.position = board.squares[square]['pos']
        self.board = copy.deepcopy(board)
        self.queen = copy.deepcopy(queen)
        self.opponent_queen = copy.deepcopy(opponent_queen)
        self.depth = depth  # This will define the amount of moves the AI will think through

    def best_move(self):
        eval, best_queen_move = self.alphabeta(self.depth, True, float('-inf'), float('+inf'), self.queen, self.opponent_queen, self.board)
        return best_queen_move

    # This code will get the heuristic (what is defined as possible moves)
    def get_eval(self, queen, opponent_queen, board):
        # Counting every possible move of the queen
        queen_moves = 0
        for square in board.squares:
            queen_copy = copy.deepcopy(queen)
            board_copy = copy.deepcopy(board)

            possible_move = queen_copy.move(board_copy, board_copy.squares[square]["pos"][0],
                                            board_copy.squares[square]["pos"][1])
            if possible_move:
                queen_moves += 1

        # Counting every possible move of the opponent queen
        opponent_queen_moves = 0
        for square in board.squares:
            opponent_queen_copy = copy.deepcopy(opponent_queen)
            board_copy = copy.deepcopy(board)

            possible_move = opponent_queen_copy.move(board_copy, board_copy.squares[square]["pos"][0],
                                            board_copy.squares[square]["pos"][1])
            if possible_move:
                opponent_queen_moves += 1

        # Having the agent play offensive in the first half and defensive in the second half
        count_available_squares = 0
        count_total_squares = 0
        for square in board.squares:
            count_total_squares += 1
            if board.squares[square]['available']:
                count_available_squares += 1

        # First half of the game
        if count_available_squares / count_total_squares > 0.5:
            # Playing offensive
            return queen_moves - (opponent_queen_moves * 2)

        # Second half of the game
        elif count_available_squares/count_total_squares <= 0.5:
            # Playing defensive
            return (queen_moves*2) - opponent_queen_moves

    def get_possible_moves(self, queen, board):
        # The parent queen is the queen who it's turn to move
        possible_moves = []
        for square in board.squares:
            queen_copy = copy.deepcopy(queen)
            board_copy = copy.deepcopy(board)
            possible_move = queen_copy.move(board_copy, board_copy.squares[square]["pos"][0],
                                                   board_copy.squares[square]["pos"][1])
            if possible_move:
                possible_moves.append(board_copy.squares[square]['pos'])
        return possible_moves

    def alphabeta(self, depth, maximizing_player, alpha, beta, queen, opponent_queen, board):
        # If the depth is zero
        if depth == 0:
            eval = self.get_eval(copy.deepcopy(queen), copy.deepcopy(opponent_queen), copy.deepcopy(board))
            return eval
        # If the game is over
        if board.blocked_pos(queen):
            if board.blocked_pos(opponent_queen):
                if maximizing_player:
                    return float('-inf')
                else:
                    return float('+inf')
            else:
                return float('-inf')
        if board.blocked_pos(opponent_queen):
            return float('+inf')

        if maximizing_player:
            maxEval = float('-inf')

            best_queen_move = None  # Save the best queen move
            # For each possible parent queen move
            for parent_move in self.get_possible_moves(queen, board):
                # making deep copies so only the right blocks in the game are moved
                board_new = copy.deepcopy(board)
                queen_new = copy.deepcopy(queen)

                # The parent_queen will move
                queen_new.move(board_new, parent_move[0], parent_move[1])

                eval = self.alphabeta(depth - 1, False, alpha, beta, queen_new, opponent_queen, board_new)
                maxEval = max(maxEval, eval)
                if eval >= maxEval:
                    best_queen_move = parent_move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, best_queen_move

        else:
            minEval = float('+inf')

            # For each possible parent queen move
            for parent_move in self.get_possible_moves(opponent_queen, board):
                # making deep copies so only the right blocks in the game are moved
                board_new = copy.deepcopy(board)
                opponent_queen_new = copy.deepcopy(opponent_queen)

                # The parent_queen will move
                opponent_queen_new.move(board_new, parent_move[0], parent_move[1])

                try:
                    eval, _ = self.alphabeta(depth - 1, True, alpha, beta, queen, opponent_queen_new, board_new)
                    minEval = min(minEval, eval)
                except:
                    eval = self.alphabeta(depth - 1, True, alpha, beta, queen, opponent_queen_new, board_new)
                    minEval = min(minEval, eval)

                beta = min(beta, eval)
            return minEval

