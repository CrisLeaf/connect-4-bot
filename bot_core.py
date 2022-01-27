import numpy as np
import pickle
from game_core import ROWS_COUNT, COLUMNS_COUNT


class GameBot():
	
	def __init__(self, rows_count=ROWS_COUNT, columns_count=COLUMNS_COUNT):
		self.rows_count = rows_count
		self.columns_count = columns_count
		
	def load_next_moves_classifier(self):
		with open("classifier.pkl", "rb") as f:
			self.classifier = pickle.load(f)
	
		return self
	
	def get_next_move(self, played_mat):
		"""
		Get the move to play, based on win probabilities of each possible next move.
		
		Params
		------
		- played_mat, numpy array : the previous played matrix on which the next move
									corresponds to the bot.
		
		Returns
		-------
		- next_move, int : the next move column index that the bot should play.
		"""
		pred_probas = []
		
		# Loop and Predict on available movements
		for j in range(self.columns_count):
			played_mat_copy = played_mat.copy()
			
			# Fill a piece on the available position in column j, if not continue with the loop
			try:
				available_position = np.where(played_mat[:, j] != 0)[0][0] - 1
			except:
				available_position = self.rows_count - 1
			
			if available_position >= 0:
				played_mat_copy[available_position, j] = -1
			else:
				continue
			
			# Predict the win probability
			pred_proba = self.classifier.predict_proba(played_mat_copy.reshape(1, -1))
			pred_probas.append(pred_proba[0][0])
			
		next_move = pred_probas.index(max(pred_probas))
		
		return next_move


# played_mat = np.zeros((ROWS_COUNT, COLUMNS_COUNT))
#
# for j in [1, 3, 4, 5, 6]:
# 	played_mat[5, j] = 1
# 	played_mat[4, j] = 1
# 	played_mat[3, j] = 1
#
#
# print(played_mat)
#
# bot = GameBot()
# bot.load_next_moves_classifier()
# next_move = bot.get_next_move(played_mat)
# print(next_move)
