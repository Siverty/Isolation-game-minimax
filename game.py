# Import the pygame library and the classes we've created
import pygame
from queen import Queen
from board import Board
from agent import Agent

# Initialize the pygame library
pygame.init()

# Set the popup window size
WIDTH = 800  # Increased window width
HEIGHT = 800  # Increased window height

# Set the size of the squares in the chess board
SQUARE_SIZE = WIDTH // 6

# Set the title of the popup window
TITLE = "Isolation Game Max And Justin"

# Load the images of the two queens
white_queen_img = pygame.image.load("images/white_queen.png")
black_queen_img = pygame.image.load("images/black_queen.png")

# Initialize the popup window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the pygame window name
pygame.display.set_caption(TITLE)

# Create a clock object to control the game speed
clock = pygame.time.Clock()

# Creating the queens
white_queen = Queen(0, 0)
black_queen = Queen(5, 5)  # Set the initial position of the black queen to (5, 5)

# Defining that white starts
white_turn = True
black_turn = False

# Creating the board
board = Board()
board.block_pos(0, 0)
board.block_pos(5, 5)  # Blocked position for the black queen

# Starting a game
game_state = True

# Game loop
running = True

# This is to delay the time when the game ends
switch = False

# This is so the player is one game white and the other game black
count_games = 0

# Set the size and position of the board within the window
BOARD_SIZE = min(WIDTH, HEIGHT) - 100  # Set the size of the board to fit within the window
SQUARE_SIZE = BOARD_SIZE // 6  # Adjust the square size accordingly
BOARD_X = (WIDTH - BOARD_SIZE) // 2  # Center the board horizontally
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2  # Center the board vertically

# Set the board outline color
BOARD_OUTLINE_COLOR = (0, 0, 0)  # Black color for the outline

def draw_board_outline():
    # Draw a rectangle to outline the board
    pygame.draw.rect(window, BOARD_OUTLINE_COLOR, (BOARD_X - 2, BOARD_Y - 2, BOARD_SIZE + 4, BOARD_SIZE + 4), 4)

def player_move():
    # Get the pos input from the user
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:  # Left mouse button
        # Get position on x-axis
        if BOARD_X <= mouse[0] <= BOARD_X + BOARD_SIZE:
            mouse_pos_x = (mouse[0] - BOARD_X) // SQUARE_SIZE

        # Get position on y-axis
        if BOARD_Y <= mouse[1] <= BOARD_Y + BOARD_SIZE:
            mouse_pos_y = (mouse[1] - BOARD_Y) // SQUARE_SIZE

        # Change queen position
        if white_turn:
            if white_queen.move(board, mouse_pos_x, mouse_pos_y):
                return True
            else:
                # Move is not possible
                pass
        elif black_turn:
            if black_queen.move(board, mouse_pos_x, mouse_pos_y):
                return True
            else:
                # Move is not possible
                pass

def agent_move():
    n = 3  # The agent will think n steps ahead

    # Change queen according to the best position
    if black_turn:
        agent = Agent(black_queen, board, white_queen, n)
        best_move = agent.best_move()
        if black_queen.move(board, best_move[0], best_move[1]):
            return True
    else:
        agent = Agent(white_queen, board, black_queen, n)
        best_move = agent.best_move()
        if white_queen.move(board, best_move[0], best_move[1]):
            return True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # While the game is running
    if game_state:
        # Clear the window
        window.fill((255, 255, 255))

        # Draw the board outline
        draw_board_outline()

        # Draw the chess board within the specified size and position
        for x in range(6):
            for y in range(6):
                # Determine if the square is available
                for square_id, square_info in board.squares.items():
                    if square_info["pos"] == (x, y):
                        if square_info["available"] == False:
                            if square_info["pos"] == (white_queen.pos_x, white_queen.pos_y) or \
                                    square_info["pos"] == (black_queen.pos_x, black_queen.pos_y):
                                # Make available squares black/white
                                if (x + y) % 2 == 0:
                                    color = (150, 150, 150)  # Black
                                else:
                                    color = (255, 255, 255)  # White
                            else:
                                # Make unavailable squares red
                                color = (205, 0, 0)  # Red
                        else:
                            # Make available squares black/white
                            if (x + y) % 2 == 0:
                                color = (150, 150, 150)  # Black
                            else:
                                color = (255, 255, 255)  # White

                # Draw the square within the board's boundaries
                pygame.draw.rect(window, color, (BOARD_X + x * SQUARE_SIZE, BOARD_Y + y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw the white queen within the board
        window.blit(white_queen_img, (BOARD_X + white_queen.pos_x * SQUARE_SIZE, BOARD_Y + white_queen.pos_y * SQUARE_SIZE))

        # Draw the black queen within the board
        window.blit(black_queen_img, (BOARD_X + black_queen.pos_x * SQUARE_SIZE, BOARD_Y + black_queen.pos_y * SQUARE_SIZE))

        # Define who's the player is playing
        if (count_games % 2) == 0:
            text = pygame.font.SysFont('arial', 40).render('You are white', True, (255, 255, 255))
        else:
            text = pygame.font.SysFont('arial', 40).render('You are black', True, (0, 0, 0))

        # Calculate the Y-coordinate for the player info text
        text_y = BOARD_Y - 50  # Adjust this value for vertical positioning

        # Calculate the Y-coordinate for the player info rectangle
        rect_y = BOARD_Y - 60+5  # added 5 pixels to make sure the text fits within the rectangle

        # Draw the player info text and rectangle above the board with dark blue background
        pygame.draw.rect(window, (50, 150, 50), (0, rect_y, WIDTH, text_y + text.get_height()))
        window.blit(text, (
            WIDTH / 2 - text.get_width() / 2, text_y))

        # Update the display
        pygame.display.update()

        # Check who won the game
        if board.blocked_pos(white_queen):
            game_state = False
            count_games += 1
            # Check exception when it's white's turn and both are in blocked pos
            if board.blocked_pos(black_queen):
                if white_turn:
                    queen_who_won = "black"
                    switch = True
                else:
                    queen_who_won = "white"
                    switch = True
            else:
                queen_who_won = "black"
                switch = True
        elif board.blocked_pos(black_queen):
            count_games += 1
            game_state = False
            queen_who_won = "white"
            switch = True

        # Move the queen
        elif white_turn:
            if (count_games % 2) == 0:
                if player_move():
                    black_turn = True
                    white_turn = False
            else:
                if agent_move():
                    black_turn = True
                    white_turn = False

        elif black_turn:
            if (count_games % 2) == 0:
                if agent_move():
                    black_turn = False
                    white_turn = True
            else:
                if player_move():
                    black_turn = False
                    white_turn = True

        # Control the game speed
        clock.tick(60)

    # When the game is finished
    else:
        if switch:  # We only want this delay once so it's more clear who won the game
            pygame.time.delay(500)  # 1 second == 1000 milliseconds
            switch = False

        # End screen
        window.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render(queen_who_won + ' won the game', True, (255, 255, 255))
        restart_button = font.render('P - Play again', True, (255, 255, 255))
        quit_button = font.render('S - Stop playing', True, (255, 255, 255))
        window.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2))
        window.blit(restart_button, (
            WIDTH / 2 - restart_button.get_width() / 2, HEIGHT / 1.9 + restart_button.get_height()))
        window.blit(quit_button, (
            WIDTH / 2 - quit_button.get_width() / 2, HEIGHT / 2 + quit_button.get_height() / 2))
        pygame.display.update()

        # When a key is pressed
        keys = pygame.key.get_pressed()

        # Restart game
        if keys[pygame.K_p]:
            game_state = True

            # Creating the queens
            white_queen = Queen(0, 0)
            black_queen = Queen(5, 5)  # Set the initial position of the black queen to (5, 5)

            # Defining that white starts
            white_turn = True
            black_turn = False

            # Creating the board
            board = Board()
            board.block_pos(0, 0)
            board.block_pos(5, 5)  # Blocked position for the black queen

        # Quit game
        if keys[pygame.K_s]:
            pygame.quit()
            quit()

# Quit the game
pygame.quit()