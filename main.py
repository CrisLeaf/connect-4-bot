from game_app2 import Game

g = Game()

while g.running:
	g.curr_menu.display_menu()
	g.game_loop()