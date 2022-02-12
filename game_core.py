import numpy as np
import pygame


# Defaults
BLUE = (50, 50, 220)
LIGHT_BLUE = (0, 0, 200)
RED = (220, 50, 50)
LIGHT_RED = (250, 80, 80)
YELLOW = (220, 220, 50)
LIGHT_YELLOW = (250, 250, 80)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

ROWS_COUNT = 6
COLUMNS_COUNT = 7

SQUARE_SIZE = 90
RADIUS = int(SQUARE_SIZE / 2 - 5)

width = COLUMNS_COUNT * SQUARE_SIZE
height = (ROWS_COUNT + 1) * SQUARE_SIZE

size = (width, height)

def create_board():
	board = np.zeros((ROWS_COUNT, COLUMNS_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROWS_COUNT - 1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROWS_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMNS_COUNT - 3):
		for r in range(ROWS_COUNT):
			if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and \
				board[r][c + 3] == piece:
				return True
	
	# Check vertical locations for win
	for c in range(COLUMNS_COUNT):
		for r in range(ROWS_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and \
				board[r + 3][c] == piece:
				return True
	
	# Check positive slope diagonal
	for c in range(COLUMNS_COUNT - 3):
		for r in range(ROWS_COUNT - 3):
			if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][
				c + 2] == piece and \
				board[r + 3][c + 3] == piece:
				return True
	
	# Check negative slope diagonal
	for c in range(COLUMNS_COUNT - 3):
		for r in range(3, ROWS_COUNT):
			if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][
				c + 2] == piece and \
				board[r - 3][c + 3] == piece:
				return True

def draw_board(screen, board):
	for c in range(COLUMNS_COUNT):
		for r in range(ROWS_COUNT):
			if r == 0:
				pygame.draw.rect(screen, LIGHT_BLUE,
								 (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE - 8,
								  SQUARE_SIZE, SQUARE_SIZE))
				pygame.draw.rect(screen, BLUE,
								 (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE - 2,
								  SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.rect(screen, BLUE,
							 (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE,
							  SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, LIGHT_BLUE,
							   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
								int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
							   RADIUS + 4)
			pygame.draw.circle(screen, GRAY,
							   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
								int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
							   RADIUS - 4)
	
	for c in range(COLUMNS_COUNT):
		for r in range(ROWS_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED,
								   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
									height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
								   RADIUS - 4)
				pygame.draw.circle(screen, LIGHT_RED,
								   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
									height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
								   RADIUS - 14)
			elif board[r][c] == -1:
				pygame.draw.circle(screen, YELLOW,
								   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
									height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
								   RADIUS - 4)
				pygame.draw.circle(screen, LIGHT_YELLOW,
								   (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
									height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
								   RADIUS - 14)
	
	pygame.display.update()
