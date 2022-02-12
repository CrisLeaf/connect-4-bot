import os


os.system('pyinstaller --noconfirm --onedir --windowed --name "Connect4" '
		  '--add-data "/home/cris/Documents/machine-learning/connect-4-bot/bot_core.py:." '
		  '--add-data "/home/cris/Documents/machine-learning/connect-4-bot/classifier.pkl:." '
		  '--add-data "/home/cris/Documents/machine-learning/connect-4-bot/game_core.py:."  '
		  '"/home/cris/Documents/machine-learning/connect-4-bot/app.py"')
