import numpy as np
import pygame
import sys
import math
from game_core import (
	create_board, drop_piece, is_valid_location, get_next_open_row,
	winning_move, draw_board,
	SQUARE_SIZE, RADIUS, width, size,
	RED, BLACK, GRAY, LIGHT_RED
)
from bot_core import GameBot


def main():
	# Board Initialization
	board = create_board()
	game_over = False
	turn = 0
	
	pygame.init()
	screen = pygame.display.set_mode(size)
	
	draw_board(screen, board)
	pygame.display.update()
	
	my_font = pygame.font.SysFont("monospace", 75)
	
	bot = GameBot()
	bot.load_next_moves_classifier()
	
	draw_check = 0
	
	# Game
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			
			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARE_SIZE - 8))
				x_pos = event.pos[0]
				
				pygame.draw.circle(screen, RED, (x_pos, int(SQUARE_SIZE / 2)), RADIUS - 4)
				pygame.draw.circle(screen, LIGHT_RED, (x_pos, int(SQUARE_SIZE / 2)), RADIUS - 14)
			
			pygame.display.update()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARE_SIZE - 8))
				
				x_pos = event.pos[0]
				user_move = int(math.floor(x_pos / SQUARE_SIZE))
				
				if is_valid_location(board, user_move):
					row = get_next_open_row(board, user_move)
					drop_piece(board, row, user_move, 1)
					
					draw_board(screen, board)
					
					if winning_move(board, 1):
						label = my_font.render("Player 1 Wins!!", 1, BLACK)
						screen.blit(label, (40, 10))
						game_over = True
						draw_board(screen, board)
						break
				
				else:
					continue
				
				pygame.time.wait(draw_check * 60)
				
				bot_move = bot.get_next_move_suggested(np.flip(board, 0))
				
				if is_valid_location(board, bot_move):
					row = get_next_open_row(board, bot_move)
					drop_piece(board, row, bot_move, -1)
					
					draw_board(screen, board)
					
					if winning_move(board, -1):
						label = my_font.render("Bot Wins!!", 1, BLACK)
						screen.blit(label, (40, 10))
						game_over = True
						draw_board(screen, board)
						break
				
				else:
					continue
				
				turn += 1
				turn = turn % 2
				
				draw_check += 1
				
				if draw_check == 21:
					label = my_font.render("Draw!!", 1, BLACK)
					screen.blit(label, (40, 10))
					game_over = True
					draw_board(screen, board)
					break
		
		if game_over:
			pygame.time.wait(2500)

if __name__ == "__main__":
	main()
