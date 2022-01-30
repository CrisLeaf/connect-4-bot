import pygame


class Menu():
	
	def __init__(self, game):
		self.game = game
		self.mid_w = self.game.DISPLAY_W / 2
		self.mid_h = self.game.DISPLAY_H / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0, 0, 80, 40)
		self.offset = -80
	
	def draw_cursor(self):
		self.game.draw_text("*", 79, self.cursor_rect.x, self.cursor_rect.y + 109)
	
	def blit_screen(self):
		self.game.window.blit(self.game.display, (0, 0))
		pygame.display.update()
		self.game.reset_keys()


class MainMenu(Menu):
	
	def __init__(self, game):
		Menu.__init__(self, game)
		
		self.state = "Start"
		self.startx, self.starty = self.mid_w, self.mid_h + 40
		self.controlsx, self.controlsy = self.mid_w, self.mid_h + 80
		self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
	
	def display_menu(self):
		self.run_display = True
		
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.draw_text("Connect 4", 100, self.game.DISPLAY_W/2,
								self.game.DISPLAY_H/2 - 100)
			self.game.draw_text("Enter", 50, self.startx, self.starty + 100)
			self.game.draw_text("Controls", 50, self.controlsx, self.controlsy + 100)
			self.draw_cursor()
			self.blit_screen()
	
	def move_cursor(self):
		if self.game.DOWN_KEY or self.game.UP_KEY:
			if self.state == "Start":
				self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
				self.state = "Controls"
			elif self.state == "Controls":
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = "Start"
		pass
		
	def check_input(self):
		self.move_cursor()
		
		if self.game.START_KEY:
			if self.state == "Start":
				self.game.curr_menu = self.game.playing = True
			elif self.state == "Controls":
				self.game.curr_menu = self.game.controls_menu
			self.run_display = False

class ControlsMenu(Menu):

	def __init__(self, game):
		Menu.__init__(self, game)

	def display_menu(self):
		self.run_display = True

		while self.run_display:
			self.game.check_events()

			if self.game.START_KEY or self.game.BACK_KEY:
				self.game.curr_menu = self.game.main_menu
				self.run_display = False

			self.game.display.fill(self.game.BLACK)
			self.game.draw_text("Left - left arrow", 50, self.game.DISPLAY_W/2,
								self.game.DISPLAY_H/2 - 50)
			self.game.draw_text("Right - right arrow", 50, self.game.DISPLAY_W/2,
								self.game.DISPLAY_H/2)
			self.game.draw_text("Drop Piece - down arrow", 50, self.game.DISPLAY_W/2,
								self.game.DISPLAY_H/2 + 50)
			
			
			self.blit_screen()

		
		
# class StartMenu(Menu):
#
# 	def __init__(self, game):
# 		Menu.__init__(self, game)
#
# 		self.state = "Player1"
# 		self.player1x, self.player1y = self.mid_w, self.mid_h + 20
# 		self.player2x, self.player2y = self.mid_w, self.mid_h + 40
# 		self.cursor_rect.midtop = (self.player1x + self.offset, self.player1y)
#
# 	def display_menu(self):
# 		self.run_display = True
#
# 		while self.run_display:
# 			self.game.check_events()
# 			self.check_input()
# 			self.game.display.fill(self.game.BLACK)
# 			self.game.draw_text("Elige Jugador", 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -
# 								20)
# 			self.game.draw_text("Jugador 1", 15, self.player1x, self.player1y)
# 			self.game.draw_text("Jugador 2", 15, self.player2x, self.player2y)
# 			self.draw_cursor()
# 			self.blit_screen()
#
# 	def move_cursor(self):
# 		if self.game.DOWN_KEY or self.game.UP_KEY:
# 			if self.state == "Player 1":
# 				self.cursor_rect.midtop = (self.player2x + self.offset, self.player2y)
# 				self.state = "Player 2"
# 			elif self.state == "Player 2":
# 				self.cursor_rect.midtop = (self.player1x + self.offset, self.player1y)
# 				self.state = "Player 1"
#
# 	def check_input(self):
# 		self.move_cursor()
#
# 		if self.game.BACK_KEY:
# 			self.game.curr_menu = self.game.main_menu
# 			self.run_display = False
#
# 		if self.game.START_KEY:
# 			if self.state == "Player 1":
# 				self.game.playing = True
# 				# self.game.playing_p1 = True
# 			elif self.state == "Player 2":
# 				self.game.playing = True
# 				# self.game.playing_p2 = True
# 			self.run_display = False
		
# class CreditsMenu(Menu):
#
# 	def __init__(self, game):
# 		Menu.__init__(self, game)
#
# 	def display_menu(self):
# 		self.run_display = True
#
# 		while self.run_display:
# 			self.game.check_events()
#
# 			if self.game.START_KEY or self.game.BACK_KEY:
# 				self.game.curr_menu = self.game.main_menu
# 				self.run_display = False
#
# 			self.game.display.fill(self.game.BLACK)
# 			self.game.draw_text("Credits", 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
# 			self.game.draw_text("Made by Cris", 15, self.game.DISPLAY_W/2,
# 								self.game.DISPLAY_H/2 + 10)
# 			self.blit_screen()
#