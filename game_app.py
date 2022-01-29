import numpy as np
import pygame
import sys
import math
from game_core import (
	create_board, drop_piece, is_valid_location, get_next_open_row,
	print_board, winning_move, draw_board,
	SQUARE_SIZE, RADIUS, width, height, size,
	BLUE, RED, YELLOW, BLACK
)
from bot_core import GameBot

# Board Initialization
board = create_board()
# print_board(board)
game_over = False
turn = 0

pygame.init()
screen = pygame.display.set_mode(size)

draw_board(screen, board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

# Bot Initialization
bot = GameBot()
bot.load_next_moves_classifier()

# Game
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
			x_pos = event.pos[0]
			
			pygame.draw.circle(screen, RED, (x_pos, int(SQUARE_SIZE / 2)), RADIUS)
	
		pygame.display.update()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
			# print(event.pos)
			
			x_pos = event.pos[0]
			user_move = int(math.floor(x_pos / SQUARE_SIZE))
			
			if is_valid_location(board, user_move):
				row = get_next_open_row(board, user_move)
				drop_piece(board, row, user_move, 1)
			
				if winning_move(board, 1):
					label = my_font.render("Player 1 Wins!!", 1, RED)
					screen.blit(label, (40, 10))
					game_over = True
					# print_board(board)
					draw_board(screen, board)
					break
					
					
			bot_move = bot.get_next_move_suggested(np.flip(board, 0))
			
			if is_valid_location(board, bot_move):
				row = get_next_open_row(board, bot_move)
				drop_piece(board, row, bot_move, -1)
				
				if winning_move(board, -1):
					label = my_font.render("Bot Wins!!", 1, YELLOW)
					screen.blit(label, (40, 10))
					game_over = True
					# print_board(board)
					draw_board(screen, board)
					break
			
			# print_board(board)
			draw_board(screen, board)
			
			turn += 1
			turn = turn % 2
			
	if game_over:
		pygame.time.wait(3000)