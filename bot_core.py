import numpy as np
import pickle
from game_core import ROWS_COUNT, COLUMNS_COUNT, winning_move


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
				available_position = np.where(played_mat_copy[:, j] != 0)[0][0] - 1
			except:
				available_position = self.rows_count - 1
			
			if available_position >= 0:
				played_mat_copy[available_position, j] = -1
			##################################################################
				
				pred_probas_ = []

				for jj in range(self.columns_count):
					played_mat_copy_ = played_mat_copy.copy()

					try:
						available_position = np.where(played_mat_copy_[:, jj] != 0)[0][0] - 1
					except:
						available_position = self.rows_count - 1

					if available_position >= 0:
						played_mat_copy_[available_position, jj] = 1
					###########################################################################

						pred_probas__ = []

						for jjj in range(self.columns_count):
							played_mat_copy__ = played_mat_copy_.copy()

							try:
								available_position = np.where(played_mat_copy__[:, jjj] != 0)[0][0] - 1
							except:
								available_position = self.rows_count - 1

							if available_position >= 0:
								played_mat_copy__[available_position, jjj] = -1
							else:
								continue

							if winning_move(played_mat_copy__, 1):
								pred_proba = [[-10]]

							else:
								pred_proba = self.classifier.predict_proba(played_mat_copy__.reshape(1, -1))

							pred_proba += np.random.uniform(-0.3, 0.3, 1)

							pred_probas__.append(pred_proba[0][0])

					###########################################################################
					else:
						continue

					# pred_proba = self.classifier.predict_proba(played_mat_copy_.reshape(1, -1))
					pred_probas_.append(np.mean(pred_probas__))
			
			###################################################################
			else:
				pred_probas.append(-100)
				continue
				
			pred_probas.append(np.mean(pred_probas_))
			
		next_move = pred_probas.index(max(pred_probas))
		
		return next_move